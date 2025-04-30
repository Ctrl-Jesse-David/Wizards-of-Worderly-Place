import os, random, time, threading
from termcolor import colored, cprint

def mystical_intro():
    from display_manager import display_row, display_border, clear_screen
    width = 75
    height = 14
    phrase = "WELCOME TO WIZARDS OF WORDERLY PLACE"
    spaced_phrase = ' '.join(phrase)

    frames = 30
    available_text_colors = [
        "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "light_red", "light_green", "light_yellow", "light_blue",
        "light_magenta", "light_cyan"
    ]

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

        display_border('on_white')
        for row in grid:
            line = ''.join(row)
            display_row(line, 'white', 'on_white')
        display_border('on_white')

        dots = '.' * ((frame % 4) + 1)
        print('\n' + ' ' * (width // 2 - 10) + f'Enchanting the Grid{dots}')
        time.sleep(0.08)

    stop_animation = threading.Event()

    def animate():
        while not stop_animation.is_set():
            clear_screen()

            display_border('on_white')

            empty_lines_before = center_y
            for _ in range(empty_lines_before):
                display_row(' ' * 75, 'white', 'on_white')

            colorful_title = ''.join(
                colored(ch, random.choice(available_text_colors), attrs=['bold']) for ch in spaced_phrase
            )
            display_row(colorful_title, 'white', 'on_white')

            for _ in range(height - empty_lines_before - 1):
                display_row(' ' * 75, 'white', 'on_white')

            display_border('on_white')

            print('\n' + ' ' * (width // 2 - 13) + "Press Enter to begin...")

            time.sleep(0.08)

    animation_thread = threading.Thread(target=animate)
    animation_thread.start()

    input()

    stop_animation.set()
    animation_thread.join()

    return

if __name__ == "__main__":
    mystical_intro()
