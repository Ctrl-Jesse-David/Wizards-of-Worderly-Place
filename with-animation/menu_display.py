from display_manager import display_header, clear_screen, display_body, get_player_input, display_border, title_color_changer
from termcolor import cprint, colored
from animations import mystical_intro

'''
Options

This module handles the game's menu options and player interactions for Wizards of Worderly Place.
It manages game sessions, displays instructions, and maintains the leaderboard system.
'''

def display_main_menu():
    
    title = [
        "",
        title_color_changer("🧙 Wizards of Worderly Place! 🧙".upper()),
        "" 
    ]

    subtitle = [
        "=" * 75,
        "Can you uncover all the hidden words?",
        "Test your wits and master the art of wordplay!",
        "-" * 75
    ]

    menu_options = [
        "📖  " + colored("[S]", 'cyan', attrs=["bold"]) + "  Start Game   📖",
        "📜  " + colored("[I]", 'green', attrs=["bold"]) + "  Instructions 📜",
        "🏆  " + colored("[L]", 'yellow', attrs=["bold"]) + "  Leaderboards 🏆",
        "🚪  " + colored("[E]", 'red', attrs=["bold"]) + "  Exit Game    🚪"
    ]

    footer = [
        "-" * 75,
        "", 
        "Please enter a choice and press Enter.",
        "" 
    ]

    clear_screen()
    
    display_border("on_white")

    display_body(title, 'blue', 'on_white')
    display_body(subtitle, 'white', 'on_white')
    display_body(menu_options, 'white', 'on_white')
    display_body(footer, 'white', 'on_white')

    display_border("on_white")

    print("\n")

    choice = get_player_input()
    return choice


def display_instructions():
    '''
    Displays the game instructions and rules to the player.

    This function shows a formatted display of how to play the game,
    including game rules and available power-ups/hints. 
    '''

    instructions = [
    " ",
    colored("📜 GAME INSTRUCTIONS 📜", attrs=["bold"]),
    " ",
    '='*75,
    colored("🕹️  How to Play:", "light_red", attrs=["bold"]),
    "  Form words using the given letters to solve the puzzle.",
    "  Type the words and press Enter to submit your answer.",
    "-" * 75,
    colored("✨ Game Rules:", "light_red", attrs=["bold"]),
    "  🏆 Find all possible words to complete the level.",
    "  🚫 Invalid words or repeated words will not be accepted.",
    "  💀 Choose your words wisely! You have limited lives.",
    "-" * 75,
    colored("🔮 Power-ups & Hints:", "light_red", attrs=["bold"]),
    "  🪄 Shuffle - Rearranges the given letters.",
    "  🔍 Hint - Reveals one letter in a hidden word.",
    "  🔵 Extra Life - Given if you find a valid word not in the grid.",
    "-" * 75,
    " ",
    colored("Press Enter to return to the main menu.", attrs=["bold"]),
    " ",
]
    clear_screen()
    display_border("on_red")
    display_body(instructions, "white", "on_red")
    display_border("on_red")
    input()
    clear_screen()


def display_leaderboard():
    '''
    Displays the top 8 player scores from the leaderboard.

    This function reads player scores from 'leaderboard.txt', sorts them
    in descending order, and displays the top scores.
    '''

    display_header(
        title="🏆 LEADERBOARD 🏆",
        color="yellow"
    )
    try:
        with open("leaderboard.txt", "r") as file:
            scores = sorted((line.strip().split(": ") for line in file), 
                            key=lambda x: int(x[1]), reverse=True)[:8]
        if scores:
            for rank, (name, score) in enumerate(scores, start=1):
                print(f"{rank}. {name} - {score}")
        else:
            print("No scores yet! Play to be the first on the leaderboard!")

    except FileNotFoundError:
        print("No leaderboard found. Play the game to create one!")

    print("-"*75)
    input(colored("Press Enter to return to the main menu.", 'yellow', attrs=["bold"]))

if __name__ == '__main__':
    display_main_menu()