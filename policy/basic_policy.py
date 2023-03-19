
import numpy as np

from .base_mf_policy import BaseModelFreePolicy
from .utils import value_to_state_id
from .utils import STAND, HIT, DOUBLE

class ScriptedEddiePolicy(BaseModelFreePolicy):
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

        # Criteria 0 -- Hit on player value < 10
        if env.player_value < 10:
            if self.debug:
                print(f"[POLICY] Choose {HIT}")
            self.Q[state_id, HIT] += 1
            return HIT

        # Criteria 1 -- STAND on value 17+
        if env.player_value >= 17:
            if self.debug:
                print(f"[POLICY] Choose {STAND}")
            self.Q[state_id, STAND] += 1
            return STAND

        # Criteria 2 -- HIT on 12-16, given dealer has more than 7
        if env.dealer_value > 7:
            if (env.player_value>=12) and (env.player_value <= 16):
                if self.debug:
                    print(f"[POLICY] Choose {HIT}")
                self.Q[state_id, HIT] += 1
                return HIT

        # Criteria 3 -- STAND on 13-16, given dealer has less than 6
        if env.dealer_value <= 6:
            if (env.player_value>=13) and (env.player_value <= 16):
                if self.debug:
                    print(f"[POLICY] Choose {STAND}")
                self.Q[state_id, STAND] += 1
                return STAND

        # Criteria 4 -- HIT on 12, given dealer shows 2 or 3
        if env.dealer_value in [2, 3]:
            if env.player_value == 12:
                if self.debug:
                    print(f"[POLICY] Choose {HIT}")
                self.Q[state_id, HIT] += 1
                return HIT

        # Criteria 5 -- Random if none of the criteria satisified
        random_act = np.random.choice([STAND, HIT])
        self.Q[state_id, DOUBLE] += 1

        if self.debug:
            print(f"[POLICY] Choose a random act: {random_act}")

        return random_act
