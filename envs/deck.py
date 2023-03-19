import numpy as np

from .utils import CARD_VALUE_MAP, SUITS, RANKS
from .card import Card              

class Deck():
    def __init__(self):
        """ Deck of cards (no jokers)
        """
        self.cards = []

        # Build set of cards
        self.reset()

        # shuffle them
        self.shuffle()

        return

    @property
    def num_cards(self) -> int:
        return len(self.cards)

    def reset(self) -> None:
        """ Places all the cards into the deck. 
        """
        for rank in RANKS:
            for suit in SUITS:
                self.cards.append(Card(suit, rank, CARD_VALUE_MAP[rank]))
        return
    
    def shuffle(self) -> None:
        """ Shuffles the order of the cards in the deck. 
        """        
        np.random.shuffle(self.cards)
        return
    

    def draw(self) -> Card:
        """ Draws the next card from the top of the deck.
        """
        card = self.cards.pop()
        return card
    

if __name__ == '__main__':

    deck = Deck()

    card = deck.draw()
    print(card)