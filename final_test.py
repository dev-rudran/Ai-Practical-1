#!/usr/bin/env python3
"""
Final test to demonstrate the GUI works with clicking
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from gui import NumberStringGameGUI
import tkinter as tk


def main():
    print("Starting Number String Game GUI test...")
    print("This will launch the GUI window. Try:")
    print("1. Click 'Start Game' to begin")
    print("2. Click on pairs of numbers to make moves")
    print("3. Watch the computer respond")
    print("4. Close the window when done")
    print()

    root = tk.Tk()
    root.title("Number String Game - Test Mode")
    app = NumberStringGameGUI(root)

    # Start the main loop
    root.mainloop()

    print("GUI test completed.")


if __name__ == "__main__":
    main()
