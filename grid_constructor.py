import random
from file_operations import get_main_and_valid_words
from display_manager import color_dots_in_grid

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

def generate_word_grid(dictionary_file, min, max):
    while True:
        main_word, valid_words = get_main_and_valid_words(dictionary_file)
        grid = [[('.') for _ in range(25)] for _ in range(15)]
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

        if min <= len(placed_words) <= max and main_has_adjacent_letter(grid):
            return color_dots_in_grid(grid), placed_words, non_placed_words
        else:
            continue
        
def main_has_adjacent_letter(grid):
    coords = [(2 + i*2, 7 + i*2) for i in range(6)]
    for r, c in coords:
        has_adjacent = any(grid[r + dr][c + dc] != '.' for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)])
        if not has_adjacent:
            return False
    return True


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



if __name__ == '__main__':
    grid, placed_words, non = generate_word_grid('corncob-lowercase.txt', 21, 25)


    print("\nGrid:")
    for row in grid:
        print('  '.join(row))

    print("\nPlaced Words (Total: {}):".format(len(placed_words)))
    for word, coords, direction in placed_words:
        print(word, coords, direction)