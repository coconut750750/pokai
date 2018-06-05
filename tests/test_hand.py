"""
Testing module for hand.py

run with:
pytest test_card.py -vs

-v : verbose
-s : switch (allows printing)
"""

import sys
sys.path.append('../')
import copy
import pokai.src.card as card
import pokai.src.hand as hand
from pokai.src.game_tools import DOUBLE_JOKER

class TestHand(object):
    """
    Test class for testing cards
    """

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        card_strs = ['7h', '6h', '8d', '7s', '6s', '5s', '7d', '4c', 'Ac',
                     'Kd', '5h', '2H', '5C', '0C', '0H', '4D', 'KH', '6d',
                     '7c']
        cls.cards = card.Card.strs_to_cards(card_strs)
        card_strs_adj_trip = ['3s', '3d', '3h', '4s', '5h', '5s', '6s', '6h', '6d',
                              '7s', '7h', '7d', '8h', '9h', '9c']
        cls.adj_trip = card.Card.strs_to_cards(card_strs_adj_trip)
        card_strs_quadplex = ['3s', '4s', '5h', '5s', '6s', '6h', '7s',
                              '7h', '7d', '7c']
        cls.quadplex = card.Card.strs_to_cards(card_strs_quadplex)

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.hand = hand.Hand([])
        self.hand.add_cards(cards=TestHand.cards)

        self.hand_adj_trip = hand.Hand([])
        self.hand_adj_trip.add_cards(cards=TestHand.adj_trip)

        self.hand_quadplex = hand.Hand([])
        self.hand_quadplex.add_cards(cards=TestHand.quadplex)

    @staticmethod
    def _print_card_list(card_play, extra_msg=""):
        """prints out a list of cards with a message"""
        if extra_msg:
            extra_msg = "({})".format(extra_msg)
        print("\nValid {} {}: {}".format(card_play.play_type, 
                                         extra_msg, 
                                         " ".join(str(c) for c in card_play.cards)))

    @staticmethod
    def _check_single(single):
        """checks if valid single"""
        assert single
        assert len(single) == 1

    @staticmethod
    def _check_double(double):
        """checks if valid double"""
        assert double
        assert len(double) == 2
        assert double[0].value == double[1].value

    @staticmethod
    def _check_triple(triple):
        """checks if triple is valid"""
        l = len(triple)
        assert triple
        assert triple[0].value == triple[1].value and triple[0].value == triple[2].value
        if l >= 4:
            assert triple[0].value != triple[3].value
        if l == 5:
            assert triple[3].value == triple[4].value

    @staticmethod
    def _check_adj_triple(adj_trip):
        """checks if adj_trip is valid"""
        l = len(adj_trip)
        assert adj_trip
        assert l >= 6 and l <= 10
        TestHand._check_triple(adj_trip[0: 3])
        TestHand._check_triple(adj_trip[3: 6])
        assert adj_trip[0].value == adj_trip[3].value - 1
        first = 6
        second = 7 if l == 8 else 8
        if l == 10:
            TestHand._check_double(adj_trip[first: second])
            TestHand._check_double(adj_trip[second:])
        assert adj_trip[first].value != adj_trip[second].value

        assert adj_trip[0].value != adj_trip[first].value\
               and adj_trip[0].value != adj_trip[second].value
        assert adj_trip[3].value != adj_trip[first].value\
               and adj_trip[3].value != adj_trip[second].value

    @staticmethod
    def _check_quadruples(quad):
        """check if valid quadruple"""
        l = len(quad)
        assert quad
        assert l == 4 or l == 6 or l == 8
        assert quad[0].value == quad[1].value and\
               quad[0].value == quad[2].value and\
               quad[0].value == quad[3].value
        if l >= 6:
            TestHand._check_double(quad[4: 5])
            assert quad[0].value != quad[4].value
            if l == 8:
                TestHand._check_double(quad[6: 7])
                assert quad[4].value != quad[6].value
                assert quad[0].value != quad[6].value

    @staticmethod
    def _check_straight(straight, each_count):
        """checks if straight is valid"""
        l = len(straight)
        assert straight
        if each_count == 1:
            assert l >= 5
        elif each_count == 2:
            assert l >= 6
            assert l % 2 == 0
        elif each_count == 3:
            assert l >= 6
            assert l % 3 == 0
        for i in range(0, l - each_count, each_count):
            assert straight[i].value == straight[i + each_count].value - 1
            assert straight[i].value == straight[i + each_count - 1].value
            assert straight[i].value == straight[i + each_count // 3].value

    def test_hand_get_cards(self):
        """testing that cards are retrieved properly"""
        assert self.hand.contains(card.Card('7', 'h'))

    """
    ADD CARDS
    """

    def test_hand_add_card_new(self):
        """testing add card works"""
        prev_len = self.hand.num_cards()
        assert not self.hand.contains(card.Card('4', 'h'))
        self.hand.add_cards([card.Card('4', 'h')])
        assert self.hand.contains(card.Card('4', 'h'))
        assert self.hand.num_cards() == prev_len + 1

    def test_hand_add_card_dup(self):
        """testing add duiplicate card doesnt work"""
        prev_len = self.hand.num_cards()
        c = card.Card('7', 'h')
        assert self.hand.contains(c)
        self.hand.add_cards([c])
        assert self.hand.num_cards() == prev_len

    """
    REMOVE CARDS
    """

    def test_hand_remove_card_valid(self):
        """testing remove cards works"""
        prev_len = self.hand.num_cards()
        c = self.hand.get_card(0)
        assert self.hand.contains(c)
        self.hand.remove_cards([c])
        assert self.hand.num_cards() == prev_len - 1

    def test_hand_remove_card_invalid(self):
        """testing remove cards works"""
        prev_len = self.hand.num_cards()
        c = card.Card('3', 'h')
        assert not self.hand.contains(c)
        self.hand.remove_cards([c])
        assert self.hand.num_cards() == prev_len

    def test_hand_remove_all_cards(self):
        """testing remove cards works"""
        cards = list(self.hand.get_cards())
        self.hand.remove_cards(cards)
        assert not self.hand.num_cards()

    """
    SORT CARDS
    """

    def test_hand_sort_cards_simple(self):
        """test lowest card has lowest val"""
        assert self.hand.get_card(0).value == 1

    def test_hand_sort_cards_order(self):
        """test other cards have values greater at equal to lowest card"""
        low = self.hand.get_card(0)
        for i in range(self.hand.num_cards()):
            assert self.hand.get_card(i) >= low

    def test_hand_organize_jokers(self):
        """tests jokers are organized"""
        self.hand.add_cards(card_strs=['Z0', 'Z1'])
        assert len(self.hand._categories[DOUBLE_JOKER]) == 1

    """
    GET LOW
    """

    def test_hand_get_low_single_valid(self):
        """tests get low on a valid single"""
        c = card.Card('3', 'h')
        each_count = 1
        play = self.hand.get_low(c, each_count)
        assert play.get_base_card() > c
        TestHand._check_single(play.cards)
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_single_invalid(self):
        """tests get low on invalid single"""
        c = card.Card('2', 'h')
        each_count = 1
        low_card_play = self.hand.get_low(c, each_count)
        assert not low_card_play

    def test_hand_get_low_double_valid(self):
        """tests get low on a valid double"""
        c = card.Card('3', 'h')
        each_count = 2
        play = self.hand.get_low(c, each_count)
        assert play.get_base_card() > c
        TestHand._check_double(play.cards)
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_double_invalid(self):
        """tests get low on invalid double"""
        c = card.Card('2', 'h')
        each_count = 2
        low_card_play = self.hand.get_low(c, each_count)
        assert not low_card_play

    def test_hand_get_low_triple_alone_valid(self):
        """tests get low on a valid triple alone"""
        c = card.Card('3', 'h')
        each_count = 3
        extra = 0
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        assert play.get_base_card() > c
        assert play.num_cards() == 3
        TestHand._check_triple(play.cards)
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_triple_alone_invalid(self):
        """tests get low on invalid triple alone"""
        c = card.Card('2', 'h')
        each_count = 3
        extra = 0
        low_card_play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        assert not low_card_play

    def test_hand_get_low_triple_single_valid(self):
        """tests get low on a valid triple single"""
        c = card.Card('3', 'h')
        each_count = 3
        extra = 1
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        assert play.get_base_card() > c
        assert play.num_cards() == 4
        TestHand._check_triple(play.cards)
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_triple_single_invalid(self):
        """tests get low on invalid triple single"""
        c = card.Card('2', 'h')
        each_count = 3
        extra = 1
        low_card_play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        assert not low_card_play

    def test_hand_get_low_triple_double_valid(self):
        """tests get low on a valid triple double"""
        c = card.Card('3', 'h')
        each_count = 3
        extra = 2
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        assert play.get_base_card() > c
        assert play.num_cards() == 5
        TestHand._check_triple(play.cards)
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_triple_double_invalid(self):
        """tests get low on invalid triple double"""
        c = card.Card('2', 'h')
        each_count = 3
        extra = 2
        low_card_play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        assert not low_card_play

    """
    GET SECOND LOW
    """

    def test_hand_get_second_low_single_valid(self):
        """tests get second low on a valid single"""
        c = card.Card('3', 'h')
        each_count = 1

        initial = copy.deepcopy(self.hand)
        first_low_cards = self.hand.get_low(c, each_count)
        first_low = first_low_cards.get_base_card()
        play = self.hand.get_second_low(c, each_count)
        TestHand._check_single(play.cards)
        assert initial == self.hand # hand shouldn't change
        assert play.get_base_card() > c
        assert play.get_base_card() >= first_low

        TestHand._print_card_list(play, extra_msg="greater than {}\
                                                    and second to {}".format(str(c), str(first_low)))

    def test_hand_get_second_low_single_invalid(self):
        """tests get low on invalid single"""
        c = card.Card('2', 'h')
        each_count = 1
        low_card_play = self.hand.get_second_low(c, each_count)
        assert not low_card_play

    def test_hand_get_second_low_double_valid(self):
        """tests get second low on a valid double"""
        c = card.Card('3', 'h')
        each_count = 2

        initial = str(self.hand)
        first_low_cards = self.hand.get_low(c, each_count)
        first_low = first_low_cards.get_base_card()
        play = self.hand.get_second_low(c, each_count)
        assert initial == str(self.hand) # hand shouldn't change
        assert play.get_base_card() > c
        assert play.get_base_card() >= first_low
        TestHand._check_double(play.cards)
        TestHand._print_card_list(play, extra_msg="greater than {}\
                                                    and second to {}".format(str(c), str(first_low)))

    """
    GET LOW STRAIGHTS
    """

    def test_hand_categories_single_straights_valid(self):
        """tests get valid low single straight"""
        c = card.Card('3', 'h')
        each_count = 1
        length = 5
        play = self.hand.get_low_straight(c, each_count, length)
        TestHand._check_straight(play.cards, 1)
        assert play.num_cards() == length * each_count
        assert play.get_base_card() > c
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_single_straights_invalid(self):
        """tests get invalid low single straight"""
        c = card.Card('5', 'h')
        each_count = 1
        length = 5
        assert not self.hand.get_low_straight(c, each_count, length)

    def test_hand_double_straights_valid(self):
        """tests get valid low double straight"""
        c = card.Card('3', 'h')
        each_count = 2
        length = 3
        play = self.hand.get_low_straight(c, each_count, length)
        TestHand._check_straight(play.cards, 2)
        assert play.num_cards() == length * each_count
        assert play.get_base_card() > c
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_double_straights_invalid(self):
        """tests get invalid low double straight"""
        c = card.Card('0', 'h')
        each_count = 2
        length = 3
        assert not self.hand.get_low_straight(c, each_count, length)

    def test_hand_triple_straights_valid(self):
        """tests get valid low triple straight"""
        c = card.Card('4', 'h')
        each_count = 3
        length = 2
        play = self.hand_adj_trip.get_low_straight(c, each_count, length)
        TestHand._check_straight(play.cards, 3)
        assert play.num_cards() == length * each_count
        assert play.get_base_card() > c
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    """
    GET LOW ADJ TRIPLES
    """

    def test_hand_get_low_adj_trip_single_valid(self):
        """tests get valid adj trip with 2 extras"""
        c = card.Card('4', 'h')
        play = self.hand_adj_trip.get_low_adj_triple(c, 2)
        assert play.num_cards() == 8
        assert play.get_base_card() > c
        TestHand._check_adj_triple(play.cards)
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_adj_trip_double_valid(self):
        """tests get valid adj trip with 4 extras"""
        c = card.Card('4', 'h')
        play = self.hand_adj_trip.get_low_adj_triple(c, 4)
        assert play.num_cards() == 10
        assert play.get_base_card() > c
        TestHand._check_adj_triple(play.cards)
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    """
    GET LOW WILDS
    """

    def test_hand_get_low_wild_simple_valid(self):
        """tests get valid low wild"""
        c = card.Card('5', 'h')
        play = self.hand.get_low_wild(c)
        TestHand._check_quadruples(play.cards)
        assert play.get_base_card() > c
        TestHand._print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_wild_simple_invalid(self):
        """tests get invalid low wild"""
        c = card.Card('7', 'h')
        assert not self.hand.get_low_wild(c)


    """
    GET NONE LOWS
    """

    def test_hand_get_none_low_single(self):
        """tests get low single where other card is None"""
        c = None
        each_count = 1
        play = self.hand.get_low(c, each_count)
        TestHand._check_single(play.cards)
        TestHand._print_card_list(play)

    def test_hand_get_none_low_double(self):
        """tests get low double where other card is None"""
        c = None
        each_count = 2
        play = self.hand.get_low(c, each_count)
        TestHand._check_double(play.cards)
        TestHand._print_card_list(play)

    def test_hand_get_none_low_triple_alone(self):
        """tests get low triple alone where other card is None"""
        c = None
        each_count = 3
        extra = 0
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        TestHand._check_triple(play.cards)
        assert play.num_cards() == 3
        TestHand._print_card_list(play)

    def test_hand_get_none_low_triple_single(self):
        """tests get low triple single where other card is None"""
        c = None
        each_count = 3
        extra = 1
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        TestHand._check_triple(play.cards)
        assert play.num_cards() == 4
        TestHand._print_card_list(play)

    def test_hand_get_low_triple_double_none(self):
        """tests get low triple double where other card is None"""
        c = None
        each_count = 3
        extra = 2
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        TestHand._check_triple(play.cards)
        assert play.num_cards() == 5
        TestHand._print_card_list(play)

    def test_hand_get_second_low_single_none(self):
        """tests get second low where other card is None"""
        c = None
        each_count = 1

        initial = copy.deepcopy(self.hand)
        first_low_cards = self.hand.get_low(c, each_count).cards
        play = self.hand.get_second_low(c, each_count)
        assert play
        second_low_cards = play.cards
        assert first_low_cards and second_low_cards
        assert initial == self.hand # hand shouldn't change
        assert len(second_low_cards) == 1
        assert second_low_cards[0] >= first_low_cards[0]
        TestHand._print_card_list(play, extra_msg="second low")

    """
    GET NONE STRAIGHTS
    """

    def test_hand_single_straights_none(self):
        """tests get valid low single straight"""
        c = None
        each_count = 1
        length = 5
        play = self.hand.get_low_straight(c, each_count, length)
        TestHand._check_straight(play.cards, 1)
        TestHand._print_card_list(play)

    def test_hand_double_straights_none(self):
        """tests get valid low double straight"""
        c = None
        each_count = 2
        length = 3
        play = self.hand.get_low_straight(c, each_count, length)
        TestHand._check_straight(play.cards, 2)
        TestHand._print_card_list(play)

    def test_hand_triple_straights_none(self):
        """tests get valid low triple straight"""
        c = None
        each_count = 3
        length = 2
        play = self.hand_adj_trip.get_low_straight(c, each_count, length)
        TestHand._check_straight(play.cards, 3)
        TestHand._print_card_list(play)

    """
    GET NONE ADJ TRIPLES
    """

    def test_hand_get_low_adj_trip_single_none(self):
        """tests get valid adj trip with 2 extras"""
        c = None
        play = self.hand_adj_trip.get_low_adj_triple(c, 2)
        assert play.num_cards() == 8
        TestHand._check_adj_triple(play.cards)
        TestHand._print_card_list(play)

    def test_hand_get_low_adj_trip_double_none(self):
        """tests get valid adj trip with 4 extras"""
        c = None
        play = self.hand_adj_trip.get_low_adj_triple(c, 4)
        assert play.num_cards() == 10
        TestHand._check_adj_triple(play.cards)
        TestHand._print_card_list(play)

    """
    GET NONE WILDS
    """

    def test_hand_get_low_wild_simple_none(self):
        """tests get valid low wild"""
        c = None
        play = self.hand.get_low_wild(c)
        TestHand._check_quadruples(play.cards)
        TestHand._print_card_list(play)
