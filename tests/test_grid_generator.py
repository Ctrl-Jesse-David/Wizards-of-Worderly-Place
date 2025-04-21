from grid_generator import generate_word_grid, generate_positions_dict
import pytest
import random

def test_generate_positions_dict():
    '''
    Tests the position dictionary generation.
    '''
    #Horizontal Word
    words = [("CAT", (0,0), 'h')]  #word, starting coordinates, direction
    result = generate_positions_dict(words)
    
    #Check if word in dict
    assert "CAT" in result
    
    #Check if positions are correct for hori word
    positions = result["CAT"]
    assert positions[0] == (0, 0) 
    assert positions[1] == (0, 1)  
    assert positions[2] == (0, 2)  
    
    #Vertical Word
    words = [("DOG", (0,0), 'v')]
    result = generate_positions_dict(words)
    assert "DOG" in result
    positions = result["DOG"]
    assert positions[0] == (0, 0)
    assert positions[1] == (1, 0)
    assert positions[2] == (2, 0)
    
    #Main Diagonal Word
    words = [("PYTHON", (2,7), 'd')]
    result = generate_positions_dict(words)
    assert "PYTHON" in result
    positions = result["PYTHON"]
    assert len(positions) == 6
    assert positions[0] == (2, 7)  #Starting pos
    assert positions[1] == (4, 9)
    assert positions[2] == (6, 11)
    assert positions[3] == (8, 13)
    assert positions[4] == (10, 15)
    assert positions[5] == (12, 17)

def test_generate_word_grid():
    '''
    Tests the word grid generation.
    '''
    #Generate grid
    grid_data, placed_words, non_placed_words = generate_word_grid()
    
    #Check grid_data is a 2D list
    assert isinstance(grid_data, list)
    assert all(isinstance(row, list) for row in grid_data)
    
    #Check grid dimensions
    assert len(grid_data) == 15 
    assert all(len(row) == 25 for row in grid_data)  
    
    #Check placed_words structure
    assert isinstance(placed_words, list)
    for word_info in placed_words:
        #(word, coords, direction)
        assert isinstance(word_info, tuple)
        assert len(word_info) == 3
        word, coords, direction = word_info

        #if str
        assert isinstance(word, str)
        
        #if coords are valid
        assert isinstance(coords, tuple)
        assert len(coords) == 2
        row, col = coords
        assert 0 <= row < 15
        assert 0 <= col < 25
        
        #if directions are valid
        assert direction in ['h', 'v', 'd']
    
    #Checks unplaced words
    assert isinstance(non_placed_words, list)
    assert all(isinstance(word, str) for word in non_placed_words)
import pytest
from grid_generator import generate_word_grid, generate_positions_dict

def test_word_placement():
    grid, placed_words, _ = generate_word_grid()
    positions = generate_positions_dict(placed_words)

    used_positions = {}

    for word, coords, direction in placed_words:
        word = word.upper()
        if direction == 'h':
            row, col = coords
            for i in range(len(word)):
                r, c = row, col + i
                letter = word[i]
                if (r, c) in used_positions:
                    assert used_positions[(r, c)] == letter, (
                        f"Conflict at {r, c}: '{used_positions[(r, c)]}' vs '{letter}' in word '{word}'"
                    )
                else:
                    used_positions[(r, c)] = letter

        elif direction == 'v':
            row, col = coords
            for i in range(len(word)):
                r, c = row + i, col
                letter = word[i]
                if (r, c) in used_positions:
                    assert used_positions[(r, c)] == letter, (
                        f"Conflict at {r, c}: '{used_positions[(r, c)]}' vs '{letter}' in word '{word}'"
                    )
                else:
                    used_positions[(r, c)] = letter

        elif direction == 'd' and coords == (2, 7):
            for i in range(len(word)):
                r, c = 2 + i * 2, 7 + i * 2
                letter = word[i]
                if (r, c) in used_positions:
                    assert used_positions[(r, c)] == letter, (
                        f"Conflict at {r, c}: '{used_positions[(r, c)]}' vs '{letter}' in word '{word}' (main diagonal)"
                    )
                else:
                    used_positions[(r, c)] = letter

        else:
            raise AssertionError(f"Invalid direction '{direction}' or unexpected diagonal at {coords} for word '{word}'")
