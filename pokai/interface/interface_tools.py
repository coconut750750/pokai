import os

window_rows, window_columns = os.popen('stty size', 'r').read().split()

def clear_lines(n=1):
    for i in range(n):
        print('\033[A' + (' ' * int(window_columns)) + '\033[A')

def print_break(n=1):
    for i in range(n):
        print("-" * int(window_columns))
