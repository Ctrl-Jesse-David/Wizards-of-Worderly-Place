from termcolor import cprint, colored
from options import start_game,display_instructions, display_leaderboard, display_header
from utilities import clear_screen
from game_levels import letters, grid, positions
import sys, time

def display_menu():
    '''
    Displays the main menu interface of the game.
    
    This function presents a formatted menu showing the game title
    and available options including starting the game, viewing instructions,
    checking the leaderboard, and exiting the game.
    '''

    display_header(
            title="🧙 Welcome to Wizards of Worderly Place! 🧙",
            color="light_blue"
        )
    print("Can you uncover all the hidden words?".center(75))
    print("Test your wits and master the art of wordplay!".center(75))
    print("-" * 75)

    print((" "*11 + "📖  " + colored("[S]", "light_blue", attrs=["bold"]) + "  Start Game   📖").center(75))
    print((" "*11 + "📜  " + colored("[I]", "light_blue", attrs=["bold"]) + "  Instructions 📜").center(75))
    print((" "*11 + "🏆  " + colored("[L]", "light_blue", attrs=["bold"]) + "  Leaderboards 🏆").center(75))
    print((" "*11 + "🚪  " + colored("[E]", "light_blue", attrs=["bold"]) + "  Exit Game    🚪").center(75))

    print("-" * 75)
    print("Please enter a choice and press Enter.".center(75))
    print("=" * 75)
    

def main_menu():
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
        display_menu()

        choice = input(colored("Select an option: ", "light_blue", attrs=["bold"])).strip().upper()

        if choice == "S": 
            while True:
                nickname = input("👤 Enter your nickname: ").strip()
                if nickname:
                    break
                else:
                    cprint("Input your name!", "red", attrs=["bold"])
                    time.sleep(0.3)
                    clear_screen()
                    display_menu()

            clear_screen()
            start_game(letters, grid, positions, nickname)

        elif choice == "I":
            display_instructions()

        elif choice == "L":
            display_leaderboard()

        elif choice == "E":
            print("Exiting...") # gagawa ako ng animation stuff pero ito muna for the meantime
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

    main_menu()
