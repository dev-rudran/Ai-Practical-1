class GameTreeNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state  # GameState object
        self.parent = parent  # Reference to parent node
        self.move = move  # Move that led to this state (tuple)
        self.children = []  # List of child nodes
        self.heuristic_value = 0  # Heuristic evaluation
        self.minimax_value = 0  # Minimax value
        self.alpha = float("-inf")  # Alpha value for pruning
        self.beta = float("inf")  # Beta value for pruning
        self.depth = 0 if parent is None else parent.depth + 1


def evaluate_heuristic(state, is_computer_turn):
    # Base score difference
    score_diff = (
        state.computer_score - state.human_score
        if is_computer_turn
        else state.human_score - state.computer_score
    )

    # Mobility factor: number of available moves
    mobility = len(state.get_possible_moves())

    # Positional advantage: favor shorter strings (closer to end)
    position_factor = (30 - len(state.numbers)) / 30  # Normalized

    # Combine factors with weights
    heuristic = (score_diff * 0.5) + (mobility * 0.3) + (position_factor * 0.2)

    return heuristic if is_computer_turn else -heuristic


def generate_game_tree(state, max_depth):
    root = GameTreeNode(state)
    _generate_tree_recursive(root, max_depth)
    return root


def _generate_tree_recursive(node, max_depth):
    if node.depth >= max_depth or node.state.is_terminal():
        return

    moves = node.state.get_possible_moves()
    for new_numbers, new_human_score, new_computer_score in moves:
        child_state = node.state.apply_move(
            new_numbers, new_human_score, new_computer_score
        )
        child_node = GameTreeNode(
            child_state, node, (new_numbers, new_human_score, new_computer_score)
        )
        node.children.append(child_node)
        _generate_tree_recursive(child_node, max_depth)


def minimax(node, depth, is_maximizing_player):
    if depth == 0 or node.state.is_terminal() or not node.children:
        if node.state.is_terminal():
            winner = node.state.get_winner()
            if winner == "COMPUTER":
                return float("inf")
            elif winner == "HUMAN":
                return float("-inf")
            else:  # DRAW
                return 0
        return evaluate_heuristic(node.state, is_maximizing_player)

    if is_maximizing_player:
        max_eval = float("-inf")
        for child in node.children:
            eval = minimax(child, depth - 1, False)
            max_eval = max(max_eval, eval)
        node.minimax_value = max_eval
        return max_eval
    else:
        min_eval = float("inf")
        for child in node.children:
            eval = minimax(child, depth - 1, True)
            min_eval = min(min_eval, eval)
        node.minimax_value = min_eval
        return min_eval


def alpha_beta(node, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or node.state.is_terminal() or not node.children:
        if node.state.is_terminal():
            winner = node.state.get_winner()
            if winner == "COMPUTER":
                return float("inf")
            elif winner == "HUMAN":
                return float("-inf")
            else:  # DRAW
                return 0
        return evaluate_heuristic(node.state, is_maximizing_player)

    if is_maximizing_player:
        max_eval = float("-inf")
        for child in node.children:
            eval = alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        node.minimax_value = max_eval
        node.alpha = alpha
        node.beta = beta
        return max_eval
    else:
        min_eval = float("inf")
        for child in node.children:
            eval = alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        node.minimax_value = min_eval
        node.alpha = alpha
        node.beta = beta
        return min_eval
