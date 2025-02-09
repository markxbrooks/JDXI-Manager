from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QComboBox,
    QLabel, QPushButton, QFrame, QCheckBox, QGroupBox, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QColor
import logging
import qtawesome as qta

from .style import Style
from ..midi import MIDIHelper


class MIDIConfigDialog(QDialog):
    def __init__(self, input_ports, output_ports, current_in=None, current_out=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MIDI Configuration")
        self.setMinimumSize(300, 300)
        self.setStyleSheet(Style.EDITOR_STYLE)
        self.input_ports = input_ports
        self.output_ports = output_ports
        self.current_in = current_in
        self.current_out = current_out
        
        # Create an instance of MIDIHelper
        self.midi_helper = MIDIHelper()

        self._create_ui()
        
    def _create_ui(self):
        """Create the dialog UI"""
        layout = QVBoxLayout(self)
        
        # Input port selection
        input_group = QGroupBox("MIDI Input")
        input_layout = QVBoxLayout(input_group)

        icons_hlayout = QHBoxLayout()
        for icon in ["mdi6.midi-port"]:
            icon_label = QLabel()
            icon = qta.icon(icon)
            pixmap = icon.pixmap(Style.ICON_SIZE, Style.ICON_SIZE)  # Set the desired size
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignHCenter)
            icons_hlayout.addWidget(icon_label)
        input_layout.addLayout(icons_hlayout)
        
        self.input_combo = QComboBox()
        self.input_combo.addItems(self.input_ports)
        if self.current_in and self.current_in in self.input_ports:
            self.input_combo.setCurrentText(self.current_in)
            
        input_layout.addWidget(self.input_combo)
        layout.addWidget(input_group)
        
        # Output port selection
        output_group = QGroupBox("MIDI Output")
        output_layout = QVBoxLayout(output_group)

        icons_hlayout = QHBoxLayout()
        for icon in ["mdi6.midi-port"]:
            icon_label = QLabel()
            icon = qta.icon(icon)
            pixmap = icon.pixmap(Style.ICON_SIZE, Style.ICON_SIZE)  # Set the desired size
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignHCenter)
            icons_hlayout.addWidget(icon_label)
        output_layout.addLayout(icons_hlayout)
        
        self.output_combo = QComboBox()
        self.output_combo.addItems(self.output_ports)
        if self.current_out and self.current_out in self.output_ports:
            self.output_combo.setCurrentText(self.current_out)
            
        output_layout.addWidget(self.output_combo)
        layout.addWidget(output_group)
        
        # Refresh button
        refresh_button = QPushButton("Refresh Ports")
        refresh_button.clicked.connect(self.refresh_ports)
        layout.addWidget(refresh_button)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def refresh_ports(self):
        """Refresh the list of MIDI ports"""
        # Use the MIDIHelper instance to get the updated port lists
        self.input_ports = self.midi_helper.get_input_ports()
        self.output_ports = self.midi_helper.get_output_ports()

        # Update the combo boxes
        self.input_combo.clear()
        self.input_combo.addItems(self.input_ports)
        self.output_combo.clear()
        self.output_combo.addItems(self.output_ports)

    def get_input_port(self) -> str:
        """Get selected input port name
        
        Returns:
            Selected input port name or empty string if none selected
        """
        return self.input_combo.currentText()

    def get_output_port(self) -> str:
        """Get selected output port name
        
        Returns:
            Selected output port name or empty string if none selected
        """
        return self.output_combo.currentText()

    def get_settings(self) -> dict:
        """Get all selected settings
        
        Returns:
            Dictionary containing input_port and output_port selections
        """
        return {
            'input_port': self.get_input_port(),
            'output_port': self.get_output_port()
        } 