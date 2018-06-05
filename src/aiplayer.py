"""
AIPlayer module with AIPlayer class
"""

from pokai.src.hand import Hand, ADJ_TRIPLES, DOUBLE_STRAIGHTS, STRAIGHTS, TRIPLES, DOUBLES, SINGLES, QUADRUPLES, DOUBLE_JOKER
from pokai.src.player import Player

class AIPlayer(Player):

    def __init__(self, hand, position, t):
        super(AIPlayer, self).__init__(hand, position, t)

        """ MUTATABLE """
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

    # def get_lead_play(self, in_game_hands, used_cards):
    #     """
    #     Gets the best play if this player is starting.
    #     Returns lead play
    #     """
    #     return super.get_lead_play(in_game_hands, used_cards)

    # def get_play(self, prev_play, in_game_hands, used_cards):
    #     """
    #     Returns lowest play of play_type
    #     """
    #     if not prev_play or prev_play.position == self.position:
    #         # lead play
    #         next_play = self.get_lead_play(in_game_hands, used_cards)
    #     else:
    #         if prev_play.play_type == SINGLES:
    #             next_play = self.hand.get_low(prev_play.get_base_card(), 1)
    #         elif prev_play.play_type == DOUBLES:
    #             next_play = self.hand.get_low(prev_play.get_base_card(), 2)
    #         elif prev_play.play_type == TRIPLES:
    #             next_play = self.hand.get_low(prev_play.get_base_card(), 3,
    #                                           prev_play.num_extra)
    #         elif prev_play.play_type == STRAIGHTS:
    #             next_play = self.hand.get_low_straight(prev_play.get_base_card(),
    #                                                    1, prev_play.num_base_cards())
    #         elif prev_play.play_type == DOUBLE_STRAIGHTS:
    #             next_play = self.hand.get_low_straight(prev_play.get_base_card(),
    #                                                    2, int(prev_play.num_base_cards() / 2))
    #         elif prev_play.play_type == ADJ_TRIPLES:
    #             next_play = self.hand.get_low_adj_triple(prev_play.get_base_card(),
    #                                                      prev_play.num_extra)
    #         else: # prev_play.play_type == QUADRUPLES or DOUBLE_JOKER:
    #             next_play = self.hand.get_low_wild(prev_play.get_base_card())

    #         # if next play is none and the player has less than 5 * (number of wilds in hand) cards,
    #         # check if any wilds and play wilds only if triples, straights,
    #         # double_straights, and adj_triples
    #         if not next_play and in_game_hands[prev_play.position].num_cards() <= \
    #                              self.bomb_threshold * self.hand.get_num_wild():
    #             if prev_play.play_type != SINGLES and prev_play.play_type != DOUBLES:
    #                 next_play = self.hand.get_low_wild(prev_play.get_base_card())

    #     if next_play:
    #         self.hand.remove_cards(next_play.cards)
    #     return next_play
