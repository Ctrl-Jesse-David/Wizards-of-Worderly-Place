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

def test_word_placement():
    '''
    Tests that words are placed correctly on the grid.
    '''
    grid_data, placed_words, _ = generate_word_grid()

    used_positions = {}
    
    for word, coords, direction in placed_words:
        row, col = coords
        
        #If words fits in grid
        if direction == 'h':
            assert col + len(word) <= 25, f"Word '{word}' exceeds grid bounds"
        elif direction == 'v':
            assert row + len(word) <= 15, f"Word '{word}' exceeds grid bounds."
        else:  #DIAGONAL
            if coords == (2, 7): 
                assert row + (len(word) - 1) * 2 <= 15 and col + (len(word) - 1) * 2 <= 25, \
                    f"Word '{word}' exceeds grid bounds"
            else:
                assert row + len(word) <= 15 and col + len(word) <= 25, \
                    f"Word '{word}' exceeds grid bounds"
        
        #Get word pos
        word_positions = []
        if direction == 'h':
            word_positions = [(row, col + i) for i in range(len(word))]
        elif direction == 'v':
            word_positions = [(row + i, col) for i in range(len(word))]
        else:  #DIAG
            if coords == (2, 7):  # Special case for main word
                word_positions = [(row + i * 2, col + i * 2) for i in range(len(word))]
            else:
                word_positions = [(row + i, col + i) for i in range(len(word))]
        
        #For Overlaps
        for pos in word_positions:
            if pos in used_positions:
                existing_word = used_positions[pos]
                assert word[pos[0] - row] == existing_word[pos[0] - row], \
                    f"Position {pos} is used by multiple words without valid intersection"
            used_positions[pos] = word