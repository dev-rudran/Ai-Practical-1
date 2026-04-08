# Number String Game - AI Assignment

This project implements a deterministic two-player game with perfect information where a computer plays against a human, fulfilling the requirements for the Fundamentals of Artificial Intelligence practical assignment.

## Game Description

The game involves manipulating a string of numbers (1-6) with the following rules:
- At the beginning, the human player chooses the length of the string (15-25 numbers)
- The software randomly generates a string of numbers according to the specified length
- Players take turns. Each player starts with 0 points.
- During a turn, a player may:
  1. Add a pair of numbers (first with second, third with fourth, etc.) and write the sum in place of the pair (if sum > 6, apply modulo 6 wrap: 7→1, 8→2, 9→3, 10→4, 11→5, 12→6), and add 1 point to their score
  2. Delete a number left unpaired (if string length is odd) and subtract one point from the opponent's score
- The game ends when only one number remains in the string
- The player with the highest score wins

## Features Implemented

1. **Graphical User Interface**: Built with Tkinter
2. **Game Options**:
   - Choose who starts the game (human or computer)
   - Choose which algorithm the computer uses (Minimax or Alpha-Beta)
   - Make moves and see game state changes
   - Start a new game after completion
3. **AI Algorithms**:
   - Minimax algorithm with N-ply look ahead
   - Alpha-Beta pruning algorithm with N-ply look ahead
4. **Game Tree Data Structure**: Proper implementation using classes and linked nodes
5. **Heuristic Evaluation Function**: Domain-specific heuristic considering score difference, mobility, and positional advantage
6. **Experiment Framework**: Automated testing to compare algorithms

## Files

- `src/game_logic.py`: Game state logic and rules
- `src/game_tree.py`: Game tree nodes, heuristic function, Minimax and Alpha-Beta algorithms
- `src/gui.py`: Graphical user interface implementation
- `src/main.py`: Entry point for the application
- `experiment_results.txt`: Results from algorithm comparison experiments
- `simple_test.py`: Command-line testing script

## How to Run

1. Ensure you have Python 3.x installed
2. Navigate to the project directory
3. Run: `python src/main.py`

## Experiment Results

See `experiment_results.txt` for detailed comparison between Minimax and Alpha-Beta algorithms showing:
- Win/loss/draw statistics
- Average computation time per move
- Average number of nodes generated and evaluated
- Performance comparison demonstrating Alpha-Beta's efficiency improvements

## Implementation Details

### Data Structures
- `GameState`: Encapsulates the current game state (number string, scores, turn)
- `GameTreeNode`: Represents nodes in the game tree with parent/child links, heuristic values, and algorithm-specific values

### Algorithms
- **Minimax**: Recursive implementation with depth limiting
- **Alpha-Beta**: Minimax with alpha-beta pruning for efficiency
- **Heuristic Function**: Combines score difference, move mobility, and positional advantage

### GUI Components
- Control panel for game configuration
- Real-time game state visualization
- Move history and game statistics
- Responsive design with scrollable number string display

## Submission Requirements Met

✅ GUI-based application (not command line)
✅ Player start selection (human/computer)
✅ Algorithm choice (Minimax/Alpha-Beta)
✅ Move making and game state visualization
✅ New game functionality
✅ Proper game tree data structure (not just variables)
✅ Both algorithms implemented as N-ply look ahead
✅ Heuristic evaluation function developed and justified
✅ 10 experiments with each algorithm recorded
✅ Report preparation in progress
✅ Code available in text format (not images)