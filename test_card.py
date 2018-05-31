"""
Testing module for card.py

run with:
pytest test_card.py -vs

-v : verbose
-s : switch (allows printing)
"""

import card
import sys

class TestCard(object):
    """
    Test class for testing cards
    """

    def test_card_is_royal_simple(self):
        """Testing is royal"""
        assert card.Card('J', card.SUITS[2]).is_royal()

    def test_card_is_royal_simple2(self):
        """Testing is royal"""
        assert not card.Card('0', card.SUITS[2]).is_royal()

    def test_card_display_6(self):
        """Testing card displays"""
        assert str(card.Card(card.VALUES[3], card.SUITS[2])) == '♠6'

    def test_card_display_Q(self):
        """Testing card displays"""
        assert str(card.Card(card.VALUES[9], card.SUITS[1])) == '♦Q'

    def test_card_display_invalid_joker(self):
        """Testing if card recognizes invalid jokers"""
        assert str(card.Card("Z", card.SUITS[3])) == 'INVALID'

    def test_card_display_big_joker(self):
        """Testing if card recognizes big joker"""
        assert str(card.Card("Z", 1)) == 'JOKER'

    def test_card_display_small_joker(self):
        """Testing if card recognizes big joker"""
        assert str(card.Card("Z", 0)) == 'joker'
