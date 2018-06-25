"""
Main command line interface for Pokai
"""
import os
import argparse

from pokai.game.card import Card
from pokai.game.hand import Hand
from pokai.game.aiplayer import AIPlayer
from pokai.game.game_tools import *
from pokai.game.game_state import GameState
from pokai.game.card_play import Play

window_rows, window_columns = os.popen('stty size', 'r').read().split()
parser = argparse.ArgumentParser(description='Play a game with the AI.')
parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help="use this flag to debug AI")
debug = parser.parse_args().debug

PLAYER_1_FILE = 'p1_cards.txt'
PLAYER_2_FILE = 'p2_cards.txt'

PROMPT_PLAYED_CARDS = "Please input played cards separated by spaces (i.e. 6h for six of hearts)\n"

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

def get_play_from_input(user_input):
    """returns card play based on user's input"""
    if not user_input:
        return None
    player_card_strs = user_input.split()
    played_cards = Card.strs_to_cards(player_card_strs)
    next_play = Play.get_play_from_cards(played_cards)
    return next_play

def init_game():
    hand = get_computer_hand()
    n_cards1 = get_n_cards_1()
    game_state = GameState(hand.num_cards(), n_cards1)
    ai = AIPlayer(hand, 0, "Computer")
    if debug:
        print("AI's hand:")
        ai.reveal()
        print("AI's hand strength:", ai.get_hand_strength(game_state))
    return game_state, ai

def main():
    game_state, ai = init_game()

    while game_state.game_is_on():
        # Game Loop
        print("-" * int(window_columns))
        turn = game_state.get_current_turn()

        if not turn:
            print("Computer's turn.")
            next_play = ai.get_best_play(game_state)                
            ai.play(next_play)
            print("Computer has {} cards left.".format(ai.amount()))
        else:
            print("Player {}'s turn.".format(turn))
            next_play = get_play_from_input(input(PROMPT_PLAYED_CARDS))
            while game_state.play_was_used(next_play):
                next_play = get_play_from_input(input(PROMPT_PLAYED_CARDS))

            next_play.position = turn
            print('Player {} has {} cards left.'.format(turn, game_state.get_player_num_cards(turn)))

        print(next_play)
        game_state.cards_played(next_play)
        game_state.increment_turn()

    print("Player {} won!".format(game_state.get_winner()))
    ai.reveal()

if __name__ == '__main__':
    main()
