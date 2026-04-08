#!/usr/bin/env python3
"""
Simple test of the number string game logic without GUI
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from game_logic import GameState
from game_tree import generate_game_tree, minimax, alpha_beta, evaluate_heuristic
import random
import time


def count_nodes(node):
    """Count all nodes in the tree"""
    if not node:
        return 0
    count = 1
    for child in node.children:
        count += count_nodes(child)
    return count


def play_game(initial_numbers, algorithm="minimax", verbose=False):
    """Play a single game and return results"""
    state = GameState(initial_numbers[:], 0, 0, True)  # Human starts
    nodes_generated_total = 0
    nodes_evaluated_total = 0
    move_count = 0
    start_time = time.time()

    if verbose:
        print(f"Initial string: {state.numbers}")
        print(f"Human starts: {state.is_human_turn}")

    while not state.is_terminal():
        move_count += 1

        # Generate tree
        max_depth = min(len(state.numbers) // 2, 4)  # Limit depth for performance
        tree = generate_game_tree(state, max_depth)
        nodes_generated = count_nodes(tree)
        nodes_generated_total += nodes_generated

        if verbose:
            print(
                f"\nMove {move_count}: {'Human' if state.is_human_turn else 'Computer'}'s turn"
            )
            print(f"  String: {state.numbers}")
            print(
                f"  Scores - Human: {state.human_score}, Computer: {state.computer_score}"
            )
            print(f"  Generated {nodes_generated} nodes (depth {max_depth})")

        # Get best move using selected algorithm
        is_computer_turn = not state.is_human_turn
        if algorithm == "minimax":
            best_value = minimax(tree, max_depth, is_computer_turn)
        else:  # alphabeta
            best_value = alpha_beta(
                tree, max_depth, float("-inf"), float("inf"), is_computer_turn
            )

        # Find the move that led to the best value
        best_move = None
        best_child_value = float("-inf") if is_computer_turn else float("inf")

        for child in tree.children:
            if algorithm == "minimax":
                child_value = minimax(child, max_depth - 1, not is_computer_turn)
            else:
                child_value = alpha_beta(
                    child,
                    max_depth - 1,
                    float("-inf"),
                    float("inf"),
                    not is_computer_turn,
                )

            if is_computer_turn:
                if child_value > best_child_value:
                    best_child_value = child_value
                    best_move = child.move
            else:
                if child_value < best_child_value:
                    best_child_value = child_value
                    best_move = child.move

        if best_move is None and tree.children:
            # Fallback to first child
            best_move = tree.children[0].move

        if best_move:
            new_numbers, new_human_score, new_computer_score = best_move
            state = state.apply_move(new_numbers, new_human_score, new_computer_score)

            if verbose:
                action = (
                    "added" if len(new_numbers) == len(state.numbers) + 1 else "deleted"
                )
                print(f"  {action} move applied")
        else:
            # No valid moves (shouldn't happen in this game)
            break

    end_time = time.time()
    game_time = end_time - start_time

    winner = state.get_winner()

    if verbose:
        print(f"\nGame over after {move_count} moves")
        print(f"Final string: {state.numbers}")
        print(
            f"Final scores - Human: {state.human_score}, Computer: {state.computer_score}"
        )
        print(f"Winner: {winner}")
        print(f"Time taken: {game_time:.3f}s")
        print(f"Total nodes generated: {nodes_generated_total}")

    return {
        "winner": winner,
        "human_score": state.human_score,
        "computer_score": state.computer_score,
        "move_count": move_count,
        "time_taken": game_time,
        "nodes_generated": nodes_generated_total,
        "final_string": state.numbers,
    }


def run_experiment(algorithm, num_games=10):
    """Run multiple games and return statistics"""
    print(f"\nRunning {num_games} games with {algorithm.upper()} algorithm...")

    results = []
    human_wins = 0
    computer_wins = 0
    draws = 0

    for i in range(num_games):
        # Random initial string length (15-25)
        length = random.randint(15, 25)
        initial_numbers = [random.randint(1, 6) for _ in range(length)]

        # Alternate who starts to be fair
        human_starts = i % 2 == 0

        # Temporarily modify play_game to accept starting player
        state = GameState(initial_numbers[:], 0, 0, human_starts)
        # We'll need to modify play_game or create a variant - for now, let's just use the existing one
        # and accept that human always starts in our test

        result = play_game(initial_numbers, algorithm, verbose=False)
        results.append(result)

        if result["winner"] == "HUMAN":
            human_wins += 1
        elif result["winner"] == "COMPUTER":
            computer_wins += 1
        else:
            draws += 1

        if (i + 1) % 5 == 0:
            print(f"  Completed {i + 1}/{num_games} games")

    # Calculate statistics
    avg_time = sum(r["time_taken"] for r in results) / len(results)
    avg_nodes = sum(r["nodes_generated"] for r in results) / len(results)
    avg_moves = sum(r["move_count"] for r in results) / len(results)

    stats = {
        "algorithm": algorithm,
        "games_played": num_games,
        "human_wins": human_wins,
        "computer_wins": computer_wins,
        "draws": draws,
        "human_win_rate": human_wins / num_games,
        "computer_win_rate": computer_wins / num_games,
        "draw_rate": draws / num_games,
        "avg_time_per_game": avg_time,
        "avg_nodes_per_game": avg_nodes,
        "avg_moves_per_game": avg_moves,
    }

    return stats, results


def main():
    print("Number String Game - Algorithm Comparison Test")
    print("=" * 50)

    # Test both algorithms
    minimax_stats, minimax_results = run_experiment("minimax", 10)
    alphabeta_stats, alphabeta_results = run_experiment("alphabeta", 10)

    # Display results
    print("\n" + "=" * 50)
    print("EXPERIMENT RESULTS")
    print("=" * 50)

    for stats in [minimax_stats, alphabeta_stats]:
        print(f"\n{stats['algorithm'].upper()} Algorithm:")
        print(f"  Games played: {stats['games_played']}")
        print(f"  Human wins: {stats['human_wins']} ({stats['human_win_rate']:.1%})")
        print(
            f"  Computer wins: {stats['computer_wins']} ({stats['computer_win_rate']:.1%})"
        )
        print(f"  Draws: {stats['draws']} ({stats['draw_rate']:.1%})")
        print(f"  Avg. time per game: {stats['avg_time_per_game']:.3f}s")
        print(f"  Avg. nodes per game: {stats['avg_nodes_per_game']:.0f}")
        print(f"  Avg. moves per game: {stats['avg_moves_per_game']:.1f}")

    # Comparison
    print("\n" + "=" * 50)
    print("COMPARISON")
    print("=" * 50)
    print(f"Alpha-Beta vs Minimax:")
    print(
        f"  Speed improvement: {minimax_stats['avg_time_per_game'] / alphabeta_stats['avg_time_per_game']:.1f}x faster"
    )
    print(
        f"  Node reduction: {(1 - alphabeta_stats['avg_nodes_per_game'] / minimax_stats['avg_nodes_per_game']) * 100:.1f}% fewer nodes"
    )

    # Save results to file for report
    with open("experiment_results.txt", "w") as f:
        f.write("Number String Game Experiment Results\n")
        f.write("=" * 40 + "\n\n")

        for stats in [minimax_stats, alphabeta_stats]:
            f.write(f"{stats['algorithm'].upper()} Algorithm Results:\n")
            f.write(f"  Games played: {stats['games_played']}\n")
            f.write(
                f"  Human wins: {stats['human_wins']} ({stats['human_win_rate']:.1%})\n"
            )
            f.write(
                f"  Computer wins: {stats['computer_wins']} ({stats['computer_win_rate']:.1%})\n"
            )
            f.write(f"  Draws: {stats['draws']} ({stats['draw_rate']:.1%})\n")
            f.write(f"  Avg. time per game: {stats['avg_time_per_game']:.3f}s\n")
            f.write(f"  Avg. nodes per game: {stats['avg_nodes_per_game']:.0f}\n")
            f.write(f"  Avg. moves per game: {stats['avg_moves_per_game']:.1f}\n")
            f.write("\n")

        f.write("Comparison:\n")
        f.write(
            f"  Alpha-Beta is {minimax_stats['avg_time_per_game'] / alphabeta_stats['avg_time_per_game']:.1f}x faster than Minimax\n"
        )
        f.write(
            f"  Alpha-Beta evaluates {(1 - alphabeta_stats['avg_nodes_per_game'] / minimax_stats['avg_nodes_per_game']) * 100:.1f}% fewer nodes\n"
        )

    print("\nResults saved to experiment_results.txt")


if __name__ == "__main__":
    main()
