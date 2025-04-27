
import os
from termcolor import cprint, colored

def reveal_word(display_grid, word, positions):
    if word in positions:
        for i, (r, c) in enumerate(positions[word]):
            display_grid[r][c] = word[i]
    return display_grid


def clear_screen():
    return os.system('cls' if os.name == 'nt' else 'clear')

def display_header(title, color):
    clear_screen()
    print("="*75)
    cprint(title.center(75), color, attrs=["bold"])
    print("="*75)

def display_footer(text):
    print("-" * 75)
    print(text.center(75))
    print("=" * 75)

def get_player_nickname():
    '''
    Prompts for and validates player nickname.
    '''
    nickname = input("👤 Enter your nickname: ").strip()
    if nickname:
        return nickname
    return 'player'

def get_player_input():
    return input(colored("Select an option: ", "light_blue", attrs=["bold"])).strip().upper()


# def convert_grid_to_display(grid):
#     return [['#' if cell != '.' else '.' for cell in row] for row in grid]

# def reveal_word(display_grid, word, positions):
#     if word in positions:
#         for i, (r, c) in enumerate(positions[word]):
#             display_grid[r][c] = word[i]
#     return display_grid
