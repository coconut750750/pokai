"""
Testing module for Monte Carlo simulations
"""

import time
from pokai.src.ai_tools.monte_carlo import *
from pokai.src.game.card import Card
import pokai.src.game.hand as hand
from pokai.src.game.player import Player
from pokai.src.game.game_state import GameState
import pokai.src.game.game_tools as game_tools
from pokai.src.game.card_play import Play

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
        hand_lv1 = hand.Hand([])
        hand_lv1.add_cards(card_strs=TestMC.card_strs_lv1)
        self.test_player_lv1 = Player(hand_lv1, 0, "")

        hand_lv2 = hand.Hand([])
        hand_lv2.add_cards(card_strs=TestMC.card_strs_lv2)
        self.test_player_lv2 = Player(hand_lv2, 0, "")

        hand_lv3 = hand.Hand([])
        hand_lv3.add_cards(card_strs=TestMC.card_strs_lv3)
        self.test_player_lv3 = Player(hand_lv3, 0, "")

        hand_lv4 = hand.Hand([])
        hand_lv4.add_cards(card_strs=TestMC.card_strs_lv4)
        self.test_player_lv4 = Player(hand_lv4, 0, "")

        self.game_state = GameState(17, 17)

    def test_simulate_one(self):
        """tests one non random game"""
        test_hand2 = hand.Hand([])
        test_hand2.add_cards(card_strs=['3d', '3s', '5c', '6h', '7h', '8h', '8d', '8s',
                                        '9c', '0s', '0d', 'js', 'Qh', 'Qs', 'Kc', '2h', 'Z1'])
        test_hand3 = hand.Hand([])
        test_hand3.add_cards(card_strs=['3c', '4c', '5h', '6d', '6c', '7s', '8c', '9s',
                                        '0c', '0h', 'Jd', 'Qc', 'Qd', 'Kh', 'As', '2s', 'Z0'])
        simulate_one_game([self.test_player_lv2,
                           Player(test_hand2, 0, ""),
                           Player(test_hand3, 0, "")], 0, [], False)

    def test_simulate_one_random(self):
        """tests the simulation of one game"""
        simulate_one_random_game(self.test_player_lv1, self.game_state, False)

    def test_simulate_multiple_lv1(self):
        """tests simulation on level 1 hand"""
        plays = 100
        print(simulate(self.test_player_lv1, plays, self.game_state) / plays)

    def test_simulate_multiple_lv2(self):
        """tests simulation on level 2 hand"""
        plays = 100
        print(simulate(self.test_player_lv2, plays, self.game_state) / plays)

    def test_simulate_multiple_lv3(self):
        """tests simulation on level 3 hand"""
        plays = 100
        print(simulate(self.test_player_lv3, plays, self.game_state) / plays)

    def test_simulate_multiple_lv4(self):
        """tests simulation on level 4 hand"""
        plays = 100
        print(simulate(self.test_player_lv4, plays, self.game_state) / plays)

    def test_simluate_multiple_correct_order(self):
        """tests that lv1, lv2, lv3, lv4 strength in correct way"""
        plays = 200
        sim1 = simulate(self.test_player_lv1, plays, self.game_state) / plays
        sim2 = simulate(self.test_player_lv2, plays, self.game_state) / plays
        sim3 = simulate(self.test_player_lv3, plays, self.game_state) / plays
        sim4 = simulate(self.test_player_lv4, plays, self.game_state) / plays
        assert sim1 < sim2 and sim2 < sim3 and sim3 < sim4

    def test_simulate_multiprocesses(self):
        """tests that multiprocesses makes it faster and is accurate"""
        plays = 1000
        processes = 2
        time1 = time.time()
        original = simulate(self.test_player_lv3, plays, self.game_state) / plays
        time2 = time.time()
        multiprocesses = simulate_multiprocesses(self.test_player_lv3, plays,
                                                 self.game_state, processes) / plays
        time3 = time.time()

        print(original, multiprocesses)
        print(time2-time1, time3-time2)
        # check that it was faster
        assert time2 - time1 > time3 - time2
        # check that it was accurate enough
        assert original / multiprocesses > 0.9 and original / multiprocesses < 1.1

    def test_estimate_hand_strength(self):
        """tests estmiate hand strength"""
        strength = estimate_hand_strength(self.test_player_lv2, self.game_state)
        assert strength >= 0 and strength <= 1

    @staticmethod
    def generate_game_state(computer_card_strs, unrevealed_card_strs, n_cards1):
        game_state = GameState(20, 17)
        game_state.unused_cards = Card.strs_to_cards(computer_card_strs + unrevealed_card_strs)
        game_state.used_cards = game_tools.remove_from_deck(get_new_ordered_deck(), game_state.unused_cards)
        game_state.player_cards = [len(computer_card_strs), n_cards1, len(unrevealed_card_strs) - n_cards1]
        computer_hand = hand.Hand([])
        computer_hand.add_cards(card_strs=computer_card_strs)
        computer = Player(computer_hand, 0, "")

        return game_state, computer

    def test_best_play_simple1(self):
        """tests best play function"""
        computer_card_strs = ['0d', '2s']
        unrevealed_card_strs = ['Qd', 'kd']
        game_state, computer = TestMC.generate_game_state(computer_card_strs, unrevealed_card_strs, 1)
        play1 = computer.get_play(None,
                                  game_state.player_cards,
                                  game_state.get_unrevealed_cards(computer.get_cards()))
        play2 = computer.get_play(Play(2, [Card('K', 'h')], 0),
                                  game_state.player_cards,
                                  game_state.get_unrevealed_cards(computer.get_cards()))
        assert get_best_play([play1, play2], computer, game_state) == play2

    def test_best_play_simple2(self):
        """tests best play function"""
        computer_card_strs = ['3d', '3s', '3c', '4c', 'Ah']
        unrevealed_card_strs = ['Qd', 'Qs', 'Qc', '7c', 'Kd', 'Ks', 'Kc', '8d']
        game_state, computer = TestMC.generate_game_state(computer_card_strs, unrevealed_card_strs, 1)
        play1 = computer.get_play(None,
                                  game_state.player_cards,
                                  game_state.get_unrevealed_cards(computer.get_cards()))
        play2 = computer.get_play(Play(2, [Card('K', 'h')], 0),
                                  game_state.player_cards,
                                  game_state.get_unrevealed_cards(computer.get_cards()))
        assert get_best_play([play1, play2], computer, game_state) == play2

