import tkinter as tk
from StartMenu import StartMenu  # Import giao diện menu chính

if __name__ == "__main__":
    root = tk.Tk()
    app = StartMenu(root)
    root.mainloop()