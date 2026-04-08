#!/bin/bash
# Simple script to run tests with proper Python path

echo "Running game logic tests..."
cd "/run/media/rudra/New Volume/Downloads/Semester5/Fundamentals of Artificial Inteligence/Practical 1"
PYTHONPATH=src python test_game.py

echo ""
echo "Running simple test (experiment framework)..."
PYTHONPATH=src python simple_test.py

echo ""
echo "Tests completed. Check experiment_results.txt for results."