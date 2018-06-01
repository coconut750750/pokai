"""
Testing module for Monte Carlo simulations
"""

from monte_carlo import *
import card
import hand

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
        cls.card_strs_lv3 = ['3s', '4h', '5d', '6c', '7s', '8s', '8c', '8d', '8h',
                             '0d', 'Jh', 'Qh', 'Ks', 'Ac', '2h', 'Z1', 'Z0']

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

    def test_simulate_one(self):
        """tests the simulation of one game"""
        simulate_one_game(self.test_hand_lv1, 17, 20, True)

    def test_simulate_multiple_lv1(self):
        """tests simulation on level 1 hand"""
        plays = 100
        print(simulate(self.test_hand_lv1, plays, 17, 20) / plays)

    def test_simulate_multiple_lv2(self):
        """tests simulation on level 1 hand"""
        plays = 100
        print(simulate(self.test_hand_lv2, plays, 17, 20) / plays)

    def test_simulate_multiple_lv3(self):
        """tests simulation on level 1 hand"""
        plays = 100
        print(simulate(self.test_hand_lv3, plays, 17, 20) / plays)
