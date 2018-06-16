"""
Probability test module
"""

import time
from itertools import combinations, groupby
import random
from pokai.src.ai_tools.probabilities import _prob_of_doubles, _prob_of_triples, _prob_of_quads, percent
from pokai.src.game.card import Card
from pokai.src.game.game_tools import get_new_shuffled_deck

# if you want to run more random tests, increase
TEST_MULTIPLIER = 1

class TestProbability(object):
    """
    Test class
    """

    @staticmethod
    def get_complement_hand(leftover_cards, hand):
        """Returns list of cards not in hand"""
        other_hand = list(leftover_cards)
        for c in hand:
            other_hand.remove(c)
        return other_hand

    @staticmethod
    def occurances_exist(card_list, occurance, base_val=-1):
        """Returns if there is a double in the list"""
        list_counts = {value : len(list(c)) for value, c in groupby(card_list, lambda c: c.value)}
        
        for value, counts in list_counts.items():
            if value > base_val and counts >= occurance:
                return True
        return False

    @staticmethod
    def prob_of_occurance_brute(leftover_cards, occurance, n_cards1, base_val=-1):
        """
        Returns the probability of an opponent having a hand with a double
        calculated via brute force
        """
        total_occurance = 0
        total = 0
        for possible in combinations(leftover_cards, n_cards1):
            total += 1
            other_hand = TestProbability.get_complement_hand(leftover_cards, possible)

            if TestProbability.occurances_exist(possible, occurance, base_val=base_val) or\
               TestProbability.occurances_exist(other_hand, occurance, base_val=base_val):
                total_occurance += 1

        return percent(total_occurance, total)

    def test_brute_is_slower(self):
        """tests that brute force is indeed slower"""
        card_strs = ['3s', '4d', '4h', '5s', '5d', '6h', '6d', '7c', '8s',
                     '9c', '0h', '0c', 'Jd', 'qs', 'Kd', 'kc', 'ah', '2c']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 8

        time1 = time.time()
        expected = TestProbability.prob_of_occurance_brute(cards, 2, n_cards1)
        time2 = time.time()
        actual = _prob_of_doubles(cards, n_cards1)
        time3 = time.time()
        assert expected == actual
        assert time3 - time2 < time2 - time1
        print("manual time: {}\tbrute force time: {}".format(time3 - time2, time2 - time1))

    @staticmethod
    def _run_test_prob_of_occurance(cards, occurance, n_cards1, base_val=-1):
        """
        tests the prob of doubles
        cards -- cards in leftover_card pile
        occurance -- the occurance of cards that we are looking for (1, 2, 3 or 4)
        n_cards1 -- cards in opponent 1's hand
                    cards in opponent 2's hand == n_total_cards - n_cards1
        base_val -- value each card must beat
        """
        expected = TestProbability.prob_of_occurance_brute(cards, occurance, n_cards1, base_val=base_val)
        if occurance == 2:
            actual = _prob_of_doubles(cards, n_cards1, base_val=base_val)
        elif occurance == 3:
            actual = _prob_of_triples(cards, n_cards1, base_val=base_val)
        elif occurance == 4:
            actual = _prob_of_quads(cards, n_cards1, base_val=base_val)
        print(expected, actual)
        assert actual == expected

    def test_prob_double_simple_three_exists(self):
        """
        100% chance of a person having a double since there is a triple
        """
        card_strs = ['3s', '4d', '4h', '4s', '5s', '5d', '6h', '6d', '7c']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 5
        TestProbability._run_test_prob_of_occurance(cards, 2, n_cards1)

    def test_prob_double_simple_hand_too_small(self):
        """
        100% chance of a person having a double since one hand is too small
        """
        card_strs = ['4d', '4h', '5h', '5c', '6h', '8d', '0c', '0h', '2c', '2h']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 8
        TestProbability._run_test_prob_of_occurance(cards, 2, n_cards1)

    def test_prob_double_simple(self):
        """tests prob of double with simple inputs"""
        card_strs = ['3h', '4d', '4h', '5s', '5d', '6h', '6d', '7c', '9d', '9s']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 6
        TestProbability._run_test_prob_of_occurance(cards, 2, n_cards1)

    def test_prob_double_with_base(self):
        """tests prob of double greater than some number"""
        card_strs = ['3c', '3s', '3h', '4d', '5c', '6h', '8c', '9s', 'Jc', 'Jh', 'Ks', 'Ah', '2h']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 6
        base_val = 5
        expected = TestProbability.prob_of_occurance_brute(cards, 2, n_cards1, base_val=base_val)
        actual = _prob_of_doubles(cards, n_cards1, base_val=base_val)
        assert actual == expected
        not_expected = TestProbability.prob_of_occurance_brute(cards, 2, n_cards1)
        assert actual != not_expected

    def test_prob_double_compare_two_bases(self):
        """tests prob of doubles multiple times"""
        card_strs = ['3c', '3s', '3h', '4d', '5c', '6h', '8c', '9s', 'Jc', 'Jh', 'Ks', 'Ah', '2h']
        cards = Card.strs_to_cards(card_strs)
        n_total_cards = 13
        n_cards1 = 6
        base_val_low = 5
        base_val_high = 10
        expected_low = TestProbability.prob_of_occurance_brute(cards, 2, n_cards1, base_val=base_val_low)
        actual_low = _prob_of_doubles(cards, n_cards1, base_val=base_val_low)
        assert actual_low == expected_low

        expected_high = TestProbability.prob_of_occurance_brute(cards, 2, n_cards1, base_val=base_val_high)
        actual_high = _prob_of_doubles(cards, n_cards1, base_val=base_val_high)
        assert actual_high == expected_high
        
        assert actual_low >= actual_high

    @staticmethod
    def _run_multiple_test_prob_of_occurance(loops, occurance, n_total_cards, n_cards1, base_val=-1):
        """
        tests the prob of doubles [loops] times
        n_total_cards -- total cards in leftover_card pile
        n_cards1 -- cards in opponent 1's hand
                    cards in opponent 2's hand == n_total_cards - n_cards1
        base_val -- value each card must beat
        """
        deck = get_new_shuffled_deck()

        for _ in range(loops):
            cards = random.sample(deck, n_total_cards)
            cards.sort(key=lambda c: c.value, reverse=False)
            print(cards)
            TestProbability._run_test_prob_of_occurance(cards, occurance, n_cards1, base_val=base_val)

    def test_prob_double_multiple(self):
        """tests prob of doubles multiple times"""
        loops = TEST_MULTIPLIER * 10
        n_total_cards = 13
        n_cards1 = 6
        TestProbability._run_multiple_test_prob_of_occurance(loops, 2, n_total_cards, n_cards1)

    def test_prob_double_multiple_with_base1(self):
        """tests prob of doubles multiple times"""
        loops = TEST_MULTIPLIER * 10
        n_total_cards = 13
        n_cards1 = 6
        base_val = 5
        TestProbability._run_multiple_test_prob_of_occurance(loops, 2, n_total_cards,
                                                           n_cards1, base_val=base_val)

    def test_prob_triple_simple(self):
        """tests probability of triples with simple inputs"""
        card_strs = ['3s', '3s', '3s', '4s', '4s','4s', '5s', '5s', '5s', '6s', '7s', '7s']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 6
        TestProbability._run_test_prob_of_occurance(cards, 3, n_cards1)

    def test_prob_triple_no_three_exists(self):
        """tests probability of triples with outcome of 0"""
        card_strs = ['3s', '3s', '4s', '4s', '5s', '5s', '6s', '7s', '7s']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 5
        TestProbability._run_test_prob_of_occurance(cards, 3, n_cards1)

    def test_prob_triple_hand_too_small(self):
        """tests probability of triples with outcome of 1"""
        card_strs = ['3s', '3s', '3s', '4s', '4s','4s', '5s', '5s', '5s', '6s', '7s', '7s']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 2
        TestProbability._run_test_prob_of_occurance(cards, 3, n_cards1)
    
    def test_prob_triple_multiple(self):
        """tests prob of triples multiple times"""
        loops = TEST_MULTIPLIER * 10
        n_total_cards = 15
        n_cards1 = 6
        base_val = 5
        TestProbability._run_multiple_test_prob_of_occurance(loops, 3, n_total_cards,
                                                           n_cards1, base_val=base_val)

    def test_prob_quad_simple(self):
        """tests the probability of quads with simple inputs"""
        card_strs = ['3s', '3h', '3d', '3c', '4s', '4h', '4d', '4c', '5c', '5s', '5d', '5h', '6s', '6h', '6c']
        cards = Card.strs_to_cards(card_strs)
        n_cards1 = 9
        TestProbability._run_test_prob_of_occurance(cards, 4, n_cards1)
