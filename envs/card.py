import numpy as np

from .utils import SUITS, RANKS, RANKS_ABREV, SUITS_ABREV

class Card():
    def __init__(self, suit:str, rank:str, value:int):        
        
        assert suit in SUITS
        assert rank in RANKS

        self._suit = suit.lower()
        self._rank = rank.lower()
        self._value = value
        
        return

    def __str__(self):
        return f"{self.rank.upper()} of {self.suit.upper()} with value {self.value}"

    def __repr__(self):
        return f"{SUITS_ABREV[self.suit]}-{RANKS_ABREV[self.rank]}-{self.value}"
    
    @property
    def suit(self):
        return self._suit    

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        
        if self.rank not in ['ace']:
            raise ValueError(f"Can only change the value of Ace. \
                                Attempted on {self.rank}")
        elif new_value not in [1, 11]:
            raise ValueError(f"Can only change Ace value between 1 and 11.  \
                             Attempted {new_value}")
        
        self._value = new_value
        return 