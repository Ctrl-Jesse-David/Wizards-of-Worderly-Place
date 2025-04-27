from termcolor import colored, cprint
from animations import mystical_intro
import os, random
import re

def get_player_nickname():
    nickname = input("👤 Enter your nickname: ").strip()
    if nickname:
        return nickname
    return 'player'

def display_header(title, color):
    clear_screen()
    print("="*75)
    cprint(title.center(75), color, attrs=["bold"])
    print("="*75)

ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def visible_length(text):
    clean_text = ansi_escape.sub('', text)
    length = 0
    for char in clean_text:
        if char in "🧙📖📜🏆🚪👉🕹️✨🏆🚫💀🔮🪄🔍🔵":
            length += 2
        else:
            length += 1
    return length

def smart_center(text, width):
    vis_len = visible_length(text)
    total_padding = max(width - vis_len, 0)
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    return ' ' * left_padding + text + ' ' * right_padding

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_border(background_color):
    cprint(' ' * 77, on_color=background_color)

def display_row(text, text_color, background_color):
    cprint(' ', text_color, background_color, end='')
    print(smart_center(text, 75), end='')
    cprint(' ', text_color, background_color)

def display_body(lines, text_color, bg_color):
    for line in lines:
        display_row(line, text_color, bg_color)

def get_player_input():
    return input(colored("👉 Your choice: ", "cyan", attrs=["bold"])).strip().upper()

def title_color_changer(text):
    available_text_colors = [
        "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "light_red", "light_green", "light_yellow", "light_blue",
        "light_magenta", "light_cyan"
    ]
    stack = []
    for i in text:
        stack.append(colored(i, random.choice(available_text_colors), attrs=["bold"]))
    return " ".join(stack)



# def convert_grid_to_display(grid):
#     return [['#' if cell != '.' else '.' for cell in row] for row in grid]

# def reveal_word(display_grid, word, positions):
#     if word in positions:
#         for i, (r, c) in enumerate(positions[word]):
#             display_grid[r][c] = word[i]
#     return display_grid
