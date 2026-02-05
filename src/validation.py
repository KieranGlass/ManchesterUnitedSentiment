import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from src import sentiment_analysis, donut_chart, styles
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

"""
    Evaluation module 
    
    Opens the sentiment validation window that allows users to load a
    manually labelled CSV dataset and evaluate the performance of the VADER
    sentiment analysis pipeline

    The validation interface provides:

    - CSV file selection for user-supplied test data
    - Automated sentiment analysis using the sentiment module
    - Donut chart visualisation of sentiment distribution
    - Confusion matrix comparing predicted vs manual labels
    - Evaluation metrics including accuracy, precision, recall, and F1 score

    If manual sentiment labels are present in the CSV file, the tool computes
    performance statistics to help users understand where the model performs
    well or struggles
    
    There is a test_sentiment.csv file in the data folder to test the evaluation
    module

    The window uses grab_set, preventing interaction with the parent window
    until closed, as an error prevention plan
    

"""

def open_test_window(parent):
    
    test_win = tk.Toplevel(parent)
    test_win.title("Sentiment Test Tool")
    test_win.geometry("820x750")
    test_win.transient(parent)
    test_win.grab_set()
    test_win.resizable(False, False)

    styles.apply_styles(test_win)
    
    def on_close():
        test_win.destroy()

    test_win.protocol("WM_DELETE_WINDOW", on_close)

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
        if path is None:
            messagebox.showwarning("No file", "Please select a CSV file first.")
            return

        try:
            df = sentiment_analysis.analyze_csv_sentiment(path)

            pos_percent = (df["sentiment"] == "Positive").mean() * 100
            neg_percent = (df["sentiment"] == "Negative").mean() * 100
            neu_percent = (df["sentiment"] == "Neutral").mean() * 100
            test_donut.update(pos_percent, neg_percent, neu_percent)

            if "manual_sentiment" in df.columns:
                y_true = df["manual_sentiment"]
                y_pred = df["sentiment"]

                total_var.set(str(len(df)))
                correct_var.set(str((y_true == y_pred).sum()))
                accuracy_var.set(f"{accuracy_score(y_true, y_pred)*100:.1f}%")

                precision, recall, f1, _ = precision_recall_fscore_support(
                    y_true, y_pred,
                    labels=["Positive", "Negative", "Neutral"],
                    average=None,
                    zero_division=0
                )

                precision_pos_var.set(f"{precision[0]*100:.1f}%")
                precision_neg_var.set(f"{precision[1]*100:.1f}%")
                precision_neu_var.set(f"{precision[2]*100:.1f}%")

                recall_pos_var.set(f"{recall[0]*100:.1f}%")
                recall_neg_var.set(f"{recall[1]*100:.1f}%")
                recall_neu_var.set(f"{recall[2]*100:.1f}%")

                f1_pos_var.set(f"{f1[0]*100:.1f}%")
                f1_neg_var.set(f"{f1[1]*100:.1f}%")
                f1_neu_var.set(f"{f1[2]*100:.1f}%")

                cm = confusion_matrix(y_true, y_pred, labels=["Positive", "Neutral", "Negative"])
                for i in range(3):
                    for j in range(3):
                        cm_vars[i][j].set(str(cm[i, j]))

            else:
                messagebox.showinfo(
                    "Info",
                    "Analysis complete.\nNo manual labels found for validation."
                )

        except Exception as e:
            messagebox.showerror("Error", f"Error running analysis:\n{e}")

    ttk.Button(
        test_win,
        text="Run VADER Analysis",
        style="Action.TButton",
        command=run_vader_analysis
    ).grid(row=2, column=0, columnspan=3, pady=15, sticky="ew", padx=10)

    middle_frame = ttk.Frame(test_win, padding=10)
    middle_frame.grid(row=3, column=0, columnspan=3, sticky="nsew")

    donut_frame = ttk.Frame(middle_frame)
    donut_frame.grid(row=0, column=0, sticky="nw", padx=(0, 20))
    test_donut = donut_chart.DonutChart(donut_frame)
    test_donut.update(0, 0, 0)

    cm_frame = ttk.LabelFrame(middle_frame, text="Confusion Matrix", padding=10)
    cm_frame.grid(row=0, column=1, sticky="nw")

    explainer = ttk.Label(cm_frame,
        text="Rows = Actual sentiment, Columns = Predicted sentiment",
        font=("Arial", 8, "italic")
    )
    explainer.grid(row=0, column=0, columnspan=4, pady=(0, 5))

    labels = ["Positive", "Neutral", "Negative"]
    cm_vars = [[tk.StringVar(value="—") for _ in range(3)] for _ in range(3)]

    for j, label in enumerate(labels):
        ttk.Label(cm_frame, text=label).grid(row=1, column=j+1)

    for i, label in enumerate(labels):
        ttk.Label(cm_frame, text=label).grid(row=i+2, column=0)
        for j in range(3):
            ttk.Label(cm_frame, textvariable=cm_vars[i][j]).grid(row=i+2, column=j+1)

    metrics_frame = ttk.LabelFrame(test_win, text="Evaluation Metrics", padding=10)
    metrics_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
    
    for i in range(3):
        metrics_frame.grid_columnconfigure(i, weight=1)

    total_var = tk.StringVar(value="—")
    correct_var = tk.StringVar(value="—")
    accuracy_var = tk.StringVar(value="—")

    ttk.Label(metrics_frame, text="Total Entries:").grid(row=0, column=0, sticky="w")
    ttk.Label(metrics_frame, textvariable=total_var).grid(row=1, column=0, sticky="w")

    ttk.Label(metrics_frame, text="Total Correct:").grid(row=0, column=1, sticky="w")
    ttk.Label(metrics_frame, textvariable=correct_var).grid(row=1, column=1, sticky="w")

    ttk.Label(metrics_frame, text="Accuracy:").grid(row=0, column=2, sticky="w")
    ttk.Label(metrics_frame, textvariable=accuracy_var).grid(row=1, column=2, sticky="w")

    precision_pos_var = tk.StringVar(value="—")
    precision_neg_var = tk.StringVar(value="—")
    precision_neu_var = tk.StringVar(value="—")

    ttk.Label(metrics_frame, text="Precision Pos:").grid(row=2, column=0, sticky="w")
    ttk.Label(metrics_frame, textvariable=precision_pos_var).grid(row=3, column=0, sticky="w")

    ttk.Label(metrics_frame, text="Precision Neg:").grid(row=2, column=1, sticky="w")
    ttk.Label(metrics_frame, textvariable=precision_neg_var).grid(row=3, column=1, sticky="w")

    ttk.Label(metrics_frame, text="Precision Neu:").grid(row=2, column=2, sticky="w")
    ttk.Label(metrics_frame, textvariable=precision_neu_var).grid(row=3, column=2, sticky="w")

    recall_pos_var = tk.StringVar(value="—")
    recall_neg_var = tk.StringVar(value="—")
    recall_neu_var = tk.StringVar(value="—")

    ttk.Label(metrics_frame, text="Recall Pos:").grid(row=4, column=0, sticky="w")
    ttk.Label(metrics_frame, textvariable=recall_pos_var).grid(row=5, column=0, sticky="w")

    ttk.Label(metrics_frame, text="Recall Neg:").grid(row=4, column=1, sticky="w")
    ttk.Label(metrics_frame, textvariable=recall_neg_var).grid(row=5, column=1, sticky="w")

    ttk.Label(metrics_frame, text="Recall Neu:").grid(row=4, column=2, sticky="w")
    ttk.Label(metrics_frame, textvariable=recall_neu_var).grid(row=5, column=2, sticky="w")

    f1_pos_var = tk.StringVar(value="—")
    f1_neg_var = tk.StringVar(value="—")
    f1_neu_var = tk.StringVar(value="—")

    ttk.Label(metrics_frame, text="F1 Pos:").grid(row=6, column=0, sticky="w")
    ttk.Label(metrics_frame, textvariable=f1_pos_var).grid(row=7, column=0, sticky="w")

    ttk.Label(metrics_frame, text="F1 Neg:").grid(row=6, column=1, sticky="w")
    ttk.Label(metrics_frame, textvariable=f1_neg_var).grid(row=7, column=1, sticky="w")

    ttk.Label(metrics_frame, text="F1 Neu:").grid(row=6, column=2, sticky="w")
    ttk.Label(metrics_frame, textvariable=f1_neu_var).grid(row=7, column=2, sticky="w")

    test_win.grid_columnconfigure(0, weight=0)
    test_win.grid_columnconfigure(1, weight=1)
    test_win.grid_columnconfigure(2, weight=1)