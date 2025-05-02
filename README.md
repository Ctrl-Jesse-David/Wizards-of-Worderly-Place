# Wizards of Worderly Place

A magical word puzzle game where players uncover hidden words in a grid using available letters.

## 🎮 How to Play

1. **Starting the Game**

   - Run 'python3 worderly.py` in your terminal
   - Enter your nickname when prompted
   - Enter 'S' to initialize the grid and play the main game

2. **Game Controls**

   - Type words using the available letters
   - Commands:
     - 'shuffle' or 's': Rearrange the available letters
     - 'hint' or 'h': Get a hint (5 free hints per game)
     - 'exit' or 'e': End the current game

3. **Scoring**

   - Points are awarded for each correct letter that was unrevealed
   - Extra Lives are also rewarded for revealing valid words that are not in the grid
   - Your total score is saved to your profile

4. **Shop System**
   - Earn points to purchase hints
     - Basic Hint (10 points): Reveals one letter
       - The 5 free hints are to be exhausted first before purchased hints

## 💻 Code Organization

The project is organized into several key modules:

- 'worderly.py': Entry point and game flow management
- 'game_engine.py': Core game logic and mechanics
- 'grid_renderer.py': Handles grid display and updates
- 'user_progress.py': Manages user profiles and progress
- 'word_utils.py': Word validation and processing
- 'display_manager.py': UI and display utilities

## ✨ Bonus Features

1. **User Profile System**

   - Persistent user profiles with saved progress
   - Track highest scores and total points
   - Purchase and use hints across games

2. **Visual Feedback**

   - Color-coded letters (blue for hints, green for correct guesses)
   - Animated grid updates
   - Clear status messages and instructions

3. **Shop System**

   - In-game currency (magic points)
   - A purchasable hint
   - Persistent hint inventory

4. **Leaderboard**

   - Track and display top scores
   - Persistent across game sessions
   - Updates automatically with new high scores

5. **Enhanced Gameplay**

   - Bonus lives for finding non-grid words
   - Free hints system
