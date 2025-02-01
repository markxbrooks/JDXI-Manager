from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap
from PySide6.QtWidgets import QWidget

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap
from PySide6.QtWidgets import QWidget


from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap
from PySide6.QtWidgets import QWidget


from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor, QPixmap
from PySide6.QtWidgets import QWidget


class ADSRPlot2(QWidget):
    def __init__(self):
        super().__init__()
        self.envelope = {
            "attackTime": 100,
            "decayTime": 400,
            "releaseTime": 100,
            "initialAmpl": 0,
            "peakAmpl": 1,
            "sustainAmpl": 0.8,
        }
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)
        self.plot_envelope()

    def plot_envelope(self):
        attack_time = self.envelope["attackTime"] / 1000
        decay_time = self.envelope["decayTime"] / 1000
        release_time = self.envelope["releaseTime"] / 1000
        sustain_amplitude = self.envelope["sustainAmpl"]
        peak_amplitude = self.envelope["peakAmpl"]
        initial_amplitude = self.envelope["initialAmpl"]

        attack_samples = int(attack_time * 44100)
        decay_samples = int(decay_time * 44100)
        sustain_samples = int(44100 * 2)  # Sustain for 2 seconds
        release_samples = int(release_time * 44100)

        envelope = np.concatenate(
            [
                np.linspace(initial_amplitude, peak_amplitude, attack_samples),
                np.linspace(peak_amplitude, sustain_amplitude, decay_samples),
                np.full(sustain_samples, sustain_amplitude),
                np.linspace(sustain_amplitude, 0, release_samples),
            ]
        )

        time = np.linspace(0, len(envelope) / 44100, len(envelope))

        self.ax.clear()
        self.ax.plot(time, envelope)
        self.ax.set_xlabel("Time [s]")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title("ADSR Envelope")
        self.canvas.draw()

    def set_values(self, envelope):
        self.envelope = envelope
        self.plot_envelope()


class ADSRPlotOld(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.border = 15
        self.bgColor = self.palette().color(self.backgroundRole())
        self.pixmap = QPixmap(self.size())
        self.envelope = None  # Initialize envelope attribute

    def setValues(self, envelope):
        self.envelope = envelope
        self.refreshPixmap()

    def refreshPixmap(self):
        if not self.envelope:
            return

        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(self.bgColor)

        painter = QPainter(self.pixmap)
        penWave = QPen(QColor(0, 0, 0))
        penWave.setStyle(Qt.SolidLine)
        penWave.setWidth(2)

        penGrid = QPen(QColor(150, 150, 150))
        penGrid.setStyle(Qt.DashLine)
        penGrid.setWidth(1)

        penBorder = QPen(QColor(0, 0, 0))
        penBorder.setStyle(Qt.SolidLine)
        penBorder.setWidth(1)

        ww = self.width() - 2 * self.border
        wh = self.height() - 2 * self.border

        total = 1.5 * (
            self.envelope.attackTime
            + self.envelope.decayTime
            + self.envelope.releaseTime
        )
        attackx = self.border + int(ww * self.envelope.attackTime / total)
        decayx = attackx + int(ww * self.envelope.decayTime / total)
        releasex = self.border + int(ww * (1 - self.envelope.releaseTime / total))

        initialy = self.height() - self.border - int(wh * self.envelope.initialAmpl)
        peaky = self.height() - self.border - int(wh * self.envelope.peakAmpl)
        sustainy = self.height() - self.border - int(wh * self.envelope.sustainAmpl)

        painter.setPen(penGrid)
        painter.drawLine(self.border, initialy, ww + self.border, initialy)
        painter.drawLine(self.border, sustainy, ww + self.border, sustainy)
        painter.drawLine(self.border, peaky, ww + self.border, peaky)
        painter.drawLine(attackx, self.border / 2, attackx, wh + self.border)
        painter.drawLine(decayx, self.border / 2, decayx, wh + self.border)
        painter.drawLine(releasex, self.border / 2, releasex, wh + self.border)

        painter.setPen(penBorder)
        painter.drawText(self.border / 4, initialy + 5, "I")
        painter.drawText(self.border / 4, sustainy + 5, "S")
        painter.drawText(self.border / 4, peaky + 5, "P")
        painter.drawText(attackx / 2, wh + self.border * 2, "A")
        painter.drawText((attackx + decayx) / 2, wh + self.border * 2, "D")
        painter.drawText((ww + self.border + releasex) / 2, wh + self.border * 2, "R")

        painter.drawLine(
            self.border,
            self.height() - self.border,
            self.width() - self.border,
            self.height() - self.border,
        )
        painter.drawLine(
            self.border, self.border, self.border, self.height() - self.border
        )

        painter.setPen(penWave)
        painter.drawLine(self.border, initialy, attackx, peaky)
        painter.drawLine(attackx, peaky, decayx, sustainy)
        painter.drawLine(decayx, sustainy, releasex, sustainy)
        painter.drawLine(releasex, sustainy, self.border + ww, self.border + wh)

        painter.end()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        super().paintEvent(event)

    def resizeEvent(self, event):
        self.refreshPixmap()
        super().resizeEvent(event)
