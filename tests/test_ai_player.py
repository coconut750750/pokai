"""
Testing Module for AI Player
"""

from pokai.src.game.card import Card
from pokai.src.game.game_state import GameState
from pokai.src.game.card_play import Play
from pokai.src.game.hand import Hand
from pokai.src.game.player import Player
from pokai.src.game.aiplayer import AIPlayer

class TestAIPlayer:

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.card_strs_lv2 = ['3h', '4s', '4h', '5d', '6s', '7c', '9h', '9d', '0c',
                             'Jh', 'Jc', 'Ks', 'Kd', 'Ac', 'Ah', '2c', '2d']
        cls.card_strs_lv3 = ['3s', '4h', '5d', '6c', '7s', '9s', '9c', '9d', '9h',
                             'QH', 'QD', 'QS', 'KH', 'KS', 'KD', 'KC', 'AC']
        

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        
        hand = Hand([])
        hand.add_cards(card_strs=TestAIPlayer.card_strs_lv2)
        self.test_player_lv2 = Player(hand, 0, "")
        self.test_ai_player_lv2 = AIPlayer(hand, 0, "")

        hand = Hand([])
        hand.add_cards(card_strs=TestAIPlayer.card_strs_lv3)
        self.test_player_lv3 = Player(hand, 0, "")
        self.test_ai_player_lv3 = AIPlayer(hand, 0, "")

        self.game_state = GameState(17, 17)

    def setup_game_state(self, plays):
        for play in plays:
            if play:
                play.position = 2
            self.game_state.cards_played(play)
        self.game_state.increment_turn()

    def test_ai_get_best_singles(self):
        prev_play = Play.get_play_from_cards([Card('3', 'h')])
        self.setup_game_state([prev_play])
        assert self.test_ai_player_lv3.get_best_singles(self.game_state).cards[0] == Card('A', 'c')

    def test_ai_get_best_singles_none(self):
        self.setup_game_state([None])
        assert self.test_ai_player_lv2.get_best_singles(self.game_state).cards[0] == Card('0', 'c')

    def test_ai_get_best_doubles(self):
        prev_play = Play.get_play_from_cards([Card('0', 's'), Card('0', 'd')])
        self.setup_game_state([prev_play])
        assert self.test_ai_player_lv2.get_best_doubles(self.game_state).cards[0] == Card('J', 'h')

    def test_ai_get_best_doubles_none(self):
        self.setup_game_state([None])
        assert self.test_ai_player_lv2.get_best_doubles(self.game_state).cards[0] == Card('9', 'h')

    def test_ai_get_best_triples_alone(self):
        prev_play = Play.get_play_from_cards([Card('3', 'h'), Card('3', 'd'), Card('3', 'c')])
        self.setup_game_state([prev_play])
        print(self.test_ai_player_lv3.get_best_triples(self.game_state))

    def test_ai_get_best_triples_single(self):
        prev_play = Play.get_play_from_cards([Card('3', 'h'), Card('3', 'd'), Card('3', 'c'),
                                              Card('4', 'c')])
        self.setup_game_state([prev_play])
        print(self.test_ai_player_lv3.get_best_triples(self.game_state))

    def test_ai_get_best_triples_double(self):
        prev_play = Play.get_play_from_cards([Card('3', 'h'), Card('3', 'd'), Card('3', 'c'),
                                              Card('4', 'c'), Card('4', 'd')])
        self.setup_game_state([prev_play])
        print(self.test_ai_player_lv3.get_best_triples(self.game_state))

