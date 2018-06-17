"""
Main command line interface for Pokai
"""
from pokai.src.game.card import Card
from pokai.src.game.hand import Hand
from pokai.src.game.player import Player
from pokai.src.game.game_tools import *
from pokai.src.game.game_state import GameState
from pokai.src.game.card_play import Play

PLAYER_1_FILE = 'p1_cards.txt'
PLAYER_2_FILE = 'p2_cards.txt'

PROMPT_PLAYED_CARDS = "Please input played cards (separated by spaces): "

def get_cards_from_file(filename):
    """returns a list of cards from file"""
    card_strs = []
    with open(filename, "r") as f:
        for line in f.readlines():
            card_str = line.strip()
            card_strs.append(card_str)
    return Card.strs_to_cards(card_strs)

def get_n_cards_1():
    """returns number of cards in player 1's hand"""
    cards = get_cards_from_file(PLAYER_1_FILE)
    return len(cards)

def get_computer_hand():
    """constructs the hand for the computer based on player's cards"""
    deck = get_new_ordered_deck()
    taken = get_cards_from_file(PLAYER_1_FILE) +\
            get_cards_from_file(PLAYER_2_FILE)

    unused_deck = remove_from_deck(deck, taken)
    return Hand(unused_deck)

def game_playing(ai_hand, n_cards1, n_cards2):
    """returns if the game is over"""
    return ai_hand.num_cards() and n_cards1 and n_cards2

def main():
    """Main method"""
    hand = get_computer_hand()
    n_cards1 = get_n_cards_1()
    game_state = GameState(hand.num_cards(), n_cards1)
    ai = Player(hand, 0, "")

    while game_state.game_is_on():
        # Game Loop
        turn = game_state.get_current_turn()

        if not turn:
            print("Computer's turn.")
            next_play = ai.get_play(game_state.prev_play,
                                    game_state.player_cards,
                                    game_state.get_unrevealed_cards(ai.hand._cards))
            if next_play:
                game_state.cards_played(next_play)
                ai.play(next_play)
        else:
            print("Player {}'s turn.".format(turn))
            player_card_strs = input(PROMPT_PLAYED_CARDS)

            if player_card_strs:
                player_card_strs = player_card_strs.split(' ')
                print(player_card_strs)
                played_cards = Card.strs_to_cards(player_card_strs)
                next_play = Play.get_play_from_cards(played_cards)
                next_play.position = turn
                game_state.cards_played(next_play)

                print("{}".format(next_play.play_type))
                for c in next_play.cards:
                    print(c, end=" ")
                print()

        game_state.increment_turn()
    print("Player {} won!".format(game_state.get_winner()))

if __name__ == '__main__':
    main()
