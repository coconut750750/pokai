"""
The card module. hook testing
Contains the class for a single Poker Card Object.
"""

VALUES = '34567890JQKA2Z'
SUITS = 'hdsc'
VALUE_DISPLAY = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2', 'joker', 'JOKER']
SMALL_JOKER_VALUE = 13
BIG_JOKER_VALUE = 14
SUIT_DISPLAY = ['♥', '♦', '♠', '♣']

class Card(object):
    """
    The Card Object
    """
    def __init__(self, name, suit):
        super(Card, self).__init__()
        self.display = 'INVALID'
        if not name in list(VALUES):
            return

        self.name = name
        self.value = -1
        self.suit = ''

        if suit in list(SUITS) and name != 'Z':
            self.value = VALUES.index(name)
            self.suit = SUIT_DISPLAY[SUITS.index(suit)]
            self.display = "{}{}".format(self.suit, VALUE_DISPLAY[self.value])
        elif name == "Z" and not str(suit).isalpha():
            self.value = VALUES.index(name) + suit
            self.display = "{}".format(VALUE_DISPLAY[self.value])
        else:
            name = "INVALID"

    def is_royal(self):
        """Returns true if card is greater than 10"""
        return self.value > VALUES.index('0')

    def __repr__(self):
        """How the card is represented in terminal"""
        return 'Card: {}'.format(self.display) + ''

    def __str__(self):
        """How the card is turned into a string"""
        return self.display
