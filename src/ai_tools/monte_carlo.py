"""
Monte Carlo module.
Provides functionality to estimate hand and play strength
"""
import multiprocessing
import copy
from random import randint
import pokai.src.game.game_tools as game_tools
from pokai.src.game.game_tools import *
from pokai.src.game.hand import Hand
from pokai.src.game.player import Player

SIMULATIONS = 1000

def simulate_one_game(players, game_state, display):
    """
    Simulates 1 game with:
    players -- list of players where starting hand is at index 0
    game_state -- the starting game state
    display -- print out results if True

    To simulate hands fairly, we use a basic Poker player to wrap all hands
    Returns if hand wins the game
    """
    game_state_sim = copy.deepcopy(game_state)
    if display:
        print("Player 0:", players[0].hand)
        print("Player 1:", players[1].hand)
        print("Player 2:", players[2].hand)
        print("simulation start")

    while not game_is_over(players):
        turn = game_state_sim.get_current_turn()
        next_play = players[turn].get_play(game_state_sim)

        if next_play:
            players[turn].play(next_play)
            game_state_sim.cards_played(next_play)
            if display:
                print(next_play)

        game_state_sim.increment_turn()

    return players[0].amount() == 0

def simulate_one_random_game(player, game_state, display):
    """
    Simulates 1 random game with:
    player -- the player object
    game_state -- game information
    display -- print out results if True

    Returns if hand wins the game
    """
    n_cards1 = game_state.get_player_num_cards((player.position + 1) % 3)
    deck = game_tools.get_new_shuffled_deck()
    deck = game_tools.remove_from_deck(deck, player.get_cards())
    deck = game_tools.remove_from_deck(deck, game_state.used_cards)

    player1 = Player(Hand(deck[0: n_cards1]), 1, "")
    player2 = Player(Hand(deck[n_cards1:]), 2, "")

    return simulate_one_game([player, player1, player2], game_state, display)

def simulate(player, n_games, game_state, display=False):
    """
    Simulates n games with:
    player -- the player object
    n_games -- number of games
    game_state -- game information
    Returns number of wins
    """
    wins = 0
    for count in range(n_games):
        if display:
            print("Simulation {}".format(count))
        player_sim = copy.deepcopy(player)
        if simulate_one_random_game(player_sim, game_state, display=display):
            wins += 1

    return wins

def _simulation_worker(index, player, n_games, game_state, return_list):
    """
    Worker for multiprocessed simulation
    index -- index of the worker and where to store the data
    player -- the player object
    n_games -- number of games
    game_state -- game information
    return_list -- where to store the data
    """
    return_list[index] = simulate(player, n_games, game_state)

def simulate_multiprocesses(player, n_games, game_state, n_processes):
    """
    Simulates n games but uses multiple processes
    player -- the player object
    n_games -- number of games
    game_state -- game information
    n_processes -- number of processes
    Returns number of wins
    """
    manager = multiprocessing.Manager()
    return_list = manager.list([0] * n_processes)

    processes = []
    sim_per_process = int(n_games / n_processes)

    for i in range(n_processes):
        sim_args = (i, player, sim_per_process, game_state, return_list)
        p = multiprocessing.Process(target=_simulation_worker, args=sim_args)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return sum(return_list)

def estimate_hand_strength(player, game_state):
    """
    Estimates hand strength by estimating the probability that the hand wins
    player -- the player object
    game_state -- game information
    """
    return simulate_multiprocesses(player, SIMULATIONS, game_state, 4) / SIMULATIONS

def estimate_play_strength(card_play, player, game_state):
    """Estimates play strength"""
    # TODO: use probabilities here
    player_sim = copy.deepcopy(player)
    game_state_sim = copy.deepcopy(game_state)
    player_sim.play(card_play)
    game_state_sim.cards_played(card_play)
    game_state_sim.increment_turn()
    return estimate_hand_strength(player_sim, game_state_sim)

def get_best_play(card_plays, player, game_state, num_best=1):
    """Gets best play from list of plays"""
    strengths = {}
    player = Player(player.hand, player.position, player.type)
    for play in card_plays:
        play.position = player.position
        strengths[play.get_base_card().value] = estimate_play_strength(play, player, game_state)
    ordered_plays = sorted(card_plays,
                           key=lambda play: strengths[play.get_base_card().value],
                           reverse=True)
    if num_best == 1:
        return ordered_plays[0]
    else:
        return ordered_plays[0: num_best]
