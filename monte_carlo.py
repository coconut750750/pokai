"""
Monte Carlo module.
Provides functionality to estimate hand and play strength
"""
import copy
import game_tools
from game_tools import SINGLES, DOUBLES, TRIPLES, QUADRUPLES, STRAIGHTS, DOUBLE_STRAIGHTS, ADJ_TRIPLES, DOUBLE_JOKER
from hand import Hand
from random import randint

def simulate_one_game(hand, n_cards1, n_cards2, display):
    """
    Simulates 1 game with:
    hand -- starting hand
    n_cards1 -- number of cards in opponent 1's hand
    n_cards2 -- number of cards in opponent 2's hand

    Returns if hand wins the game
    TODO: use the used_cards list to strategically play cards
    """

    used_cards = hand.get_cards()
    deck = game_tools.get_new_shuffled_deck()
    deck = game_tools.remove_from_deck(deck, used_cards)

    hand1 = Hand(deck[0: n_cards1])
    hand2 = Hand(deck[n_cards1: n_cards1 + n_cards2])

    if display:
        print("Player 0:", hand)
        print("Player 1:", hand1)
        print("Player 2:", hand2)
        print("simulation start")

    hands = [hand, hand1, hand2]

    used_cards = deck[n_cards2:]

    turn = randint(0, 2)
    end = hand.num_cards() == 0 or hand1.num_cards() == 0 or hand2.num_cards() == 0
    prev_play = None

    while not end:
        next_play = None
        if not prev_play or prev_play.position == turn:
            # lead play
            next_play = hands[turn].get_lead_play()
            if not next_play:
                break
            next_play.pos = turn

            hands[turn].remove_cards(next_play.cards)
        else:
            # need to beat prev play
            if prev_play.play_type == SINGLES:
                next_play = hands[turn].get_low(prev_play.get_base_card(), 1)
            elif prev_play.play_type == DOUBLES:
                next_play = hands[turn].get_low(prev_play.get_base_card(), 2)
            elif prev_play.play_type == TRIPLES:
                next_play = hands[turn].get_low(prev_play.get_base_card(), 2,
                                                prev_play.num_extra)
            elif prev_play.play_type == STRAIGHTS:
                next_play = hands[turn].get_low_straight(prev_play.get_base_card(),
                                                         1, prev_play.num_base_cards())
            elif prev_play.play_type == DOUBLE_STRAIGHTS:
                next_play = hands[turn].get_low_straight(prev_play.get_base_card(),
                                                         2, int(prev_play.num_base_cards() / 2))
            elif prev_play.play_type == ADJ_TRIPLES:
                next_play = hands[turn].get_low_adj_triple(prev_play.get_base_card(),
                                                           prev_play.num_extra)
            else: # prev_play.play_type == QUADRUPLES or DOUBLE_JOKER:
                next_play = hands[turn].get_low_wild(prev_play.get_base_card())

            # if next play is none, check if any wilds and play
            # wilds only if triples, straights, double_straights, and adj_triples
            if not next_play:
                if prev_play.play_type != SINGLES and prev_play.play_type != DOUBLES:
                    next_play = hands[turn].get_low_wild(prev_play.get_base_card())

        if next_play:
            hands[turn].remove_cards(next_play.cards)
            next_play.position = turn
            if display:
                print(next_play)
            if next_play.play_type == DOUBLE_JOKER:
                prev_play = None
            else:
                prev_play = next_play

        if prev_play and prev_play.play_type != DOUBLE_JOKER:
            turn = (turn + 1) % game_tools.NUM_PLAYERS

        end = hand.num_cards() == 0 or hand1.num_cards() == 0 or hand2.num_cards() == 0

    return hand.num_cards() == 0

def simulate(hand, n_games, n_cards1, n_cards2, display=False):
    """
    Simulates n games with:
    hand -- starting hand
    n_games -- number of games
    n_cards1 -- number of cards in opponent 1's hand
    n_cards2 -- number of cards in opponent 2's hand

    Returns number of wins
    """
    wins = 0
    for count in range(n_games):
        if display:
            print("Simulation {}".format(count))
        hand_sim = copy.deepcopy(hand)
        if simulate_one_game(hand_sim, n_cards1, n_cards2, display=display):
            wins += 1

    return wins

def estimate_hand_strength(hand, leftover_cards):
    """Estimates hand strength"""
    pass

def estimate_play_strength():
    """Estimates play strength"""
    pass
