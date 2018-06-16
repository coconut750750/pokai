"""
Probability module for poker
"""

import operator as op
from functools import reduce
from itertools import groupby
from pokai.src.game.game_tools import TOTAL_CARDS

##########  HELPER FUNCTIONS START  ##########

def percent(numerator, denominator):
    """return percentage based off of numberator and denominator"""
    return int(numerator * 100 / denominator) / 100

def choose(n, r):
    """
    An efficient choose function
    Source: https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python
    Returns n C r
    """
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer // denom

def get_num_less_occurances(card_list, occurances, base_val=-1):
    """returns number of times a card appears for less than occurances times"""
    c = [(1 if len(list(c)) < occurances and value > base_val else 0)\
                 for value, c in groupby(card_list, lambda c: c.value)]
    return sum(c)

def get_num_exact_occurances(card_list, occurances, base_val=-1):
    """returns number of times a card appears for exactly occurances times"""
    c = [(1 if len(list(c)) == occurances and value > base_val else 0)\
                 for value, c in groupby(card_list, lambda c: c.value)]
    return sum(c)

def get_num_more_occurances(card_list, occurances, base_val=-1):
    """returns number of times a card appears for greater than occurances times"""
    c = [(1 if len(list(c)) > occurances and value > base_val else 0)\
                 for value, c in groupby(card_list, lambda c: c.value)]
    return sum(c)

##########  HELPER FUNCTIONS END  ##########

##########  PROBABILITY FUNCTIONS START  ##########

def _prob_of_doubles(leftover_cards, n_cards1, base_val=-1):
    """
    Returns the probability of an opponent having a hand with a double
    calculated manually
    LEFTOVER_CARDS MUST BE SORTED

      To calculate the probability of an opponent having a double we
    calculate the probability of both opponents not having a double.
    This occurs when the players successfully split up every pair
    by taking one card from each existing pairs. There are 2 ways
    to split up a pair: (12, 21). So, the total number of ways
    to split up doubles is: 2 ^ [number of doubles].
      Then we look at the ways to split up the cards that do not
    participate in a double. We call those not doubles. From
    that group of cards, player 1 must take some number of them
    and player 2 takes the rest. The number of ways player 1 can
    take cards from that pile is [number of not doubles] CHOOSE
    [number of cards player 1 can freely choose]. That number of cards
    player 1 can freely choose is [number of player 1 cards] - [number
    of doubles] since each player must take one card from each pair.
      So the final number of hands where a player has a double is:
    [total cards] - (2 ^ [number of doubles]) *
    ( [number of not doubles] CHOOSE [number of player 1 cards] - [number of doubles] )
    """
    num_cards = len(leftover_cards)
    total = choose(num_cards, n_cards1)
    n_cards2 = num_cards - n_cards1

    # if there is a triple or quad, someone MUST have a double
    if get_num_more_occurances(leftover_cards, 2, base_val=base_val):
        return 1

    # DOES NOT include cards that are less than base_val
    num_doubles = get_num_exact_occurances(leftover_cards, 2, base_val=base_val)
    if not num_doubles:
        return 0

    # both hands are big enough to hold all of the pairs
    if n_cards1 >= num_doubles and n_cards2 >= num_doubles:
        # num extra cards is just cards not part of num_doubles
        num_not_double = num_cards - 2 * num_doubles
        # must take num_doubles for each player to avoid double
        num_take_from_double = num_doubles
        num_poss = total - choose(num_not_double, n_cards1 - num_take_from_double) * (2 ** num_doubles)
        return percent(num_poss, total)

    # one hands is not big enough to hold all the pairs so the other has to
    return 1

def _prob_of_triples(leftover_cards, n_cards1, base_val=-1):
    """
    Returns the probability of an opponent having a hand with a triple
    calculated manually
    LEFTOVER_CARDS MUST BE SORTED
    
      To calculate the probability of an opponent having a triple, we
    calculate the probability of both opponents not having a triple.
    This occurs when they have successfully split up the threes (2 and 1)
    and have successfully split up the quadruples (2 and 2). There are
    3 ways to split up a three (122, 212, 221) where one person takes 1.
    There are 6 ways to split up a quad (1122, 1212, 1221, 2112, 2121, 2211)
    where one person takes 2. So, the total number of ways to split up all
    the triples and quads is: 3 ^ [number of triples] * 4 ^ [number of quads].
      Then, we look at the number of ways to split up the cards that do not
    participate in any triples or quadruples. We call them not_triples. From
    that group of cards, player 1 must take some number of them and player 2
    takes the rest. The number of ways player 1 can take cards from that pile is
    [number of not triples] CHOOSE [number of cards player 1 can freely choose].
    The number of cards player 1 can freely choose depends on how player 1
    and 2 splits up the threes. Essentially, the number of free cards player 1
    has ranges from [number of cards player 1 has] - [number of triples] -
    2 * [number of quad] to [number of cards player 1 has] -
    2 * [number of triples] - 2 * [number of quad]. 2 * [number of triples]
    because he/she can potentially take 2 cards from the triple. 2 * [number of
    quads] because he/she must take 2 cards from all the quads.
      Moreover, there is a number of different ways player 1 can take 2 cards
    from i number of triples where i ranges from 0 to [number of triples].
    That number is [number of triples] CHOOSE i.
      So the final number of hands where a player has a triple is:
    [total cards] - ( 3 ^ [number of triples] * 4 ^ [number of quadruples] ) *
        ( [number not triple] CHOOSE [number player 1 cards] - i - 2  * [number of quads] ) *
        ( [number of triples] CHOOSE j )
    where i : [number of triples : number of triples * 2] (inclusive)
    and j : [0 : number of triples] (inclusive)
    """
    num_cards = len(leftover_cards)
    total = choose(num_cards, n_cards1)
    n_cards2 = num_cards - n_cards1

    num_triples = get_num_exact_occurances(leftover_cards, 3, base_val=base_val)
    num_quads = get_num_exact_occurances(leftover_cards, 4, base_val=base_val)
    num_more_triples = num_triples + num_quads

    if not num_more_triples:
        return 0

    # both hands are big enough to separate the triples
    if n_cards1 >= num_more_triples and n_cards2 >= num_more_triples:
        # num extra cards is just num cards not part of num_more_triples
        num_not_triple = num_cards - 3 * num_triples - 4 * num_quads
        # must take 2 * num_quad for each player to avoid triples
        num_take_from_quad = num_quads * 2
        num_ways_to_avoid_triples = 0

        for i in range(num_triples, num_triples * 2 + 1):
            num_ways_to_take_non_trips = choose(num_not_triple, n_cards1 - i - num_take_from_quad)
            # how many ways to split i threes in 2 such that one pile has 1 taken and the other has 2 taken
            num_ways_to_split_splitted_threes = choose(num_triples, i - num_triples)
            num_ways_to_avoid_triples += num_ways_to_take_non_trips * num_ways_to_split_splitted_threes

        num_ways_to_split_threes_and_quads = 3 ** num_triples * 6 ** num_quads
        num_ways_to_avoid_triples *= num_ways_to_split_threes_and_quads

        num_poss = total - num_ways_to_avoid_triples
        return percent(num_poss, total)

    # one hands is not big enough to hold all the pairs so the other has to
    return 1

def _prob_of_quads(leftover_cards, n_cards1, base_val=-1):
    """
    Returns the probability of an opponent having a hand with a quad
    """
    num_cards = len(leftover_cards)
    total = choose(num_cards, n_cards1)
    n_cards2 = num_cards - n_cards1

    num_quads = get_num_exact_occurances(leftover_cards, 4, base_val=base_val)
    if not num_quads:
        return 0

    num_not_quad = num_cards - 4 * num_quads

    num_ways_for_quad = 0
    for i in range(1, num_quads + 1):
        num_leftover_cards1 = n_cards1 - (4 * i)
        num_leftover_quads = num_quads - i

        num_cards_after_i_quads = num_cards - (4 * i)

        num_ways_to_choose_i_quads = choose(num_quads, i)

        if num_leftover_cards1 > 0:
            num_ways_to_choose_non_quads_p1 = choose(num_cards_after_i_quads, num_leftover_cards1)
        else:
            num_ways_to_choose_non_quads_p1 = 0

        if i & 2:
            num_ways_to_choose_i_quads *= -1
        print("bla", i, num_ways_to_choose_i_quads, (num_ways_to_choose_non_quads_p1))
        num_ways_for_quad += num_ways_to_choose_i_quads * (num_ways_to_choose_non_quads_p1)

    return percent(num_ways_for_quad, total)

##########  PROBABILITY FUNCTIONS END  ##########

def prob_doubles_greater_than(leftover_cards, n_cards1, base_card):
    """
    Returns the probability of an opponent having a hand with a double
    bigger than base_card
    """
    leftover_cards.sort(key=lambda c: c.value, reverse=False)
    base_val = -1 if not base_card else base_card.value
    return _prob_of_doubles(leftover_cards, n_cards1, base_val=base_val)


def probability_of_win_play(play, n_cards1, known_cards):
    """
    Calculates the probability of a play winning the round given:
    play -- the actual play
    n_cards1 -- number of cards opponent 1 has
                number of cards opponent 2 has = 52 - known_cards - n_cards1
    known_cards -- list of cards known to player 
                   (revealed, the player's cards themselves and the play cards)
    Returns the probability that the play wins
    """
    n_cards2 = TOTAL_CARDS - n_cards1 - len(known_cards)
    total_combinations = choose(n_cards1 + n_cards2, n_cards1)
    base_card = play.get_base_card()
    return
