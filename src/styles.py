# style.py
from tkinter import ttk

# Define colors
PALE_RED = "#ffdddd"
BUTTON_COLOR = "#ffaaaa"
TEXT_COLOR = "#333333"

def apply_styles(root):
    
    root.configure(bg=PALE_RED)
    
    style = ttk.Style()
    
    style.configure("TLabelframe", background=PALE_RED)
    style.configure("TLabelframe.Label", foreground="black", background=PALE_RED, bordercolor=PALE_RED)
    style.configure("TFrame", background=PALE_RED)
    style.configure("TLabel", background=PALE_RED, foreground=TEXT_COLOR, font=("Arial", 12))
    style.configure("TButton", background=BUTTON_COLOR, foreground=TEXT_COLOR, font=("Arial", 11, "bold"))