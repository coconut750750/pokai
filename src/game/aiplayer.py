"""
AIPlayer module with AIPlayer class
"""

from pokai.src.ai_tools.monte_carlo import get_best_play
from pokai.src.game.hand import Hand, ADJ_TRIPLES, DOUBLE_STRAIGHTS, STRAIGHTS, TRIPLES, DOUBLES, SINGLES, QUADRUPLES, DOUBLE_JOKER
from pokai.src.game.player import Player

class AIPlayer(Player):

    def __init__(self, hand, position, t):
        super(AIPlayer, self).__init__(hand, position, t)

        """ MUTATABLE
        # order of lead plays
        self.order = [ADJ_TRIPLES, DOUBLE_STRAIGHTS, STRAIGHTS, TRIPLES, 
                      DOUBLES, SINGLES, QUADRUPLES, DOUBLE_JOKER]
        # order of playing extra triple cards
        self.triple_order = [2, 1, 0]
        # order of playing extra adj_triple cards
        self.adj_triple_order = [2, 4, 0]
        # play long (True) straights or short straights first?
        self.long_straight_priority = True
        if self.long_straight_priority:
            self._straight_start = 12
            self._straight_end = 5
            self._straight_diff = -1
        else:
            self._straight_start = 5
            self._straight_end = 12
            self._straight_diff = 1
        # the greater it is, the earlier player will bomb, use ace, use two
        self.bomb_threshold = 5
        self.use_ace_threshold = 5
        self.use_two_threshold = 5
        """

    def get_play(self, game_state):
        prev_play = game_state.prev_play
        unrevealed_cards = []
        if not prev_play or prev_play.position == self.position:
            # lead play
            next_play = self._get_lead_play(game_state)
        else:
            next_play = self.hand.get_low_play(prev_play)
            # if next play is none and the player has less than 5 * (number of wilds in hand) cards,
            # play wilds
            if not next_play and game_state.get_player_num_cards(prev_play.position) <= 5 * self.hand.get_num_wild():
                next_play = self.hand.get_low_wild(None)

        if next_play:
            next_play.position = self.position
        return next_play

    def get_best_singles(self, game_state):
        prev_play = game_state.prev_play
        possible_plays = self.hand.get_possible_basics(prev_play.get_base_card(), 1)
        best_possible = get_best_play(possible_plays, self, game_state)
        return best_possible

    def get_best_doubles(self, game_state):
        pass

    def get_best_extra(self, game_state):
        pass

    def get_best_triples(self, game_state):
        pass

    def get_best_straights(self, game_state):
        pass

    def get_best_double_straights(self, game_state):
        pass

    def get_best_adj_triples(self, game_state):
        pass

    def get_best_wild(self, game_state):
        pass
