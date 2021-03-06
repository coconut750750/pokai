"""
Testing module for hand.py

run with:
pytest test_card.py -vs

-v : verbose
-s : switch (allows printing)
"""

import copy
import random

import pokai.game.card as card
from pokai.game.card import SMALL_JOKER_VALUE, BIG_JOKER_VALUE
import pokai.game.hand as hand
from pokai.game.game_tools import get_new_shuffled_deck, DOUBLE_JOKER

from tests.play_checker import _check_single, _check_double, _check_triple, _check_adj_triple,\
                                     _check_quadruples, _check_straight, _check_wild

# if you want to run more random tests, increase
TEST_MULTIPLIER = 1

def setup_module(module):
    global cards, adj_trip, quadplex
    cards = card.Card.strs_to_cards(['7h', '6h', '8d', '7s', '6s', '5s',
                                     '7d', '4c', 'Ac', 'Kd', '5h', '2H',
                                     '5C', '0C', '0H', '4D', 'KH', '6d', '7c'])
    adj_trip = card.Card.strs_to_cards(['3s', '3d', '3h', '4s', '5h', '5s',
                                        '6s', '6h', '6d', '7s', '7h', '7d',
                                        '8h', '9h', '9c'])
    quadplex = card.Card.strs_to_cards(['3s', '4s', '5h', '5s', '6s', '6h',
                                        '7s', '7h', '7d', '7c'])

class TestHand(object):
    """
    Test class for testing cards
    """

    def setup_method(self):
        self.hand = hand.Hand(cards)
        self.hand_adj_trip = hand.Hand(adj_trip)
        self.hand_quadplex = hand.Hand(quadplex)

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

    def test_hand_organize_cards(self):
        """tests organize function"""
        print(self.hand._categories)

    def test_hand_sort_cards_order(self):
        """test other cards have values greater at equal to lowest card"""
        low = self.hand.get_card(0)
        for i in range(self.hand.num_cards()):
            assert self.hand.get_card(i) >= low

    def test_hand_organize_jokers(self):
        """tests jokers are organized"""
        self.hand.add_cards(card_strs=['Z0', 'Z1'])
        assert len(self.hand._categories[DOUBLE_JOKER]) == 1

class TestGetLow(object):
    def setup_method(self):
        self.hand = hand.Hand(cards)
        self.hand_adj_trip = hand.Hand(adj_trip)
        self.hand_quadplex = hand.Hand(quadplex)

    def test_hand_get_low_single_valid(self):
        """tests get low on a valid single"""
        c = card.Card('3', 'h')
        each_count = 1
        play = self.hand.get_low(c, each_count)
        assert play.get_base_card() > c
        _check_single(play.cards)
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

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
        _check_double(play.cards)
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

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
        _check_triple(play.cards)
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

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
        _check_triple(play.cards)
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

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
        _check_triple(play.cards)
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_triple_double_invalid(self):
        """tests get low on invalid triple double"""
        c = card.Card('2', 'h')
        each_count = 3
        extra = 2
        low_card_play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        assert not low_card_play

    def test_hand_get_none_low_single(self):
        """tests get low single where other card is None"""
        c = None
        each_count = 1
        play = self.hand.get_low(c, each_count)
        _check_single(play.cards)
        _print_card_list(play)

    def test_hand_get_none_low_double(self):
        """tests get low double where other card is None"""
        c = None
        each_count = 2
        play = self.hand.get_low(c, each_count)
        _check_double(play.cards)
        _print_card_list(play)

    def test_hand_get_none_low_triple_alone(self):
        """tests get low triple alone where other card is None"""
        c = None
        each_count = 3
        extra = 0
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        _check_triple(play.cards)
        assert play.num_cards() == 3
        _print_card_list(play)

    def test_hand_get_none_low_triple_single(self):
        """tests get low triple single where other card is None"""
        c = None
        each_count = 3
        extra = 1
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        _check_triple(play.cards)
        assert play.num_cards() == 4
        _print_card_list(play)

    def test_hand_get_low_triple_double_none(self):
        """tests get low triple double where other card is None"""
        c = None
        each_count = 3
        extra = 2
        play = self.hand_adj_trip.get_low(c, each_count, extra=extra)
        _check_triple(play.cards)
        assert play.num_cards() == 5
        _print_card_list(play)

    def test_random_hand_single(self):
        """tests get low single with random hands"""
        plays = TEST_MULTIPLIER * 100
        each_count = 1
        _run_random_hand(plays, hand.Hand.get_low, (each_count, ),
                                  _check_single, ())

    def test_random_hand_doubles(self):
        """tests get low double with random hands"""
        plays = TEST_MULTIPLIER * 100
        each_count = 2
        _run_random_hand(plays, hand.Hand.get_low, (each_count, ),
                                  _check_double, ())

    def test_random_hand_triple_alone(self):
        """tests get low triple with random hands"""
        plays = TEST_MULTIPLIER * 100
        each_count = 3
        extra = 0
        _run_random_hand(plays, hand.Hand.get_low, (each_count, extra),
                                  _check_triple, ())

    def test_random_hand_triple_single(self):
        """tests get low triple with random hands"""
        plays = TEST_MULTIPLIER * 200
        each_count = 3
        extra = 1
        _run_random_hand(plays, hand.Hand.get_low, (each_count, extra),
                                  _check_triple, ())

    def test_random_hand_triple_double(self):
        """tests get low triple with random hands"""
        plays = TEST_MULTIPLIER * 300
        each_count = 3
        extra = 2
        _run_random_hand(plays, hand.Hand.get_low, (each_count, extra),
                                  _check_triple, ())

    def test_random_hand_quad_alone(self):
        """tests get low triple with random hands"""
        plays = TEST_MULTIPLIER * 400
        each_count = 4
        extra = 0
        _run_random_hand(plays, hand.Hand.get_low, (each_count, extra),
                                  _check_quadruples, ())

    def test_random_hand_quad_single(self):
        """tests get low triple with random hands"""
        plays = TEST_MULTIPLIER * 400
        each_count = 4
        extra = 2
        _run_random_hand(plays, hand.Hand.get_low, (each_count, extra),
                                  _check_quadruples, ())

    def test_random_hand_quad_double(self):
        """tests get low triple with random hands"""
        plays = TEST_MULTIPLIER * 400
        each_count = 4
        extra = 4
        _run_random_hand(plays, hand.Hand.get_low, (each_count, extra),
                                  _check_quadruples, ())

class TestGetStraights(object):
    def setup_method(self):
        self.hand = hand.Hand(cards)
        self.hand_adj_trip = hand.Hand(adj_trip)
        self.hand_quadplex = hand.Hand(quadplex)

    def test_hand_single_straights_valid(self):
        """tests get valid low single straight"""
        c = card.Card('3', 'h')
        each_count = 1
        length = 5
        play = self.hand.get_low_straight(c, each_count, length)
        _check_straight(play.cards, 1)
        assert play.num_cards() == length * each_count
        assert play.get_base_card() > c
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

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
        _check_straight(play.cards, 2)
        assert play.num_cards() == length * each_count
        assert play.get_base_card() > c
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

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
        _check_straight(play.cards, 3)
        assert play.num_cards() == length * each_count
        assert play.get_base_card() > c
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_single_straights_none(self):
        """tests get valid low single straight"""
        c = None
        each_count = 1
        length = 5
        play = self.hand.get_low_straight(c, each_count, length)
        _check_straight(play.cards, 1)
        _print_card_list(play)

    def test_hand_double_straights_none(self):
        """tests get valid low double straight"""
        c = None
        each_count = 2
        length = 3
        play = self.hand.get_low_straight(c, each_count, length)
        _check_straight(play.cards, 2)
        _print_card_list(play)

    def test_hand_triple_straights_none(self):
        """tests get valid low triple straight"""
        c = None
        each_count = 3
        length = 2
        play = self.hand_adj_trip.get_low_straight(c, each_count, length)
        _check_straight(play.cards, 3)
        _print_card_list(play)

    def test_random_hand_straight_single(self):
        """tests get straight with random hands"""
        plays = TEST_MULTIPLIER * 100
        each_count = 1
        length = 5
        _run_random_hand(plays, hand.Hand.get_low_straight, (each_count, length),
                                  _check_straight, (each_count, ))

    def test_random_hand_straight_double(self):
        """tests get straight with random hands"""
        plays = TEST_MULTIPLIER * 200
        each_count = 2
        length = 3
        _run_random_hand(plays, hand.Hand.get_low_straight, (each_count, length),
                                  _check_straight, (each_count, ))

    def test_random_hand_straight_triples(self):
        """tests get straight with random hands"""
        plays = TEST_MULTIPLIER * 1000
        each_count = 3
        length = 2
        _run_random_hand(plays, hand.Hand.get_low_straight, (each_count, length),
                                  _check_straight, (each_count, ))

class TestGetAdjTriples(object):
    def setup_method(self):
        self.hand = hand.Hand(cards)
        self.hand_adj_trip = hand.Hand(adj_trip)
        self.hand_quadplex = hand.Hand(quadplex)

    def test_hand_get_low_adj_trip_alone_valid(self):
        """tests get valid adj trip with 2 extras"""
        c = card.Card('4', 'h')
        play = self.hand_adj_trip.get_low_adj_triple(c, 0)
        assert play.num_cards() == 6
        assert play.get_base_card() > c
        _check_adj_triple(play.cards, 0)
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_adj_trip_single_valid(self):
        """tests get valid adj trip with 2 extras"""
        c = card.Card('4', 'h')
        play = self.hand_adj_trip.get_low_adj_triple(c, 2)
        assert play.num_cards() == 8
        assert play.get_base_card() > c
        _check_adj_triple(play.cards, 2)
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_adj_trip_double_valid(self):
        """tests get valid adj trip with 4 extras"""
        c = card.Card('4', 'h')
        play = self.hand_adj_trip.get_low_adj_triple(c, 4)
        assert play.num_cards() == 10
        assert play.get_base_card() > c
        _check_adj_triple(play.cards, 4)
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_adj_trip_alone_none(self):
        """tests get valid adj trip with 2 extras"""
        c = None
        play = self.hand_adj_trip.get_low_adj_triple(c, 0)
        assert play.num_cards() == 6
        _check_adj_triple(play.cards, 0)
        _print_card_list(play)

    def test_hand_get_low_adj_trip_single_none(self):
        """tests get valid adj trip with 2 extras"""
        c = None
        play = self.hand_adj_trip.get_low_adj_triple(c, 2)
        assert play.num_cards() == 8
        _check_adj_triple(play.cards, 2)
        _print_card_list(play)

    def test_hand_get_low_adj_trip_double_none(self):
        """tests get valid adj trip with 4 extras"""
        c = None
        play = self.hand_adj_trip.get_low_adj_triple(c, 4)
        assert play.num_cards() == 10
        _check_adj_triple(play.cards, 4)
        _print_card_list(play)
    
    def test_random_hand_adj_triple_alone(self):
        """tests get low adj triple with random hands"""
        plays = TEST_MULTIPLIER * 1000
        extra = (0, )
        _run_random_hand(plays, hand.Hand.get_low_adj_triple, extra, _check_adj_triple, extra)

    def test_random_hand_adj_triple_single(self):
        """tests get low adj triple with random hands"""
        plays = TEST_MULTIPLIER * 1000
        extra = (2, )
        _run_random_hand(plays, hand.Hand.get_low_adj_triple, extra, _check_adj_triple, extra)

    def test_random_hand_adj_triple_double(self):
        """tests get low adj triple with random hands"""
        plays = TEST_MULTIPLIER * 1000
        extra = (4, )
        _run_random_hand(plays, hand.Hand.get_low_adj_triple, extra, _check_adj_triple, extra)

class TestGetWilds(object):
    def setup_method(self):
        self.hand = hand.Hand(cards)
        self.hand_adj_trip = hand.Hand(adj_trip)
        self.hand_quadplex = hand.Hand(quadplex)

    def test_hand_get_low_wild_simple_valid(self):
        """tests get valid low wild"""
        c = card.Card('5', 'h')
        play = self.hand.get_low_wild(c)
        _check_quadruples(play.cards)
        assert play.get_base_card() > c
        _print_card_list(play, extra_msg="greater than {}".format(str(c)))

    def test_hand_get_low_wild_simple_invalid(self):
        """tests get invalid low wild"""
        c = card.Card('7', 'h')
        assert not self.hand.get_low_wild(c)   

    def test_hand_get_low_wild_simple_none(self):
        """tests get valid low wild"""
        c = None
        play = self.hand.get_low_wild(c)
        _check_quadruples(play.cards)
        _print_card_list(play)

    def test_random_hand_wilds(self):
        """runs get wilds with random hands"""
        plays = TEST_MULTIPLIER * 1000
        _run_random_hand(plays, hand.Hand.get_low_wild, (), _check_wild, ())

def _print_card_list(card_play, extra_msg=""):
    """prints out a list of cards with a message"""
    if extra_msg:
        extra_msg = "({})".format(extra_msg)
    print("\nValid {} {}: {}".format(card_play.play_type,
                                     extra_msg,
                                     " ".join(str(c) for c in card_play.cards)))

def _get_random_hands_with_opposing_card(num_cards_per_hand, num_hands):
        """
        gets a list of [num_hands] random hand with 
        [num_cards_per_hand] cards coupled with [num_hands] cards
        """
        deck = get_new_shuffled_deck()
        hands = []
        cards = []
        for _ in range(num_hands):
            c = random.sample(deck, num_cards_per_hand)
            hands.append(hand.Hand(c))
            cards.append(random.choice(deck + [None]))
        return hands, cards

def _run_random_hand(plays, get_low_type, get_low_args, _checker, _checker_args):
    """runs [plays] number of tests on random hands for get_low()"""
    random_hands, random_cards = _get_random_hands_with_opposing_card(17, plays)
    for i, h in enumerate(random_hands):
        c = random_cards[i]
        play = get_low_type(h, c, *get_low_args)
        if play:
            if c and c.value < SMALL_JOKER_VALUE:
                assert play.get_base_card() > c
            _checker(play.cards, *_checker_args)
            #_print_card_list(play, extra_msg="greater than {}".format(str(c)))
