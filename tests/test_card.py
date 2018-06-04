"""
Testing module for card.py

run with:
pytest test_card.py -vs

-v : verbose
-s : switch (allows printing)
"""

import pokai.src.card as card

class TestCard(object):
    """
    Test class for testing cards
    """

    """
    IS ROYAL
    """

    def test_card_is_royal_simple(self):
        """Testing is royal"""
        assert card.Card('J', card.SUITS[2]).is_royal()

    def test_card_is_royal_simple2(self):
        """Testing is royal"""
        assert not card.Card('0', card.SUITS[2]).is_royal()

    """
    COMPARISONS
    """

    def test_card_is_lt(self):
        """Testing less than"""
        assert card.Card('8', 'c') < card.Card('9', 'h')

    def test_card_is_le(self):
        """Testing less than or equal"""
        assert card.Card('9', 'c') <= card.Card('9', 'h')

    def test_card_is_eq(self):
        """Testing equals"""
        assert card.Card('6', 'c') == card.Card('6', 'c')

    def test_card_is_ge(self):
        """Testing greater than or equal"""
        assert card.Card('0', 'c') >= card.Card('9', 'h')

    def test_card_is_gt(self):
        """Testing greater than"""
        assert card.Card('Z', 1) > card.Card('9', 'h')

    """
    __STR__
    """

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
