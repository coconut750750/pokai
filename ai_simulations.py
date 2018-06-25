"""
Runs simulations with Player and AIPlayer and compares
"""
import argparse
from time import time

from pokai.game.card import Card
from pokai.game.game_state import GameState
from pokai.game.hand import Hand
from pokai.game.player import Player
from pokai.game.aiplayer import AIPlayer
from pokai.ai_tools.monte_carlo import simulate, simulate_multiprocesses

parser = argparse.ArgumentParser(description='Simulate AI and Player.')
parser.add_argument("hand_strength", type=int, choices=[1, 2, 3], 
                    help='choose the strength of the starting hand.')
parser.add_argument("num_simulations", type=int,
                    help='choose the number of simulations.')
parsed_args = parser.parse_args()
hand_strength = parsed_args.hand_strength
num_simulations = parsed_args.num_simulations

def time_simulation(simulation):
    def wrapper(*args, **kwargs):
        print('Simulation started.')
        start = time()
        ai_wins, player_wins = simulation(*args, **kwargs)
        end = time()

        duration = int(end - start)
        print('Simulation took {} seconds.'.format(duration))
        percent_increase = int((ai_wins - player_wins) / player_wins * 100)
        print('The AI had a {}% increase in win rate'.format(percent_increase))

    return wrapper

def setup_game(card_strs):
    hand = Hand(Card.strs_to_cards(card_strs))
    print("Starting hand:", hand)
    aiplayer = AIPlayer(hand, 0, "")
    player = Player(hand, 0, "")
    game_state = GameState(17, 17)
    return aiplayer, player, game_state

@time_simulation
def simulate_ai_with_cards(card_strs, num_simulations):
    aiplayer, player, game_state = setup_game(card_strs)
    player_wins = simulate_multiprocesses(player, num_simulations, game_state, 4)
    ai_wins = simulate(aiplayer, num_simulations, game_state, display_progress_only=True)
    print(player_wins, ai_wins)
    return ai_wins, player_wins

def main(hand, num_simulations):
    strength1 = ['7h', '6h', '0d', '3s', '6s', 'Js', '7d', '9c', 'Ac',
                 'Kd', '5h', '2H', '5C', '0C', '0H', '4D', 'KH']
    strength2 = ['3h', '4s', '4h', '5d', '6s', '7c', '9h', '9d', '0c',
                 'Jh', 'Jc', 'Ks', 'Kd', 'Ac', 'Ah', '2c', '2d']
    strength3 = ['4h', '5d', '6c', '7s', '8s', '0s', '0c', '0d', '0h',
                 'QH', 'QD', 'QS', 'KH', 'KS', 'KD', 'KC', 'AC']
    hands = [strength1, strength2, strength3]
    simulate_ai_with_cards(hands[hand - 1], num_simulations)

if __name__ == '__main__':
    main(hand_strength, num_simulations)
