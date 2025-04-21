
# def mystical_intro():
#     width = 75
#     height = 20
#     bg_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ    "
#     top_phrase = "WELCOME TO"
#     bottom_phrase = "WIZARDS OF WORDERLY PLACE"
#     center_top = width // 2 - len(top_phrase) // 2
#     center_bottom = width // 2 - len(bottom_phrase) // 2
#     center_y_top = height // 2 - 2
#     center_y_bottom = height // 2
#     frames = 40

#     for frame in range(frames):
#         clear_screen()
#         grid = [[' ' for _ in range(width)] for _ in range(height)]

#         # ✨ Floating magical letters
#         for r in range(height):
#             for c in range(width):
#                 if random.random() < 0.02:
#                     char = random.choice(bg_charset)
#                     grid[r][c] = colored(char, random.choice(['cyan', 'green', 'magenta']))

#         # ✨ Gradually reveal welcome message
#         fade_top = int(len(top_phrase) * frame / frames)
#         fade_bottom = int(len(bottom_phrase) * frame / frames)

#         for i in range(fade_top):
#             grid[center_y_top][center_top + i] = colored(top_phrase[i], 'yellow', attrs=['bold'])
#         for i in range(fade_bottom):
#             grid[center_y_bottom][center_bottom + i] = colored(bottom_phrase[i], 'yellow', attrs=['bold'])

#         # 🧙‍♂️ Print the magical grid
#         for row in grid:
#             print(''.join(row))

#         # 🌀 Loading text with emoji
#         dots = '.' * ((frame % 4) + 1)
#         loading_msg = f"🪄 Summoning Word Magic{dots}"
#         print('\n' + colored(loading_msg.center(width), 'white', 'on_blue'))
#         time.sleep(0.07)

#     # 🏁 Final reveal
#     clear_screen()
#     print("\n" * (center_y_top - 3))
#     print(colored("~" * width, 'blue'))
#     print(colored(top_phrase.center(width), 'cyan', attrs=['bold']))
#     print(colored(bottom_phrase.center(width), 'magenta', attrs=['bold']))
#     print(colored("~" * width, 'blue'))
#     print("\n" * 2)
#     print(colored("Press any key to begin...".center(width), 'yellow'))
#     time.sleep(2)
