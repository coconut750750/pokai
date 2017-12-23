from hand import Hand, CATEGORIES
from card import Card

class Player(object):
	"""docstring for Player"""
	def __init__(self, hand, position, t):
		super(Player, self).__init__()
		self.hand = hand
		self.position = position
		self.type = t
		self.amount = hand.length()
		self.ingame = self.amount > 0

	def reveal(self):
		return self.hand.print()

	def info(self):
		self.hand.print_categories()

	def play(self, cards):
		self.hand.remove_cards(cards)
		for c in cards:
			print(c, end=" ")
		print()

	def get_low(self, other_card, num):
		return self.hand.get_low(other_card, num)

	def get_low_straight(self, other_card, num, length):
		return self.hand.get_low_straight(other_card, num, length)

	def refresh(self):
		self.amount = self.hand.length()
		self.ingame = self.amount > 0


