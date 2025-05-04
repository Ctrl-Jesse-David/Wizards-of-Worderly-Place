import random
from termcolor import colored
from display_manager import display_body, display_border, clear_screen, ansi_escape

def is_valid(guess, letters):
    guess_cap = guess.upper()
    letters_cap = letters.upper()
    return all(guess_cap.count(letter) <= letters_cap.count(letter) 
        for letter in guess_cap)

def get_player_nickname():
    clear_screen()
    """Get nickname with colorful header (no animation)"""
    colors = ['light_red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
    
    message = "👤 ENTER YOUR USERNAME 👤"
    colored_chars = [colored(char, random.choice(colors), attrs=['bold']) for char in message]
    colorful_message = ' '.join(colored_chars)
    
    display_border('on_white')
    display_body(['', colorful_message, ''], 'white', 'on_white')
    display_border('on_white')
    
    nickname = input(colored("\n👉 Your username: ", "white", attrs=["bold"])).strip().upper()
    return nickname if nickname else 'PLAYER'


def get_player_input():
    return input(colored("👉 Your choice: ", "white", attrs=["bold"])).strip().upper()

def get_wrapped_words(label, word_list, width=73):
        words = sorted(word_list)
        prefix_visible_len = len(ansi_escape.sub('', f"{label}: "))
        prefix = f"{label}: "
        lines = []
        line = prefix
        for word in words:
            word_str = f"{word}, "
            if len(ansi_escape.sub('', line)) + len(word_str.rstrip()) > width:
                lines.append(line.rstrip(', '))
                line = " " * prefix_visible_len + word_str
            else:
                line += word_str
        if line.strip():
            lines.append(line.rstrip(', '))

        max_length = max(len(ansi_escape.sub('', l)) for l in lines)

        padded_lines = []
        for l in lines:
            visible_len = len(ansi_escape.sub('', l))
            padding = max_length - visible_len
            padded_lines.append(l + ' ' * padding)
        
        return padded_lines