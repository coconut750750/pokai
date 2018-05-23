"""
Hand object
Contains a list of cards, _cards.
Contains a dictionary of categories that a hand can play
"""

from itertools import groupby
from card import Card, SMALL_JOKER_VALUE, BIG_JOKER_VALUE

SMALLEST_STRAIGHT = [5, 3]
SMALLEST_TRIPLE_STRAIGHT = 2
CATEGORIES = ["singles", "doubles", "triples", "fours", "straights", "double_straights",
              "adj_triples", "double_joker"]
ORDER = ["singles", "doubles", "triples", "straights", "double_straights", "adj_triples"]
WILDS = ["fours", "double_joker"]
ORDER.reverse()
WILDS.reverse()

class Hand(object):
    """docstring for Hand"""
    def __init__(self, cards):
        super(Hand, self).__init__()
        self._cards = cards
        self._categories = {}
        self.sort_cards()
        self._organize()

    def get_next_play(self):
        play = []
        for play_type in ORDER:
            if not self._categories[play_type]:
                continue
            else:
                play += self._categories[play_type][0]
                if "triples" in play_type:
                    if len(self._categories[CATEGORIES[0]]) >= 1:
                        play += self._categories[CATEGORIES[0]][0]
                        if play_type == "adj_triples":
                            play += self._categories[CATEGORIES[0]][1]
                    elif len(self._categories[CATEGORIES[1]]) >= 1:
                        play += self._categories[CATEGORIES[1]][0]
                        if play_type == "adj_triples":
                            play += self._categories[CATEGORIES[1]][1]
                return play

    def sort_cards(self):
        """Sorts the cards in order by value"""
        self._cards.sort(key=lambda x: x.value, reverse=False)

    def _organize(self):
        """Organizes the cards in categories"""
        self._categories = {x:[] for x in CATEGORIES}
        counts = {value : list(g) for value, g in groupby(self._cards, lambda card: card.value)}
        for value, group in counts.items():
            amount = len(group)
            for i in range(4):
                if amount == i + 1:
                    self._categories[CATEGORIES[i]].append(group)
                    break
            self._organize_adj_triples(counts, value)
        self._organize_straights(counts)
        if SMALL_JOKER_VALUE in counts and BIG_JOKER_VALUE in counts:
            self._categories[CATEGORIES[-1]].append([self._cards[-1], self._cards[-2]])

    def _organize_straights(self, counts):
        """Organize straights"""
        visited = [[-1], [-1]]
        for value, _ in counts.items():
            for i in range(1, 3):
                if value <= visited[i - 1][-1]:
                    continue
                straight_group = []
                val = value
                while val in counts and len(counts[val]) >= i:
                    for j in range(i):
                        straight_group.append(counts[val][j])
                    val += 1
                if len(straight_group) // i >= SMALLEST_STRAIGHT[i - 1]:
                    self._categories[CATEGORIES[4 + i - 1]].append(straight_group)
                    visited[i - 1].append(straight_group[-1].value)

                    for j in range(0, len(straight_group), i):
                        sub_group = straight_group[j: j + i]
                        if sub_group in self._categories[CATEGORIES[i - 1]]:
                            self._categories[CATEGORIES[i - 1]].remove(sub_group)

    def _organize_adj_triples(self, counts, value):
        if len(counts[value]) == 3 and len(counts[value + 1]) == 3:
            pair = counts[value] + counts[value + 1]
            self._categories[CATEGORIES[6]].append(pair)

    def get_low(self, other_card, num):
        if num <= 4:
            for card_group in self._categories[CATEGORIES[num-1]]:
                card = card_group[0]
                if card.value > other_card.value:
                    return card_group

    def get_low_straight(self, other_card, num, length):
        if length < SMALLEST_STRAIGHT[num - 1]:
            return
        for card_group in self._categories[CATEGORIES[4 + num - 1]]:
            if card_group[0].value <= other_card.value:
                for i, c in enumerate(card_group):
                    if c.value > other_card.value and len(card_group) - i >= length * num:
                        return card_group[i: i + length * num]
            else:
                if len(card_group) >= length * num:
                    return card_group[0: length * num]

    def add_cards(self, cards=[], card_strs=[]):
        """adds a list of cards or list of string of cards to hand"""
        for c in cards:
            self._add(c)
        for card_str in card_strs:
            name = card_str[0].upper()
            if name == 'Z':
                suit = int(card_str[1])
            else:
                suit = card_str[1].lower()
            self._add(Card(str(name), suit))
        self.sort_cards()
        self._organize()

    def _add(self, card):
        if card.value > -1 and not self.contains(card):
            self._cards.append(card)

    def remove_cards(self, cards):
        """removes a list of cards from hand"""
        for c in cards:
            self._remove(c)
        self._organize()

    def _remove(self, card):
        if self.contains(card):
            self._cards.remove(card)

    def contains(self, card):
        """returns true if the same card exists in hand"""
        for c in self._cards:
            if card.display == c.display:
                return True
        return False

    def get_card(self, index):
        """gets a single card at index"""
        return self._cards[index]

    def get_cards(self):
        """gets all cards in hand"""
        return self._cards

    def num_cards(self):
        """number of cards"""
        return len(self._cards)

    def print_categories(self):
        """prints out the categories of the hand"""
        for i, j in self._categories.items():
            print("{}: {}".format(i, j))

    def __str__(self):
        """How the card is turned into a string"""
        sep = " | "
        s = sep
        for card in self._cards:
            s += card.display + sep
        return s.strip()
