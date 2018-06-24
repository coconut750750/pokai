"""
Hand module
Contains the Hand class and other constants
"""

from itertools import groupby, combinations, chain

from pokai.game.card import Card, SMALL_JOKER_VALUE, BIG_JOKER_VALUE, MIN_VALUE, MAX_VALUE
from pokai.game.game_tools import SINGLES, DOUBLES, TRIPLES, QUADRUPLES, STRAIGHTS,\
                                      DOUBLE_STRAIGHTS, ADJ_TRIPLES, DOUBLE_JOKER
from pokai.game.card_play import Play

STRAIGHT_TERMINAL_VAL = 11
SMALLEST_STRAIGHT = [5, 3, 2]
CATEGORIES = [SINGLES, DOUBLES, TRIPLES, QUADRUPLES, STRAIGHTS, DOUBLE_STRAIGHTS,
              ADJ_TRIPLES, DOUBLE_JOKER]
WILDS = [DOUBLE_JOKER, QUADRUPLES]

class Hand(object):
    """
    Hand object
    Contains a list of cards, _cards.
    Contains a dictionary of categories that a hand can play
    """
    def __init__(self, cards):
        super(Hand, self).__init__()
        self._cards = []
        for c in cards:
            self._cards.append(c)
        self._categories = {}
        self._organize()

    def _organize(self):
        """
        Sorts the cards based on value and organizes the cards in categories
        """
        self._cards.sort(key=lambda x: x.value, reverse=False)
        self._categories = {x:[] for x in CATEGORIES}
        counts = {value : list(c) for value, c in groupby(self._cards, lambda card: card.value)}
        self._organize_basics(counts)
        self._organize_straights(counts)
        self._organize_jokers(counts)

    def _organize_basics(self, counts):
        """helper function that organizes singles, doubles, triples, and quadruples"""
        for value, card_group in counts.items():
            length = len(card_group)
            for i in range(length):
                self._categories[CATEGORIES[i]].append(card_group[: i + 1])
            self._organize_adj_triples(counts, value)

    def _organize_adj_triples(self, counts, value):
        """helper function that organizes adj triples that start
        at value"""
        if (value + 1) not in counts:
            return
        if len(counts[value]) == 3 and len(counts[value + 1]) == 3:
            pair = counts[value] + counts[value + 1]
            self._categories[ADJ_TRIPLES].append(pair)

    def _organize_straights(self, counts):
        """helper function that organizes straights"""
        for i in range(2):
            last_visited = -1
            for value in counts:
                if value <= last_visited:
                    continue
                
                straight_group = []
                # make sure value is Ace or less
                while value in counts and value <= STRAIGHT_TERMINAL_VAL and len(counts[value]) > i:
                    straight_group += counts[value][0: i + 1]
                    value += 1
                if len(straight_group) // (i + 1) >= SMALLEST_STRAIGHT[i]:
                    self._categories[CATEGORIES[4 + i]].append(straight_group)
                    last_visited = value - 1

    def _organize_jokers(self, counts):
        """helper function that organizes jokers"""
        if SMALL_JOKER_VALUE in counts and BIG_JOKER_VALUE in counts:
            self._categories[DOUBLE_JOKER].append([self._cards[-1], self._cards[-2]])

    def generate_possible_extra_cards(self, exclude_cards, each_count, extra_type):
        """
        Returns an iterator of all possible extra card combinations
        exclude_cards -- cards to exclude from the list
        each_count -- whether the extra cards should be singles are doubles
        extra_type -- (1 or 2) the groupings of the extra cards (1 or 2 singles or doubles)
        """
        if extra_type != 1 and extra_type != 2:
            return []
        extra_cards = []
        exclude_values = set([c.value for c in exclude_cards])
        possible_cards = []
        for card_group in self._categories[CATEGORIES[each_count - 1]]:
            if card_group[0].value not in exclude_values:
                possible_cards.append(card_group)
        extra_card_combos = combinations(possible_cards, extra_type)
        for combo in extra_card_combos:
            yield list(chain.from_iterable(combo))

    def _get_extra_cards(self, exclude_cards, each_count, extra_type):
        """        
        exclude_cards -- cards to exclude from the list
        each_count -- whether the extra cards should be singles are doubles
        extra_type -- (1 or 2) the groupings of the extra cards (1 or 2 singles or doubles)
        """
        iterator = self.generate_possible_extra_cards(exclude_cards, each_count, extra_type)
        return next(iterator, [])

    def generate_possible_low_foundations(self, other_card, play_type):
        """
        Returns an iterator of all basic foundations
        (individual singles, doubles, triples, or quadruples)
        """
        possibles = []
        for card_group in self._categories[play_type]:
            card = card_group[0]
            if not other_card or card.value > other_card.value:
                yield Play(-1, card_group, 0, play_type=play_type)

    def generate_possible_basics(self, other_card, each_count, extra=0):
        """
        Returns an iterator of all the possible basic plays
        """
        if each_count > 4:
            return None
        if each_count < 3:
            extra = 0

        plays = self.generate_possible_low_foundations(other_card, CATEGORIES[each_count - 1])
        for play in plays:
            extra_cards = []
            if each_count == 3 and extra:
                extra_cards = self._get_extra_cards(play.cards, extra, 1)
            elif each_count == 4 and extra:
                extra_cards = self._get_extra_cards(play.cards, extra // 2, 2)
            if extra_cards or not extra:
                play.cards += extra_cards
                play.num_extra = len(extra_cards)
                yield play

    def get_low(self, other_card, each_count, extra=0):
        """
        Gets the lowest basic that meets the properties
        Arguments:
        other_card -- lowest card in the basic
        each_count -- if its a single, double, triple, or quad (wild)
        extra -- the number of extra cards (1 or 2 for triple)
                                           (2 or 4 for quad)
        Returns the lowest play with pos -1 or None
        """
        iterator = self.generate_possible_basics(other_card, each_count, extra=extra)
        return next(iterator, Play.get_pass_play())

    def generate_possible_straights(self, other_card, each_count, length):
        """
        Returns an iterator of all the possible straights
        length = each_count * distinct number of cards
        """
        play_type = CATEGORIES[4 + each_count - 1]
        for card_group in self._categories[play_type]:
            if not other_card:
                yield Play(-1, card_group, 0, play_type=play_type)
                continue
            for i, c in enumerate(card_group):
                if c.value > other_card.value and len(card_group) - i >= length * each_count:
                    yield Play(-1, card_group[i: i + length * each_count], 0, play_type=play_type)

    def get_low_straight(self, other_card, each_count, length):
        """
        Gets the lowest straight that meets the properties
        Arguments:
        other_card -- lowest card in the opposing straight
        each_count -- if its a single, double, or triple straight
        length -- length of the opposing straight
                  each_count * distinct number of cards
                  length is ignored when other_card is None

        Returns play with pos of -1 or None
        """
        iterator = self.generate_possible_straights(other_card, each_count, length)
        return next(iterator, Play.get_pass_play())

    def generate_possible_adj_triples(self, other_card, num_extra):
        """
        Returns an iterator of all the possible adj triples
        """
        plays = self.generate_possible_straights(other_card, 3, 2)
        for play in plays:
            extra_cards = []
            extra_cards = self._get_extra_cards(play.cards, num_extra // 2, 2)
            if not num_extra or extra_cards:
                play.cards += extra_cards
                play.num_extra = len(extra_cards)
                yield play

    def get_low_adj_triple(self, other_card, num_extra):
        """
        Gets the lowest adj triple that meets the properties
        Arguments:
        other_card -- the lowest card value of the triples
        num_extra -- 2 if it carries 2 singles
                       4 if it carries 2 doubles
        Returns play with pos of -1 or None
        """
        iterator = self.generate_possible_adj_triples(other_card, num_extra)
        return next(iterator, Play.get_pass_play())

    def generate_possible_wilds(self, other_card):
        """
        Returns an iterator of all the possible wilds
        """
        yield from self.generate_possible_basics(other_card, 4)
        if self._categories[DOUBLE_JOKER]:
            yield Play(-1, self._categories[DOUBLE_JOKER][0], 0, play_type=DOUBLE_JOKER)

    def get_low_wild(self, other_card):
        """
        Returns the lowest wild play that is above given card
        Pos of the play is -1
        """
        iterator = self.generate_possible_wilds(other_card)
        return next(iterator, Play.get_pass_play())

    def get_num_wild(self):
        """
        Returns the number of wild cards in hand
        """
        return len(self._categories[DOUBLE_JOKER]) + len(self._categories[QUADRUPLES])

    def add_cards(self, cards=None, card_strs=None):
        """adds a list of cards or list of string of cards to hand"""
        did_add = cards or card_strs
        if cards:
            for c in cards:
                self._add(c)
        if card_strs:
            for card_str in card_strs:
                self._add(Card.str_to_card(card_str))
        if did_add:
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
        return card in self._cards

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

    def __eq__(self, other):
        """equality function"""
        for c in self._cards:
            if not other.contains(c):
                return False
        return True

    def __str__(self):
        """How the card is turned into a string"""
        sep = " | "
        s = sep
        for card in self._cards:
            s += card.display + sep
        return s.strip()
