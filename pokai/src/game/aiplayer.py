"""
AIPlayer module with AIPlayer class
"""

from copy import deepcopy

from pokai.src.ai_tools.monte_carlo import get_best_play, estimate_play_strength,\
                                           estimate_hand_strength

from pokai.src.game.card_play import Play
from pokai.src.game.hand import Hand, ADJ_TRIPLES, DOUBLE_STRAIGHTS, STRAIGHTS,\
                                TRIPLES, DOUBLES, SINGLES, QUADRUPLES, DOUBLE_JOKER
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
        self.best_play_threshold = 0.95 # will only play if the best play strength is >= .95 * pass_play_strength

    def get_hand_strength(self, game_state):
        return estimate_hand_strength(self, game_state)

    def _get_best_singular_basic(self, game_state, each_count):
        """
        Gets the best singluar basic play
        each_count -- the occurance of the cards in the play
        """
        prev_play = game_state.prev_play
        base_card = None if not prev_play else prev_play.get_base_card()
        possible_plays = self.hand.generate_possible_basics(base_card, each_count)
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
        possible_extras = self.hand.generate_possible_extra_cards(base_play.cards, extra_each_count, extra_count)
        possible_plays = [Play(self.position, base_play.cards + extra, prev_play.num_extra, prev_play.play_type)\
                          for extra in possible_extras]
        return get_best_play(possible_plays, self, game_state)

    def _get_best_singular_straight(self, game_state, each_count):
        """
        Gets the best straight without any extras
        each_count -- the occurance of each card in the straight
        """
        prev_play = game_state.prev_play
        # TODO: if prev play is None, get best possible straight length
        base_card = None if not prev_play else prev_play.get_base_card()
        base_length = -1 if not prev_play else prev_play.num_base_cards() // each_count
        possible_plays = self.hand.generate_possible_straights(base_card, each_count, base_length)
        return get_best_play(possible_plays, self, game_state)

    def include_pass_play(get_best_specific_play):
        def wrapper(self, game_state):
            best_play = get_best_specific_play(self, game_state)
            if best_play:
                pass_play_strength = estimate_play_strength(None, self, game_state)
                if best_play.strength < pass_play_strength * self.best_play_threshold:
                    return None
            return best_play
        return wrapper

    def get_best_lead_play(self, game_state):
        """
        Gets the best play if this player is starting.
        Returns lead play
        """
        possible_leads = self.get_possible_leads(game_state)
        return get_best_play(possible_leads, self, game_state)

    @include_pass_play
    def get_best_singles(self, game_state):
        return self._get_best_singular_basic(game_state, 1)

    @include_pass_play
    def get_best_doubles(self, game_state):
        return self._get_best_singular_basic(game_state, 2)

    @include_pass_play
    def get_best_triples(self, game_state):
        best_play = self._get_best_singular_basic(game_state, 3)
        if not best_play:
            return None
        extra_each_count = game_state.prev_play.num_extra
        return self._get_best_play_with_extra(game_state, best_play, 1, extra_each_count)

    @include_pass_play
    def get_best_straights(self, game_state):
        return self._get_best_singular_straight(game_state, 1)

    @include_pass_play
    def get_best_double_straights(self, game_state):
        return self._get_best_singular_straight(game_state, 2)

    @include_pass_play
    def get_best_adj_triples(self, game_state):
        best_play = self._get_best_singular_straight(game_state, 3)
        if not best_play:
            return None
        extra_each_count = game_state.prev_play.num_extra // 2
        return self._get_best_play_with_extra(game_state, best_play, 2, extra_each_count)

    @include_pass_play
    def get_best_quad(self, game_state):
        best_play = self._get_best_singular_basic(game_state, 4)
        if not best_play:
            return None
        extra_each_count = game_state.prev_play.num_extra // 2
        return self._get_best_play_with_extra(game_state, best_play, 2, extra_each_count)

    @include_pass_play
    def get_best_wild(self, game_state):
        prev_play = game_state.prev_play
        base_card = None if not prev_play else prev_play.get_base_card()
        possible_plays = self.hand.generate_possible_wilds(base_card)
        return get_best_play(possible_plays, self, game_state)
