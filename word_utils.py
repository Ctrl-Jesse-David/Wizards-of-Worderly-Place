import random
from termcolor import colored
from display_manager import display_body, display_border, clear_screen

def is_valid(guess, letters):
    guess_cap = guess.upper()
    letters_cap = letters.upper()
    return all(guess_cap.count(letter) <= letters_cap.count(letter) 
        for letter in guess_cap)

def get_player_nickname():
    clear_screen()
    """Get nickname with colorful header (no animation)"""
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
    
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

