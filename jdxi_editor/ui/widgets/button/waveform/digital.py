from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal
from jdxi_editor.midi.data.constants.constants import Waveform
from PIL import Image, ImageDraw
import base64
from io import BytesIO


class DigitalWaveformButton(WaveformButton):
    """Button for selecting oscillator waveform"""
    
    waveform_selected = Signal(Waveform)  # Emits selected waveform
    
    def __init__(self, waveform: Waveform, style="digital", parent=None):
        """Initialize waveform button
        
        Args:
            waveform: Waveform enum value
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Style
        self.setMinimumWidth(60)
        self.setStyleSheet("""
            QPushButton {
                background-color: #222222;
                color: #CCCCCC;
                border: 1px solid #666666;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:checked {
                background-color: #333333;
                color: white;
                border: 1px solid #FF4444;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)




