from .abstract_policy import AbstractPolicy
from rllib.dataset.datatypes import Distribution
from typing import Iterator
from torch import Tensor


class RandomPolicy(AbstractPolicy):
    def __init__(self, dim_state: int, dim_action: int,
                 num_states: int = None, num_actions: int = None) -> None: ...


    def __call__(self, state: Tensor) -> Distribution: ...
