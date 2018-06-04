"""
Probability test module
"""

import sys
sys.path.append('../')
import time
from itertools import combinations
from pokai.src.probabilities import prob_of_doubles, percent, get_num_more_than_occurances
from pokai.src.card import Card

class TestProbability(object):
    """
    Test class
    """

    def strs_to_cards(self, card_strs):
        """
        returns a list of cards with values of card_strs
        """
        card_list = []
        for card_str in card_strs:
            name = card_str[0].upper()
            if name == 'Z':
                suit = int(card_str[1])
            else:
                suit = card_str[1].lower()
            card_list.append(Card(str(name), suit))
        return card_list

    def prob_of_doubles_brute_manual(self, leftover_cards, n_cards1):
        """
        Returns the probability of an opponent having a hand with a double
        calculated via brute force
        """
        total_doubles = 0
        total = 0
        combos = combinations(leftover_cards, n_cards1)
        for possible in combos:
            total += 1
            num_doubles = 0
            other_hand = list(leftover_cards)

            for c in possible:
                other_hand.remove(c)

            for i, c in enumerate(possible):
                for j in range(i + 1, n_cards1):
                    if c.value == possible[j].value:
                        num_doubles += 1

            for i, c in enumerate(other_hand):
                for j in range(i + 1, len(other_hand)):
                    if c.value == other_hand[j].value:
                        num_doubles += 1

            if num_doubles > 0:
                total_doubles += 1

        return percent(total_doubles, total)

    def test_brute_is_slower(self):
        """tests that brute force is indeed slower"""
        card_strs = ['3s', '4d', '4h', '5s', '5d', '6h', '6d', '7c', '8s',
                     '9c', '0h', '0c', 'Jd', 'qs', 'Kd', 'kc', 'ah', '2c']
        cards = self.strs_to_cards(card_strs)
        n_cards1 = 8

        time1 = time.time()
        expected = self.prob_of_doubles_brute_manual(cards, n_cards1)
        time2 = time.time()
        calculated = prob_of_doubles(cards, n_cards1)
        time3 = time.time()
        assert expected == calculated
        assert time3 - time2 < time2 - time1
        print(time3 - time2, time2 - time1)

    def test_prob_double_simple1(self):
        """tests with simple inputs"""
        card_strs = ['3s', '4d', '4h', '5s', '5d', '6h', '6d', '7c']
        cards = self.strs_to_cards(card_strs)
        n_cards1 = 5

        assert self.prob_of_doubles_brute_manual(cards, n_cards1) == prob_of_doubles(cards, n_cards1)

    def test_prob_double_simple2(self):
        """tests with simple inputs"""
        card_strs = ['3d', '4d', '4h', '5s', '5h', '6s', '6d', '7c', '8d',
                     '9h', '0h', '0s', 'Js', 'qc', 'Kc', 'ad' 'ac', '2s']
        cards = self.strs_to_cards(card_strs)
        n_cards1 = 8

        assert self.prob_of_doubles_brute_manual(cards, n_cards1) == prob_of_doubles(cards, n_cards1)

    def test_prob_double_simple3(self):
        """tests with simple inputs"""
        card_strs = ['3h', '4d', '4h', '5s', '5d', '6h', '6d', '7c', '9d', '9s', '9c']
        cards = self.strs_to_cards(card_strs)
        n_cards1 = 6

        assert self.prob_of_doubles_brute_manual(cards, n_cards1) == prob_of_doubles(cards, n_cards1)
