"""SoftMax Policy."""

import torch

from rllib.util.utilities import tensor_to_distribution
from .abstract_q_function_policy import AbstractQFunctionPolicy
from ..random_policy import RandomPolicy


class SoftMax(AbstractQFunctionPolicy):
    r"""Implementation of Softmax Policy.

    A soft-max policy is one that has a policy given by:
    .. math:: \pi(a|s) \propto \rho(a|s) \exp[q(s, a) / \tau],
    where \rho(a|s) is a prior policy, usually selected at random.

    """

    def __init__(self, q_function, param, prior=None):
        super().__init__(q_function, param)
        if prior is None:
            prior = RandomPolicy(q_function.dim_state,
                                 q_function.dim_action,
                                 num_states=q_function.num_states,
                                 num_actions=q_function.num_actions)
        self.prior = prior

    @property
    def temperature(self):
        """Return temperature."""
        return self.param()

    def forward(self, state):
        """See `AbstractQFunctionPolicy.forward'."""
        q_val = self.q_function(state)
        prior = tensor_to_distribution(self.prior(state)).probs
        return torch.log(prior * torch.softmax(q_val / self.temperature, dim=-1))
