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
from pokai.src.game.aiplayer import AIPlayer

SIMULATIONS = 1000

def simulate_one_game(hands, start_pos, used_cards, display):
    """
    Simulates 1 game with:
    hands -- list of hands where starting hand is at index 0
    start_pos -- player that starts
    used_cards -- list of used cards
    display -- print out results if True

    To simulate hands fairly, we use a basic Poker player to wrap all hands
    Returns if hand wins the game
    """
    if display:
        print("Player 0:", hands[0])
        print("Player 1:", hands[1])
        print("Player 2:", hands[2])
        print("simulation start")

    players = [Player(hands[0], 0, ""), Player(hands[1], 1, ""), Player(hands[2], 2, "")]

    turn = start_pos
    prev_play = None

    while not game_is_over(hands):
        hand_counts = [hand.num_cards() for hand in hands]
        next_play = players[turn].get_play(prev_play, hand_counts, used_cards)

        if next_play:
            players[turn].hand.remove_cards(next_play.cards)
            if display:
                print(next_play)
            if next_play.play_type == DOUBLE_JOKER:
                prev_play = None
            else:
                prev_play = next_play

        if prev_play:
            turn = (turn + 1) % game_tools.NUM_PLAYERS

    return hands[0].num_cards() == 0

def simulate_one_random_game(hand, n_cards1, used_cards, display):
    """
    Simulates 1 random game with:
    hand -- starting hand
    n_cards1 -- number of cards in opponent 1's hand
                number of cards in opponent 2's hand = deck - hand - n_cards1 - used_cards
    used_cards -- list of revealed cards
    display -- print out results if True

    Returns if hand wins the game
    """
    deck = game_tools.get_new_shuffled_deck()
    deck = game_tools.remove_from_deck(deck, hand.get_cards())
    deck = game_tools.remove_from_deck(deck, used_cards)

    hand1 = Hand(deck[0: n_cards1])
    hand2 = Hand(deck[n_cards1:])

    return simulate_one_game([hand, hand1, hand2], randint(0, 2), used_cards, display)

def simulate(hand, n_games, n_cards1, used_cards, display=False):
    """
    Simulates n games with:
    hand -- starting hand
    n_games -- number of games
    n_cards1 -- number of cards in opponent 1's hand
                number of cards in opponent 2's hand = deck - hand - n_cards1 - used_cards
    used_cards -- list of revealed cards
    Returns number of wins
    """
    wins = 0
    for count in range(n_games):
        if display:
            print("Simulation {}".format(count))
        hand_sim = copy.deepcopy(hand)
        if simulate_one_random_game(hand_sim, n_cards1, list(used_cards), display=display):
            wins += 1

    return wins

def _simulation_worker(index, hand, n_games, n_cards1, used_cards, return_list):
    """
    Worker for multiprocessed simulation
    index -- index of the worker and where to store the data
    hand -- starting hand
    n_games -- number of games
    n_cards1 -- number of cards in opponent 1's hand
                number of cards in opponent 2's hand = deck - hand - n_cards1 - used_cards
    used_cards -- list of revealed cards
    return_list -- where to store the data
    """
    return_list[index] = simulate(hand, n_games, n_cards1, used_cards)

def simulate_multiprocesses(hand, n_games, n_cards1, used_cards, n_processes):
    """
    Simulates n games but uses multiple processes
    hand -- starting hand
    n_games -- number of games
    n_cards1 -- number of cards in opponent 1's hand
                number of cards in opponent 2's hand = deck - hand - n_cards1 - used_cards
    used_cards -- list of revealed cards
    n_processes -- number of processes
    Returns number of wins
    """
    manager = multiprocessing.Manager()
    return_list = manager.list([0] * n_processes)

    processes = []
    sim_per_process = int(n_games / n_processes)

    for i in range(n_processes):
        sim_args = (i, hand, sim_per_process, n_cards1, used_cards, return_list)
        p = multiprocessing.Process(target=_simulation_worker, args=sim_args)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    return sum(return_list)

def estimate_hand_strength(hand, n_cards1, used_cards):
    """
    Estimates hand strength by estimating the probability that the hand wins
    hand -- the hand to test
    n_cards1 -- number of cards in opponent 1's hand
                number of cards in opponent 2's hand = deck - hand - n_cards1 - used_cards
    used_cards -- list of revealed cards
    """
    return simulate_multiprocesses(hand, SIMULATIONS, n_cards1, used_cards, 2) / SIMULATIONS

def estimate_play_strength(card_play, hand, n_cards1, used_cards):
    """Estimates play strength"""
    pass
