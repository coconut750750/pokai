"""
Testing module for Monte Carlo simulations
"""

import time
from pokai.src.monte_carlo import *
import pokai.src.card as card
import pokai.src.hand as hand

class TestMC(object):
    """
    Test class for monte carlo
    """

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.card_strs_lv1 = ['7h', '6h', '0d', '3s', '6s', 'Js', '7d', '9c', 'Ac',
                             'Kd', '5h', '2H', '5C', '0C', '0H', '4D', 'KH']
        cls.card_strs_lv2 = ['3h', '4s', '4h', '5d', '6s', '7c', '9h', '9d', 'jh',
                             'jc', 'ks', 'kd', 'ac', 'ah', '2c', '2d']
        cls.card_strs_lv3 = ['3s', '4h', '5d', '6c', '7s', '9s', '9c', '9d', '9h',
                             '0d', 'Jh', 'Qh', 'Ks', 'As', 'Ah', '2h', '2c']
        cls.card_strs_lv4 = ['Z1', 'Z0', '2H', '2S', '2D', '2C', 'AS', 'AD', 'AH',
                             'AC', 'KH', 'KS', 'KD', 'KC', 'QH', 'QD', 'QS']

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.test_hand_lv1 = hand.Hand([])
        self.test_hand_lv1.add_cards(card_strs=TestMC.card_strs_lv1)

        self.test_hand_lv2 = hand.Hand([])
        self.test_hand_lv2.add_cards(card_strs=TestMC.card_strs_lv2)

        self.test_hand_lv3 = hand.Hand([])
        self.test_hand_lv3.add_cards(card_strs=TestMC.card_strs_lv3)

        self.test_hand_lv4 = hand.Hand([])
        self.test_hand_lv4.add_cards(card_strs=TestMC.card_strs_lv4)

    def test_simulate_one(self):
        """tests one non random game"""
        test_hand2 = hand.Hand([])
        test_hand2.add_cards(card_strs=['3d', '3s', '5c', '6h', '7h', '8h', '8d', '8s', '9c', '0s', '0d', 'js', 'Qh', 'Qs', 'Kc', '2h', 'Z1'])
        test_hand3 = hand.Hand([])
        test_hand3.add_cards(card_strs=['3c', '4c', '5h', '6d', '6c', '7s', '8c', '9s', '0c', '0h', 'Jd', 'Qc', 'Qd', 'Kh', 'As', '2s', 'Z0'])
        simulate_one_game(self.test_hand_lv2, test_hand2, test_hand3, 0, [], False)

    def test_simulate_one_random(self):
        """tests the simulation of one game"""
        simulate_one_random_game(self.test_hand_lv1, 17, [], False)

    def test_simulate_multiple_lv1(self):
        """tests simulation on level 1 hand"""
        plays = 100
        print(simulate(self.test_hand_lv1, plays, 17, []) / plays)

    def test_simulate_multiple_lv2(self):
        """tests simulation on level 2 hand"""
        plays = 100
        print(simulate(self.test_hand_lv2, plays, 17, []) / plays)

    def test_simulate_multiple_lv3(self):
        """tests simulation on level 3 hand"""
        plays = 100
        print(simulate(self.test_hand_lv3, plays, 17, []) / plays)

    def test_simulate_multiple_lv4(self):
        """tests simulation on level 4 hand"""
        plays = 100
        print(simulate(self.test_hand_lv4, plays, 17, []) / plays)

    def test_simluate_multiple_correct_order(self):
        """tests that lv1, lv2, lv3, lv4 strength in correct way"""
        plays = 200
        sim1 = simulate(self.test_hand_lv1, plays, 17, []) / plays
        sim2 = simulate(self.test_hand_lv2, plays, 17, []) / plays
        sim3 = simulate(self.test_hand_lv3, plays, 17, []) / plays
        sim4 = simulate(self.test_hand_lv4, plays, 17, []) / plays
        assert sim1 < sim2 and sim2 < sim3 and sim3 < sim4

    def test_simulate_multiprocesses(self):
        """tests that multiprocesses makes it faster and is accurate"""
        plays = 1000
        processes = 2
        time1 = time.time()
        original = simulate(self.test_hand_lv3, plays, 17, []) / plays
        time2 = time.time()
        multiprocesses = simulate_multiprocesses(self.test_hand_lv3, plays,
                                                 17, [], processes) / plays
        time3 = time.time()

        print(original, multiprocesses)
        print(time2-time1, time3-time2)
        # check that it was faster
        assert time2 - time1 > time3 - time2
        # check that it was accurate enough
        assert original / multiprocesses > 0.9 and original / multiprocesses < 1.1

    def test_estimate_hand_strength(self):
        """tests estmiate hand strength"""
        strength = estimate_hand_strength(self.test_hand_lv2, 20, [])
        assert strength >= 0 and strength <= 1
