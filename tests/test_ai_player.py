"""
Testing Module for AI Player
"""

from pokai.src.game.hand import Hand
from pokai.src.game.aiplayer import AIPlayer

class TestAIPlayer:

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.card_strs = ['3s', '4h', '5d', '6c', '7s', '9s', '9c', '9d', '9h',
                             'AC', 'KH', 'KS', 'KD', 'KC', 'QH', 'QD', 'QS']

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        
        hand = Hand([])
        hand.add_cards(card_strs=TestMC.card_strs)
        self.test_player = Player(hand, 0, "")
        self.game_state = GameState(17, 17)