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
                         'Kd', '5h', '2H', '5C', '0C', '0H', '4D', 'KH', '6d',
                         '7c']

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.test_hand = hand.Hand([])
        self.test_hand.add_cards(card_strs=TestHand.card_strs)

    def test_hand_get_cards(self):
        """testing that cards are retrieved properly"""
        assert self.test_hand.contains(card.Card('7', 'h'))

    """
    ADD CARDS
    """

    def test_hand_add_card_new(self):
        """testing add card works"""
        prev_len = self.test_hand.num_cards()
        assert not self.test_hand.contains(card.Card('4', 'h'))
        self.test_hand.add_cards([card.Card('4', 'h')])
        assert self.test_hand.contains(card.Card('4', 'h'))
        assert self.test_hand.num_cards() == prev_len + 1

    def test_hand_add_card_dup(self):
        """testing add duiplicate card doesnt work"""
        prev_len = self.test_hand.num_cards()
        c = card.Card('7', 'h')
        assert self.test_hand.contains(c)
        self.test_hand.add_cards([c])
        assert self.test_hand.num_cards() == prev_len

    """
    REMOVE CARDS
    """

    def test_hand_remove_card_valid(self):
        """testing remove cards works"""
        prev_len = self.test_hand.num_cards()
        c = self.test_hand.get_card(0)
        assert self.test_hand.contains(c)
        self.test_hand.remove_cards([c])
        assert self.test_hand.num_cards() == prev_len - 1

    def test_hand_remove_card_invalid(self):
        """testing remove cards works"""
        prev_len = self.test_hand.num_cards()
        c = card.Card('3', 'h')
        assert not self.test_hand.contains(c)
        self.test_hand.remove_cards([c])
        assert self.test_hand.num_cards() == prev_len

    def test_hand_remove_all_cards(self):
        """testing remove cards works"""
        cards = list(self.test_hand.get_cards())
        self.test_hand.remove_cards(cards)
        assert not self.test_hand.num_cards()

    """
    ORGANIZE CARDS
    """

    def test_hand_organize_cards_print(self):
        """prints out hand categories"""
        print(self.test_hand.print_categories())

    """
    SORT CARDS
    """

    def test_hand_sort_cards_simple(self):
        """test lowest card has lowest val"""
        assert self.test_hand.get_card(0).value == 1

    def test_hand_sort_cards_order(self):
        """test other cards have values greater at equal to lowest card"""
        lowest_val = self.test_hand.get_card(0).value
        for i in range(self.test_hand.num_cards()):
            assert self.test_hand.get_card(i).value >= lowest_val

    """
    GET LEAD PLAY
    """

    def test_hand_get_lead_play(self):
        """tests getn ext play simple"""
        print(self.test_hand.get_lead_play())

    """
    GET LOW
    """

    def test_hand_get_low_single_nonnull(self):
        """tests get low on a valid single"""
        c = card.Card('3', 'h')
        each_count = 1
        low_cards = self.test_hand.get_low(c, each_count)
        assert low_cards[0].value > c.value
        assert len(low_cards) == 1

    def test_hand_get_low_single_null(self):
        """tests get low on invalid single"""
        c = card.Card('2', 'h')
        each_count = 1
        low_cards = self.test_hand.get_low(c, each_count)
        assert not low_cards

    def test_hand_get_low_double_nonnull(self):
        """tests get low on a valid double"""
        c = card.Card('3', 'h')
        each_count = 2
        low_cards = self.test_hand.get_low(c, each_count)
        assert low_cards[0].value > c.value
        assert len(low_cards) == 2
        assert low_cards[0].value == low_cards[1].value

    def test_hand_get_low_double_null(self):
        """tests get low on invalid double"""
        c = card.Card('2', 'h')
        each_count = 2
        low_cards = self.test_hand.get_low(c, each_count)
        assert not low_cards

    def test_hand_get_low_triple_alone_nonnull(self):
        """tests get low on a valid triple alone"""
        c = card.Card('3', 'h')
        each_count = 3
        extra = 0
        low_cards = self.test_hand.get_low(c, each_count, extra=extra)
        low = low_cards[0]
        assert low.value > c.value
        assert len(low_cards) == 3
        assert low.value == low_cards[1].value
        assert low.value == low_cards[2].value

    def test_hand_get_low_triple_alone_null(self):
        """tests get low on invalid triple alone"""
        c = card.Card('2', 'h')
        each_count = 3
        extra = 0
        low_cards = self.test_hand.get_low(c, each_count, extra=extra)
        assert not low_cards

    def test_hand_get_low_triple_single_nonnull(self):
        """tests get low on a valid triple single"""
        c = card.Card('3', 'h')
        each_count = 3
        extra = 1
        low_cards = self.test_hand.get_low(c, each_count, extra=extra)
        assert low_cards[0].value > c.value
        assert len(low_cards) == 4

    def test_hand_get_low_triple_single_null(self):
        """tests get low on invalid triple single"""
        c = card.Card('2', 'h')
        each_count = 3
        extra = 1
        low_cards = self.test_hand.get_low(c, each_count, extra=extra)
        assert not low_cards

    def test_hand_get_low_triple_double_nonnull(self):
        """tests get low on a valid triple double"""
        c = card.Card('3', 'h')
        each_count = 3
        extra = 2
        low_cards = self.test_hand.get_low(c, each_count, extra=extra)
        assert low_cards[0].value > c.value
        assert len(low_cards) == 5
        assert low_cards[3].value == low_cards[4].value

    def test_hand_get_low_triple_double_null(self):
        """tests get low on invalid triple double"""
        c = card.Card('2', 'h')
        each_count = 3
        extra = 2
        low_cards = self.test_hand.get_low(c, each_count, extra=extra)
        assert not low_cards

    """
    GET LOW STRAIGHTS
    """

    def test_hand_categories_single_straights_nonnull(self):
        """tests get valid low single straight"""
        c = card.Card('3', 'h')
        each_count = 1
        length = 5
        assert self.test_hand.get_low_straight(c, each_count, length)

    def test_hand_categories_single_straights_null(self):
        """tests get invalid low single straight"""
        c = card.Card('5', 'h')
        each_count = 1
        length = 5
        assert not self.test_hand.get_low_straight(c, each_count, length)

    def test_hand_categories_double_straights_nonnull(self):
        """tests get valid low double straight"""
        c = card.Card('3', 'h')
        each_count = 2
        length = 3
        assert self.test_hand.get_low_straight(c, each_count, length)

    def test_hand_categories_double_straights_null(self):
        """tests get invalid low double straight"""
        c = card.Card('0', 'h')
        each_count = 2
        length = 3
        assert not self.test_hand.get_low_straight(c, each_count, length)

    def test_hand_categories_triple_straights_nonnull(self):
        """tests get valid low triple straight"""
        c = card.Card('4', 'h')
        each_count = 3
        length = 2
        assert self.test_hand.get_low_straight(c, each_count, length)

    """
    GET LOW WILDS
    """

    def test_hand_get_low_wild_simple_nonnull(self):
        """tests get valid low wild"""
        c = card.Card('5', 'h')
        low_wild = self.test_hand.get_low_wild(c)
        low = low_wild[0]
        assert low_wild
        assert len(low_wild) == 4
        assert low.value > c.value
        assert low.value == low_wild[1].value
        assert low.value == low_wild[2].value
        assert low.value == low_wild[3].value

    def test_hand_get_low_wild_simple_null(self):
        """tests get invalid low wild"""
        c = card.Card('7', 'h')
        assert not self.test_hand.get_low_wild(c)
