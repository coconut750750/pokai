"""
Hand object
"""

from itertools import groupby
from card import SMALL_JOKER_VALUE, BIG_JOKER_VALUE

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
        self.cards = cards
        self.sort_cards()
        self.organize()

    def get_next_play(self):
        play = []
        for play_type in ORDER:
            if not self.categories[play_type]:
                continue
            else:
                play += self.categories[play_type][0]
                if "triples" in play_type:
                    if len(self.categories[CATEGORIES[0]]) >= 1:
                        play += self.categories[CATEGORIES[0]][0]
                        if play_type == "adj_triples":
                            play += self.categories[CATEGORIES[0]][1]
                    elif len(self.categories[CATEGORIES[1]]) >= 1:
                        play += self.categories[CATEGORIES[1]][0]
                        if play_type == "adj_triples":
                            play += self.categories[CATEGORIES[1]][1]
                return play

    def sort_cards(self):
        self.cards.sort(key=lambda x: x.value, reverse=False)

    def organize(self):
        self.categories = {x:[] for x in CATEGORIES}
        counts = {value : list(g) for value, g in groupby(self.cards, lambda card: card.value)}
        for value, group in counts.items():
            amount = len(group)
            for i in range(4):
                if amount == i + 1:
                    self.categories[CATEGORIES[i]].append(group)
                    break
            self.organize_adj_triples(counts, value)
        self.organize_straights(counts)
        if SMALL_JOKER_VALUE in counts and BIG_JOKER_VALUE in counts:
            self.categories[CATEGORIES[-1]].append([self.cards[-1], self.cards[-2]])

    def organize_straights(self, counts):
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
                    self.categories[CATEGORIES[4 + i - 1]].append(straight_group)
                    visited[i - 1].append(straight_group[-1].value)

                    for j in range(0, len(straight_group), i):
                        sub_group = straight_group[j: j + i]
                        if sub_group in self.categories[CATEGORIES[i - 1]]:
                            self.categories[CATEGORIES[i - 1]].remove(sub_group)

    def organize_adj_triples(self, counts, value):
        if len(counts[value]) == 3 and len(counts[value + 1]) == 3:
            pair = counts[value] + counts[value + 1]
            self.categories[CATEGORIES[6]].append(pair)

    def get_low(self, other_card, num):
        if num <= 4:
            for card_group in self.categories[CATEGORIES[num-1]]:
                card = card_group[0]
                if card.value > other_card.value:
                    return card_group

    def get_low_straight(self, other_card, num, length):
        if length < SMALLEST_STRAIGHT[num - 1]:
            return
        for card_group in self.categories[CATEGORIES[4 + num - 1]]:
            if card_group[0].value <= other_card.value:
                for i, c in enumerate(card_group):
                    if c.value > other_card.value and len(card_group) - i >= length * num:
                        return card_group[i: i + length * num]
            else:
                if len(card_group) >= length * num:
                    return card_group[0: length * num]

    def add_cards(self, cards):
        for c in cards:
            self._add(c)
        self.sort_cards()
        self.organize()

    def _add(self, card):
        if card.value > -1:
            self.cards.append(card)

    def remove_cards(self, cards):
        for c in cards:
            self._remove(c)
        self.organize()

    def _remove(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def length(self):
        return len(self.cards)

    def print(self):
        sep = " | "
        s = sep
        for card in self.cards:
            s += card.display + sep
        print(s.strip())

    def print_categories(self):
        for i, j in self.categories.items():
            print("{}: {}".format(i, j))
