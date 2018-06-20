"""
Game State module
"""

from pokai.src.game.game_tools import TOTAL_CARDS, NUM_PLAYERS,\
                                 get_new_ordered_deck, remove_from_deck

class GameState(object):
    """
    Holds information about the current game state
    """

    def __init__(self, n_cards0, n_cards1):
        self.used_cards = []
        self.player_cards = [n_cards0, n_cards1,
                             TOTAL_CARDS - n_cards0 - n_cards1]
        self.current_turn = self.player_cards.index(20)
        self.prev_play = None

    def cards_played(self, card_play):
        """
        Called when a player plays cards
        cards_played -- Play of cards that were played
        """
        self.discard_cards(card_play)
        self.prev_play = card_play

    def discard_cards(self, card_play):
        if card_play:
            self.player_cards[card_play.position] -= len(card_play.cards)
            self.used_cards += card_play.cards

    def increment_turn(self):
        """
        Called when the game progresses by a turn
        """
        self.current_turn = (self.current_turn + 1) % NUM_PLAYERS

    def get_player_num_cards(self, player_position):
        """Returns number of cards in player's hands"""
        return self.player_cards[player_position]

    def get_current_turn(self):
        """Returns current turn"""
        return self.current_turn

    def game_is_on(self):
        """returns true if game is still going on"""
        return self.player_cards[0] and self.player_cards[1] and self.player_cards[2]

    def get_unrevealed_cards(self, player0_cards):
        """
        Returns a list of unrevealed cards based on player 0's perspective
        """
        deck = get_new_ordered_deck()
        deck = remove_from_deck(deck, self.used_cards)
        deck = remove_from_deck(deck, player0_cards)
        return deck

    def get_winner(self):
        """returns turn number of winner"""
        if not self.game_is_on():
            return self.player_cards.index(0)
        else:
            return -1

    def __eq__(self, other):
        return other != None and\
               self.used_cards == other.used_cards and\
               self.player_cards == other.player_cards and\
               self.current_turn == other.current_turn and\
               str(self.prev_play) == str(other.prev_play)