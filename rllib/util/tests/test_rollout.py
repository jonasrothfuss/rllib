import pytest

from rllib.agent import RandomAgent
from rllib.environment import GymEnvironment, EasyGridWorld
from rllib.policy import RandomPolicy
from rllib.util import rollout_policy, rollout_agent


@pytest.fixture(params=['CartPole-v0', 'Pendulum-v0', 'MountainCarContinuous-v0',
                        'Taxi-v2'])
def environment(request):
    return GymEnvironment(request.param)


def test_rollout_policy(environment):
    policy = RandomPolicy(environment.dim_state, environment.dim_action,
                          num_actions=environment.num_actions)
    trajectory = rollout_policy(environment, policy)

    assert len(trajectory) > 0


def test_rollout_agent(environment):
    agent = RandomAgent(environment.dim_state, environment.dim_action,
                        num_actions=environment.num_actions)
    rollout_agent(environment, agent)


def test_rollout_easy_grid_world():
    environment = EasyGridWorld()
    agent = RandomAgent(environment.dim_state, environment.dim_action,
                        num_actions=environment.num_actions)
    rollout_agent(environment, agent, max_steps=20)

    policy = agent.policy
    rollout_policy(environment, policy)
