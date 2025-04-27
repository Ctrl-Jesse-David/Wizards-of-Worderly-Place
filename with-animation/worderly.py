import sys, os, time
from termcolor import colored, cprint
from display_manager import clear_screen, get_player_input
from game_master import start_game_session
from menu_display import display_instructions, display_leaderboard, display_main_menu
from animations import mystical_intro

def main():
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
    - E: Exit the application
    '''

    while True:
        display_main_menu()

        choice = get_player_input()

        if choice == "S":
            start_game_session(dictionary_file)
        elif choice == "I":
            display_instructions()
        elif choice == "L":
            display_leaderboard()
        elif choice == "E":
            print("Exiting...")
            time.sleep(0.8)

            cprint("Thanks for playing!\n", 'red', attrs = ["bold"])
            sys.exit()

        else:
            print("Invalid Choice. Please try again!")
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