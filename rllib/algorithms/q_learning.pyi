from typing import Union

from torch import Tensor
from torch.nn.modules.loss import _Loss

from rllib.dataset.datatypes import Observation
from rllib.policy.q_function_policy import SoftMax
from rllib.util.parameter_decay import ParameterDecay
from rllib.value_function import AbstractQFunction

from .abstract_algorithm import AbstractAlgorithm, TDLoss

class QLearning(AbstractAlgorithm):
    q_function: AbstractQFunction
    q_target: AbstractQFunction
    criterion: _Loss
    gamma: float
    def __init__(
        self, q_function: AbstractQFunction, criterion: _Loss, gamma: float
    ) -> None: ...
    def get_target(
        self, reward: Tensor, next_state: Tensor, done: Tensor
    ) -> Tensor: ...
    def forward(self, observation: Observation, **kwargs) -> TDLoss: ...
    def _build_return(self, pred_q: Tensor, target_q: Tensor) -> TDLoss: ...
    def update(self) -> None: ...

class GradientQLearning(QLearning): ...
class DQN(QLearning): ...
class DDQN(QLearning): ...

class SoftQLearning(QLearning):
    policy: SoftMax
    policy_target: SoftMax
    def __init__(
        self,
        q_function: AbstractQFunction,
        criterion: _Loss,
        temperature: Union[float, ParameterDecay],
        gamma: float,
    ) -> None: ...
