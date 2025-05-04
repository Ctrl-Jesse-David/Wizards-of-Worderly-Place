import sys, os, time
from termcolor import cprint
from display_manager import clear_screen
from game_master import start_game_session
from menu_display import display_instructions, display_leaderboard, display_main_menu
from animations import mystical_intro, mystical_loading
from user_progress import display_shop, display_user_profile, login_user
from word_utils import get_player_nickname, get_player_input

"""
WORDERLY

--------------------ADD LATER
"""

def main():
    '''
    Entry point of the Wizards of Worderly Place game.
    
    This function handles command-line arguments and initializes the game:
    - If no arguments are provided, starts the game with default dictionary
    - If one argument is provided, validates it as a dictionary file
    - Raises errors for invalid arguments or non-existent files
    '''
    
    if len(sys.argv) >= 3:
        raise IndexError('Provide only one filename.')
    
    elif len(sys.argv) == 2:
        filename = sys.argv[1]

        if not os.path.isfile(filename):
            raise FileNotFoundError('File does not exist.')
        
        else:
            main_game_loop(filename)
    else:
        main_game_loop()

def main_game_loop(dictionary_file='corncob-lowercase.txt'):
    '''
    Manages the main menu flow and user interaction.
    
    This function implements the main control loop for the game menu,
    handling user input and directing program flow to the appropriate   
    functions based on user selection. It continues running until the
    player chooses to exit the game.
    
    Options:
    - S: Start a new game (prompts for the player's nickname)
    - I: Display game instructions
    - L: Display leaderboard
    - P: Display user profile
    - M: Display magical shop
    - E: Exit the application
    '''

    mystical_intro()

    nickname = get_player_nickname()
    login_user(nickname)
    
    while True:

        display_main_menu()
        choice = get_player_input()

        if choice == "S":
            start_game_session(dictionary_file, nickname)
        elif choice == "I":
            display_instructions()
        elif choice == "L":
            display_leaderboard()
        elif choice == "P":
            display_user_profile()
        elif choice == "M":
            display_shop()  
        elif choice == "E":
            mystical_loading('CLOSING THE PORTAL...', 'SAFE TRAVELS, SORCERER!', "red", 'on_red')
            sys.exit()

        else:
            display_main_menu(text_bg='on_red')
            cprint("🚫 Invalid Choice. Please try again!", 'red', attrs=["bold"])
            time.sleep(0.35)
            clear_screen()


if __name__ == "__main__":
    '''
    Entry point of the program.
    '''
    try:
        main()

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)