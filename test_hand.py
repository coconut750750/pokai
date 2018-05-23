"""
Testing module for hand.py

run with:
pytest test_card.py -vs

-v : verbose
-s : switch (allows printing)
"""

import card
import hand

class TestHand(object):
    """
    Test class for testing cards
    """

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.card_strs = ['7h', '6h', '8d', '7s', '6s', '5s', '7d', '4c', 'Ac',
                         'Kd', '5h', '2H', '5C', '0C', '0H', '4D', 'KH']

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.test_hand = hand.Hand([])
        self.test_hand.add_cards(card_strs=TestHand.card_strs)

    def test_hand_get_cards(self):
        """testing that cards are retrieved properly"""
        assert self.test_hand.contains(card.Card('7', 'h'))

    def test_hand_add_card_new(self):
        """testing add card works"""
        prev_len = self.test_hand.length()
        assert not self.test_hand.contains(card.Card('4', 'h'))
        self.test_hand.add_cards([card.Card('4', 'h')])
        assert self.test_hand.contains(card.Card('4', 'h'))
        assert self.test_hand.length() == prev_len + 1

    def test_hand_add_card_dup(self):
        """testing add duiplicate card doesnt work"""
        prev_len = self.test_hand.length()
        assert self.test_hand.contains(card.Card('7', 'h'))
        self.test_hand.add_cards([card.Card('7', 'h')])
        assert self.test_hand.length() == prev_len

    def test_hand_remove_card(self):
        """testing remove cards works"""
        cards = list(self.test_hand.cards)
        self.test_hand.remove_cards(cards)
        assert not self.test_hand.cards

    def test_hand_sort_cards_simple(self):
        """test lowest card has lowest val"""
        assert self.test_hand.get_card(0).value == 1

    def test_hand_sort_cards_order(self):
        """test other cards have values greater at equal to lowest card"""
        lowest_val = self.test_hand.get_card(0).value
        for c in self.test_hand.cards:
            assert c.value >= lowest_val
