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
		print(self.hand.print())

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

		
c1 = Card("4","s")
c2 = Card("4","h")
c3 = Card("4","d")
c0 = Card("4","c")
c4 = Card("3","c")
c5 = Card("7","d")
c6 = Card("6","s")
c7 = Card("5","s")
c8 = Card("Z",1)
c9 = Card("Z",0)
c11 = Card("8", "s")
c12 = Card("9", "s")

c_list = [c1, c2, c3, c5, c6, c6, c7, c5, c6, c7, c7, c8, c9, c0, c11, c12]
h = Hand(c_list)
p = Player(h, 1, 1)
