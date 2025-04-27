import os, random, time, sys
from termcolor import colored, cprint

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def mystical_intro():
    width = 75
    height = 12
    phrase = "WELCOME TO WIZARDS OF WORDERLY PLACE"
    spaced_phrase = ' '.join(phrase)

    frames = 30
    available_text_colors = [
        "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "light_red", "light_green", "light_yellow", "light_blue",
        "light_magenta", "light_cyan"
    ]

    # -- First: animated loading screen --
    bg_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    center_x = width // 2 - len(spaced_phrase) // 2
    center_y = height // 2

    for frame in range(frames):
        clear_screen()
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        for r in range(height):
            for c in range(width):
                if random.random() < 0.02:
                    grid[r][c] = random.choice(bg_charset)

        fade_progress = frame / frames
        reveal_len = int(len(spaced_phrase) * fade_progress)
        for i in range(reveal_len):
            grid[center_y][center_x + i] = colored(spaced_phrase[i],
                                                   random.choice(available_text_colors),
                                                   attrs=['bold'])

        # Top border
        cprint(' ' * (width + 2), 'white', 'on_white', end='')
        print()

        # Side borders + grid
        for row in grid:
            cprint(' ', 'white', 'on_white', end='')
            print(''.join(row), end='')
            cprint(' ', 'white', 'on_white')

        # Bottom border
        cprint(' ' * (width + 2), 'white', 'on_white', end='')
        print()

        dots = '.' * ((frame % 4) + 1)
        print('\n' + ' ' * (width // 2 - 10) + f'Enchanting the Grid{dots}')
        time.sleep(0.08)

    # -- Final centered color changing text with white border --
    try:
        import msvcrt
        def key_pressed():
            return msvcrt.kbhit()
    except ImportError:
        import termios, tty, select
        def key_pressed():
            dr, dw, de = select.select([sys.stdin], [], [], 0)
            return dr != []

    while True:
        clear_screen()

        # Top border
        cprint(' ' * (width + 2), 'white', 'on_white', end='')
        print()

        # Empty lines to center the phrase vertically
        empty_lines_before = center_y
        for _ in range(empty_lines_before):
            cprint(' ', 'white', 'on_white', end='')
            print(' ' * width, end='')
            cprint(' ', 'white', 'on_white')
            
        # Line with phrase
        cprint(' ', 'white', 'on_white', end='')
        print(' ' * center_x, end='')  # manually align it
        for ch in spaced_phrase:
            print(colored(ch, random.choice(available_text_colors), attrs=['bold']), end='')
        print(' ' * (width - center_x - len(spaced_phrase)), end='')  # fill remaining space
        cprint(' ', 'white', 'on_white')


        # Empty lines after
        for _ in range(height - empty_lines_before - 1):
            cprint(' ', 'white', 'on_white', end='')
            print(' ' * width, end='')
            cprint(' ', 'white', 'on_white')

        # Bottom border
        cprint(' ' * (width + 2), 'white', 'on_white', end='')
        print()

        # "Press any key"
        print('\n' + ' ' * (width // 2 - 13) + "Press any key to begin...")

        time.sleep(0.08)

        if key_pressed():
            sys.stdin.read(1)
            break

if __name__ == "__main__":
    mystical_intro()
