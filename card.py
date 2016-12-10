from enum import IntEnum

class Suit(IntEnum):
    C = 1
    D = 2
    H = 3
    S = 4

Rank = IntEnum('Rank', 'A 2 3 4 5 6 7 8 9 10 J Q K')

class Card(object):
    """
    A card from a playing deck. Has a rank and suit.
    """

    def __init__(self, r, s):
        """
        constructor
        :param r: Rank
        :param s: Suit
        """
        self.rank = r
        self.suit = s
        self.covering = set()
        self.covered_by = set()

    def covers(self, other):
        """
        adds other to this set's covering. adds self to others covered_by
        :param other: a Card
        :return: None
        """
        self.covering.add(other)
        other.covered_by.add(self)

    def can_play(self, other):
        if {self.rank, other.rank} == {Rank.K, Rank.A}:
            return True

        if self.rank + 1 == other.rank:
            return True

        if self.rank -1 == other.rank:
            return True

        return False

    def __str__(self):
        return self.rank.name + self.suit.name

    def __repr__(self):
        return str(self) # TODO: improve
