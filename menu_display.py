from display_manager import display_header, clear_screen, display_body, display_border, title_color_changer
from termcolor import cprint, colored
from animations import mystical_intro
from word_utils import get_player_input

'''
Menu Display

This module handles the game's menu options and player interactions for Wizards of Worderly Place.
It manages game sessions, displays instructions, and maintains the leaderboard system.
'''

def display_main_menu(text_color="white", text_bg="on_white"):
    
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
    "📖  " + colored("[S]", 'light_cyan', attrs=["bold"]) + "  Start Game    📖",
    "📜  " + colored("[I]", 'light_green', attrs=["bold"]) + "  Instructions  📜",
    "🏆  " + colored("[L]", 'light_yellow', attrs=["bold"]) + "  Leaderboards  🏆",
    "🧙  " + colored("[P]", "light_blue", attrs=["bold"]) + "  Soul Crystal  🧙",
    "🛒  " + colored("[M]", "light_magenta", attrs=["bold"]) + "  Mystic Market 🛒",
    "🚪  " + colored("[E]", 'light_red', attrs=["bold"]) + "  Exit Game     🚪"
    ]

    footer = [
        "-" * 75,
        "", 
        "Please enter a choice and press Enter.",
        "" 
    ]

    clear_screen()
    
    display_border(text_bg)

    display_body(title, text_color, text_bg)
    display_body(subtitle, text_color, text_bg)
    display_body(menu_options, text_color, text_bg)
    display_body(footer, text_color, text_bg)

    display_border(text_bg)

    print("\n")


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
    colored("🕹️ How to Play:", "light_red", attrs=["bold"]),
    "  Form words using the given letters to solve the puzzle.",
    "  Type the words and press Enter to submit your answer.",
    "-" * 75,
    colored("✨ Game Rules:", "light_red", attrs=["bold"]),
    "  🏆 Find all possible words to complete the level.",
    "  🚫 Invalid words or repeated words will not be accepted.",
    "  💀 Choose your words wisely! You have limited lives.",
    "-" * 75,
    colored("🔮 Power-ups & Hints:", "light_red", attrs=["bold"]),
    "  ✨ Shuffle - Rearranges the given letters.",
    "  🔍 Hint - Reveals one letter in a hidden word.",
    "  🔵 Extra Life - Given if you find a valid word not in the grid.",
    "-" * 75,
    " ",
    colored("Press Enter to return to the main menu.", attrs=["bold"]),
    " ",
]
    clear_screen()
    display_border("on_light_red")
    display_body(instructions, "white", "on_light_red")
    display_border("on_light_red")
    print("")
    input()
    clear_screen()
def display_leaderboard():
    '''
    Displays the top 8 player scores from the leaderboard with left-aligned text.
    '''
    try:
        with open("leaderboard.txt", "r") as file:
            scores = sorted((line.strip().split(": ") for line in file), 
                        key=lambda x: int(x[1]), reverse=True)[:8]
        
        leaderboard_lines = [
            " ",
            colored("🏆 THE CELESTIAL SCROLL OF CHAMPIONS 🏆", attrs=["bold"]),
            " ",
            colored('═'*75, 'light_yellow'),
            " "
        ]
        
        if scores:
            # Find longest name for consistent padding
            max_name_len = max(len(name) for name, _ in scores)
            
            for rank, (name, score) in enumerate(scores, start=1):
                # Left-align names and scores with consistent padding
                entry = f"{rank}. {name.ljust(max_name_len)} - {score}"
                leaderboard_lines.append(colored(entry, "white"))
        else:
            leaderboard_lines.append(colored("No scores yet! Play to be the first on the leaderboard!", "white"))
        
        leaderboard_lines.extend([
            " ",  # Empty line after scores
            colored('─'*75, 'light_yellow'),
            " ",
            colored("Press Enter to return to the main menu.", attrs=["bold"]),
            " "
        ])
        
        clear_screen()
        display_border("on_light_yellow")
        display_body(leaderboard_lines, 'light_yellow', "on_light_yellow")
        display_border("on_light_yellow")
        print("")
        input()
        
    except FileNotFoundError:
        error_lines = [
            " ",
            colored("🏆 THE CELESTIAL SCROLL OF CHAMPIONS 🏆", "light_yellow", attrs=["bold"]),
            " ",
            colored('═'*75, 'light_yellow'),
            colored("No leaderboard found.", "white"),
            colored("Play the game to create one!", "white"),
            colored('─'*75, 'light_yellow'),
            " ",
            colored("Press Enter to return to the main menu.", attrs=["bold"]),
            " "
        ]
        clear_screen()
        display_border("on_light_yellow")
        display_body(error_lines, "light_yellow", "on_light_yellow")
        display_border("on_light_yellow")
        
        input()


if __name__ == '__main__':
    display_leaderboard()
