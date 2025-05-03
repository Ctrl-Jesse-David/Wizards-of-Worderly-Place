# Wizards of Worderly Place

A magical word puzzle game where players uncover hidden words in a grid using available letters.

## 🎮 How to Play

1. **Starting the Game**

   - Run 'python3 worderly.py' in your terminal
   - Enter your nickname when prompted
   <img width="551" alt="Image" src="https://github.com/user-attachments/assets/b8cbb0ff-bad2-4e89-811b-b5e7278d4c6f" />

   - Enter 'S' to initialize the main game
   <img width="543" alt="Image" src="https://github.com/user-attachments/assets/cb437b37-27d1-4ed7-810d-5a5898d081e1" />

     - Select a difficulty level (based on preferred word count in the grid)
       <img width="543" alt="Image" src="https://github.com/user-attachments/assets/22d8cce0-a998-4550-8246-b73a4735a618" />

       - Play the game!
       <img width="540" alt="Image" src="https://github.com/user-attachments/assets/b6211224-8ed7-46c1-aad8-43ba0c21bbaa" />

1. **Game Controls**

<img width="522" alt="Image" src="https://github.com/user-attachments/assets/b01dbd10-8917-432e-9d46-5bebdd80acf0" />

   - Guess the words that are hidden in the grid by using the available letters provided

     - The letters provided are based on the main 6 letter-word diagonally placed in the grid

   - Commands:
     - '-shuffle' or '-s': Rearrange the available letters
     - '-hint' or '-h': Get a hint (5 free hints per game)
     - '-exit' or '-e': End the current game

3. **Scoring**

   - Points are awarded for each correct letter that was unrevealed
   - Extra Lives are rewarded for revealing valid words that are not in the grid
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

2. **Enhanced Visuals and Visual Feedback**

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
