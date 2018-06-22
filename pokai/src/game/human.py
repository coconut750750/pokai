"""
Human module
"""

class Human(object):
    """docstring for Human"""
    def __init__(self, request_play, num_cards, revealed_cards=None):
        """
        Arguments
        request_play -- function to call when ask for the play
        num_cards -- number of cards player has
        revealed_cards -- list of revealed cards (if human is king)
        """
        self.request_play = request_play
        self.num_cards = n_cards
        if not revealed_cards:
            self.revealed_cards = []
        else:
            self.revealed_cards = revealed_cards

    def request_for_play(self):
        """
        Gets the play from human by calling request_play
        """
        cards = self.request_play()
        return cards

    def play(self, card_play):
        self.n_cards -= card_play.num_cards()
        print("{}".format(card_play.play_type))
        for c in card_play.cards:
            print(c, end=" ")
        print()

    def amount(self):
        return self.n_cards

    def in_game(self):
        return self.amount() > 0