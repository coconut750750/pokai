"""
Testing module for game tools
"""

from pokai.src.game.game_tools import *

class TestTools(object):
    """
    Test class for game tools
    """

    def test_get_shuffled_deck(self):
        """tests getting a new deck"""
        deck = get_new_shuffled_deck()
        assert deck
        assert len(deck) == 54

    def test_get_untaken_deck_valid_list(self):
        """tests removing some cards"""
        deck = get_new_shuffled_deck()
        cards = [deck[27], deck[43]]
        cleaned = remove_from_deck(deck, cards)
        assert cleaned
        assert len(cleaned) == 54 - len(cards)
        for c in cards:
            assert c not in cleaned

    def test_get_untaken_deck_empty_list(self):
        """tests removing no cards"""
        deck = get_new_shuffled_deck()
        cards = []
        cleaned = remove_from_deck(deck, cards)
        assert cleaned
        assert cleaned == deck
