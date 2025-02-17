"""
ADSR Widget
Editing ADSR parameters
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLabel, QSpinBox, QDoubleSpinBox, QGridLayout

from jdxi_manager.ui.widgets.adsr_plot import ADSRPlot


class ADSRWidget(QWidget):
    envelopeChanged = Signal(dict)

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
        self.setMinimumHeight(150)  # Adjust height as needed
        self.attack_sb = self.create_spinbox(
            0, 1000, " ms", self.envelope["attackTime"]
        )
        self.decay_sb = self.create_spinbox(0, 1000, " ms", self.envelope["decayTime"])
        self.release_sb = self.create_spinbox(
            0, 1000, " ms", self.envelope["releaseTime"]
        )
        self.initial_sb = self.create_double_spinbox(
            0, 1, 0.01, self.envelope["initialAmpl"]
        )
        self.peak_sb = self.create_double_spinbox(0, 1, 0.01, self.envelope["peakAmpl"])
        self.sustain_sb = self.create_double_spinbox(
            0, 1, 0.01, self.envelope["sustainAmpl"]
        )
        self.setStyleSheet(
            """
                    QSpinBox {
                           font-family: Myriad Pro, sans-serif;
                           font-size: 10px;
                    }
                           QDoubleSpinBox {
                           font-family: Myriad Pro, sans-serif;
                           font-size: 10px;
                    }
                    QSlider::groove:vertical {
                        background: red;
                        width: 6px;
                        border-radius: 3px;
                    }
                    
                    QSlider::handle:vertical {
                        background: gray;
                        border: 1px solid darkgray;
                        width: 14px;
                        height: 14px;
                        margin: -6px 0;
                        border-radius: 7px;
                    }
                """
        )
        self.plot = ADSRPlot()

        self.layout = QGridLayout(self)
        self.layout.addWidget(QLabel("Attack:"), 0, 0)
        self.layout.addWidget(self.attack_sb, 0, 1)
        self.layout.addWidget(QLabel("Decay:"), 1, 0)
        self.layout.addWidget(self.decay_sb, 1, 1)
        self.layout.addWidget(QLabel("Release:"), 2, 0)
        self.layout.addWidget(self.release_sb, 2, 1)
        self.layout.addWidget(QLabel("Initial:"), 0, 2)
        self.layout.addWidget(self.initial_sb, 0, 3)
        self.layout.addWidget(QLabel("Peak:"), 1, 2)
        self.layout.addWidget(self.peak_sb, 1, 3)
        self.layout.addWidget(QLabel("Sustain:"), 2, 2)
        self.layout.addWidget(self.sustain_sb, 2, 3)
        self.layout.addWidget(self.plot, 0, 4, 4, 1)
        self.layout.setColumnMinimumWidth(4, 150)

        self.attack_sb.valueChanged.connect(self.valueChanged)
        self.decay_sb.valueChanged.connect(self.valueChanged)
        self.release_sb.valueChanged.connect(self.valueChanged)
        self.initial_sb.valueChanged.connect(self.valueChanged)
        self.peak_sb.valueChanged.connect(self.valueChanged)
        self.sustain_sb.valueChanged.connect(self.valueChanged)

        self.setLayout(self.layout)
        self.plot.set_values(self.envelope)

    def create_spinbox(self, min_value, max_value, suffix, value):
        sb = QSpinBox()
        sb.setRange(min_value, max_value)
        sb.setSuffix(suffix)
        sb.setValue(value)
        return sb

    def create_double_spinbox(self, min_value, max_value, step, value):
        sb = QDoubleSpinBox()
        sb.setRange(min_value, max_value)
        sb.setSingleStep(step)
        sb.setValue(value)
        return sb

    def valueChanged(self):
        self.envelope["attackTime"] = self.attack_sb.value()
        self.envelope["decayTime"] = self.decay_sb.value()
        self.envelope["releaseTime"] = self.release_sb.value()
        self.envelope["initialAmpl"] = self.initial_sb.value()
        self.envelope["peakAmpl"] = self.peak_sb.value()
        self.envelope["sustainAmpl"] = self.sustain_sb.value()
        self.plot.set_values(self.envelope)
        self.envelopeChanged.emit(self.envelope)
