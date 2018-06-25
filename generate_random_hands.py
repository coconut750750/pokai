"""
Generates random hands and writes them into p1_cards.txt and p2_cards.txt
These files can then be used for main.py

Example usage: python3 generate_random_hands.py
"""

from pokai.game.game_tools import get_new_shuffled_deck
from pokai.game.card import Card

def write_cards(cards, filename):
    cards = sorted(cards, key=lambda card: card.value)
    with open(filename, 'w') as f:
        for card in cards:
            f.write(Card.card_to_str(card) + "\n")

def main():
    deck = get_new_shuffled_deck()
    p1_cards = deck[0: 20]
    p2_cards = deck[20: 37]
    write_cards(p1_cards, 'p1_cards.txt')
    write_cards(p2_cards, 'p2_cards.txt')

if __name__ == '__main__':
    main()
