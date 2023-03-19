
import numpy as np

from .base_mf_policy import BaseModelFreePolicy
from .base_mb_policy import BaseModelBasedPolicy
from .utils import value_to_state_id

from .utils import STAND, HIT, DOUBLE

class RandomPolicy(BaseModelFreePolicy):
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug

        return
    
    def step(self, env):
        
        # Step time
        self._t += 1

        # Grab current state id
        # Parse the env, get the state.
        state_id = value_to_state_id(env.player_value, env.dealer_value)

        # Criteria 5 -- Random if none of the criteria satisified
        random_act = np.random.choice([STAND, HIT, DOUBLE])
        if (random_act == DOUBLE) and (env.player_value not in [10, 11]):
            # Double is not a valid action atm. 
            random_act = np.random.choice([STAND, HIT])
        self.Q[state_id, random_act] += 1

        if self.debug:
            print(f"[POLICY] Choose a random act: {random_act}")

        return random_act
