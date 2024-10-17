# main.py

import tkinter as tk
from tarea_ui import AplicacionListaTareas

def main():
    root = tk.Tk()
    root.resizable(False, False)
    app = AplicacionListaTareas(root)
    root.mainloop()

if __name__ == "__main__":
    main() 