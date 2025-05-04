import os, random, re, time, subprocess, sys
from termcolor import colored, cprint
from termcolor import colored

"""
DISPLAY MANAGER

----------------ADD LATER
"""


def display_top(main_text):
    return [
            "",
            main_text,
            ""
        ]
    
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])'
                         )
def visible_length(text):
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
    if sys.stdout.isatty():
        clear_cmd = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run([clear_cmd])

def display_border(background_color="on_white"):
    cprint(' ' * 77, on_color=background_color)

def display_row(text, text_color="white", background_color="on_white"):
    cprint(' ', text_color, background_color, end='')
    print(smart_center(text, 75), end='')
    cprint(' ', text_color, background_color)

def display_body(lines, text_color="white", bg_color="on_white"):
    for line in lines:
        display_row(line, text_color, bg_color)

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


def display_header(title, color):
    clear_screen()
    print("="*75)
    cprint(title.center(75), color, attrs=["bold"])
    print("="*75)


def color_dots_in_grid(grid):
    return [[colored(char, 'dark_grey') if char == '.' else char for char in row]
        for row in grid]


def welcome_display(message, nickname, on_color):
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
    clear_screen()
    max_visible_length = 17

    options = [
        '',
        colored("💡 Select a difficulty based on your preferred word count. 💡", attrs=["bold"]),
        '',
        '='*75,
        '',
        format_difficulty('✨', 'APPRENTICE', '[1]', 'light_green', '21 - 25 words', max_visible_length),
        format_difficulty('🔮', ' MAGE', '[2]', 'light_blue', '26 - 30 words', max_visible_length),
        format_difficulty('🧙', ' ARCHMAGE', '[3]', "light_magenta", '31+ words     ', max_visible_length),
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

def format_difficulty(icon, label, tag, color, right_text, target_width):
    raw_label = f"{icon} {tag} {label}"
    vis_len = visible_length(raw_label)
    padding = ' ' * (target_width - vis_len)
    colored_label = colored(raw_label + padding, color, attrs=['bold'])
    return f"{colored_label}: {right_text}"


