"""Implementation of TRPO Algorithm."""

import torch.nn.modules.loss as loss
from torch.optim import Adam

from rllib.algorithms.trpo import TRPO
from rllib.policy import NNPolicy
from rllib.value_function import NNValueFunction

from .on_policy_agent import OnPolicyAgent


class TRPOAgent(OnPolicyAgent):
    """Implementation of the TRPO Agent.

    References
    ----------
    Schulman, J., Levine, S., Abbeel, P., Jordan, M., & Moritz, P. (2015).
    Trust region policy optimization. ICML.
    """

    def __init__(
        self,
        policy,
        value_function,
        optimizer,
        criterion,
        regularization=False,
        epsilon_mean=0.05,
        epsilon_var=None,
        lambda_=0.97,
        *args,
        **kwargs,
    ):
        super().__init__(optimizer=optimizer, *args, **kwargs)

        self.algorithm = TRPO(
            critic=value_function,
            policy=policy,
            regularization=regularization,
            epsilon_mean=epsilon_mean,
            epsilon_var=epsilon_var,
            criterion=criterion(reduction="mean"),
            lambda_=lambda_,
            gamma=self.gamma,
        )
        # Over-write optimizer.
        self.optimizer = type(optimizer)(
            [
                p
                for name, p in self.algorithm.named_parameters()
                if "target" not in name
            ],
            **optimizer.defaults,
        )

        self.policy = self.algorithm.policy

    @classmethod
    def default(cls, environment, *args, **kwargs):
        """See `AbstractAgent.default'."""
        policy = NNPolicy(
            dim_state=environment.dim_state,
            dim_action=environment.dim_action,
            num_states=environment.num_states,
            num_actions=environment.num_actions,
            layers=[200, 200],
            biased_head=True,
            non_linearity="Tanh",
            squashed_output=True,
            action_scale=environment.action_scale,
            tau=5e-3,
            initial_scale=0.5,
            deterministic=False,
            goal=environment.goal,
            input_transform=None,
        )
        value_function = NNValueFunction(
            dim_state=environment.dim_state,
            num_states=environment.num_states,
            layers=[200, 200],
            biased_head=True,
            non_linearity="Tanh",
            tau=5e-3,
            input_transform=None,
        )

        optimizer = Adam(
            [
                {"params": policy.parameters(), "lr": 3e-4},
                {"params": value_function.parameters(), "lr": 1e-3},
            ]
        )
        criterion = loss.MSELoss

        return cls(
            policy=policy,
            value_function=value_function,
            optimizer=optimizer,
            criterion=criterion,
            regularization=False,
            epsilon_mean=0.01,
            epsilon_var=None,
            lambda_=0.95,
            num_iter=80,
            target_update_frequency=1,
            train_frequency=0,
            num_rollouts=8,
            comment=environment.name,
            *args,
            **kwargs,
        )