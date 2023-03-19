import numpy as np

from .utils import STAND, HIT, DOUBLE

class BaseModelBasedPolicy(object):
    """ Initializes a Q Learning Model. """
    def __init__(self):
        self._t = 0
        self._num_states = 172
        self._num_actions = 3

        raise NotImplementedError()
        return
    
    def _initialize_mg(self):
        # Discount Factor
        self.gamma = 0.9

        # State Space
        self.states = self._num_states*[0]

        # Action Space
        self.actions = [STAND, HIT, DOUBLE]

        # Transition Count
        self.transition = np.zeros((self._num_states, 
                                    self._num_actions, 
                                    self._num_states))

        # Reward -- sum (p)
        self.rewardsum = np.zeros((self._num_states, 
                                self._num_actions))

        # Utility -- value function -- one utility value for each state
        self.utility = np.zeros(self._num_states)

        return
    

    def lookahead(self, s, a) -> float:
        """ Maximum Likelihood MDP -- lookahead function. """

        num_visits = np.sum(self.transition[s, a, :])
        if not num_visits:
            return 0
        reward = self.rewardsum[s, a] / num_visits

        utility = reward + self.gamma*np.sum((self.transition/num_visits)*self.utility)
        return utility
    
    def backup(self, s) -> float:
        """ Maximum Likelihood MDP -- backup function. """

        state_utility = np.maximum(self.lookahead(s, a) for a in self.actions)

        return state_utility

    def update(self, s, a, r, sp) -> None:
        """ Maximum Likelihood MDP -- update function. """
        
        return

    def reset(self):
        self._t = 0
    
        return
    
    @property
    def t(self):
        return self._t
    
    