"""
Card play module.
Contains a class that holds information about a
play in the game.
"""

from itertools import groupby
from pokai.src.game.game_tools import SINGLES, DOUBLES, TRIPLES, QUADRUPLES, STRAIGHTS,\
                                 DOUBLE_STRAIGHTS, ADJ_TRIPLES, DOUBLE_JOKER
from pokai.src.game.card import SMALL_JOKER_VALUE

class Play(object):
    """Play class"""

    @staticmethod
    def get_play_from_cards(cards_played):
        """Returns a new Play object based on cards played"""
        total_cards = len(cards_played)
        group_counts = [0, 0, 0, 0]
        counts = {value : len(list(c)) for value, c in groupby(cards_played, lambda card: card.value)}
        distinct_cards = len(counts)

        for val, count in counts.items():
            group_counts[count - 1] += 1

        if total_cards == 1:
            return Play(-1, cards_played, 0, play_type=SINGLES)
        elif total_cards == 2 and cards_played[0].value < SMALL_JOKER_VALUE:
            return Play(-1, cards_played, 0, play_type=DOUBLES)
        elif total_cards == 2 and cards_played[0].value >= SMALL_JOKER_VALUE:
            return Play(-1, cards_played, 0, play_type=DOUBLE_JOKER)
        elif group_counts[0] == distinct_cards:
            return Play(-1, cards_played, 0, play_type=STRAIGHTS)
        elif group_counts[1] == distinct_cards:
            return Play(-1, cards_played, 0, play_type=DOUBLE_STRAIGHTS)
        elif group_counts[2] == 1:
            extra = group_counts[0] + group_counts[1] * 2
            return Play(-1, cards_played, extra, play_type=TRIPLES)
        elif group_counts[2] == 2:
            extra = group_counts[0] + group_counts[1] * 2
            return Play(-1, cards_played, extra, play_type=ADJ_TRIPLES)
        elif group_counts[3] == 1:
            extra = group_counts[0] + group_counts[1] * 2
            return Play(-1, cards_played, extra, play_type=QUADRUPLES)

        return None

    def __init__(self, position, cards, num_extra, play_type=""):
        """
        Constructor
        Arguments:
        position -- the position of the player that played this
        cards -- the cards played
        num_extra -- the extra cards that were played
        play_type -- the kind of play
        """
        self.position = position
        self.cards = cards
        self.num_extra = num_extra
        if not play_type:
            self.play_type = Play.get_play_from_cards(cards).play_type
        else:
            self.play_type = play_type

    def num_base_cards(self):
        """Returns number of cards in play"""
        return len(self.cards) - self.num_extra

    def num_cards(self):
        """returns total number of cards"""
        return len(self.cards)

    def get_base_card(self):
        """Returns the base card of this play (the card another player needs to beat)"""
        return self.cards[0]

    def __str__(self):
        """Return string representation"""
        sep = " | "
        s = "Player {} ({} with {} extra cards) ".format(self.position, self.play_type, self.num_extra) + sep
        for card in self.cards:
            s += card.display + sep
        return s.strip()

    def __repr__(self):
        sep = " | "
        s = "{} with {} extra cards".format(self.play_type, self.num_extra) + sep
        for card in self.cards:
            s += card.display + sep
        return "[{}]".format(s.strip())
