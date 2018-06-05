"""
Game tools module.
Provides useful functionality for game operations
"""

from random import shuffle
from pokai.src.card import Card, VALUES, SUITS

NUM_PLAYERS = 3
TOTAL_CARDS = 52

# PLAY TYPES
SINGLES = 'singles'
DOUBLES = 'doubles'
TRIPLES = 'triples'
QUADRUPLES = 'fours'
STRAIGHTS = 'straights'
DOUBLE_STRAIGHTS = 'double_straights'
TRIPLE_STRAIGHTS = 'triple_straights'
ADJ_TRIPLES = 'adj_triples'
DOUBLE_JOKER = 'double_joker'

def get_new_shuffled_deck():
    """Returns a shuffled list of all the cards"""
    deck = []
    for v in VALUES:
        for s in SUITS:
            if v == "Z":
                deck.append(Card(v, 0))
                deck.append(Card(v, 1))
                break
            else:
                deck.append(Card(v, s))
    shuffle(deck)
    return deck

def remove_from_deck(deck, cards):
    """Returns a shuffled list of all the untaken cards"""
    if not deck or not cards:
        return deck

    for c in cards:
        deck.remove(c)
    return deck
