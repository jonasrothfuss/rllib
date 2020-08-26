"""Interface for policies."""

from abc import ABCMeta

import numpy as np
import torch
import torch.jit
import torch.nn as nn


class AbstractPolicy(nn.Module, metaclass=ABCMeta):
    """Interface for policies to control an environment.

    Parameters
    ----------
    dim_state: Tuple
        dimension of state.
    dim_action: Tuple
        dimension of action.
    num_states: int, optional
        number of discrete states (None if state is continuous).
    num_actions: int, optional
        number of discrete actions (None if action is continuous).

    Attributes
    ----------
    dim_state: Tuple
        dimension of state.
    dim_action: Tuple
        dimension of action.
    num_states: int
        number of discrete states (None if state is continuous).
    num_actions: int
        number of discrete actions (None if action is continuous).
    tau: float, optional.
        low pass coefficient for parameter update.
    deterministic: bool, optional.
        flag that indicates if the policy is deterministic.
    action_scale: float, optional.
        Magnitude of output scale.
    """

    def __init__(
        self,
        dim_state,
        dim_action,
        num_states=-1,
        num_actions=-1,
        tau=0.0,
        deterministic=False,
        action_scale=1,
        goal=None,
        *args,
        **kwargs,
    ):
        super().__init__()
        self.dim_state = dim_state
        self.dim_action = dim_action
        self.num_states = num_states if num_states is not None else -1
        self.num_actions = num_actions if num_actions is not None else -1
        self.deterministic = deterministic
        self.discrete_state = self.num_states >= 0
        self.discrete_action = self.num_actions >= 0
        self.tau = tau

        if self.discrete_action:
            action_scale = torch.tensor(1)
        elif isinstance(action_scale, np.ndarray):
            action_scale = torch.tensor(action_scale, dtype=torch.get_default_dtype())
        elif not isinstance(action_scale, torch.Tensor):
            action_scale = torch.full(
                self.dim_action, action_scale, dtype=torch.get_default_dtype()
            )

        if not self.discrete_action and len(action_scale) < self.dim_action[0]:
            extra_dim = self.dim_action[0] - len(action_scale)
            action_scale = torch.cat((action_scale, torch.ones(extra_dim)))

        self.action_scale = action_scale
        self.goal = goal

    def random(self, batch_size=None, normalized=False):
        """Return a uniform random distribution of the output space.

        Parameters
        ----------
        batch_size: tuple, optional
        normalized: bool, optional.

        Returns
        -------
        distribution: torch.distribution.Distribution

        """
        if self.discrete_action:  # Categorical
            if batch_size is None:
                return torch.ones(self.num_actions)
            else:
                return torch.ones(*batch_size, self.num_actions)
        else:
            cov = torch.eye(self.dim_action[0])
            if not normalized:
                cov *= self.action_scale

            if batch_size is None:
                return torch.zeros(self.dim_action[0]), cov
            else:
                return (
                    torch.zeros(*batch_size, self.dim_action[0]),
                    cov.expand(*batch_size, self.dim_action[0], self.dim_action[0]),
                )

    @torch.jit.export
    def reset(self):
        """Reset policy parameters (for example internal states)."""
        pass

    @torch.jit.export
    def update(self):
        """Update policy parameters."""
        pass

    @torch.jit.export
    def set_goal(self, goal=None):
        """Set policy goal."""
        if goal is not None:
            self.goal = goal
