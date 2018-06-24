"""
Main command line interface for Pokai
"""
from pokai.game.card import Card
from pokai.game.hand import Hand
from pokai.game.aiplayer import AIPlayer
from pokai.game.game_tools import *
from pokai.game.game_state import GameState
from pokai.game.card_play import Play

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
    player_card_strs = user_input.split()
    played_cards = Card.strs_to_cards(player_card_strs)
    next_play = Play.get_play_from_cards(played_cards)
    return next_play

def main():
    """Main method"""
    hand = get_computer_hand()
    n_cards1 = get_n_cards_1()
    game_state = GameState(hand.num_cards(), n_cards1)
    ai = AIPlayer(hand, 0, "Computer")
    ai.reveal()

    while game_state.game_is_on():
        # Game Loop
        turn = game_state.get_current_turn()

        if not turn:
            print("Computer's turn.")
            next_play = ai.get_best_play(game_state)
            if next_play:
                game_state.cards_played(next_play)
                ai.play(next_play, display=True)
            else:
                print("Computer passes.")
            print("Computer has {} cards left.".format(ai.amount()))
        else:
            print("Player {}'s turn.".format(turn))
            user_input = input(PROMPT_PLAYED_CARDS)
            if not user_input:
                print('Player {} passes'.format(turn))
            else:
                next_play = get_play_from_input(user_input)
                if next_play:
                    next_play.position = turn
                    game_state.cards_played(next_play)
                    print(next_play)
                else:
                    print('Invalid Play.')

        game_state.increment_turn()
        print()
    print("Player {} won!".format(game_state.get_winner()))
    ai.reveal()

if __name__ == '__main__':
    main()
