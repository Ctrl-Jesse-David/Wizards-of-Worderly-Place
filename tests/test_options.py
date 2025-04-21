from options import start_game, display_instructions, display_leaderboard
import pytest
import os
import tempfile
import builtins

def sample_game_data():
    '''
    Creates sample game data for testing
    '''
    letters = ['C', 'A', 'T', 'D', 'O', 'G']
    grid = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]
    positions = {"CAT": [(0,0), (0,1), (0,2)]}
    non_placed_words = ["ACT", "TAG"]
    return letters, grid, positions, "TestPlayer", non_placed_words

def create_temp_leaderboard():
    '''
    Creates temporary leaderboard file for testing
    '''
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("Player1: 100\n")
        f.write("Player2: 200\n")
        f.write("Player3: 150\n")
        return f.name

def test_start_game_retry_option():
    '''
    Tests game's retry functionality
    '''
    letters, grid, positions, name, non_placed_words = sample_game_data()
    
    #Saves original input
    original_input = builtins.input
    
    try:
        builtins.input = lambda _: 'y'
        result = start_game(letters, grid, positions, name, non_placed_words)
        assert result == 'y'

        builtins.input = lambda _: 'n'
        result = start_game(letters, grid, positions, name, non_placed_words)
        assert result == 'n'
    except Exception as e:
        builtins.input = original_input
        raise e
    else:
        builtins.input = original_input

def test_start_game_invalid_option():
    letters, grid, positions, name, non_placed_words = sample_game_data()
    original_input = builtins.input
    
    try:
        inputs = ['x', 'n']
        builtins.input = lambda _: inputs.pop(0) if inputs else 'n'
        result = start_game(letters, grid, positions, name, non_placed_words)
        assert result == 'n'
    except Exception as e:
        builtins.input = original_input
        raise e
    else:
        builtins.input = original_input
from options import display_leaderboard
from unittest.mock import patch
import builtins
import io
import os

def test_display_leaderboard():
    temp_path = create_temp_leaderboard()

    with open(temp_path, "a") as f:
        f.write("Alice: 300\n")
        f.write("Bob: 250\n")

    real_open = builtins.open  # Save real open

    def mocked_open(file, mode='r', *args, **kwargs):
        if file == "leaderboard.txt":
            return real_open(temp_path, mode, *args, **kwargs)
        return real_open(file, mode, *args, **kwargs)

    try:
        with patch("builtins.open", new=mocked_open), \
             patch("builtins.input", return_value=""), \
             patch("builtins.print") as mock_print:
            
            display_leaderboard()
            output_lines = [call.args[0] for call in mock_print.call_args_list]
            assert any("1. Alice - 300" in line for line in output_lines)
            assert any("2. Bob - 250" in line for line in output_lines)
    finally:
        os.unlink(temp_path)


def test_display_instructions():
    original_input = builtins.input
    
    try:
        builtins.input = lambda _: ''
        display_instructions()
    except Exception as e:
        builtins.input = original_input
        raise e
    else:
        builtins.input = original_input 