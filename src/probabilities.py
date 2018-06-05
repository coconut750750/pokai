"""
Probability module for poker
"""

import operator as op
from functools import reduce
from itertools import groupby
from pokai.src.game_tools import TOTAL_CARDS

##########  HELPER FUNCTIONS START  ##########

def percent(numerator, denominator):
    """return percentage based off of numberator and denominator"""
    return int(numerator / denominator * 100) / 100

def choose(n, r):
    """An efficient choose function"""
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer//denom

def get_num_exact_occurances_greater_than_base(card_list, occurances, base_val=-1):
    """returns number of times a card appears for exactly occurances times"""
    c = [(1 if len(list(c)) == occurances and value > base_val else 0)\
                 for value, c in groupby(card_list, lambda c: c.value)]
    return sum(c)

def get_num_occurances_greater_than_base(card_list, occurances, base_val=-1):
    """returns number of times a card appears for exactly occurances times"""
    c = [(1 if len(list(c)) >= occurances and value > base_val else 0)\
                 for value, c in groupby(card_list, lambda c: c.value)]
    return sum(c)

##########  HELPER FUNCTIONS END  ##########

def prob_of_doubles(leftover_cards, n_cards1, base_val=-1):
    """
    Returns the probability of an opponent having a hand with a double
    calculated manually
    LEFTOVER_CARDS MUST BE SORTED
    """
    total = choose(len(leftover_cards), n_cards1)

    num_more_doubles = get_num_occurances_greater_than_base(leftover_cards, 3, base_val=base_val)
    if num_more_doubles:
        return 1

    # DOES NOT include cards that are less than base_val
    num_doubles = get_num_exact_occurances_greater_than_base(leftover_cards, 2, base_val=base_val)
    if not num_doubles:
        return 0

    # both hands are big enough to hold all of the pairs
    if n_cards1 >= num_doubles and len(leftover_cards) - n_cards1 >= num_doubles:
        # number of singles is just cards not part of num_doubles
        num_singles = len(leftover_cards) - 2 * num_doubles
        num_poss = total - choose(num_singles, n_cards1 - num_doubles) * (2 ** num_doubles)
        return percent(num_poss, total)

    # one hands is not big enough to hold all the pairs so the other has to
    return 1

def prob_doubles_greater_than(leftover_cards, n_cards1, base_card):
    """
    Returns the probability of an opponent having a hand with a double
    bigger than base_card
    LEFTOVER_CARDS MUST BE SORTED
    """


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
