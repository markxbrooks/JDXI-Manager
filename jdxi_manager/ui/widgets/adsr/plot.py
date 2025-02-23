"""
ADSR Plot
==========

This module defines the `ADSRPlot` class, a QWidget subclass that visualizes an ADSR (Attack,
Decay, Sustain, Release) envelope using Matplotlib. The plot displays the envelope's progression
over time, with adjustable parameters for attack, decay, sustain, and release times, as well as
initial, peak, and sustain amplitudes.

The plot is rendered in a QWidget, and the background and text colors are customized for better
visibility, with the envelope plotted in orange on a dark gray background.

Classes:
--------
- `ADSRPlot`: A QWidget subclass that generates and displays an ADSR envelope plot.

Methods:
--------
- `__init__(self)`: Initializes the widget and sets up the figure and layout for the plot.
- `plot_envelope(self)`: Generates and plots the ADSR envelope based on the current envelope parameters.
- `set_values(self, envelope)`: Updates the envelope parameters and refreshes the plot.

Customization:
-------------
- The plot background is dark gray (`#333333`), with all plot elements (ticks, labels, title) in
  orange for better visibility against the dark background.
- The time is represented in seconds, and the amplitude in a range from 0 to 1.
"""


import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt

import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath
from PySide6.QtCore import Qt

import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt


class ADSRPlot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Default envelope parameters (times in ms)
        self.envelope = {
            "attack_time": 100,
            "decay_time": 400,
            "release_time": 100,
            "initial_level": 0,
            "peak_level": 1,
            "sustain_level": 0.8,
        }
        # Set a fixed size for the widget (or use layouts as needed)
        self.setMinimumSize(400, 400)
        # Use dark gray background
        self.setStyleSheet("""
        QWidget {
            background-color: #333333;
        }
        """)
        # Sample rate for converting times to samples
        self.sample_rate = 44100

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Use orange for drawing
        pen = QPen(QColor("orange"))
        axis_pen = QPen(QColor("white"))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setFont(QFont("Consolas", 10))

        # Compute envelope segments in seconds
        attack_time = self.envelope["attack_time"] / 1000.0
        decay_time = self.envelope["decay_time"] / 1000.0
        release_time = self.envelope["release_time"] / 1000.0
        sustain_level = self.envelope["sustain_level"]
        peak_level = self.envelope["peak_level"]
        initial_level = self.envelope["initial_level"]

        # Convert times to sample counts (for internal computation)
        attack_samples = int(attack_time * self.sample_rate)
        decay_samples = int(decay_time * self.sample_rate)
        sustain_samples = int(self.sample_rate * 2)  # Fixed 2 seconds sustain
        release_samples = int(release_time * self.sample_rate)

        # Construct the ADSR envelope as one concatenated array
        attack = np.linspace(initial_level, peak_level, attack_samples, endpoint=False)
        decay = np.linspace(peak_level, sustain_level, decay_samples, endpoint=False)
        sustain = np.full(sustain_samples, sustain_level)
        release = np.linspace(sustain_level, 0, release_samples)

        envelope = np.concatenate([attack, decay, sustain, release])
        total_samples = len(envelope)
        total_time = 5 # in seconds total_samples / self.sample_rate  # in seconds

        # Prepare points for drawing
        # Map time (x) to widget width and amplitude (y) to widget height (inverting y)
        w = self.width()
        h = self.height()
        # Leave some padding for axes labels (optional)
        padding = 60
        plot_w = w - 2 * padding
        plot_h = h - 2 * padding

        # Create a list of points for the envelope polyline.
        points = []
        # We'll sample a fixed number of points for efficiency
        num_points = 500
        indices = np.linspace(0, total_samples - 1, num_points).astype(int)
        for i in indices:
            t = i / self.sample_rate  # time in seconds
            # x coordinate: map [0, total_time] to [padding, padding+plot_w]
            x = padding + (t / total_time) * plot_w
            # y coordinate: map amplitude [0, 1] to [padding+plot_h, padding] (invert y)
            y = padding + plot_h - (envelope[i] * plot_h)
            points.append((x, y))

        # Draw the envelope polyline
        if points:
            # Convert points to QPainterPath
            from PySide6.QtGui import QPainterPath
            path = QPainterPath()
            first_point = points[0]
            path.moveTo(*first_point)
            for pt in points[1:]:
                path.lineTo(*pt)
            painter.drawPath(path)

        # Optionally draw axis lines and labels
        painter.setPen(axis_pen)
        painter.drawLine(padding, padding, padding, padding + plot_h)  # Y-axis
        painter.drawLine(padding, padding + plot_h, padding + plot_w, padding + plot_h)  # X-axis
        painter.drawText(padding - 30, padding + plot_h + 5, "0s")
        for i in range(1, 5):
            x = padding + i * plot_w / 5
            painter.drawLine(x, padding + plot_h, x, padding + plot_h + 5)
            painter.drawText(x - 10, padding + plot_h + 20, f"{i}s")
        for i in range(1, 5):
            y = padding + i * plot_h / 5
            painter.drawLine(padding, y, padding - 5, y)
            painter.drawText(padding - 35, y + 5, f"{1 - i * 0.2:.1f}")
        painter.drawText(padding - 35, padding + 5, "1")
        painter.drawText(padding - 35, padding + plot_h, "0")

    def set_values(self, envelope):
        """Update envelope values and trigger a redraw."""
        self.envelope = envelope
        self.update()


class ADSRMatplot(QWidget):
    def __init__(self):
        super().__init__()
        self.envelope = {
            "attack_time": 100,
            "decay_time": 400,
            "release_time": 100,
            "initial_level": 0,
            "peak_level": 1,
            "sustain_level": 0.8,
        }

        # Set font globally
        plt.rcParams["font.family"] = "Consolas"

        # Create the figure and axis
        self.figure, self.ax = plt.subplots(figsize=(4, 4))
        self.ax.set_facecolor("#333333")  # Dark gray background
        self.figure.patch.set_facecolor("#333333")  # Background color for the figure

        # Create canvas and layout
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        # Plot the envelope
        self.plot_envelope()

    def plot_envelope(self):
        """ Draw matplotlib plot in JDXI style"""
        self.ax.clear()  # Clear previous plot
        self.ax.set_facecolor("#333333")  # Ensure background stays dark gray

        # Adjust tick and label colors for visibility
        self.ax.tick_params(axis="both", colors="orange")
        self.ax.xaxis.label.set_color("orange")
        self.ax.yaxis.label.set_color("orange")
        self.ax.title.set_color("orange")
        self.ax.set_xlim(0, 5)

        # Extract envelope parameters
        attack_time = self.envelope["attack_time"] / 1000
        decay_time = self.envelope["decay_time"] / 1000
        release_time = self.envelope["release_time"] / 1000
        sustain_level = self.envelope["sustain_level"]
        peak_level = self.envelope["peak_level"]
        initial_level = self.envelope["initial_level"]

        # Convert to samples (assuming a 44.1 kHz sample rate)
        attack_samples = int(attack_time * 44100)
        decay_samples = int(decay_time * 44100)
        sustain_samples = int(44100 * 2)  # Sustain for 2 seconds
        release_samples = int(release_time * 44100)

        # Construct ADSR envelope
        envelope = np.concatenate([
            np.linspace(initial_level, peak_level, attack_samples),
            np.linspace(peak_level, sustain_level, decay_samples),
            np.full(sustain_samples, sustain_level),
            np.linspace(sustain_level, 0, release_samples)
        ])

        time = np.linspace(0, len(envelope) / 44100, len(envelope))

        # Plot envelope with orange color
        self.ax.plot(time, envelope, color="orange", linewidth=2)
        self.ax.set_xlabel("Time [s]")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title("ADSR Envelope")

        self.canvas.draw()

    def set_values(self, envelope):
        """Update envelope values and refresh the plot."""
        self.envelope = envelope
        self.plot_envelope()
