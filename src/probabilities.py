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

def get_num_more_than_occurances(card_list, occurances):
    """returns number of times a card appears for than occurances"""
    return sum([(1 if len(list(c)) > occurances else 0) for _, c in groupby(card_list, lambda c: c.value)])

def get_num_occurances(card_list, occurances):
    """returns number of times a card appears for exactly occurances times"""
    return sum([(1 if len(list(c)) == occurances else 0) for _, c in groupby(card_list, lambda c: c.value)])

##########  HELPER FUNCTIONS END  ##########

def prob_of_doubles(leftover_cards, n_cards1):
    """
    Returns the probability of an opponent having a hand with a double
    calculated manually
    """
    total = choose(len(leftover_cards), n_cards1)

    num_doubles = get_num_occurances(leftover_cards, 2)
    if not num_doubles:
        return 0

    num_more_doubles = get_num_more_than_occurances(leftover_cards, 2)
    if num_more_doubles > 0:
        return 1

    if n_cards1 >= num_doubles and len(leftover_cards) - n_cards1 >= num_doubles:
        num_singles = get_num_occurances(leftover_cards, 1)
        num_poss = total - choose(num_singles, n_cards1 - num_doubles) * (2 ** num_doubles)
        return percent(num_poss, total)

    return 0

def prob_doubles_greater_than(leftover_cards, n_cards1, base_card):
    """
    Returns the probability of an opponent having a hand with a double
    bigger than base_card
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
