from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFrame, QLabel, QComboBox, QCheckBox, QPushButton,
    QScrollArea, QGroupBox
)
from PySide6.QtCore import Qt
import logging
from typing import Optional

from jdxi_manager.midi.constants.sysex import ARPEGGIO_AREA
from jdxi_manager.ui.style import Style
from jdxi_manager.ui.widgets import Slider
from jdxi_manager.midi.messages import JDXiSysEx
from jdxi_manager.midi.constants.arpeggio import (
    ArpGrid,
    ArpDuration,
    ArpOctaveRange,
    ArpSwitch,
    ARP_AREA,
    ARP_PART,
    ARP_GROUP,
    ArpParameters
)
from jdxi_manager.midi import MIDIHelper
from jdxi_manager.ui.editors.base_editor import BaseEditor

class ArpeggioEditor(BaseEditor):
    def __init__(self, midi_helper: Optional[MIDIHelper] = None, parent: Optional[QWidget] = None):
        super().__init__(midi_helper, parent)
        self.setWindowTitle("Arpeggio")
        if self.midi_helper:
            print("Midi helper available")
        else:
            print("No Midi helper available!")
        # Allow resizing
        self.setMinimumSize(400, 300)  # Set minimum size
        self.resize(800, 600)  # Set default size
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create container widget
        container = QWidget()
        container_layout = QVBoxLayout()
        container.setLayout(container_layout)
        
        # Add custom style for arpeggiator groups
        container.setStyleSheet("""
            QGroupBox {
                border: 1px solid #FF0000;  /* Red border */
                border-radius: 3px;
                margin-top: 1.5ex;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                color: #FFFFFF;
                background-color: #1A1A1A;
            }
        """)
        
        # Add switch control at the top
        switch_row = QHBoxLayout()
        switch_label = QLabel("Arpeggiator:")
        self.switch_button = QPushButton("OFF")
        self.switch_button.setCheckable(True)
        self.switch_button.clicked.connect(self._on_switch_changed)
        switch_row.addWidget(switch_label)
        switch_row.addWidget(self.switch_button)
        container_layout.insertLayout(0, switch_row)  # Add at top
        
        # Add sections
        container_layout.addWidget(self._create_pattern_section())
        container_layout.addWidget(self._create_timing_section())
        container_layout.addWidget(self._create_velocity_section())
        
        # Add container to scroll area
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        
        # Set up area and part for parameter requests
        self.area = ARP_AREA
        self.part = ARP_PART
        self.group = ARP_GROUP
        self.start_param = 0x00
        self.param_size = 0x40  # Request arpeggiator parameters
        
        # ... rest of initialization ...
        
    def _update_ui_from_sysex(self, addr, data):
        """Update UI controls based on received SysEx data"""
        try:
            section = addr[2]  # Arpeggio section in third byte
            param = addr[3]    # Parameter number
            value = data[0]    # Parameter value
            
            # Update appropriate arpeggio section
            if section == 0x00:  # Common parameters
                self._update_common_controls(param, value)
            elif section == 0x10:  # Pattern parameters
                self._update_pattern_controls(param, value)
            elif section == 0x20:  # Rhythm parameters
                self._update_rhythm_controls(param, value)
                
        except Exception as e:
            logging.error(f"Error updating arpeggio UI: {str(e)}") 

    def _create_pattern_section(self):
        """Create the arpeggio pattern section"""
        group = QFrame()
        group.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        # Pattern type selection
        pattern_row = QHBoxLayout()
        pattern_label = QLabel("Pattern:")
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems([
            "UP", "DOWN", "UP/DOWN", "RANDOM", 
            "NOTE ORDER", "MOTIF", "PHRASE"
        ])
        self.pattern_combo.currentIndexChanged.connect(self._on_pattern_changed)
        pattern_row.addWidget(pattern_label)
        pattern_row.addWidget(self.pattern_combo)
        layout.addLayout(pattern_row)
        
        # Octave range
        octave_row = QHBoxLayout()
        octave_label = QLabel("Octave Range:")
        self.octave_combo = QComboBox()
        self.octave_combo.addItems([
            octave.display_name for octave in ArpOctaveRange
        ])
        # Set default to 0
        self.octave_combo.setCurrentIndex(3)  # Index 3 is OCT_ZERO
        self.octave_combo.currentIndexChanged.connect(self._on_octave_changed)
        octave_row.addWidget(octave_label)
        octave_row.addWidget(self.octave_combo)
        layout.addLayout(octave_row)
        
        return group

    def _create_timing_section(self):
        """Create the arpeggio timing section"""
        group = QGroupBox("Timing")
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        # Grid settings
        grid_row = QHBoxLayout()
        grid_label = QLabel("Grid:")
        self.grid_combo = QComboBox()
        self.grid_combo.addItems([grid.display_name for grid in ArpGrid])
        self.grid_combo.currentIndexChanged.connect(self._on_grid_changed)
        grid_row.addWidget(grid_label)
        grid_row.addWidget(self.grid_combo)
        layout.addLayout(grid_row)
        
        # Duration settings
        duration_row = QHBoxLayout()
        duration_label = QLabel("Duration:")
        self.duration_combo = QComboBox()
        self.duration_combo.addItems([
            duration.display_name for duration in ArpDuration
        ])
        self.duration_combo.currentIndexChanged.connect(self._on_duration_changed)
        duration_row.addWidget(duration_label)
        duration_row.addWidget(self.duration_combo)
        layout.addLayout(duration_row)
        
        return group

    def _create_velocity_section(self):
        """Create the arpeggio velocity section"""
        group = QGroupBox("Velocity")
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        # Velocity settings
        self.velocity_slider = Slider("Velocity", 0, 127)
        self.velocity_slider.valueChanged.connect(self._on_velocity_changed)
        layout.addWidget(self.velocity_slider)
        
        # Accent settings
        self.accent_slider = Slider("Accent", 0, 127)
        self.accent_slider.valueChanged.connect(self._on_accent_changed)
        layout.addWidget(self.accent_slider)
        
        # Swing settings
        self.swing_slider = Slider("Swing", 0, 100)
        self.swing_slider.valueChanged.connect(self._on_swing_changed)
        layout.addWidget(self.swing_slider)
        
        return group

    def _on_pattern_changed(self, index):
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ARP_AREA,
                part=ARP_PART,
                group=ARP_GROUP,
                param=ArpParameters.PATTERN,
                value=index
            )

    def _on_octave_changed(self, index: int):
        """Handle octave range change"""
        if self.midi_helper:
            octave = ArpOctaveRange(index - 3)  # Convert index to -3 to +3 range
            logging.debug(f"Sending arp octave change: area={ARP_AREA:02x}, part={ARP_PART:02x}, group={ARP_GROUP:02x}, param={ArpParameters.OCTAVE_RANGE:02x}, value={octave.midi_value:02x}")
            self.midi_helper.send_parameter(
                area=ARP_AREA,
                part=ARP_PART,
                group=ARP_GROUP,
                param=ArpParameters.OCTAVE_RANGE,
                value=octave.midi_value
            )

    def _on_grid_changed(self, index: int):
        """Handle grid value change"""
        if self.midi_helper:
            grid = ArpGrid(index)
            logging.debug(f"Sending arp grid change: area={ARP_AREA:02x}, part={ARP_PART:02x}, group={ARP_GROUP:02x}, param={ArpParameters.GRID:02x}, value={grid.midi_value:02x}")
            self.midi_helper.send_parameter(
                area=ARP_AREA,
                part=ARP_PART,
                group=ARP_GROUP,
                param=ArpParameters.GRID,
                value=grid.midi_value
            )

    def _on_duration_changed(self, index: int):
        """Handle duration value change"""
        if self.midi_helper:
            duration = ArpDuration(index)
            logging.debug(f"Sending arp duration change: area={ARP_AREA:02x}, part={ARP_PART:02x}, group={ARP_GROUP:02x}, param={ArpParameters.DURATION:02x}, value={duration.midi_value:02x}")
            self.midi_helper.send_parameter(
                area=ARP_AREA,
                part=ARP_PART,
                group=ARP_GROUP,
                param=ArpParameters.DURATION,
                value=duration.midi_value
            )

    def _on_velocity_changed(self, value: int):
        """Handle velocity change"""
        if self.midi_helper:
            logging.debug(f"Sending arp velocity change: area={ARP_AREA:02x}, part={ARP_PART:02x}, group={ARP_GROUP:02x}, param={ArpParameters.VELOCITY:02x}, value={value:02x}")
            self.midi_helper.send_parameter(
                area=ARP_AREA,
                part=ARP_PART,
                group=ARP_GROUP,
                param=ArpParameters.VELOCITY,
                value=value
            )

    def _on_accent_changed(self, value: int):
        """Handle accent change"""
        if self.midi_helper:
            logging.debug(f"Sending arp accent change: area={ARP_AREA:02x}, part={ARP_PART:02x}, group={ARP_GROUP:02x}, param={ArpParameters.ACCENT:02x}, value={value:02x}")
            self.midi_helper.send_parameter(
                area=ARP_AREA,
                part=ARP_PART,
                group=ARP_GROUP,
                param=ArpParameters.ACCENT,
                value=value
            )

    def _on_swing_changed(self, value):
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ARP_AREA,
                part=ARP_PART,
                group=ARP_GROUP,
                param=ArpParameters.SWING,
                value=value
            )

    def _on_switch_changed(self, checked: bool):
        """Handle arpeggiator switch change"""
        if self.midi_helper:
            switch = ArpSwitch.ON if checked else ArpSwitch.OFF
            logging.debug(f"Sending arp switch change: area={ARP_AREA:02x}, part={ARP_PART:02x}, group={ARP_GROUP:02x}, param={ArpParameters.SWITCH:02x}, value={switch.midi_value:02x}")
            self.midi_helper.send_parameter(
                area=ARP_AREA,
                part=ARP_PART,
                group=ARP_GROUP,
                param=ArpParameters.SWITCH,
                value=switch.midi_value
            )
            # Update button text
            self.switch_button.setText(switch.display_name) 