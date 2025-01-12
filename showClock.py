import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

class Clock:
    def __init__(self, time, date, title=None, show_seconds=True, show_main_ticks_only=False):
        # Convert the input date and time to a datetime object
        datetime_str = f"{date} {time}"
        self.dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        self.show_seconds = show_seconds
        self.show_main_ticks_only = show_main_ticks_only
        self.title = title

    def draw_clock_face(self, ax):
        # Draw clock circle
        clock_circle = plt.Circle((0, 0), 1, edgecolor='black', facecolor='white', lw=2)
        ax.add_artist(clock_circle)

        # Draw clock ticks (12-hour markers or just 12, 3, 6, 9)
        if self.show_main_ticks_only:
            clock_ticks = np.array([0, 3, 6, 9])
        else:
            clock_ticks = np.arange(0,12)
            
        for i in clock_ticks:  # All 12 markers
            angle = np.deg2rad(i * 30.0)
            x_start, y_start = 0.85*np.cos(angle), 0.85*np.sin(angle)
            x_end, y_end = np.cos(angle), np.sin(angle)
            ax.plot([x_start, x_end], [y_start, y_end], color='black', lw=2)

    def draw_clock_hands(self, ax):
        # Get the hour, minute, and second from the input datetime
        hour = self.dt.hour % 12
        minute = self.dt.minute
        second = self.dt.second

        # Hour hand (shorter)
        hour_angle = np.deg2rad(90 - (hour + minute / 60) * 30)
        ax.plot([0, 0.5 * np.cos(hour_angle)], [0, 0.5 * np.sin(hour_angle)], color='black', lw=6)

        # Minute hand (longer)
        minute_angle = np.deg2rad(90 - (minute + second / 60) * 6)
        ax.plot([0, 0.9*np.cos(minute_angle)], [0, 0.9*np.sin(minute_angle)], color='black', lw=4)

        # Second hand (thinnest and fastest), if enabled
        if self.show_seconds:
            second_angle = np.deg2rad(90 - second*6)
            cs, sn = np.cos(second_angle), np.sin(second_angle)
            # set extension_len = 0.1 to zero so seconds arm start at (0,0)
            extension_len = 0.1
            ax.plot([0-extension_len*cs, 0.8*cs], [0-extension_len*sn, 0.8*sn], color='red', lw=2)

    def display_title(self, ax): 
        if self.title:
            ax.text(0, 1.3, f"{self.title}", 
                    horizontalalignment='center', 
                    verticalalignment='center', fontsize=18
                   )
            
    def draw(self):
        # Create a figure and axis for drawing
        fig, ax = plt.subplots(figsize=(6,6))
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.set_facecolor('white')

        # Draw the clock components
        self.draw_clock_face(ax)
        self.draw_clock_hands(ax)
        self.display_title(ax)

        # Hide axis lines and ticks
        ax.axis('off')

        # Show clock
        plt.savefig('clockNow.jpg')
        plt.show()


# Example usage:
dt_now = datetime.now()
# print(dt_now)
now_date = dt_now.strftime('%Y-%m-%d')
now_time = dt_now.strftime('%H:%M:%S')

clock = Clock(time=now_time, date=now_date, 
              title="Current Time", 
              show_seconds=True, show_main_ticks_only=False
             )
clock.draw()
