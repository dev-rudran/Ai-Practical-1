from game_logic import GameState
from game_tree import generate_game_tree, minimax, alpha_beta, evaluate_heuristic


def test_game_logic():
    print("Testing game logic...")

    # Test initial state
    state = GameState([1, 2, 3, 4, 5, 6])
    print(f"Initial state: {state.numbers}")
    print(f"Is terminal: {state.is_terminal()}")
    print(f"Possible moves: {len(state.get_possible_moves())}")

    # Test move application
    if state.get_possible_moves():
        new_nums, new_human, new_computer = state.get_possible_moves()[0]
        new_state = state.apply_move(new_nums, new_human, new_computer)
        print(f"After move: {new_state.numbers}")
        print(
            f"Scores - Human: {new_state.human_score}, Computer: {new_state.computer_score}"
        )

    # Test tree generation
    print("\nTesting tree generation...")
    tree = generate_game_tree(state, 2)
    print(f"Tree depth: {tree.depth}")
    print(f"Number of nodes: {count_nodes(tree)}")

    # Test minimax
    print("\nTesting minimax...")
    mm_value = minimax(tree, 2, False)
    print(f"Minimax value: {mm_value}")

    # Test alpha-beta
    print("\nTesting alpha-beta...")
    ab_value = alpha_beta(tree, 2, float("-inf"), float("inf"), False)
    print(f"Alpha-beta value: {ab_value}")

    print("\nAll tests completed!")


def count_nodes(node):
    if not node:
        return 0
    count = 1
    for child in node.children:
        count += count_nodes(child)
    return count


if __name__ == "__main__":
    test_game_logic()
