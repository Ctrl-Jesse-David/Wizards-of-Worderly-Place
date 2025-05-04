import random, time, threading
from termcolor import colored, cprint
from display_manager import display_body, display_border, clear_screen, title_color_changer

"""
ANIMATIONS

----------------------__ADD LATER
"""


def mystical_intro():
    from display_manager import display_body, display_border, clear_screen, title_color_changer
    width = 75
    height = 14
    phrase = "WELCOME TO WIZARDS OF WORDERLY PLACE"
    spaced_phrase = ' '.join(phrase)

    frames = 30
    available_text_colors = [
        "red", "green", 'light_yellow', "blue", "magenta", "cyan", "white",
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

        lines = [''.join(row) for row in grid]
        display_border()
        display_body(lines)
        display_border()

        dots = '.' * ((frame % 4) + 1)
        print('\n' + ' ' * (width // 2 - 10) + f'Enchanting the Grid{dots}')
        time.sleep(0.08)

    stop_animation = threading.Event()

    def animate():
        while not stop_animation.is_set():
            clear_screen()
            display_border()

            lines = [' ' * width for _ in range(center_y)]
            colorful_title = ''.join(
                colored(ch, random.choice(available_text_colors), attrs=['bold']) for ch in spaced_phrase
            )
            lines.append(colorful_title)
            lines.extend([' ' * width for _ in range(height - center_y - 1)])

            display_body(lines)
            display_border()

            print('\n' + ' ' * (width // 2 - 13) + "Press Enter to begin...")
            time.sleep(0.08)

    animation_thread = threading.Thread(target=animate)
    animation_thread.start()

    input()

    stop_animation.set()
    animation_thread.join()

def mystical_loading(message, final_message, color, bg_color):
    message = ' '.join(i for i in message)
    width = 75
    height = 7
    bg_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    available_text_colors = [
        "red", "green", 'light_yellow', "blue", "magenta", "cyan",
        "light_red", "light_green", "light_yellow", "light_blue",
        "light_magenta", "light_cyan"
    ]
    center_y = height // 2

    for i in range(1, len(message) + 1):
        current_message = message[:i]
        center_x = width // 2 - len(current_message) // 2

        clear_screen()
        grid = [[' ' for _ in range(width)] for _ in range(height)]

        for r in range(height):
            for c in range(width):
                if random.random() < 0.03:
                    grid[r][c] = random.choice(bg_charset)

        for j, char in enumerate(current_message):
            if 0 <= center_x + j < width:
                grid[center_y][center_x + j] = colored(char, random.choice(available_text_colors), attrs=['bold'])

        lines = [''.join(row) for row in grid]

        display_border()
        display_body(lines)
        display_border()
        print('')
        time.sleep(0.055)
    
    if not final_message:
        return
    else:
        final_message =  colored(' '.join(i for i in final_message), color, attrs=['bold'])
        clear_screen()
        display_border(bg_color)
        display_body(['', '', '', final_message, '', '', '',], color, bg_color)
        display_border(bg_color)
        print('')
        time.sleep(0.8)
