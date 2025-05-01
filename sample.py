
def place_word_on_grid(word, row, col, direction, grid):
    color_choices = ["red", "green", "yellow", "blue", "magenta", "cyan"]
    color = random.choice(color_choices)
    for i, letter in enumerate(word):
        r = row + (i if direction == 'v' else 0)
        c = col + (i if direction == 'h' else 0)
        grid[r][c] = colored(letter, color, attrs=["bold"])

def generate_positions_dict(placed_words):
    positions = {}
    for word, coords, direction in placed_words:
        r, c = coords
        if direction == 'd':
            positions[word] = [(r + i*2, c + i*2) for i in range(6)]
        elif direction == 'h':
            positions[word] = [(r, c + i) for i in range(len(word))]
        elif direction == 'v':
            positions[word] = [(r + i, c) for i in range(len(word))]
    return positions