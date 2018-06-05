"""
Player module with Player class
"""

from pokai.src.hand import Hand, ADJ_TRIPLES, DOUBLE_STRAIGHTS, STRAIGHTS, TRIPLES, DOUBLES, SINGLES, QUADRUPLES, DOUBLE_JOKER

class Player(object):
    """docstring for Player"""
    def __init__(self, hand, position, t):
        super(Player, self).__init__()
        self.hand = hand
        self.position = position
        self.type = t

    def reveal(self):
        print(self.hand)

    def info(self):
        self.hand.print_categories()

    def get_lead_play(self, in_game_hands, used_cards):
        """
        Gets the best play if this player is starting.
        Returns lead play
        """
        return self.hand.get_lead_play()

    def play(self, cards):
        self.hand.remove_cards(cards)
        for c in cards:
            print(c, end=" ")
        print()

    def get_play(self, prev_play, in_game_hands, used_cards):
        """
        Returns lowest play of play_type
        """
        if not prev_play or prev_play.position == self.position:
            # lead play
            next_play = self.get_lead_play(in_game_hands, used_cards)
        else:
            if prev_play.play_type == SINGLES:
                next_play = self.hand.get_low(prev_play.get_base_card(), 1)
            elif prev_play.play_type == DOUBLES:
                next_play = self.hand.get_low(prev_play.get_base_card(), 2)
            elif prev_play.play_type == TRIPLES:
                next_play = self.hand.get_low(prev_play.get_base_card(), 3,
                                              prev_play.num_extra)
            elif prev_play.play_type == STRAIGHTS:
                next_play = self.hand.get_low_straight(prev_play.get_base_card(),
                                                       1, prev_play.num_base_cards())
            elif prev_play.play_type == DOUBLE_STRAIGHTS:
                next_play = self.hand.get_low_straight(prev_play.get_base_card(),
                                                       2, int(prev_play.num_base_cards() / 2))
            elif prev_play.play_type == ADJ_TRIPLES:
                next_play = self.hand.get_low_adj_triple(prev_play.get_base_card(),
                                                         prev_play.num_extra)
            else: # prev_play.play_type == QUADRUPLES or DOUBLE_JOKER:
                next_play = self.hand.get_low_wild(prev_play.get_base_card())

            # if next play is none and the player has less than 5 * (number of wilds in hand) cards,
            # check if any wilds and play wilds only if triples, straights,
            # double_straights, and adj_triples
            if not next_play and in_game_hands[prev_play.position].num_cards() <= 5 * self.hand.get_num_wild():
                if prev_play.play_type != SINGLES and prev_play.play_type != DOUBLES:
                    next_play = self.hand.get_low_wild(None)

        if next_play:
            self.hand.remove_cards(next_play.cards)
            next_play.position = self.position
        return next_play

    def amount(self):
        return self.hand.num_cards()

    def in_game(self):
        return self.amount() > 0
