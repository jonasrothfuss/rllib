from .abstract_q_function_policy import AbstractQFunctionPolicy
from torch import Tensor
from torch.distributions import Categorical


class MellowMax(AbstractQFunctionPolicy):
    def forward(self, *args: Tensor, **kwargs) -> Categorical: ...
