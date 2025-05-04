import sys, os, time, argparse
from termcolor import cprint
from display_manager import clear_screen
from game_master import start_game_session
from menu_display import display_instructions, display_leaderboard, display_main_menu
from animations import mystical_intro, mystical_loading
from user_progress import display_shop, display_user_profile, login_user
from word_utils import get_player_nickname, get_player_input


def main():
    '''
    Entry point of the Wizards of Worderly Place game.

    Uses argparse to handle command-line arguments:
    - If a dictionary file is provided, uses it after validating existence
    - If no file is provided, defaults to the built-in dictionary (corncob-lowercase.txt)
    '''

    parser = argparse.ArgumentParser(
        
        description="Wizards of Worderly Place: A word puzzle game."
    )
    parser.add_argument(
        'dictionary_file',
        nargs='?',
        help='Optional path to a custom dictionary file.'
    )

    args = parser.parse_args()

    if args.dictionary_file:
        if not os.path.isfile(args.dictionary_file):
            raise FileNotFoundError(f"File '{args.dictionary_file}' does not exist.")
        main_game_loop(args.dictionary_file)
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
            mystical_loading('UNWEAVING THE ENCHANTMENT...', 'SAFE TRAVELS, SORCERER!', "light_red", 'on_light_red')
            sys.exit()

        else:
            display_main_menu(text_bg='on_light_red')
            cprint("🚫 Invalid Choice. Please try again!", 'light_red', attrs=["bold"])
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