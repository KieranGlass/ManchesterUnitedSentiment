from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DonutChart:
    def __init__(self, parent_frame, bg_color="#ffdddd"):
        self.parent_frame = parent_frame
        self.bg_color = bg_color

        # self.fig, self.ax = plt.subplots(figsize=(3, 3), dpi=100, facecolor=self.bg_color)
        
        self.fig = Figure(figsize=(3, 3), dpi=100, facecolor=self.bg_color)
        self.ax = self.fig.add_subplot(111)
         
        self.ax.set_facecolor(self.bg_color)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, padx=10, pady=10)

        # Draw initial empty donut (0%)
        self.update(0, 0, 0)

    def update(self, positive_percent, negative_percent, neutral_percent):
        
        self.ax.clear()
        self.ax.set_facecolor(self.bg_color)

        values = [positive_percent, negative_percent, neutral_percent]
        total = sum(values)

        if total == 0:
            values = [1]
            colors = ["#e0e0e0"]
            self.ax.pie(
                values,
                startangle=90,
                colors=colors,
                wedgeprops=dict(width=0.3, edgecolor="black")
            )

            self.ax.text(
                0, 0,
                "0%",
                ha="center",
                va="center",
                fontsize=16,
                fontweight="bold"
            )
        else:
            colors = ["#4caf50", "#f44336", "#9e9e9e"]

            self.ax.pie(
                values,
                startangle=90,
                colors=colors,
                wedgeprops=dict(width=0.3, edgecolor="black")
            )

            self.ax.text(
                0, 0.25,
                f"{positive_percent:.0f}%",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
                color="#4caf50"
            )

            self.ax.text(
                0, 0.0,
                f"{neutral_percent:.0f}%",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
                color="#9e9e9e"
            )

            self.ax.text(
                0, -0.25,
                f"{negative_percent:.0f}%",
                ha="center",
                va="center",
                fontsize=14,
                fontweight="bold",
                color="#f44336"
            )
            
        self.ax.axis("equal")
        self.canvas.draw()