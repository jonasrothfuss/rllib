"""Derived Agent."""
from itertools import chain

from torch.optim import Adam

from rllib.algorithms.model_learning_algorithm import ModelLearningAlgorithm
from rllib.dataset.transforms import DeltaState, MeanFunction, StateNormalizer
from rllib.model import EnsembleModel, NNModel, TransformedModel

from .model_based_agent import ModelBasedAgent


class DerivedMBAgent(ModelBasedAgent):
    """Implementation of a Derived Agent.

    A Derived Agent gets a model-free algorithm and uses the model to derive an
    algorithm.
    """

    def __init__(
        self,
        base_algorithm,
        derived_algorithm_,
        dynamical_model,
        reward_model,
        num_samples=15,
        num_steps=1,
        termination_model=None,
        *args,
        **kwargs,
    ):
        algorithm = derived_algorithm_(
            base_algorithm=base_algorithm,
            dynamical_model=dynamical_model,
            reward_model=reward_model,
            termination_model=termination_model,
            num_steps=num_steps,
            num_samples=num_samples,
            *args,
            **kwargs,
        )
        algorithm.criterion = type(algorithm.criterion)(reduction="mean")

        super().__init__(policy_learning_algorithm=algorithm, *args, **kwargs)

        self.optimizer = type(self.optimizer)(
            [
                p
                for name, p in self.algorithm.named_parameters()
                if ("model" not in name and "target" not in name and p.requires_grad)
            ],
            **self.optimizer.defaults,
        )

    @property
    def name(self) -> str:
        """See `AbstractAgent.name'."""
        derived_name = self.__class__.__name__[:-5]
        base_name = self.algorithm.base_algorithm_name
        return f"{derived_name}+{base_name}Agent"

    @classmethod
    def default(
        cls,
        environment,
        base_agent_name="SAC",
        dynamical_model=None,
        reward_model=None,
        *args,
        **kwargs,
    ):
        """See `AbstractAgent.default'."""
        from importlib import import_module

        base_agent = getattr(
            import_module("rllib.agent"), f"{base_agent_name}Agent"
        ).default(environment, *args, **kwargs)
        base_agent.logger.delete_directory()
        base_algorithm = base_agent.algorithm
        if dynamical_model is None:
            model = EnsembleModel.default(environment, deterministic=True)
            dynamical_model = TransformedModel(
                model, [StateNormalizer(), MeanFunction(DeltaState())]
            )

        if reward_model is None:
            reward_model = TransformedModel(
                NNModel.default(environment, model_kind="rewards", deterministic=False),
                dynamical_model.forward_transformations,
            )

        model_optimizer = Adam(
            chain(dynamical_model.parameters(), reward_model.parameters()),
            lr=1e-3,
            weight_decay=1e-4,
        )

        model_learning_algorithm = ModelLearningAlgorithm(
            dynamical_model=dynamical_model,
            reward_model=reward_model,
            num_epochs=4 if kwargs.get("test", False) else 50,
            model_optimizer=model_optimizer,
        )

        return cls(
            base_algorithm=base_algorithm,
            dynamical_model=dynamical_model,
            reward_model=reward_model,
            model_learning_algorithm=model_learning_algorithm,
            optimizer=base_agent.optimizer,
            num_iter=base_agent.num_iter,
            batch_size=base_agent.batch_size,
            train_frequency=base_agent.train_frequency,
            num_rollouts=base_agent.num_rollouts,
            thompson_sampling=False,
            learn_from_real=True,
            gamma=base_algorithm.gamma,
            *args,
            **kwargs,
        )
