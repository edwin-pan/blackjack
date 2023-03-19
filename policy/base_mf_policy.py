import numpy as np

from .utils import value_to_state_id, STAND, HIT, DOUBLE

class BaseModelFreePolicy(object):
    """ Initializes a Maximum Likelihood MDP. """
    def __init__(self):
        self._t = 0
        self._num_states = 172
        self._num_actions = 3

        self._initialize_mg()

        return
    
    def _initialize_mg(self):
        # Learning rate
        self.lr = 1E-3 # Alpha

        # Discount Factor
        self.gamma = 0.95

        # State Space
        self.states = self._num_states*[0]

        # Action Space
        self.actions = [STAND, HIT, DOUBLE]

        # Action Value Function 
        self.Q = np.zeros((self._num_states, self._num_actions))

        return

    def lookahead(self, s, a) -> float:
        """ Q-Learning -- lookahead function. """
        return self.Q[s,a]
    
    def update(self, s, a, r, sp) -> None:
        """ Q-Learning -- update function. """
        self.Q[s,a] += self.lr*(r + self.gamma*np.max(self.Q[sp]) - self.Q[s,a])
        return


    def step(self, env):
        """ Step taken in the simulator. Update the model, choose an action. """
        
        # Parse the env, get the state.
        state_id = value_to_state_id(env.player_value, env.dealer_value)

        # Get action
        action = np.argmax(self.Q[state_id])
        if (action == DOUBLE) and (env.player_value not in [10, 11]):
            # Double is not a valid action atm. 
            action = np.argmax(self.Q[state_id, :-1])

        return action


    def reset(self):
        self._t = 0
    
        return
    
    @property
    def t(self):
        return self._t
    
    