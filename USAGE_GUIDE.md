# How to Use the Number String Game GUI

## 🎮 Starting the Game

1. **Launch the Application**:
   ```bash
   cd "/run/media/rudra/New Volume/Downloads/Semester5/Fundamentals of Artificial Inteligence/Practical 1"
   python src/main.py
   ```

2. **Configure Game Settings**:
   - **String Length**: Select a number between 15 and 25 using the spinner
   - **Who Starts**: Choose "Human" or "Computer" using radio buttons
   - **Algorithm**: Select "Minimax" or "Alpha-Beta" using radio buttons

3. **Begin Play**:
   - Click the **"Start Game"** button
   - A random number string of your selected length will be generated
   - The game state will be displayed showing the numbers, scores, and whose turn it is

## 🖱️ Making Moves

### When It's Your Turn (Human):
- The turn indicator will show "Human"
- The status bar will show "Your turn"
- **Click on pairs of numbers** to make a move:
  - Numbers are displayed in pairs: (1st&2nd), (3rd&4th), (5th&6th), etc.
  - Click on either number in a pair to select that pair for addition
  - If the string length is odd, you can also click the last number to delete it
- Valid moves will be processed immediately:
  - **Pair Addition**: Two numbers are replaced Eur their sum (with 7→1, 8→2, 9→3, 10→4, 11→5, 12→6 wrap)
  - **Single Deletion**: The last number is removed (only when string length is odd)
  - Your score increases by 1 for pair additions
  - Computer's score decreases by 1 for your deletions

### When It's Computer's Turn:
- The turn indicator will show "Computer"
- The status bar will show "Computer is thinking..."
- The computer will:
  1. Generate a game tree to a reasonable depth
  2. Use your selected algorithm (Minimax or Alpha-Beta) to evaluate moves
  3. Choose the best move
  4. Execute the move after a short delay (for visibility)
  5. Update the game state and scores
- The move description will show which algorithm was used, execution time, and nodes evaluated

## 🎯 Understanding the Display

### Number String Visualization:
- **Light Blue**: Regular numbers in pairs
- **Light Green**: Second number in a pair (helps visualize pairs)
- **Light Coral**: The unpaired last number (only appears when string length is odd)

### Information Panels:
- **Human Score**: Your current points
- **Computer Score**: Computer's current points
- **Turn**: Shows whose turn it is
- **Move Info**: Description of the last move made
- **Status Bar**: Game status messages (ready, thinking, game over)

## 🏁 Game End

The game ends when only one number remains in the string. The winner is determined by:
- Higher score wins
- Equal scores result in a draw
- A popup message shows the final result
- The status bar prompts you to click "New Game" to play again

## 🔄 Starting a New Game

After a game ends:
1. Click the **"New Game"** button
2. The interface resets to initial state
3. You can adjust settings or keep the same ones
4. Click "Start Game" to begin again

## ⚙️ Algorithm Comparison

To compare Minimax vs Alpha-Beta:
1. Play several games with each algorithm
2. Notice the difference in "thinking" time (shown in move info)
3. Alpha-Beta should be noticeably faster, especially on longer strings
4. Both algorithms should produce equally good moves (similar win rates)

## 💡 Tips for Better Gameplay

- **String Length**: Longer strings (20-25) create more complex games with more possible moves
- **First Move Advantage**: Notice whether starting first helps or hurts your chances
- **Algorithm Choice**: Alpha-Beta will be faster but should play equally well as Minimax
- **Scoring Strategy**: Sometimes taking a point now might lead to fewer opportunities later
- **Defensive Play**: Consider moves that limit your opponent's options

## 🛠️ Troubleshooting

If you encounter issues:
1. **Click Not Working**: Make sure it's actually your turn (Human indicator showing)
2. **No Moves Available**: The game should automatically end when no moves remain
3. **Display Issues**: Try resizing the window - the canvas should adjust properly
4. **Application Hangs**: The computer's thinking time increases with string length and look-ahead depth
5. **Errors**: Check the console output if running from terminal for debug information

## 📊 Experimental Data

Run the included test scripts to see algorithm performance:
```bash
# Run basic logic tests
PYTHONPATH=src python test_game.py

# Run comparison experiments
PYTHONPATH=src python simple_test.py

# View results
cat experiment_results.txt
```

Enjoy playing the Number String Game and observing how the AI algorithms perform!