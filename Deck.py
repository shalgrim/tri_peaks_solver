from collections import OrderedDict
import random
from Card import Card
from Card import Rank
from Card import Suit

class Deck(object):
    """
    A 52-card playing deck
    """

    def __init__(self):
        """
        Creates list of cards, one for each in a 52-card deck
        """
        self.cards = OrderedDict()
        for r in Rank:
            for s in Suit:
                self.cards[r.name+s.name] = Card(Rank[r.name], Suit[s.name])
        assert len(self.cards) == 52

    def shuffle(self, seed=None):
        """
        Randomly sorts cards
        :param seed: you can seed the shuffle if you want
        :return: None
        """
        random.seed(seed)
        random.shuffle(self.cards)
