import numpy as np
import pytest
import torch

from rllib.agent import (
    A2CAgent,
    ActorCriticAgent,
    DDQNAgent,
    DPGAgent,
    DQNAgent,
    ExpectedActorCriticAgent,
    ExpectedSARSAAgent,
    GAACAgent,
    MPCAgent,
    MPOAgent,
    PPOAgent,
    QLearningAgent,
    RandomAgent,
    REINFORCEAgent,
    REPSAgent,
    SACAgent,
    SARSAAgent,
    SoftQLearningAgent,
    TD3Agent,
    TRPOAgent,
    VMPOAgent,
)
from rllib.environment import GymEnvironment
from rllib.util.training import evaluate_agent, train_agent

MAX_STEPS = 25
NUM_EPISODES = 25
SEED = 0


@pytest.fixture(params=["CartPole-v0", "NChain-v0"])
def discrete_environment(request):
    return request.param


@pytest.fixture(params=["MountainCarContinuous-v0"])
def continuous_environment(request):
    return request.param


@pytest.fixture(
    params=[
        ActorCriticAgent,
        A2CAgent,
        ExpectedActorCriticAgent,
        GAACAgent,
        REINFORCEAgent,
        ExpectedSARSAAgent,
        SARSAAgent,
        QLearningAgent,
        SoftQLearningAgent,
        DDQNAgent,
        DQNAgent,
        REPSAgent,
        MPOAgent,
        PPOAgent,
        TRPOAgent,
        RandomAgent,
        VMPOAgent,
    ]
)
def discrete_agent(request):
    return request.param


@pytest.fixture(
    params=[
        ActorCriticAgent,
        A2CAgent,
        ExpectedActorCriticAgent,
        GAACAgent,
        REINFORCEAgent,
        DPGAgent,
        TD3Agent,
        SACAgent,
        REPSAgent,
        MPOAgent,
        MPCAgent,
        PPOAgent,
        TRPOAgent,
        RandomAgent,
        VMPOAgent,
    ]
)
def continuous_agent(request):
    return request.param


def rollout_agent(environment, agent):
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    environment = GymEnvironment(environment, SEED)
    agent = agent.default(environment, test=True)
    train_agent(agent, environment, NUM_EPISODES, MAX_STEPS, plot_flag=False)
    evaluate_agent(agent, environment, 1, MAX_STEPS, render=False)


def test_discrete_agent(discrete_environment, discrete_agent):
    rollout_agent(discrete_environment, discrete_agent)


def test_continuous_agent(continuous_environment, continuous_agent):
    rollout_agent(continuous_environment, continuous_agent)