from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QMessageBox, QLabel, QPushButton,
    QFrame, QGridLayout, QGroupBox
)
from PySide6.QtCore import Qt, QSettings, QByteArray
from PySide6.QtGui import QIcon, QAction, QFont, QPixmap, QImage, QPainter, QPen, QColor

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

def get_jdxi_image():
    """Create a QPixmap of the JD-Xi"""
    # Create a black background image with correct aspect ratio
    width = 1000
    height = 400
    image = QImage(width, height, QImage.Format_RGB32)
    image.fill(Qt.black)
    
    pixmap = QPixmap.fromImage(image)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Use smaller margins without border
    margin = 15
    
    # Define display position and size first
    display_x = margin + 20
    display_y = margin + 20
    display_width = 180
    display_height = 45
    
    # Title above display (moved down)
    title_x = display_x
    title_y = margin + 15
    painter.setPen(QPen(Qt.white))
    painter.setFont(QFont("Arial", 28, QFont.Bold))
    painter.drawText(title_x, title_y, "JD-Xi Manager")
    
    # LED display area (enlarged for 2 rows)
    display_x = margin + 20
    display_y = title_y + 30
    display_width = 180
    display_height = 70
    
    # Draw dark grey background for display
    painter.setBrush(QColor("#1A1A1A"))
    painter.setPen(QPen(QColor("#FF8C00"), 1))
    painter.drawRect(display_x, display_y, display_width, display_height)
    
    # Load/Save buttons in display (without boxes)
    button_width = 70
    button_height = 25
    button_margin = 10
    button_y = display_y + (display_height - button_height*2 - button_margin) / 2
    
    # Load button (text only)
    load_x = display_x + button_margin
    painter.setPen(QPen(QColor("#FF8C00")))
    painter.setFont(QFont("Arial", 20))
    painter.drawText(
        load_x, 
        button_y + button_height - 8, 
        "Load Part"
    )
    
    # Save button (text only)
    save_x = display_x + button_margin
    painter.drawText(
        save_x, 
        button_y + button_height*2 + button_margin - 8, 
        "Save Part"
    )
    
    # Keyboard section (moved to bottom)
    keyboard_width = 800
    keyboard_start = width - keyboard_width - margin - 20
    key_width = keyboard_width / 25
    white_keys = 25
    black_key_width = key_width * 0.6
    black_key_height = 70
    white_key_height = 110
    keyboard_y = height - white_key_height  # Removed bottom margin
    
    # Draw white keys
    painter.setBrush(Qt.white)
    painter.setPen(Qt.black)
    for i in range(white_keys):
        painter.drawRect(
            keyboard_start + i*key_width, 
            keyboard_y,
            key_width-1,
            white_key_height
        )
    
    # Draw black keys
    painter.setBrush(Qt.black)
    black_key_positions = [0,1,3,4,5]
    for octave in range(4):
        for pos in black_key_positions:
            x = keyboard_start + (octave*7 + pos)*key_width + key_width/2
            painter.drawRect(
                int(x),
                keyboard_y,
                int(black_key_width),
                black_key_height
            )
    
    # Draw control sections
    section_margin = 40
    section_width = (keyboard_start - margin - section_margin) / 2
    section_height = 200
    section_y = margin + 100
    
    # Remove the red box borders for effects sections
    # (Delete or comment out these lines)
    """
    # Draw horizontal Effects section above keyboard
    effects_y = keyboard_y - 60  # Position above keyboard
    effects_width = 120  # Width for each section
    effects_height = 40
    effects_spacing = 20
    
    # Arpeggiator section
    arp_x = keyboard_start + (keyboard_width - (effects_width * 2 + effects_spacing)) / 2
    painter.drawRect(arp_x, effects_y, effects_width, effects_height)
    
    # Effects section
    fx_x = arp_x + effects_width + effects_spacing
    painter.drawRect(fx_x, effects_y, effects_width, effects_height)
    """
    
    # Draw sequencer section
    seq_y = keyboard_y - 50  # Position above keyboard
    seq_height = 30
    seq_width = keyboard_width * 0.5  # Use roughly half keyboard width
    seq_x = width - margin - 20 - seq_width  # Align with right edge of keyboard
    
    # Calculate step dimensions
    step_count = 16
    step_size = seq_height  # Make steps square
    step_spacing = (seq_width - (step_count * step_size)) / (step_count - 1)
    
    # Draw horizontal measure lines (white)
    painter.setPen(QPen(Qt.white, 1))
    line_spacing = seq_height / 3  # Divide height into 4 sections
    for i in range(4):  # 3 lines (4 sections)
        y = seq_y + (i + 1) * line_spacing
        painter.drawLine(
            int(seq_x), 
            int(y), 
            int(seq_x + seq_width), 
            int(y)
        )
    
    # Draw sequence steps
    for i in range(step_count):
        x = seq_x + i * (step_size + step_spacing)
        
        # Draw step squares with double grey border
        painter.setPen(QPen(QColor("#666666"), 2))  # Mid-grey, doubled width
        painter.setBrush(Qt.black)  # All steps unlit
        
        painter.drawRect(
            int(x),
            seq_y,
            step_size,
            step_size
        )
    
    painter.end()
    return pixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JD-Xi Manager")
        self.setMinimumSize(620, 248)
        
        # Store window dimensions
        self.width = 1000
        self.height = 400
        self.margin = 15
        
        # Store display coordinates as class variables
        self.display_x = self.margin + 20
        self.display_y = self.margin + 15 + 30  # title_y + 30
        self.display_width = 180
        self.display_height = 70
        
        # Initialize MIDI indicators
        self.midi_in_indicator = MIDIIndicator()
        self.midi_out_indicator = MIDIIndicator()
        
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
        
        # Single layout to hold the image and overlays
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create container for image and overlays
        container = QWidget()
        container.setLayout(QVBoxLayout())
        container.layout().setContentsMargins(0, 0, 0, 0)
        
        # Get the JD-Xi image
        pixmap = get_jdxi_image()
        
        # Create label for image
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        container.layout().addWidget(image_label)
        
        # Add overlaid controls
        self._add_overlaid_controls(container)
        
        layout.addWidget(container)
        
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
        
        # Add MIDI activity indicators at left side
        status_bar.addWidget(QLabel("MIDI In:"))
        status_bar.addWidget(self.midi_in_indicator)
        status_bar.addWidget(QLabel("MIDI Out:"))
        status_bar.addWidget(self.midi_out_indicator)
        status_bar.addWidget(QLabel(""))  # Spacer
        
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
        
        # Connect MIDI ports and indicators
        if self.midi_in:
            self.midi_in.set_callback(self._handle_midi_input)
        if self.midi_out:
            original_send = self.midi_out.send_message
            def send_with_indicator(msg):
                original_send(msg)
                self.midi_out_indicator.flash()
            self.midi_out.send_message = send_with_indicator
            
        editor.set_midi_ports(self.midi_in, self.midi_out)
        
    def _handle_midi_input(self, message, timestamp):
        """Handle incoming MIDI messages and flash indicator"""
        self.midi_in_indicator.flash()
        
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
        
    def _add_overlaid_controls(self, widget):
        """Add interactive controls overlaid on the JD-Xi image"""
        # Create absolute positioning layout
        widget.setLayout(QVBoxLayout())
        
        # Parts Select section with Arpeggiator
        parts_container = QWidget(widget)
        parts_x = self.display_x + self.display_width + 30
        parts_y = self.display_y - (self.height * 0.15)  # Move up by 15% of window height
        
        parts_container.setGeometry(parts_x, parts_y, 220, 250)
        parts_layout = QVBoxLayout(parts_container)
        parts_layout.setSpacing(15)  # Increased from 5 to 15 for more vertical spacing
        
        # Add Parts Select label
        parts_label = QLabel("Parts Select")
        parts_label.setStyleSheet("""
            font-size: 14px;
            color: #d51e35;
            font-weight: bold;
            background: transparent;
            padding-bottom: 10px;
        """)
        parts_label.setAlignment(Qt.AlignCenter)
        parts_layout.addWidget(parts_label)
        
        # Parts buttons
        digital1_row = self._create_button_row("Digital Synth 1", self._open_digital_synth1)
        digital2_row = self._create_button_row("Digital Synth 2", self._open_digital_synth2)
        drums_row = self._create_button_row("Drums", self._open_drums)
        analog_row = self._create_button_row("Analog Synth", self._open_analog_synth)
        arp_row = self._create_button_row("Arpeggiator", self._open_arpeggiator)
        
        parts_layout.addLayout(digital1_row)
        parts_layout.addLayout(digital2_row)
        parts_layout.addLayout(drums_row)
        parts_layout.addLayout(analog_row)
        parts_layout.addLayout(arp_row)
        
        # Effects button in top row
        fx_container = QWidget(widget)
        fx_container.setGeometry(self.width - 200, self.margin + 25, 150, 50)
        fx_layout = QHBoxLayout(fx_container)
        
        effects_row = self._create_button_row("Effects", self._open_effects)
        fx_layout.addLayout(effects_row)
        
        # Make containers transparent
        parts_container.setStyleSheet("background: transparent;")
        fx_container.setStyleSheet("background: transparent;") 