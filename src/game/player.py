"""
Player module with Player class
"""

from pokai.src.game.hand import Hand
from pokai.src.game.game_tools import SINGLES, DOUBLES, TRIPLES, QUADRUPLES, STRAIGHTS,\
                                      DOUBLE_STRAIGHTS, ADJ_TRIPLES, DOUBLE_JOKER
class Player(object):
    """docstring for Player"""
    def __init__(self, hand, position, t):
        super(Player, self).__init__()
        self.hand = hand
        self.position = position
        self.type = t

    def get_cards(self):
        return self.hand.get_cards()

    def reveal(self):
        print(self.hand)

    def info(self):
        self.hand.print_categories()

    def _get_possible_leads(self, game_state):
        possible_leads = []
        possible_leads.append(self._get_lead_adj_triples(game_state))
        possible_leads.append(self._get_lead_straight(2, game_state))
        possible_leads.append(self._get_lead_straight(1, game_state))
        possible_leads.append(self._get_lead_triple(game_state))
        possible_leads.append(self._get_lead_basic(2, game_state))
        possible_leads.append(self._get_lead_basic(1, game_state))
        possible_leads.append(self._get_lead_wild(game_state))
        possible_leads = list(filter(lambda play: play != None, possible_leads))
        return possible_leads + [None]

    def _get_lead_play(self, game_state):
        """
        Gets the best play if this player is starting.
        Returns lead play
        """
        return self._get_possible_leads(game_state)[0]

    def _get_lead_basic(self, each_count, game_state):
        return self.hand.get_low(None, each_count)

    def _get_lead_triple(self, game_state):
        for i in [2, 1, 0]:
            next_play = self.hand.get_low(None, 3, i)
            if next_play:
                return next_play
        return None

    def _get_lead_adj_triples(self, game_state):
        for i in [2, 4, 0]:
            next_play = self.hand.get_low_adj_triple(None, i)
            if next_play:
                return next_play
        return None

    def _get_lead_straight(self, each_count, game_state):
        return self.hand.get_low_straight(None, each_count, -1)

    def _get_lead_wild(self, game_state):
        return self.hand.get_low_wild(None)

    def get_play(self, game_state):
        """
        Returns lowest play of play_type
        """
        prev_play = game_state.prev_play
        unrevealed_cards = []
        if not prev_play or prev_play.position == self.position:
            # lead play
            next_play = self._get_lead_play(game_state)
        else:
            next_play = self.hand.get_low_play(prev_play)
            # if next play is none and the player has less than 5 * (number of wilds in hand) cards,
            # play wilds
            if not next_play and game_state.get_player_num_cards(prev_play.position) <= 5 * self.hand.get_num_wild():
                next_play = self.hand.get_low_wild(None)

        if next_play:
            next_play.position = self.position
        return next_play

    def play(self, card_play, display=False):
        self.hand.remove_cards(card_play.cards)
        if display:
            print("{}".format(card_play.play_type))
            for c in card_play.cards:
                print(c, end=" ")
            print()

    def amount(self):
        return self.hand.num_cards()

    def in_game(self):
        return self.amount() > 0
