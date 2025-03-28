from termcolor import cprint, colored
from options import start_game,display_instructions, display_leaderboard, display_header
from utilities import clear_screen
from game_levels import letters, grid, positions
import sys, time

def main_menu():
    while True:
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

        choice = input(colored("Select an option: ", "light_blue", attrs=["bold"])).strip().upper()

        if choice == "S": 
            nickname = input("👤 Enter your nickname: ")
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
    main_menu()
