# 🧙🏽‍♂️ WIZARDS OF WORDERLY PLACE 🧙🏽‍♂️

Step into a realm where language is magic and every letter holds power!

In this enchanted word puzzle adventure, spellcasters unravel hidden words woven into a mystical grid using the sacred letters of *The First Sigil*, a six-rune incantation. Summon your vocabulary, wield your wits, and rise through the ranks of arcane linguists.

The scrolls await…will your name be etched among the legends?

## 🪄 HOW TO PLAY 🪄

### **Summoning the Game**

<img width="546" alt="Start" src="https://github.com/user-attachments/assets/986bcc08-3c20-4ef7-8f36-2976dd68172e" />

   1. To begin your magical journey, cast the  incantation 'python3 worderly.py' in your terminal from the sacred project root directory.
   2. You shall be asked to reveal your wizarding name—enter it with pride.
   <img width="546" alt="Name" src="https://github.com/user-attachments/assets/46ab8c18-9a7e-47bb-af9e-e5d965d75d13" />

   3. Next, consult the ancient runes (your keyboard) and choose an action by invoking the letter nestled within brackets. To unlock the Game, invoke the letter 'S'.
   <img width="546" alt="Menu" src="https://github.com/user-attachments/assets/cf6168f3-77c1-4db5-9081-487ad9d8c014" />

   4. Select your preffered level of mastery (based on preferred word count in the grid).
   <img width="546" alt="Level" src="https://github.com/user-attachments/assets/0f010fae-eaf9-4548-b94a-0380298d1971" />

   5. Embrace your inner wizard and start summoning spells as your trial begins!
   <img width="544" alt="Start" src="https://github.com/user-attachments/assets/ae071cf0-89bc-4432-a5c4-7396366ea056" />


### **Spellcasting**

<img width="523" alt="Controls" src="https://github.com/user-attachments/assets/d59d0d14-be46-471c-bfc9-b793c739234e" />


   - As a spellcaster, you are tasked with uncovering the enchanted words hidden within the ruins using the letters summoned from *The First Sigil*, a powerful six-letter word that lies diagonally across the grid like a secret rune.

   - Spells:

     - 🌀 '-shuffle' or '-s':  Stir the cauldron and rearrange the available letters for new inspiration!
     - 🔍 '-whisper' or '-w': Receive a whisper of guidance from the spirits. You may call upon this magic five (5) times freely per game.
     - 💥 '-flash' or '-f': Cast this spell in dire times to enchant all unanswered runes pulse with crimson light,
       guiding your gaze toward the missing incantations still awaiting your chant.
     - 💨 '-exit' or '-e': Retreat from the spell chamber and end your trial as a wizard.

   - Once the genesis of all utterance, *The First Sigil*, revealed itself, do not forget to chant its runes to complete your divine task as a spellcaster!

### **Spell Points**

   - Each time you unearth a hidden word from the enchanted grid, every hidden letter you unveil glows with point-bearing power.
   - Should you conjure a valid word not inscribed within the grid, the spirits of language shall bestow you EXTRA LIVES as a reward for your clever sorcery.
   - All your hard-earned spell points are sealed within your soul crystal, etched into your eternal profile for future spellwork and magic purchases.
   - Those who prove most potent in the mystical arts shall have their names etched upon the Celestial Scroll of Champions, a leaderboard of the realm’s finest spellcasters. Climb the ranks, surpass your fellow word-wizards, and let all behold your sorcerous skill!


### **The Mystic Market**

   - Use your hard-earned spell points to purchase more hints when your free ones run dry.
      - A Whisper from the Spirits (10 points): Reveals a single mystical letter.
      - Remember, your first five hints are gifts from the mystic elders. Spend wisely after they are gone.

## 💻 CODE ORGANIZATION 💻

The project is organized into several key modules:

- 'worderly.py': Entry point and game flow management
- 'game_engine.py': Core game logic and mechanics
- 'grid_renderer.py': Handles grid display and updates
- 'user_progress.py': Manages user profiles and progress
- 'word_utils.py': Word validation and processing
- 'display_manager.py': UI and display utilities

## ✨ BONUS FEATURES ✨

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

## 🧪 UNIT TESTING 🧪

This project uses the pytest framework for unit testing located in test_wonderly.py to ensure the correctness and robustness of the game's core logic and its application under both normal and unexpected cases.

### **Running Tests**

   1. From the project root directory, run 'pytest test_worderly.py'.
   2. A report of passed or failed test will be displayed after running the test.

### **Test Coverage**

   - Grid Construction
      - Validates correct placement of the main diagonal word and other words in the grid.
   - Word Intersection & Placement Validation
      - Ensures that words can be placed without conflicts and with correct overlap logic.
   - Word Validation
      - Determines whether a word input is valid (i.e. included in the word list or a bonus word) using available letters while validating repeated and incorrect inputs. 
   - Game Mechanics
      - Verifies initialization, point calculation, input handling, and the full gameplay, such as completing the game or running out of lives.

### **Adding Tests**

   1. Create a new function in 'test_worderly.py' using the 'test_' prefix.
   2. Use assert statements to verify expected outcomes.
   3. Reuse or extend the 'create_game()' function for consistent test setup if needed.
   3. Run pytest to confirm your test behaves as expected.
