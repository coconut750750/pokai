"""
Generates random hands and writes into p1_cards.txt and p2_cards.txt
"""

from pokai.src.game.game_tools import get_new_shuffled_deck
from pokai.src.game.card import Card

def write_cards(cards, filename):
    cards = sorted(cards, key=lambda card: card.value)
    with open(filename, 'w') as f:
        for card in cards:
            f.write(Card.card_to_str(card) + "\n")

def main():
    deck = get_new_shuffled_deck()
    p1_cards = deck[0: 17]
    p2_cards = deck[17: 37]
    write_cards(p1_cards, 'p1_cards.txt')
    write_cards(p2_cards, 'p2_cards.txt')

if __name__ == '__main__':
    main()
