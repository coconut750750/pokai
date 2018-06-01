"""
Card play module.
Contains a class that holds information about a
play in the game.
"""

class Play(object):
    """Play class"""

    def __init__(self, position, cards, num_extra, play_type):
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
        self.play_type = play_type

    def num_base_cards(self):
        """Returns number of cards in play"""
        return len(self.cards) - self.num_extra

    def get_base_card(self):
        """Returns the base value of this play"""
        return self.cards[0]

    def __str__(self):
        """Return string representation"""
        sep = " | "
        s = "Player {} ".format(self.position) + sep
        for card in self.cards:
            s += card.display + sep
        return s.strip()
