import numpy as np

from .base_mf_policy import BaseModelFreePolicy
from .base_mb_policy import BaseModelBasedPolicy
from .utils import STAND, HIT, DOUBLE


class EpsilonGreedyPolicy(BaseModelFreePolicy):
    def __init__(self, epsilon=0.3):
        super().__init__()

        self._epsilon = epsilon

        return
    
    @property
    def epsilon(self):
        return self._epsilon

    @epsilon.setter
    def epsilon(self, value):
        if value < 0:
            raise ValueError(f"Epsilon cannot be less than 0. Got {value}")
        elif value > 1:
            raise ValueError(f"Epsilon cannot be greater than 1. Got {value}")
        print("Setting value...")
        self._epsilon = value

    @property
    def epsilon(self, epsilon):
        self.epsilon = epsilon
        return

    def step(self, env):

        # Step time
        self._t += 1

        # Be epsilon greedy
        if np.random.rand() < self._epsilon:
            # Be greedy
            action = np.random.choice(self.actions)
            if (action == DOUBLE) and (env.player_value not in [10, 11]):
                # Double is not a valid action atm. 
                action = np.random.choice([STAND, HIT])
        else:
            # Be compliant
            action = super().step(env)

        return action