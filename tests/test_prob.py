"""
Probability test module
"""

import time
from itertools import combinations
from pokai.src.probabilities import prob_of_doubles, percent
from pokai.src.card import Card

class TestProbability(object):
    """
    Test class
    """

    def get_complement_hand(self, leftover_cards, hand):
        """Returns list of cards not in hand"""
        other_hand = list(leftover_cards)
        for c in hand:
            other_hand.remove(c)
        return other_hand

    def double_exists(self, card_list):
        """Returns if there is a double in the list"""
        for i, c in enumerate(card_list):
            for j in range(i + 1, len(card_list)):
                if c.value == card_list[j].value:
                    return True
        return False

    def prob_of_doubles_brute_manual(self, leftover_cards, n_cards1):
        """
        Returns the probability of an opponent having a hand with a double
        calculated via brute force
        """
        total_doubles = 0
        total = 0
        for possible in combinations(leftover_cards, n_cards1):
            total += 1
            other_hand = self.get_complement_hand(leftover_cards, possible)

            if self.double_exists(possible) or self.double_exists(other_hand):
                total_doubles += 1

        return percent(total_doubles, total)

    def test_brute_is_slower(self):
        """tests that brute force is indeed slower"""
        card_strs = ['3s', '4d', '4h', '5s', '5d', '6h', '6d', '7c', '8s',
                     '9c', '0h', '0c', 'Jd', 'qs', 'Kd', 'kc', 'ah', '2c']
        cards = Card.strs_to_cards(card_strs)
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
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 5

        assert self.prob_of_doubles_brute_manual(cards, n_cards1) == prob_of_doubles(cards, n_cards1)

    def test_prob_double_simple2(self):
        """tests with simple inputs"""
        card_strs = ['3d', '4d', '4h', '5s', '5h', '6s', '6d', '7c', '8d',
                     '9h', '0h', '0s', 'Js', 'qc', 'Kc', 'ad' 'ac', '2s']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 8

        assert self.prob_of_doubles_brute_manual(cards, n_cards1) == prob_of_doubles(cards, n_cards1)

    def test_prob_double_simple3(self):
        """tests with simple inputs"""
        card_strs = ['3h', '4d', '4h', '5s', '5d', '6h', '6d', '7c', '9d', '9s', '9c']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 6

        assert self.prob_of_doubles_brute_manual(cards, n_cards1) == prob_of_doubles(cards, n_cards1)
