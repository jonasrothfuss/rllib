from typing import Any, Optional

from torch import Tensor

from rllib.dataset.datatypes import Observation, Termination
from rllib.model import AbstractModel
from rllib.policy import AbstractPolicy
from rllib.reward import AbstractReward
from rllib.util.utilities import RewardTransformer
from rllib.value_function import AbstractValueFunction

from .abstract_algorithm import AbstractAlgorithm

class DynaAlgorithm(AbstractAlgorithm):
    base_algorithm: AbstractAlgorithm
    policy: Optional[AbstractPolicy]

    dynamical_model: AbstractModel
    reward_model: AbstractReward
    termination: Optional[Termination]
    reward_transformer: RewardTransformer
    value_function: Optional[AbstractValueFunction]

    num_steps: int
    num_samples: int
    def __init__(
        self,
        base_algorithm: AbstractAlgorithm,
        dynamical_model: AbstractModel,
        reward_model: AbstractReward,
        num_steps: int = ...,
        num_samples: int = ...,
        termination: Optional[Termination] = ...,
    ) -> None: ...
    def simulate(self, state: Tensor) -> Observation: ...
    def forward(self, observation: Tensor, **kwargs: Any) -> Observation: ...
