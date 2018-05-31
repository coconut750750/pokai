"""
Hand module
Contains the Hand class and other constants
"""

from itertools import groupby
from card import Card, SMALL_JOKER_VALUE, BIG_JOKER_VALUE

SMALLEST_STRAIGHT = [5, 3, 2]
SINGLES = 'singles'
DOUBLES = 'doubles'
TRIPLES = 'triples'
QUADRUPLES = 'fours'
STRAIGHTS = 'straights'
DOUBLE_STRAIGHTS = 'double_straights'
ADJ_TRIPLES = 'adj_triples'
DOUBLE_JOKER = 'double_joker'
CATEGORIES = [SINGLES, DOUBLES, TRIPLES, QUADRUPLES, STRAIGHTS, DOUBLE_STRAIGHTS,
              ADJ_TRIPLES, DOUBLE_JOKER]
ORDER = [ADJ_TRIPLES, DOUBLE_STRAIGHTS, STRAIGHTS, TRIPLES, DOUBLES, SINGLES]
WILDS = [DOUBLE_JOKER, QUADRUPLES]

class Hand(object):
    """
    Hand object
    Contains a list of cards, _cards.
    Contains a dictionary of categories that a hand can play
    """
    def __init__(self, cards):
        super(Hand, self).__init__()
        self._cards = cards
        self._categories = {}
        self._sort_cards()
        self._organize()

    def _sort_cards(self):
        """Sorts the cards in order by value"""
        self._cards.sort(key=lambda x: x.value, reverse=False)

    def _organize(self):
        """Organizes the cards in categories"""
        self._categories = {x:[] for x in CATEGORIES}
        counts = {value : list(c) for value, c in groupby(self._cards, lambda card: card.value)}
        for value, card_group in counts.items():
            amount = len(card_group) - 1
            for i in range(4):
                if amount == i:
                    self._categories[CATEGORIES[i]].append(card_group)
                    break
            self._organize_adj_triples(counts, value)
        self._organize_straights(counts)
        if SMALL_JOKER_VALUE in counts and BIG_JOKER_VALUE in counts:
            self._categories[DOUBLE_JOKER].append([self._cards[-1], self._cards[-2]])

    def _organize_straights(self, counts):
        """helper function that organizes straights"""
        for i in range(2):
            last_visited = -1
            for value, _ in counts.items():
                if value <= last_visited:
                    continue
                straight_group = []
                while value in counts and len(counts[value]) > i:
                    straight_group += counts[value][0: i + 1]
                    value += 1
                if len(straight_group) // (i + 1) >= SMALLEST_STRAIGHT[i]:
                    self._categories[CATEGORIES[4 + i]].append(straight_group)
                    last_visited = value - 1

    def _organize_adj_triples(self, counts, value):
        """helper function that organizes adj triples that start
        at value"""
        if len(counts[value]) == 3 and len(counts[value + 1]) == 3:
            pair = counts[value] + counts[value + 1]
            self._categories[ADJ_TRIPLES].append(pair)

    def get_lead_play(self):
        """
        Gets the best play if this player is starting.
        """
        play = []
        for play_type in ORDER:
            if not self._categories[play_type]:
                continue
            else:
                play += self._categories[play_type][0]
                # need to check triples because there is possibility of adding
                # on extra cards
                if TRIPLES in play_type:
                    if len(self._categories[SINGLES]) >= 1:
                        play += self._categories[SINGLES][0]
                        if play_type == ADJ_TRIPLES:
                            play += self._categories[SINGLES][1]
                    elif len(self._categories[DOUBLES]) >= 1:
                        play += self._categories[DOUBLES][0]
                        if play_type == ADJ_TRIPLES:
                            play += self._categories[DOUBLES][1]
                return play
        return None

    def get_low(self, other_card, each_count, extra=0):
        """
        Gets the lowest single that meets the properties
        Arguments:
        other_card -- lowest card in the single
        each_count -- if its a single, double, triple, or quad (wild)
        extra -- the number of extra cards (1 or 2 for triple)
                                           (2 or 4 for quad)
        """
        if each_count < 3:
            extra = 0

        extra_cards = []
        if extra == 1 and not self._categories[SINGLES]:
            return None
        elif extra == 1:
            extra_cards += self._categories[SINGLES][0]
        if extra == 2:
            if each_count == 3 and not self._categories[DOUBLES]:
                return None
            elif each_count == 3:
                extra_cards += self._categories[DOUBLES][0]
            if each_count == 4 and len(self._categories[SINGLES]) < 2:
                return None
            elif each_count == 4:
                extra_cards += self._categories[SINGLES][0:2]
        if extra == 4 and len(self._categories[DOUBLES]) < 2:
            return None
        elif extra == 4:
            extra_cards += self._categories[DOUBLES][0:2]

        if each_count <= 4:
            for card_group in self._categories[CATEGORIES[each_count - 1]]:
                card = card_group[0]
                if other_card == None:
                    return card_group + extra_cards
                if card.value > other_card.value:
                    return card_group + extra_cards

        return None

    def get_low_straight(self, other_card, each_count, length):
        """
        Gets the lowest straight that meets the properties
        Arguments:
        other_card -- lowest card in the opposing straight
        each_count -- if its a single, double, or triple straight
        length -- length of the opposing straight
        """
        if length < SMALLEST_STRAIGHT[each_count - 1]:
            return None
        for card_group in self._categories[CATEGORIES[4 + each_count - 1]]:
            if card_group[0].value <= other_card.value:
                for i, c in enumerate(card_group):
                    if c.value > other_card.value and len(card_group) - i >= length * each_count:
                        return card_group[i: i + length * each_count]
            else:
                if len(card_group) >= length * each_count:
                    return card_group[0: length * each_count]
        return None

    def get_low_adj_triple(self, other_card, extra_card_count):
        """
        Gets the lowest adj triple that meets the properties
        Arguments:
        other_card -- the lowest card value of the triples
        extra_card_count -- 1 if it carries 2 singles
                            2 if it carries 2 doubles
        """
        foundation = self.get_low_straight(other_card, 3, 2)
        extra = self.get_low(None, extra_card_count)
        return foundation + extra

    def get_low_wild(self, other_card):
        """Returns the lowest wild that is above given card"""
        lowest_four = self.get_low(other_card, 4)
        if lowest_four:
            return lowest_four
        if self._categories[DOUBLE_JOKER]:
            return self._categories[DOUBLE_JOKER]
        return None

    def add_cards(self, cards=None, card_strs=None):
        """adds a list of cards or list of string of cards to hand"""
        if not cards:
            cards = []
        if not card_strs:
            card_strs = []
        for c in cards:
            self._add(c)
        for card_str in card_strs:
            name = card_str[0].upper()
            if name == 'Z':
                suit = int(card_str[1])
            else:
                suit = card_str[1].lower()
            self._add(Card(str(name), suit))
        self._sort_cards()
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
        """prints out the sorted categories of the hand"""
        for i, j in self._categories.items():
            if not j:
                continue
            print("\n{}:".format(i))
            for k in j:
                print('|' + ' '.join('{}'.format(str(l)) for l in k) + '|')

    def __str__(self):
        """How the card is turned into a string"""
        sep = " | "
        s = sep
        for card in self._cards:
            s += card.display + sep
        return s.strip()
