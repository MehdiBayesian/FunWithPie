import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import tkinter as tk
from tkinter import font
from showClock import Clock

class QuadrantDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quadrant Display")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.font_style = font.Font(family="Helvetica", size=16, weight="bold")

        # Create four frames for each quadrant
        self.top_left = tk.Frame(self.root, width=400, height=300, bg="lightblue")
        self.top_right = tk.Frame(self.root, width=400, height=300, bg="lightgreen")
        self.bottom_left = tk.Frame(self.root, width=400, height=300, bg="lightgrey")
        self.bottom_right = tk.Frame(self.root, width=400, height=300, bg="lightcoral")

        self.top_left.grid(row=0, column=0, sticky="nsew")
        self.top_right.grid(row=0, column=1, sticky="nsew")
        self.bottom_left.grid(row=1, column=0, sticky="nsew")
        self.bottom_right.grid(row=1, column=1, sticky="nsew")

    def update_top_left(self, draw_function, *args, **kwargs):
        """Update the top left quadrant with a custom draw function."""
        for widget in self.top_left.winfo_children():
            widget.destroy()
        draw_function(self.top_left, *args, **kwargs)

    def update_top_right(self, draw_function, *args, **kwargs):
        """Update the top right quadrant with a custom draw function."""
        for widget in self.top_right.winfo_children():
            widget.destroy()
        draw_function(self.top_right, *args, **kwargs)

    def update_bottom_left(self, draw_function, *args, **kwargs):
        """Update the bottom left quadrant with a custom draw function."""
        for widget in self.bottom_left.winfo_children():
            widget.destroy()
        draw_function(self.bottom_left, *args, **kwargs)

    def update_bottom_right(self, draw_function, *args, **kwargs):
        """Update the bottom right quadrant with a custom draw function."""
        for widget in self.bottom_right.winfo_children():
            widget.destroy()
        draw_function(self.bottom_right, *args, **kwargs)

    def run(self):
        """Run the main loop for the GUI."""
        self.root.mainloop()

def draw_message(frame, message):
    label = tk.Label(frame, text=message, font=("Helvetica", 16), bg=frame.cget("bg"))
    label.place(relx=0.5, rely=0.5, anchor="center")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_clock_with_matplotlib(frame):
    """Draw a clock using matplotlib and embed it in the tkinter frame."""
    # Create a figure for the clock
    fig, ax = plt.subplots(figsize=(4, 2))
    # Example usage:
    dt_now = datetime.now()
    # print(dt_now)
    now_date = dt_now.strftime('%Y-%m-%d')
    now_time = dt_now.strftime('%H:%M:%S')

    clock = Clock(time=now_time, date=now_date,
              title="Current Time",
              show_seconds=True, show_main_ticks_only=False,
              figure=fig, axis=ax
              )
    ax = clock.draw()
    # ax.text(0.5, 0.5, "12:34 PM", fontsize=24, ha='center', va='center')
    ax.axis('off')  # Remove axes for a cleaner look

    # Embed the figure in the tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()


# Example usage
if __name__ == "__main__":
    app = QuadrantDisplay()
    
    app.update_top_left(draw_clock_with_matplotlib)
    app.update_top_right(draw_message, "Stay awesome!")
    app.update_bottom_left(draw_message, "San Mateo")
    app.update_bottom_right(draw_message, "Temp: 22 \u00b0C")

    app.run()

