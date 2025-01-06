from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ...data import ARP

class ArpeggioEditor(QMainWindow):
    def __init__(self, midi_out=None):
        super().__init__()
        self.midi_out = midi_out
        self.setFixedSize(480, 340)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
    def set_midi_ports(self, midi_in, midi_out):
        self.midi_in = midi_in
        self.midi_out = midi_out 