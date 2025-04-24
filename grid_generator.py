import random, sys
from utilities import is_valid

def get_main_and_valid_words(file_path):
    def read_words():
        try:
            with open(file_path) as f:
                return [line.strip() for line in f]
        except FileNotFoundError:
            print(f"Error: Dictionary file '{file_path}' not found!")
            sys.exit(1)

    words = read_words()
    six_letter_words = [w for w in words if len(w) == 6]
    if not six_letter_words:
        return None

    main_word = random.choice(six_letter_words)
    valid_words = [w for w in words if 3 <= len(w) <= 6 and w != main_word and is_valid(w, main_word)]

    return (main_word, valid_words) if len(valid_words) >= 20 else get_main_and_valid_words(file_path)

def place_main_diagonal(word, grid):
    for i, letter in enumerate(word.upper()):
        grid[2 + i*2][7 + i*2] = letter
    return grid

def find_intersections(word, grid):
    intersections = []
    for i, letter in enumerate(word):
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == letter:
                    start_c = c - i
                    if 0 <= start_c and start_c + len(word) <= len(grid[0]):
                        if all(grid[r][start_c + j] in ('.', word[j]) for j in range(len(word))):
                            intersections.append((r, start_c, 'h'))
                    start_r = r - i
                    if 0 <= start_r and start_r + len(word) <= len(grid):
                        if all(grid[start_r + j][c] in ('.', word[j]) for j in range(len(word))):
                            intersections.append((start_r, c, 'v'))
    return intersections

def place_word_on_grid(word, row, col, direction, grid):
    for i, letter in enumerate(word):
        r = row + (i if direction == 'v' else 0)
        c = col + (i if direction == 'h' else 0)
        grid[r][c] = letter

def is_valid_placement(word, row, col, direction, grid):
    rows, cols = len(grid), len(grid[0])
    for i, letter in enumerate(word):
        r, c = row + (i if direction == 'v' else 0), col + (i if direction == 'h' else 0)
        if not (0 <= r < rows and 0 <= c < cols):
            return False
        cell = grid[r][c]
        if cell != '.' and cell != letter:
            return False
        if cell == '.':
            adjacents = []
            if direction == 'h':
                if r > 0: 
                    adjacents.append(grid[r-1][c])
                if r < rows - 1: 
                    adjacents.append(grid[r+1][c])
            else:
                if c > 0: 
                    adjacents.append(grid[r][c-1])
                if c < cols - 1: 
                    adjacents.append(grid[r][c+1])
            if any(a != '.' for a in adjacents):
                return False

    pre_r, pre_c = row - (direction == 'v'), col - (direction == 'h')
    post_r, post_c = row + (direction == 'v') * len(word), col + (direction == 'h') * len(word)
    if 0 <= pre_r < rows and 0 <= pre_c < cols and grid[pre_r][pre_c] != '.':
        return False
    if 0 <= post_r < rows and 0 <= post_c < cols and grid[post_r][post_c] != '.':
        return False

    return True

def place_word(word, grid):
    intersections = find_intersections(word, grid)
    random.shuffle(intersections)

    for row, col, direction in intersections:
        if is_valid_placement(word, row, col, direction, grid):
            place_word_on_grid(word, row, col, direction, grid)
            return True, (row, col, direction)

    return False, None

def generate_word_grid(dictionary_file):
    main_word, valid_words = get_main_and_valid_words(dictionary_file)

    while True:
        grid = [['.' for _ in range(25)] for _ in range(15)]
        placed_words = [(main_word.upper(), (2, 7), 'd')]
        non_placed_words = []
        place_main_diagonal(main_word, grid)

        for word in sorted(valid_words, key=len, reverse=True):
            word = word.upper()
            success, placement = place_word(word, grid)
            if success:
                placed_words.append((word, placement[:2], placement[2]))
            else:
                non_placed_words.append(word)

        if len(placed_words) - 1 >= 20 and main_has_adjacent_letter(grid):
            return grid, placed_words, non_placed_words
        continue
        
def main_has_adjacent_letter(grid):
    coords = [(2 + i*2, 7 + i*2) for i in range(6)]
    for r, c in coords:
        has_neighbor = False
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != '.':
                has_neighbor = True
                break
        if not has_neighbor:
            return False
    return True

def generate_positions_dict(placed_words):
    positions = {}
    for word, coords, direction in placed_words:
        if coords == (2, 7):
            r, c = coords
            positions[word] = [(r + i*2, c + i*2) for i in range(6)]
        elif direction == 'h':
            positions[word] = [(coords[0], coords[1] + i) for i in range(len(word))]
        elif direction == 'v':
            positions[word] = [(coords[0] + i, coords[1]) for i in range(len(word))]
    return positions

def convert_grid_to_display(grid):
    return [['#' if cell != '.' else '.' for cell in row] for row in grid]

def reveal_word(display_grid, word, positions):
    if word in positions:
        for i, (r, c) in enumerate(positions[word]):
            display_grid[r][c] = word[i]
    return display_grid


if __name__ == '__main__':
    grid, placed_words, non = generate_word_grid('corncob-lowercase.txt')

    print("\nGrid:")
    for row in grid:
        print('  '.join(row))

    print("\nPlaced Words (Total: {}):".format(len(placed_words)))
    for word, coords, direction in placed_words:
        print(word, coords, direction)