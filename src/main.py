import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from gui import NumberStringGameGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberStringGameGUI(root)
    root.mainloop()
