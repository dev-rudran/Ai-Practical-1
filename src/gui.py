import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from game_logic import GameState
from game_tree import (
    generate_game_tree,
    minimax,
    alpha_beta,
    evaluate_heuristic,
)


class NumberStringGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number String Game - AI Assignment")
        self.root.geometry("800x600")

        self.game_state = None
        self.current_tree = None
        self.experiment_mode = False
        self.experiment_results = []

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Game Controls", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        # String length selector
        ttk.Label(control_frame, text="String Length:").grid(
            row=0, column=0, padx=(0, 5)
        )
        self.length_var = tk.IntVar(value=20)
        length_spinbox = ttk.Spinbox(
            control_frame, from_=15, to=25, width=5, textvariable=self.length_var
        )
        length_spinbox.grid(row=0, column=1, padx=(0, 20))

        # Player start selector
        ttk.Label(control_frame, text="Who starts:").grid(row=0, column=2, padx=(0, 5))
        self.start_var = tk.StringVar(value="human")
        ttk.Radiobutton(
            control_frame, text="Human", variable=self.start_var, value="human"
        ).grid(row=0, column=3, padx=(0, 5))
        ttk.Radiobutton(
            control_frame, text="Computer", variable=self.start_var, value="computer"
        ).grid(row=0, column=4, padx=(0, 20))

        # Algorithm selector
        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=5, padx=(0, 5))
        self.algo_var = tk.StringVar(value="minimax")
        ttk.Radiobutton(
            control_frame, text="Minimax", variable=self.algo_var, value="minimax"
        ).grid(row=0, column=6, padx=(0, 5))
        ttk.Radiobutton(
            control_frame, text="Alpha-Beta", variable=self.algo_var, value="alphabeta"
        ).grid(row=0, column=7, padx=(0, 5))

        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=8, padx=(20, 0))

        self.start_button = ttk.Button(
            button_frame, text="Start Game", command=self.start_game
        )
        self.start_button.grid(row=0, column=0, padx=(0, 5))

        self.new_game_button = ttk.Button(
            button_frame, text="New Game", command=self.new_game, state="disabled"
        )
        self.new_game_button.grid(row=0, column=1)

        # Game Display
        display_frame = ttk.LabelFrame(main_frame, text="Game State", padding="10")
        display_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 10))
        display_frame.columnconfigure(0, weight=1)
        display_frame.rowconfigure(1, weight=1)

        # Info labels
        info_frame = ttk.Frame(display_frame)
        info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(3, weight=1)

        ttk.Label(info_frame, text="Human Score:").grid(row=0, column=0, sticky=tk.W)
        self.human_score_label = ttk.Label(
            info_frame, text="0", font=("Arial", 12, "bold")
        )
        self.human_score_label.grid(row=0, column=1, sticky=tk.W, padx=(5, 20))

        ttk.Label(info_frame, text="Computer Score:").grid(row=0, column=2, sticky=tk.W)
        self.computer_score_label = ttk.Label(
            info_frame, text="0", font=("Arial", 12, "bold")
        )
        self.computer_score_label.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))

        ttk.Label(info_frame, text="Turn:").grid(
            row=0, column=4, sticky=tk.W, padx=(20, 5)
        )
        self.turn_label = ttk.Label(
            info_frame, text="Human", font=("Arial", 12, "bold")
        )
        self.turn_label.grid(row=0, column=5, sticky=tk.W)

        # String display
        self.string_frame = ttk.Frame(display_frame)
        self.string_frame.grid(row=1, column=0, sticky="nsew")
        self.string_frame.columnconfigure(0, weight=1)
        self.string_frame.rowconfigure(0, weight=1)

        self.string_canvas = tk.Canvas(self.string_frame, height=80, bg="white")
        self.string_canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbar for string
        string_scrollbar = ttk.Scrollbar(
            self.string_frame, orient="horizontal", command=self.string_canvas.xview
        )
        string_scrollbar.grid(row=1, column=0, sticky="ew")
        self.string_canvas.configure(xscrollcommand=string_scrollbar.set)

        # Move execution info
        self.move_info_label = ttk.Label(display_frame, text="", font=("Arial", 10))
        self.move_info_label.grid(row=2, column=0, pady=(10, 0))

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to start game")
        status_bar = ttk.Label(
            main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(5, 0))

        # Bind canvas resize and click events
        self.string_canvas.bind("<Configure>", self.on_canvas_configure)
        self.string_canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_configure(self, event):
        if self.game_state:
            self.draw_string()

    def on_canvas_click(self, event):
        if not self.game_state or not self.game_state.is_human_turn:
            return

        # Get the canvas x coordinate of the click, adjusting for scrolling
        canvas_x = self.string_canvas.canvasx(event.x)
        # Get the string length and number dimensions
        numbers = self.game_state.numbers
        n = len(numbers)
        if n == 0:
            return

        # Dimensions used in draw_string
        padding = 10
        number_width = 40

        # Calculate which number was clicked
        number_index = int((canvas_x - padding) // number_width)

        # Check if the click is within the string bounds
        if number_index < 0 or number_index >= n:
            return

        # Determine the move index based on the clicked number
        if n % 2 == 0:
            # Even length: only pair moves
            if number_index < n:
                pair_index = number_index // 2
                # Number of pairs is n//2
                if pair_index < n // 2:
                    move_index = pair_index
                else:
                    return
            else:
                return
        else:
            # Odd length: pair moves and then deletion move
            if number_index < n - 1:
                # Part of a pair (indices 0 to n-2)
                pair_index = number_index // 2
                # Number of pairs is (n-1)//2
                if pair_index < (n - 1) // 2:
                    move_index = pair_index
                else:
                    return
            elif number_index == n - 1:
                # Deletion move (last number)
                move_index = (n - 1) // 2
            else:
                return

        # Make the human move
        self.make_human_move(move_index)

    def start_game(self):
        # Generate random string
        length = self.length_var.get()
        initial_numbers = [random.randint(1, 6) for _ in range(length)]

        # Determine who starts
        is_human_start = self.start_var.get() == "human"

        # Initialize game state
        self.game_state = GameState(initial_numbers, 0, 0, is_human_start)
        self.current_tree = None
        self.experiment_mode = False

        # Update UI
        self.update_display()
        self.start_button.config(state="disabled")
        self.new_game_button.config(state="normal")

        # If computer starts, make computer move
        if not self.game_state.is_human_turn:
            self.root.after(500, self.computer_move)

    def new_game(self):
        self.start_button.config(state="normal")
        self.new_game_button.config(state="disabled")
        self.status_var.set("Ready to start game")
        self.move_info_label.config(text="")
        self.string_canvas.delete("all")
        self.human_score_label.config(text="0")
        self.computer_score_label.config(text="0")
        self.turn_label.config(text="Human")
        self.game_state = None
        self.current_tree = None

    def update_display(self):
        if not self.game_state:
            return

        # Update scores
        self.human_score_label.config(text=str(self.game_state.human_score))
        self.computer_score_label.config(text=str(self.game_state.computer_score))

        # Update turn
        turn_text = "Human" if self.game_state.is_human_turn else "Computer"
        self.turn_label.config(text=turn_text)

        # Update string display
        self.draw_string()

        # Check for game end
        if self.game_state.is_terminal():
            self.end_game()

    def draw_string(self):
        self.string_canvas.delete("all")
        if not self.game_state:
            return

        numbers = self.game_state.numbers
        if not numbers:
            return

        # Calculate dimensions
        padding = 10
        number_width = 40
        number_height = 30

        # Update canvas scroll region
        total_width = padding * 2 + len(numbers) * number_width
        self.string_canvas.configure(
            scrollregion=(0, 0, total_width, number_height + 2 * padding)
        )

        # Draw numbers
        for i, num in enumerate(numbers):
            x1 = padding + i * number_width
            y1 = padding
            x2 = x1 + number_width
            y2 = y1 + number_height

            # Determine color based on whether it's part of a pair
            fill_color = "lightblue"
            if (
                i % 2 == 1 and i < len(numbers) - 1
            ):  # Second in pair (except last if odd)
                fill_color = "lightgreen"
            elif (
                i % 2 == 0 and i == len(numbers) - 1 and len(numbers) % 2 == 1
            ):  # Last if odd
                fill_color = "lightcoral"

            self.string_canvas.create_rectangle(
                x1, y1, x2, y2, fill=fill_color, outline="black"
            )
            self.string_canvas.create_text(
                (x1 + x2) / 2, (y1 + y2) / 2, text=str(num), font=("Arial", 14, "bold")
            )

    def make_human_move(self, move_index):
        if not self.game_state or self.game_state.is_human_turn == False:
            return

        moves = self.game_state.get_possible_moves()
        if move_index >= len(moves):
            return

        new_numbers, new_human_score, new_computer_score = moves[move_index]
        self.game_state = self.game_state.apply_move(
            new_numbers, new_human_score, new_computer_score
        )

        # Update move info
        self.move_info_label.config(
            text=f"Human made move: {self.format_move_description(move_index, moves)}"
        )

        self.update_display()

        # If game not over, computer's turn
        if not self.game_state.is_terminal():
            self.root.after(500, self.computer_move)

    def computer_move(self):
        if not self.game_state or self.game_state.is_human_turn:
            return

        self.status_var.set("Computer is thinking...")
        self.root.update()

        start_time = time.time()

        # Generate tree
        max_depth = min(len(self.game_state.numbers) // 2, 6)  # Reasonable limit
        self.current_tree = generate_game_tree(self.game_state, max_depth)

        # Choose algorithm
        if self.algo_var.get() == "minimax":
            best_value = minimax(
                self.current_tree, max_depth, False
            )  # Computer is minimizing player from its perspective
        else:  # alphabeta
            best_value = alpha_beta(
                self.current_tree, max_depth, float("-inf"), float("inf"), False
            )

        # Find best move (simplified - in practice we'd track during search)
        best_node = self.find_best_move_node(self.current_tree, False)

        end_time = time.time()
        move_time = end_time - start_time

        if best_node and best_node.move:
            new_numbers, new_human_score, new_computer_score = best_node.move
            self.game_state = self.game_state.apply_move(
                new_numbers, new_human_score, new_computer_score
            )

            # Update move info with algorithm and time
            algo_name = "Minimax" if self.algo_var.get() == "minimax" else "Alpha-Beta"
            nodes_generated = count_nodes(self.current_tree)
            self.move_info_label.config(
                text=f"Computer ({algo_name}) made move in {move_time:.3f}s ({nodes_generated} nodes)"
            )
        else:
            # Fallback to random move
            moves = self.game_state.get_possible_moves()
            if moves:
                choice = random.choice(moves)
                self.game_state = self.game_state.apply_move(*choice)
                self.move_info_label.config(text="Computer made random move (fallback)")

        self.update_display()
        self.status_var.set("Your turn")

    def find_best_move_node(self, node, is_maximizing_player):
        """Find the child node with the best minimax value"""
        if not node.children:
            return None

        if is_maximizing_player:
            best_child = max(node.children, key=lambda x: x.minimax_value)
        else:
            best_child = min(node.children, key=lambda x: x.minimax_value)

        return best_child

    def format_move_description(self, move_index, moves):
        """Create a human-readable description of the move"""
        if not self.game_state or move_index >= len(moves):
            return "Invalid move"

        new_numbers, new_human_score, new_computer_score = moves[move_index]
        old_numbers = self.game_state.numbers

        # Find what changed
        if len(new_numbers) == len(old_numbers) - 1:
            # Deletion move
            if old_numbers[-1] != new_numbers[-1] if new_numbers else True:
                deleted = old_numbers[-1]
                return f"Deleted {deleted} (end)"

        # Look for pair changes
        for i in range(0, len(old_numbers) - 1, 2):
            if i + 1 < len(new_numbers):
                old_pair = (old_numbers[i], old_numbers[i + 1])
                new_pair = (
                    (new_numbers[i],)
                    if i + 1 >= len(new_numbers)
                    else (new_numbers[i], new_numbers[i + 1])
                )
                if old_pair != new_pair:
                    a, b = old_pair
                    sum_val = a + b
                    if sum_val > 6:
                        sum_val = ((sum_val - 1) % 6) + 1
                    return f"Added {a}+{b}={sum_val} at position {i // 2 + 1}"

        return f"Made move {move_index + 1}"

    def end_game(self):
        if not self.game_state:
            return

        winner = self.game_state.get_winner()
        if winner == "HUMAN":
            result_msg = f"Human wins! Score: Human {self.game_state.human_score} - Computer {self.game_state.computer_score}"
        elif winner == "COMPUTER":
            result_msg = f"Computer wins! Score: Computer {self.game_state.computer_score} - Human {self.game_state.human_score}"
        else:
            result_msg = f"Draw! Score: Human {self.game_state.human_score} - Computer {self.game_state.computer_score}"

        self.move_info_label.config(text=result_msg)
        self.status_var.set("Game over - Click New Game to play again")
        messagebox.showinfo("Game Over", result_msg)


def count_nodes(node):
    """Count all nodes in the tree"""
    if not node:
        return 0
    count = 1
    for child in node.children:
        count += count_nodes(child)
    return count


def run_experiments():
    """Run automated experiments for reporting"""
    print("Running experiments...")
    # This would be implemented for the report generation
    pass


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberStringGameGUI(root)
    root.mainloop()
