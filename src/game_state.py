"""
Game state module
"""

from player import Player
from hand import Hand
from card import Card, VALUES, SUITS
from random import shuffle

NUM_SUITS = len(SUITS)

deck = []
for v in VALUES:
    for s in SUITS:
        if v == "Z":
            deck.append(Card(v, 0))
            deck.append(Card(v, 1))
            break
        else:
            deck.append(Card(v, s))

taken = []

for i in range(1, 3):
    with open("p{}_cards.txt".format(i), "r") as f:
        for line in f.readlines():
            card_str = line.strip()
            value_index = VALUES.index(card_str[0].upper())
            if value_index == len(VALUES) - 1:
                suit_index = int(card_str[1])
            else:
                suit_index = SUITS.index(card_str[1].lower())
            card_index = value_index * NUM_SUITS + suit_index
            taken.append(deck[card_index])

for c in taken:
    deck.remove(c)

leftover = Hand(deck)
