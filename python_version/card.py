VALUES = "34567890JQKA2Z"
SUITS = "hdsc"
VALUE_DISPLAY = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2", "joker", "JOKER"]
SMALL_JOKER_VALUE = 13
BIG_JOKER_VALUE = 14
SUIT_DISPLAY = ["♥", "♦", "♠", "♣"]

class Card(object):
	"""docstring for Card"""
	def __init__(self, name, suit):
		super(Card, self).__init__()

		self.name = name
		self.value = -1
		self.suit = ""
		self.display = "INVALID"

		if suit in list(SUITS):
			self.value = VALUES.index(name)
			self.suit = SUIT_DISPLAY[SUITS.index(suit)]
			self.display = "{}{}".format(self.suit, VALUE_DISPLAY[self.value])
		elif name == "Z":
			self.name = name
			self.value = VALUES.index(name) + suit
			self.display = "{}".format(VALUE_DISPLAY[self.value])

	def __repr__(self):
		return "Card: {}".format(self.display)
		
	def __str__(self):
		return self.display
			
		