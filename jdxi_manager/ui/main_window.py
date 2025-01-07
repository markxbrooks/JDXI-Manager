from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QMessageBox, QLabel, QPushButton,
    QFrame, QGridLayout, QGroupBox
)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIcon, QAction, QFont

from .editors import (
    AnalogSynthEditor,
    DigitalSynthEditor,
    DrumEditor,
    ArpeggioEditor,
    EffectsEditor
)
from .midi_config import MidiConfigFrame
from .patch_manager import PatchManager
from .widgets import MIDIIndicator, LogViewer
from ..midi import MIDIHelper

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JD-Xi Manager")
        self.setMinimumSize(800, 600)
        
        # Set black background for entire application
        self.setStyleSheet("""
            QMainWindow {
                background-color: black;
            }
            QWidget {
                background-color: black;
                color: white;
            }
            QMenuBar {
                background-color: black;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #333333;
            }
            QMenu {
                background-color: black;
                color: white;
            }
            QMenu::item:selected {
                background-color: #333333;
            }
            QGroupBox {
                border: 1px solid #333333;
            }
            QLabel {
                background-color: transparent;
            }
            QStatusBar {
                background-color: black;
                color: white;
            }
        """)
        
        # Initialize MIDI ports
        self.midi_in = None
        self.midi_out = None
        
        # Create UI
        self._create_menu_bar()
        self._create_central_widget()
        self._create_status_bar()
        
        # Load settings
        self.settings = QSettings("jdxi_manager", "settings")
        self._load_settings()
        
        # Show MIDI config if no ports configured
        if not self.midi_in or not self.midi_out:
            self._show_midi_config()
            
    def _create_central_widget(self):
        """Create the main dashboard"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Welcome header
        header = QLabel("JD-Xi Manager")
        header.setFont(QFont(self.font().family(), 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: white;")
        layout.addWidget(header)
        
        # LED-style patch display
        patch_display = QFrame()
        patch_display.setFixedWidth(200)  # Control width of display
        patch_display.setFixedHeight(50)  # 25% of previous height (was ~200)
        patch_display.setStyleSheet("""
            QFrame {
                background-color: #111111;
                padding: 1px;  /* Reduced from 5px */
            }
        """)
        patch_layout = QVBoxLayout(patch_display)
        patch_layout.setSpacing(2)  # Reduced from 4
        patch_layout.setContentsMargins(1, 1, 1, 1)  # Minimal margins
        
        load_label = QLabel("Load Patch")
        load_label.setStyleSheet("""
            QLabel {
                color: #FF8C00;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        load_label.mousePressEvent = lambda e: self._load_patch()
        
        save_label = QLabel("Save Patch")
        save_label.setStyleSheet("""
            QLabel {
                color: #FF8C00;  /* Digital orange */
                font-family: 'Consolas', monospace;  /* Digital font */
                font-size: 12px;
                font-weight: bold;
            }
        """)
        save_label.mousePressEvent = lambda e: self._save_patch()
        
        patch_layout.addWidget(load_label)
        patch_layout.addWidget(save_label)
        
        # Add patch display to top-left
        patch_container = QHBoxLayout()
        patch_container.addWidget(patch_display)
        patch_container.addStretch()  # Push display to left
        layout.addLayout(patch_container)
        
        # Quick access buttons
        button_grid = QGridLayout()
        button_grid.setSpacing(10)
        
        # Parts Select label - moved above boxes
        parts_label = QLabel("Parts Select")
        parts_label.setStyleSheet("""
            font-size: 14px;
            color: #d51e35;
            font-weight: bold;
        """)
        button_grid.addWidget(parts_label, 0, 0)  # Row 0
        
        # Create boxes container
        boxes_container = QHBoxLayout()
        
        # Synth section (without title)
        synth_group = QGroupBox()
        synth_group.setFixedWidth(int(self.width() * 0.5))
        synth_group.setMaximumHeight(200)
        synth_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #333333;
            }
        """)
        
        # Create button rows first
        digital1_row = self._create_button_row("Digital Synth 1", self._open_digital_synth1)
        digital2_row = self._create_button_row("Digital Synth 2", self._open_digital_synth2)
        drums_row = self._create_button_row("Drums", self._open_drums)
        analog_row = self._create_button_row("Analog Synth", self._open_analog_synth)
        
        # Add synth buttons to layout
        synth_layout = QVBoxLayout(synth_group)
        synth_layout.setSpacing(10)
        synth_layout.setContentsMargins(15, 15, 15, 15)
        synth_layout.addLayout(digital1_row)
        synth_layout.addLayout(digital2_row)
        synth_layout.addLayout(drums_row)
        synth_layout.addLayout(analog_row)
        
        boxes_container.addWidget(synth_group)
        
        # Effects section (without title)
        fx_group = QGroupBox()
        fx_group.setFixedWidth(int(self.width() * 0.5))
        fx_group.setMaximumHeight(120)
        fx_group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #333333;
            }
        """)
        
        # Create effects button rows
        arp_row = self._create_button_row("Arpeggiator", self._open_arpeggiator)
        effects_row = self._create_button_row("Effects", self._open_effects)
        
        # Add effects buttons to layout
        fx_layout = QVBoxLayout(fx_group)
        fx_layout.setSpacing(10)
        fx_layout.setContentsMargins(15, 15, 15, 15)
        fx_layout.addLayout(arp_row)
        fx_layout.addLayout(effects_row)
        
        boxes_container.addWidget(fx_group)
        
        # Add boxes below label
        button_grid.addLayout(boxes_container, 1, 0, 1, 2)  # Row 1
        
        layout.addLayout(button_grid)
        
    def _create_section(self, title):
        """Create a section frame with title"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setMinimumHeight(150)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont(self.font().family(), 12, QFont.Bold))
        layout.addWidget(title_label)
        
        return frame

    def _create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        load_action = QAction("Load Patch...", self)
        load_action.triggered.connect(self._load_patch)
        file_menu.addAction(load_action)
        
        save_action = QAction("Save Patch...", self)
        save_action.triggered.connect(self._save_patch)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        midi_config_action = QAction("MIDI Configuration...", self)
        midi_config_action.triggered.connect(self._show_midi_config)
        edit_menu.addAction(midi_config_action)
        
        # Synth menu - reordered to match buttons
        synth_menu = menubar.addMenu("Synth")
        
        digital1_action = QAction("Digital Synth 1", self)
        digital1_action.triggered.connect(self._open_digital_synth1)
        synth_menu.addAction(digital1_action)
        
        digital2_action = QAction("Digital Synth 2", self)
        digital2_action.triggered.connect(self._open_digital_synth2)
        synth_menu.addAction(digital2_action)
        
        drums_action = QAction("Drums", self)
        drums_action.triggered.connect(self._open_drums)
        synth_menu.addAction(drums_action)
        
        analog_action = QAction("Analog Synth", self)
        analog_action.triggered.connect(self._open_analog_synth)
        synth_menu.addAction(analog_action)
        
        # Effects menu
        fx_menu = menubar.addMenu("Effects")
        
        arp_action = QAction("Arpeggiator", self)
        arp_action.triggered.connect(self._open_arpeggiator)
        fx_menu.addAction(arp_action)
        
        effects_action = QAction("Effects", self)
        effects_action.triggered.connect(self._open_effects)
        fx_menu.addAction(effects_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        log_viewer_action = QAction("Log Viewer", self)
        log_viewer_action.triggered.connect(self._show_log_viewer)
        help_menu.addAction(log_viewer_action)
        
    def _create_status_bar(self):
        status_bar = self.statusBar()
        
        # Add MIDI activity indicators
        self.midi_in_indicator = MIDIIndicator()
        self.midi_out_indicator = MIDIIndicator()
        
        status_bar.addPermanentWidget(QLabel("MIDI In:"))
        status_bar.addPermanentWidget(self.midi_in_indicator)
        status_bar.addPermanentWidget(QLabel("MIDI Out:"))
        status_bar.addPermanentWidget(self.midi_out_indicator)
        
    def _show_midi_config(self):
        """Show MIDI configuration dialog"""
        dialog = MidiConfigFrame(self)
        if self.midi_in and self.midi_out:
            dialog.set_settings({
                'input_port': self.midi_in.port_name,
                'output_port': self.midi_out.port_name
            })
            
        dialog.portsChanged.connect(self._update_midi_ports)
        dialog.exec_()
        
    def _update_midi_ports(self, midi_in, midi_out):
        """Update MIDI port connections"""
        self.midi_in = midi_in
        self.midi_out = midi_out
        
        # Save settings
        if midi_in and midi_out:
            self.settings.setValue("midi/input_port", midi_in.port_name)
            self.settings.setValue("midi/output_port", midi_out.port_name)
            
    def _load_settings(self):
        """Load application settings"""
        input_port = self.settings.value("midi/input_port")
        output_port = self.settings.value("midi/output_port")
        
        if input_port and output_port:
            try:
                self.midi_in = MIDIHelper.open_input(input_port)
                self.midi_out = MIDIHelper.open_output(output_port)
            except Exception as e:
                QMessageBox.warning(self, "Error",
                    "Failed to open MIDI ports from saved settings")
                
    def _show_editor(self, title, editor_class, **kwargs):
        """Show a synth editor window"""
        editor = editor_class(midi_out=self.midi_out, **kwargs)
        editor.setWindowTitle(title)
        editor.show()
        
        # Connect MIDI ports
        editor.set_midi_ports(self.midi_in, self.midi_out)
        
    def _open_analog_synth(self):
        self._show_editor("Analog Synth", AnalogSynthEditor)
        
    def _open_digital_synth1(self):
        self._show_editor("Digital Synth 1", DigitalSynthEditor, synth_num=1)
        
    def _open_digital_synth2(self):
        self._show_editor("Digital Synth 2", DigitalSynthEditor, synth_num=2)
        
    def _open_drums(self):
        self._show_editor("Drums", DrumEditor)
        
    def _open_arpeggiator(self):
        self._show_editor("Arpeggiator", ArpeggioEditor)
        
    def _open_effects(self):
        self._show_editor("Effects", EffectsEditor)
        
    def _load_patch(self):
        """Show patch manager for loading"""
        dialog = PatchManager(self)
        dialog.patchSelected.connect(self._apply_patch)
        dialog.exec_()
        
    def _save_patch(self):
        """Show patch manager for saving"""
        # TODO: Implement patch saving
        pass
        
    def _apply_patch(self, patch_data):
        """Apply loaded patch data"""
        # TODO: Implement patch loading
        pass
        
    def closeEvent(self, event):
        """Handle application shutdown"""
        # Close MIDI ports
        if self.midi_in:
            self.midi_in.close()
        if self.midi_out:
            self.midi_out.close()
            
        super().closeEvent(event) 
        
    def _show_log_viewer(self):
        """Show log viewer dialog"""
        viewer = LogViewer(self)
        viewer.exec_() 
        
    def _create_button_row(self, text, slot):
        """Create a row with label and circular button"""
        row = QHBoxLayout()
        row.setSpacing(10)
        
        # Add label with color based on text
        label = QLabel(text)
        if text == "Analog Synth":
            label.setStyleSheet("""
                font-size: 13px;
                color: #00A0E9;  /* Blue for Analog */
                font-weight: bold;
            """)
        else:
            label.setStyleSheet("""
                font-size: 13px;
                color: #d51e35;  /* Base red */
                font-weight: bold;
            """)
        row.addWidget(label)
        
        # Add spacer to push button to right
        row.addStretch()
        
        # Add button
        button = QPushButton()
        button.setFixedSize(30, 30)
        button.clicked.connect(slot)
        
        # Style the button with brighter hover/pressed states
        button.setStyleSheet("""
            QPushButton {
                background-color: black;
                border: 4px solid #d51e35;
                border-radius: 15px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #1A1A1A;
                border-color: #ff4d4d;
            }
            QPushButton:pressed {
                background-color: #333333;
                border-color: #ff6666;
            }
        """)
        
        row.addWidget(button)
        return row 