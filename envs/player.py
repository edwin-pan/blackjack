import numpy as np

from envs.card import Card

class Player():
    def __init__(self):
        self._value = 0     # Value of the current hand
        self._cards = []    # Cards in the current hand

        return
    
    def reset(self):
        self._value = 0
        self._cards = []

    def add_card(self, card:Card):
        """ Add a card and increment the value of the hand
        
        """
        self._cards.append(card)
        self._value += card.value
        return
    
    @property
    def value(self):
        return self._value
    
    @property
    def cards(self):
        return self._cards