from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QComboBox,
    QLabel, QPushButton, QFrame, QCheckBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette, QColor
import logging

from ..midi import MIDIHelper
from .style import Style

class MidiConfigFrame(QDialog):
    portsChanged = Signal(object, object)  # (midi_in, midi_out)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MIDI Configuration")
        self.setFixedSize(400, 390)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # MIDI Input section
        input_frame = self._create_section("MIDI Input", Style.COM_BG)
        self.input_port = QComboBox()
        ports = MIDIHelper.get_input_ports()
        self.input_port.addItems(ports)
        if not ports:
            logging.warning("No MIDI input ports found")
        input_frame.layout().addWidget(self.input_port)
        
        # Input options
        self.thru_enabled = QCheckBox("MIDI Thru")
        self.thru_enabled.setToolTip("Forward incoming MIDI messages to output")
        input_frame.layout().addWidget(self.thru_enabled)
        
        layout.addWidget(input_frame)
        
        # MIDI Output section
        output_frame = self._create_section("MIDI Output", Style.COM_BG)
        self.output_port = QComboBox()
        ports = MIDIHelper.get_output_ports()
        self.output_port.addItems(ports)
        if not ports:
            logging.warning("No MIDI output ports found")
        output_frame.layout().addWidget(self.output_port)
        
        # Output options
        self.auto_load = QCheckBox("Auto-load patches")
        self.auto_load.setToolTip("Automatically request patch data when switching editors")
        output_frame.layout().addWidget(self.auto_load)
        
        layout.addWidget(output_frame)
        
        # Status section
        status_frame = self._create_section("Status", Style.COM_BG)
        self.status_label = QLabel("Not connected")
        status_frame.layout().addWidget(self.status_label)
        layout.addWidget(status_frame)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.refresh_btn = QPushButton("Refresh Ports")
        self.refresh_btn.clicked.connect(self._refresh_ports)
        button_layout.addWidget(self.refresh_btn)
        
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.clicked.connect(self._test_connection)
        button_layout.addWidget(self.test_btn)
        
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self._apply_settings)
        button_layout.addWidget(self.apply_btn)
        
        layout.addLayout(button_layout)
        
        logging.info("MIDI configuration dialog initialized")
        
    def _create_section(self, title, color):
        """Create a section frame with header"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        
        # Header
        header = QFrame()
        header.setFixedHeight(24)
        header.setAutoFillBackground(True)
        
        palette = header.palette()
        # Convert color string to QColor
        palette.setColor(QPalette.Window, QColor(color))
        header.setPalette(palette)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(6, 0, 6, 0)
        
        label = QLabel(title)
        label.setStyleSheet("color: white; font-weight: bold;")
        header_layout.addWidget(label)
        
        layout.addWidget(header)
        return frame
        
    def _refresh_ports(self):
        """Refresh the available MIDI ports"""
        try:
            logging.debug("Refreshing MIDI ports")
            current_in = self.input_port.currentText()
            current_out = self.output_port.currentText()
            
            self.input_port.clear()
            self.output_port.clear()
            
            in_ports = MIDIHelper.get_input_ports()
            out_ports = MIDIHelper.get_output_ports()
            
            self.input_port.addItems(in_ports)
            self.output_port.addItems(out_ports)
            
            # Restore previous selections if still available
            in_idx = self.input_port.findText(current_in)
            out_idx = self.output_port.findText(current_out)
            
            if in_idx >= 0:
                self.input_port.setCurrentIndex(in_idx)
                logging.debug(f"Restored input port: {current_in}")
            else:
                logging.info(f"Previous input port {current_in} no longer available")
                
            if out_idx >= 0:
                self.output_port.setCurrentIndex(out_idx)
                logging.debug(f"Restored output port: {current_out}")
            else:
                logging.info(f"Previous output port {current_out} no longer available")
                
            self.status_label.setText("Ports refreshed")
            logging.info(f"Found {len(in_ports)} input ports and {len(out_ports)} output ports")
            
        except Exception as e:
            msg = f"Error refreshing ports: {str(e)}"
            logging.error(msg)
            self.status_label.setText(msg)
            
    def _test_connection(self):
        """Test MIDI connection by sending identity request"""
        try:
            port_name = self.output_port.currentText()
            logging.debug(f"Testing connection to {port_name}")
            
            midi_out = MIDIHelper.open_output(port_name)
            if midi_out:
                # Send identity request message
                msg = MIDIHelper.create_identity_request()
                midi_out.send_message(msg)
                status = "Test message sent"
                logging.info(f"Sent test message to {port_name}")
                midi_out.close()
            else:
                status = "Could not open output port"
                logging.error(f"Failed to open output port {port_name}")
                
            self.status_label.setText(status)
            
        except Exception as e:
            msg = f"Test failed: {str(e)}"
            logging.error(msg)
            self.status_label.setText(msg)
            
    def _apply_settings(self):
        """Apply the MIDI settings"""
        try:
            in_port = self.input_port.currentText()
            out_port = self.output_port.currentText()
            
            logging.debug(f"Opening MIDI ports - In: {in_port}, Out: {out_port}")
            
            midi_in = MIDIHelper.open_input(in_port)
            midi_out = MIDIHelper.open_output(out_port)
            
            if midi_in and midi_out:
                status = "Connected"
                logging.info(f"Successfully connected to {in_port} and {out_port}")
                self.portsChanged.emit(midi_in, midi_out)
                self.accept()
            else:
                status = "Connection failed"
                if not midi_in:
                    logging.error(f"Failed to open input port {in_port}")
                if not midi_out:
                    logging.error(f"Failed to open output port {out_port}")
                    
            self.status_label.setText(status)
            
        except Exception as e:
            msg = f"Connection error: {str(e)}"
            logging.error(msg)
            self.status_label.setText(msg)
            
    def get_settings(self):
        """Get current MIDI settings"""
        return {
            'input_port': self.input_port.currentText(),
            'output_port': self.output_port.currentText(),
            'thru_enabled': self.thru_enabled.isChecked(),
            'auto_load': self.auto_load.isChecked()
        }
        
    def set_settings(self, settings):
        """Apply saved MIDI settings"""
        if 'input_port' in settings:
            idx = self.input_port.findText(settings['input_port'])
            if idx >= 0:
                self.input_port.setCurrentIndex(idx)
                
        if 'output_port' in settings:
            idx = self.output_port.findText(settings['output_port'])
            if idx >= 0:
                self.output_port.setCurrentIndex(idx)
                
        if 'thru_enabled' in settings:
            self.thru_enabled.setChecked(settings['thru_enabled'])
            
        if 'auto_load' in settings:
            self.auto_load.setChecked(settings['auto_load']) 