from tkinter import ttk
import tkinter as tk
from tkinter import font

PALE_RED = "#ffdddd"
TEXT_COLOR = "#141414"

def apply_styles(root):
    
    root.configure(bg=PALE_RED)
    
    style = ttk.Style()
    style.theme_use("clam")
    
    style.configure("TLabelframe", background=PALE_RED)
    style.configure("TLabelframe.Label", foreground="black", background=PALE_RED, bordercolor=PALE_RED)
    style.configure("TFrame", background=PALE_RED)
    style.configure("Image.TLabel", background=PALE_RED)
    style.configure("TLabel", background=PALE_RED, foreground=TEXT_COLOR, font=("Arial", 12, "bold"))
    style.configure("Action.TButton", background="black", foreground="white", font=("Arial", 11, "bold"), padding=(10, 6), borderwidth=0, relief="flat")
    style.map("Action.TButton", background=[("active", "#222222"), ("pressed", "#111111"), ("disabled", "#444444")], foreground=[("disabled", "#999999")])
    
def create_info_dot(parent, command):
    info_font = font.Font(
        family="Segoe UI",
        size=9,
        slant="italic",
        weight="bold"
    )

    lbl = tk.Label(
        parent,
        text="i",
        font=info_font,
        fg="white",
        bg="black",
        width=2,
        height=1,
        cursor="hand2"
    )

    lbl.configure(padx=2, pady=0)

    lbl.bind("<Enter>", lambda e: lbl.config(bg="#333333"))
    lbl.bind("<Leave>", lambda e: lbl.config(bg="black"))

    lbl.bind("<Button-1>", lambda e: command())
    return lbl

def create_test_dot(parent, command):
    test_font = font.Font(
        family="Segoe UI",
        size=9,
        slant="italic",
        weight="bold"
    )

    lbl = tk.Label(
        parent,
        text="Test", 
        font=test_font,
        fg="white",
        bg="black",
        width=4,
        height=1,
        cursor="hand2"
    )

    lbl.configure(padx=2, pady=0)

    lbl.bind("<Enter>", lambda e: lbl.config(bg="#333333"))
    lbl.bind("<Leave>", lambda e: lbl.config(bg="black"))

    lbl.bind("<Button-1>", lambda e: command())
    return lbl