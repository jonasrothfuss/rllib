"""DQN Algorithm."""

from .q_learning import QLearning


class DQN(QLearning):
    r"""Implementation of Delayed Q Learning algorithm.

    The deep q-learning algorithm has a separate target network for the target value.

    Q_{target} = (r(s, a) + \gamma \max_a Q_{target}(s', a)).detach()

    References
    ----------
    Watkins, C. J., & Dayan, P. (1992). Q-learning. Machine learning, 8(3-4), 279-292.

    Mnih, Volodymyr, et al. "Human-level control through deep reinforcement learning."
    Nature 518.7540 (2015): 529-533.
    """

    def get_target(self, reward, next_state, done):
        """Get q function target."""
        next_v = self.q_target(next_state).max(dim=-1)[0]
        target_q = reward + self.gamma * next_v * (1 - done)
        return target_q
