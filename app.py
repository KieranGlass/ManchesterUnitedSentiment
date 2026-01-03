import tkinter as tk
from tkinter import ttk

# Main window
root = tk.Tk()
root.title("Bristol City Sentiment Analyzer")
root.geometry("400x300")  # width x height

# Label
label = ttk.Label(root, text="Bristol City Sentiment Analyzer", font=("Arial", 14))
label.pack(pady=20)

# Button placeholder
def analyze_sentiment():
    print("Analyze Recent Sentiment clicked!")

analyze_button = ttk.Button(root, text="Analyze Recent Sentiment", command=analyze_sentiment)
analyze_button.pack(pady=10)

# Placeholder output area
output_label = ttk.Label(root, text="Results will appear here.", font=("Arial", 12))
output_label.pack(pady=20)

# Run the app
root.mainloop()