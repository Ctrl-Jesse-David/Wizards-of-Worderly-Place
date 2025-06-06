import os, random, re, time
from termcolor import colored, cprint
from termcolor import colored

'''
Display Manager
- This module provides reusable terminal formatting functions for the game. 
It includes functions for screen layout, centered and colored text formatting 
with grids and borders, decorative display animations, and user interface components 
like welcome messages and difficulty selection menus. These functions help maintain 
a consistent visual theme throughout the game's terminal interface.
'''

def display_top(main_text):
    '''
    Used for consistent vertical spacing in screen layouts.
    '''
    return [
            "",
            main_text,
            ""
        ]
    
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
                         )
def visible_length(text):
    '''
    Calculates the visual length of a string, excluding ANSI color codes
    and accounting for emojis and wide Unicode characters that helps center 
    content correctly in the terminal.
    '''
    clean_text = ansi_escape.sub('', text)
    length = 0
    for char in clean_text:
        if char in ["🕹", "✨", "🪄"]:
            length += 1
        elif ord(char) > 0xffff:
            length += 2
        else:
            length += 1
    return length

def smart_center(text, width):
    '''
    Centers text based on visible length.
    Adjusts padding for emojis, which may affect width rendering.
    Ensures clean and aligned display for colored/emojified text.
    '''
    vis_len = visible_length(text)
    total_padding = width - vis_len
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    
    clean_text = ansi_escape.sub('', text)
    
    if "🕹" in clean_text:
        left_padding += 1
    elif "✨" in clean_text:
        left_padding -= 1
    
    return (' ' * max(left_padding, 0)) + text + (' ' * max(right_padding, 0))

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_border(background_color="on_white"):
    '''
    Displays a solid horizontal border bar using the specified background color.
    Used for framing of content.
    '''
    cprint(' ' * 77, on_color=background_color)

def display_row(text, text_color="white", background_color="on_white"):
    '''
    Prints a single line of centered text, surrounded by a space on each side,
    and enclosed with specified foreground and background colors.
    '''
    cprint(' ', text_color, background_color, end='')
    print(smart_center(text, 75), end='')
    cprint(' ', text_color, background_color)

def display_body(lines, text_color="white", bg_color="on_white"):
    for line in lines:
        display_row(line, text_color, bg_color)

def title_color_changer(text):
    '''
    Randomly assigns vibrant colors to each character in the input text.
    Creates a lively, animated text appearance.
    '''
    available_text_colors = [
        "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "light_red", "light_green", "light_yellow", "light_blue",
        "light_magenta", "light_cyan"
    ]
    stack = []
    for i in text:
        stack.append(colored(i, random.choice(available_text_colors), attrs=["bold"]))
    return " ".join(stack)


def display_header(title, color):
    '''
    Clears the screen and displays a bold, colored title between horizontal lines for 
    major section headers.
    '''
    clear_screen()
    print("="*75)
    cprint(title.center(75), color, attrs=["bold"])
    print("="*75)


def color_dots_in_grid(grid):
    '''
    Re-colors all '.' characters in a given 2D grid to appear in 'dark_grey'.
    '''
    return [[colored(char, 'dark_grey') if char == '.' else char for char in row]
        for row in grid]


def welcome_display(message, nickname, on_color):
    '''
    Display a welcome animation for the player.
    '''
    colorful_nick = title_color_changer(nickname)
    welcome = [
        '',
        message.replace(nickname, colorful_nick),
        ''
    ]

    base_text = colored("   🔮 Summoning Arcane Forces", attrs=['bold'])

    for frame in range(14):
        clear_screen()
        display_border(on_color)
        display_body(welcome, 'white', on_color)
        display_border(on_color)

        dots = '.' * ((frame % 4) + 1)
        animated_line = base_text + dots

        print('\n' * 2 + (animated_line).center(77))
        time.sleep(0.08)

def ask_game_difficulty(on_color="on_white"):
    '''
    Displays the difficulty selection menu:
    - APPRENTICE: 21–25 words
    - MAGE: 26–30 words
    - ARCHMAGE: 31+ words
    Users can select by number or press 'E' to exit.
    '''
    clear_screen()
    max_visible_length = 17

    options = [
    '',
    colored("💡 Select a difficulty based on your preferred word count. 💡", attrs=["bold"]),
    '',
    '='*75,
    '',
    colored('✨ [1] APPRENTICE : 21 - 25 words', 'light_green', attrs=['bold']),
    colored('🔮 [2] MAGE       : 26 - 30 words ', 'light_blue', attrs=['bold']),
    colored('🧙 [3] ARCHMAGE   : 31+ words     ', 'light_magenta', attrs=['bold']),
    '',
    '-'*75,
    '',
    colored(f"Select a difficulty level [{colored('Enter Number', 'light_cyan', attrs=['bold'])}] or "
            f"[{colored('E', 'light_red', attrs=['bold'])}] to exit:", attrs=['bold']),
    ''
]

    
    display_border(on_color)
    display_body(options, 'white', on_color)
    display_border(on_color)
    print('')