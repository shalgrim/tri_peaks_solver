from Card import Card
from Card import Suit
from Card import Rank
from Deck import Deck
from copy import deepcopy

class Game(object):
    """
    Has a tableau, stock, and discard
    Game.solve() generates a solution if one exists
    Game.moves() returns a list of Cards that are all legal moves, with discarding the top of the stock last
    Game.play(card) discards a card, whether from tableau or stock
    """
    def __init__(self, gameno=None):
        """
        Creates a game
        """
        self.tableau = []
        self.stock = []
        self.discard = None
        self.deck = Deck()
        self._setup(gameno)

    def _setup(self, gameno=None):
        if gameno is None:
            self.tableau = [
                self.deck['4S'], self.deck['10H'], self.deck['3D'],
                    self.deck['5S'], self.deck['10S'],
                    self.deck['AH'], self.deck['QC'],
                    self.deck['JD'], self.deck['4C'],
                        self.deck['2S'], self.deck['10D'], self.deck['6D'],
                        self.deck['10C'], self.deck['6C'], self.deck['3H'],
                        self.deck['AS'], self.deck['QS'], self.deck['JS'],
                self.deck['KD'], self.deck['QH'], self.deck['5H'],self.deck['AD'], self.deck['9C'],
                self.deck['KC'], self.deck['4H'], self.deck['7C'], self.deck['2C'], self.deck['JH'],
            ]
            self.stock = [
                self.deck['5D'], self.deck['6S'], self.deck['8H'], self.deck['3S'], self.deck['6H'], self.deck['8D'],
                self.deck['QD'], self.deck['JS'], self.deck['KS'], self.deck['9S'], self.deck['5C'], self.deck['8C'],
                self.deck['AC'], self.deck['3C'], self.deck['KH'], self.deck['7S'], self.deck['2H'], self.deck['7D'],
                self.deck['7H'], self.deck['8S'], self.deck['4D'], self.deck['9H'], self.deck['2D']
            ]
            self.discard = self.deck['9D']

        self._set_covering()

    def _set_covering(self):
        t = self.tableau

        t[27].covers(t[17])
        t[26].covers(t[17])
        t[26].covers(t[16])
        t[25].covers(t[16])
        t[25].covers(t[15])
        t[24].covers(t[15])
        t[24].covers(t[14])
        t[23].covers(t[14])
        t[23].covers(t[13])
        t[22].covers(t[13])
        t[22].covers(t[12])
        t[21].covers(t[12])
        t[21].covers(t[11])
        t[20].covers(t[11])
        t[20].covers(t[10])
        t[19].covers(t[10])
        t[19].covers(t[9])
        t[18].covers(t[9])

        t[17].covers(t[8])
        t[16].covers(t[8])
        t[16].covers(t[7])
        t[15].covers(t[7])

        t[14].covers(t[6])
        t[13].covers(t[6])
        t[13].covers(t[5])
        t[12].covers(t[5])

        t[11].covers(t[4])
        t[10].covers(t[4])
        t[10].covers(t[3])
        t[9].covers(t[3])

        t[8].covers(t[2])
        t[7].covers(t[2])
        t[6].covers(t[1])
        t[5].covers(t[1])
        t[4].covers(t[0])
        t[3].covers(t[0])

    def get_moves(self):
        moves = []
        for card in self.tableau:
            if card.covered_by:
                continue
            elif card.can_play(self.discard):
                moves.append(card)

        if self.stock:
            if self.stock[0].can_play(self.discard):
                moves.append(self.stock[0])

        return moves

    def play(self, card):
        if card in self.tableau:
            for covered in card.covering:
                del covered.covered_by[card]

            self.discard = card

        else: # must be in stock
            self.discard = card
            del self.stock[0]


    def solve(self, prev_moves = None):

        if len(self.tableau) == 0:
            return prev_moves

        if not prev_moves:
            prev_moves = []

        moves = self.get_moves()

        if not moves:
            return False

        for move in moves:
            new_game = deepcopy(self)
            new_game.play(move)
            prev_moves.append(move)
            solution =  new_game.solve(prev_moves)
            if solution:
                return solution
            else:
                prev_moves = prev_moves[:-1]

