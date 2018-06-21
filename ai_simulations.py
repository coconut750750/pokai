"""
Runs simulations with Player and AIPlayer and compares
"""

from time import time
from pokai.src.game.card import Card
from pokai.src.game.game_state import GameState
from pokai.src.game.hand import Hand
from pokai.src.game.player import Player
from pokai.src.game.aiplayer import AIPlayer
from pokai.src.ai_tools.monte_carlo import simulate, simulate_multiprocesses

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

card_strs_decent = ['3h', '4s', '4h', '5d', '6s', '7c', '9h', '9d', '0c',
                    'Jh', 'Jc', 'Ks', 'Kd', 'Ac', 'Ah', '2c', '2d']
card_strs_good = ['4h', '5d', '6c', '7s', '8s', '0s', '0c', '0d', '0h',
                  'QH', 'QD', 'QS', 'KH', 'KS', 'KD', 'KC', 'AC']

def setup_game(card_strs):
    hand = Hand(Card.strs_to_cards(card_strs))
    aiplayer = AIPlayer(hand, 0, "")
    player = Player(hand, 0, "")
    game_state = GameState(17, 17)
    return aiplayer, player, game_state

@time_simulation
def simulate_ai_with_cards(card_strs):
    aiplayer, player, game_state = setup_game(card_strs)
    player_wins = simulate_multiprocesses(player, 100, game_state, 4)
    ai_wins = simulate(aiplayer, 100, game_state)
    return ai_wins, player_wins

if __name__ == '__main__':
    simulate_ai_with_cards(card_strs_decent)
    simulate_ai_with_cards(card_strs_good)
