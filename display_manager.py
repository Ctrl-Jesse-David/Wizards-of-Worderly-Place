from termcolor import colored, cprint
import os, random, re, time
from termcolor import colored

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
    os.system('cls' if os.name == 'nt' else 'clear')

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

