"""
AIPlayer module with AIPlayer class
"""

from copy import deepcopy

from pokai.src.ai_tools.monte_carlo import get_best_play

from pokai.src.game.card_play import Play
from pokai.src.game.hand import Hand, ADJ_TRIPLES, DOUBLE_STRAIGHTS, STRAIGHTS, TRIPLES, DOUBLES, SINGLES, QUADRUPLES, DOUBLE_JOKER
from pokai.src.game.player import Player

class AIPlayer(Player):

    def __init__(self, hand, position, t):
        super(AIPlayer, self).__init__(hand, position, t)

        """ Mutable configuration to decide lead play
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

    def _get_best_singular_basic(self, game_state, each_count):
        prev_play = game_state.prev_play
        base_card = None if not prev_play else prev_play.get_base_card()
        possible_plays = self.hand.get_possible_basics(base_card, each_count)
        return get_best_play(possible_plays, self, game_state)

    def _get_best_play_with_extra(self, game_state, base_play, extra_count, extra_each_count):
        """
        Gets the best play with extras assuming that the base play is the best of the base plays

        game_state -- current game state
        base_play -- the play to add extras to
        extra_count -- number of extras to add (1 for a one single or double; 2 for two singles or doubles)
        extra_each_count -- the occurance of the extras (1 for single, 2 for double)
        """

        prev_play = game_state.prev_play
        if not prev_play or not prev_play.num_extra:
            # TODO: if prev play is None, get best possible triple extras
            return base_play
        possible_extras = self.hand.get_possible_extra_cards(base_play.cards, extra_each_count, extra_count)
        possible_plays = [Play(self.position, base_play.cards + extra, prev_play.num_extra, prev_play.play_type)\
                          for extra in possible_extras]
        return get_best_play(possible_plays, self, game_state)

    def _get_best_singular_straight(self, game_state, each_count):
        prev_play = game_state.prev_play
        # TODO: if prev play is None, get best possible straight length
        base_card = None if not prev_play else prev_play.get_base_card()
        base_length = -1 if not prev_play else prev_play.num_base_cards() // each_count
        possible_plays = self.hand.get_possible_straights(base_card, each_count, base_length)
        return get_best_play(possible_plays, self, game_state)

    def get_best_singles(self, game_state):
        return self._get_best_singular_basic(game_state, 1)

    def get_best_doubles(self, game_state):
        return self._get_best_singular_basic(game_state, 2)

    def get_best_triples(self, game_state):
        best_play = self._get_best_singular_basic(game_state, 3)
        extra_each_count = game_state.prev_play.num_extra
        return self._get_best_play_with_extra(game_state, best_play, 1, extra_each_count)

    def get_best_straights(self, game_state):
        return self._get_best_singular_straight(game_state, 1)

    def get_best_double_straights(self, game_state):
        return self._get_best_singular_straight(game_state, 2)

    def get_best_adj_triples(self, game_state):
        best_play = self._get_best_singular_straight(game_state, 3)
        extra_each_count = game_state.prev_play.num_extra // 2
        return self._get_best_play_with_extra(game_state, best_play, 2, extra_each_count)

    def get_best_quad(self, game_state):
        best_play = self._get_best_singular_basic(game_state, 4)
        extra_each_count = game_state.prev_play.num_extra // 2
        return self._get_best_play_with_extra(game_state, best_play, 2, extra_each_count)

    def get_best_wild(self, game_state):
        pass
