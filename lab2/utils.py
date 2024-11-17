import tkinter as tk

def clear_window(root):
    """Clear all widgets from the window."""
    for widget in root.winfo_children():
        widget.destroy()
