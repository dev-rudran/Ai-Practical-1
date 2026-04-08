class GameState:
    def __init__(
        self, numbers=None, human_score=0, computer_score=0, is_human_turn=True
    ):
        self.numbers = numbers or []  # List of integers 1-6
        self.human_score = human_score
        self.computer_score = computer_score
        self.is_human_turn = is_human_turn

    def is_terminal(self):
        return len(self.numbers) == 1

    def get_winner(self):
        if not self.is_terminal():
            return None
        if self.human_score > self.computer_score:
            return "HUMAN"
        elif self.computer_score > self.human_score:
            return "COMPUTER"
        else:
            return "DRAW"

    def get_possible_moves(self):
        moves = []
        n = len(self.numbers)

        # Pair addition moves (positions 0&1, 2&3, 4&5, etc.)
        for i in range(0, n - 1, 2):
            a, b = self.numbers[i], self.numbers[i + 1]
            sum_val = a + b
            # Apply modulo 6 wrap: 7→1, 8→2, 9→3, 10→4, 11→5, 12→6
            if sum_val > 6:
                sum_val = ((sum_val - 1) % 6) + 1

            new_numbers = self.numbers[:i] + [sum_val] + self.numbers[i + 2 :]
            if self.is_human_turn:
                moves.append((new_numbers, self.human_score + 1, self.computer_score))
            else:
                moves.append((new_numbers, self.human_score, self.computer_score + 1))

        # Single number deletion moves (for unpaired numbers at end if odd length)
        if n % 2 == 1:  # Odd length means last number is unpaired
            new_numbers = self.numbers[:-1]  # Remove last number
            if self.is_human_turn:
                # Human deletes: computer loses point
                moves.append((new_numbers, self.human_score, self.computer_score - 1))
            else:
                # Computer deletes: human loses point
                moves.append((new_numbers, self.human_score - 1, self.computer_score))

        return moves

    def apply_move(self, new_numbers, new_human_score, new_computer_score):
        return GameState(
            new_numbers, new_human_score, new_computer_score, not self.is_human_turn
        )
