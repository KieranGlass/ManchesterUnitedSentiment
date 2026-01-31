import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from src import sentiment_analysis, donut_chart, styles
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support, confusion_matrix)

def open_test_window(parent):
    test_win = tk.Toplevel(parent)
    test_win.title("Sentiment Test Tool")
    test_win.geometry("820x900")
    test_win.transient(parent)
    test_win.grab_set()
    test_win.resizable(False, False)
    
    styles.apply_styles(test_win)

    selected_file = tk.StringVar(value="No file selected")
    selected_path = None
    
    ttk.Label(
        test_win,
        text="Sentiment Testing Tool",
        font=("Arial", 14, "bold")
    ).grid(row=0, column=0, columnspan=3, pady=(10, 15))
    
    def browse_csv():
        nonlocal selected_path
        path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv")]
        )
        if path:
            selected_path = path
            selected_file.set(os.path.basename(path))

    ttk.Button(test_win, text="Browse CSV", command=browse_csv).grid(row=1, column=0, padx=10, sticky="ew")
    ttk.Label(test_win, textvariable=selected_file, wraplength=300).grid(row=1, column=1, columnspan=2, sticky="w", padx=5)
    
    def run_vader_analysis():
        path = selected_path
        if path == "No file selected":
            messagebox.showwarning("No file", "Please select a CSV file first.")
            return

        try:
            df = sentiment_analysis.analyze_csv_sentiment(path)

            pos_percent = (df["sentiment"] == "Positive").mean() * 100
            neg_percent = (df["sentiment"] == "Negative").mean() * 100
            neu_percent = (df["sentiment"] == "Neutral").mean() * 100

            test_donut.update(pos_percent, neg_percent, neu_percent)
            
            if "manual_sentiment" in df.columns:
                results = evaluate_predictions(df)

                accuracy_var.set(f"{results['accuracy']*100:.1f}%")
                precision_var.set(f"{results['precision']:.2f}")
                recall_var.set(f"{results['recall']:.2f}")
                f1_var.set(f"{results['f1']:.2f}")

                cm = results["confusion_matrix"]
                for i in range(3):
                    for j in range(3):
                        cm_vars[i][j].set(str(cm[i, j]))
            else:
                messagebox.showerror("Error")
        except Exception as e:
            messagebox.showerror("Error", f"Error running analysis:\n{e}")

    ttk.Button(test_win, text="Run VADER Analysis", style="Action.TButton", command=run_vader_analysis).grid(row=2, column=0, columnspan=3, pady=15, sticky="ew", padx=10)

    donut_frame = ttk.Frame(test_win, padding=10)
    donut_frame.grid(row=3, column=0, columnspan=3, pady=(5, 15))

    test_donut = donut_chart.DonutChart(donut_frame)
    test_donut.update(0, 0, 0)
    
    def evaluate_predictions(df):
        y_true = df["manual_sentiment"]
        y_pred = df["sentiment"]

        accuracy = accuracy_score(y_true, y_pred)

        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true,
            y_pred,
            labels=["Positive", "Neutral", "Negative"],
            average="macro",
            zero_division=0
        )

        cm = confusion_matrix(
            y_true,
            y_pred,
            labels=["Positive", "Neutral", "Negative"]
        )

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "confusion_matrix": cm
        }
    
    metrics_frame = ttk.LabelFrame(test_win, text="Evaluation Metrics", padding=10)
    metrics_frame.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

    accuracy_var = tk.StringVar(value="—")
    precision_var = tk.StringVar(value="—")
    recall_var = tk.StringVar(value="—")
    f1_var = tk.StringVar(value="—")

    ttk.Label(metrics_frame, text="Accuracy:").grid(row=0, column=0, sticky="w")
    ttk.Label(metrics_frame, textvariable=accuracy_var).grid(row=0, column=1, sticky="w")

    ttk.Label(metrics_frame, text="Precision (macro):").grid(row=1, column=0, sticky="w")
    ttk.Label(metrics_frame, textvariable=precision_var).grid(row=1, column=1, sticky="w")

    ttk.Label(metrics_frame, text="Recall (macro):").grid(row=2, column=0, sticky="w")
    ttk.Label(metrics_frame, textvariable=recall_var).grid(row=2, column=1, sticky="w")

    ttk.Label(metrics_frame, text="F1-score (macro):").grid(row=3, column=0, sticky="w")
    ttk.Label(metrics_frame, textvariable=f1_var).grid(row=3, column=1, sticky="w")
    
    cm_frame = ttk.LabelFrame(test_win, text="Confusion Matrix", padding=10)
    cm_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    cm_vars = [[tk.StringVar(value="—") for _ in range(3)] for _ in range(3)]

    labels = ["Positive", "Neutral", "Negative"]

    for j, label in enumerate(labels):
        ttk.Label(cm_frame, text=label).grid(row=0, column=j+1)

    for i, label in enumerate(labels):
        ttk.Label(cm_frame, text=label).grid(row=i+1, column=0)
        for j in range(3):
            ttk.Label(cm_frame, textvariable=cm_vars[i][j]).grid(row=i+1, column=j+1)

    test_win.grid_columnconfigure(0, weight=0)
    test_win.grid_columnconfigure(1, weight=1)
    test_win.grid_columnconfigure(2, weight=1)


   