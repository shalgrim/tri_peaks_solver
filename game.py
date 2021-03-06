import sys
from deck import Deck
from copy import deepcopy

lowest_remaining = 28
unsolvable_games = set()


def game_from_file(fn):
    with open(fn) as f:
        lines = f.readlines()

    tline = lines[0].strip().split()
    sline = lines[1].strip().split()
    dline = lines[2].strip()

    deck = Deck()
    tableau = [deck[k] for k in tline]
    stock = [deck[k] for k in sline]
    discard = deck[dline]

    g = Game()
    g.setup_from_objects(deck, tableau, stock, discard)
    # g.deck = deck
    # g.tableau = tableau
    # g.stock = stock
    # g.discard = discard
    return g


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
        self.prev_moves = []
        if gameno:
            self._setup_from_number(gameno)

    def __repr__(self):
        """
        Used to represent a given state in a game so that we don't re-search states known to be unsolveable
        """
        answer = ''
        if self.tableau:
            answer += ','.join([str(c) for c in self.tableau])

        answer += '|'

        if self.stock:
            answer += ','.join(str(c) for c in self.stock)

        answer += '|'

        if self.discard:
            answer += str(self.discard)

        return answer


    def _setup_from_number(self, gameno=None):
        self.deck = Deck()
        if gameno is None:
            self.tableau = [
                self.deck['3D'], self.deck['QH'], self.deck['4D'],
                self.deck['9S'], self.deck['QC'],
                self.deck['10D'], self.deck['KC'],
                self.deck['8H'], self.deck['10S'],
                self.deck['AC'], self.deck['3H'], self.deck['2S'],
                self.deck['8D'], self.deck['5C'], self.deck['KS'],
                self.deck['2C'], self.deck['6H'], self.deck['2D'],
                self.deck['4S'], self.deck['6D'], self.deck['5D'], self.deck['JD'], self.deck['AH'],
                self.deck['6S'], self.deck['QS'], self.deck['JH'], self.deck['3S'], self.deck['2H'],
            ]
            self.stock = [
                self.deck['9D'], self.deck['8S'], self.deck['6C'], self.deck['5H'], self.deck['7H'], self.deck['7S'],
                self.deck['4H'], self.deck['JS'], self.deck['4C'], self.deck['8C'], self.deck['KH'], self.deck['10C'],
                self.deck['QD'], self.deck['JC'], self.deck['KD'], self.deck['10H'], self.deck['3C'], self.deck['7D'],
                self.deck['7C'], self.deck['AS'], self.deck['9H'], self.deck['AD'], self.deck['9C']
            ]
            self.discard = self.deck['5S']

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
            moves.append(self.stock[0])

        return moves

    def play(self, card_string):
        card = self.deck[card_string]
        if card in self.tableau:
            for covered in card.covering:
                covered.covered_by.remove(card)

            self.discard = card
            self.tableau.remove(card)

        else:  # must be in stock
            assert card in self.stock, '{} not in stock'.format(card)
            self.discard = card
            self.stock.remove(card)

        self.prev_moves.append(card)

        return

    def solve(self):
        global lowest_remaining, unsolvable_games

        if len(self.tableau) == 0:  # solved
            print('Successful moves: {}'.format(self.prev_moves))
            return self.prev_moves

        if repr(self) in unsolvable_games:
            return False

        moves = self.get_moves()

        if not moves:  # failed

            if len(self.tableau) <= lowest_remaining:
                print('Failing with {} cards left in tableau'.format(len(self.tableau)), file=sys.stderr)
                print('Failed sequence: {}'.format(str(self.prev_moves)), file=sys.stderr)
                lowest_remaining = len(self.tableau)

            return False

        for move in moves:
            new_game = deepcopy(self)
            new_game.play(str(move))
            solution = new_game.solve()
            if solution:
                return solution

        unsolvable_games.add(repr(self))
        return False

    def setup_from_objects(self, deck, tableau, stock, discard):
        self.deck = deck
        self.tableau = tableau
        self.stock = stock
        self.discard = discard
        self._set_covering()
        return
