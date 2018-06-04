from player import Player
from game_state import leftover

position = int(input("Enter position relative to King: "))
t = int(input("Enter player type (0: peasant, 1: king): "))

computer = Player(leftover, position, t)