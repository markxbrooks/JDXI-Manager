from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QMenu, QMessageBox, QLabel, QPushButton,
    QFrame, QGridLayout, QGroupBox
)
from PySide6.QtCore import Qt, QSettings, QByteArray, QTimer
from PySide6.QtGui import QIcon, QAction, QFont, QPixmap, QImage, QPainter, QPen, QColor, QFontDatabase
import logging
from pathlib import Path

from .editors import (
    AnalogSynthEditor,
    DigitalSynthEditor,
    DrumEditor,
    ArpeggioEditor,
    EffectsEditor
)
from .midi_config import MIDIConfigDialog
from .patch_manager import PatchManager
from .widgets import MIDIIndicator, LogViewer
from ..midi import MIDIHelper, MIDIConnection
from .midi_debugger import MIDIDebugger
from .midi_message_debug import MIDIMessageDebug
from ..midi.connection import MIDIConnection
from .patch_name_editor import PatchNameEditor
from jdxi_manager.midi.constants import (
    START_OF_SYSEX, ROLAND_ID, DEVICE_ID, MODEL_ID_1, MODEL_ID_2,
    MODEL_ID, JD_XI_ID, DT1_COMMAND_12, END_OF_SYSEX,
    DIGITAL_SYNTH_AREA, ANALOG_SYNTH_AREA, DRUM_KIT_AREA,
    EFFECTS_AREA
)
from .widgets.piano_keyboard import PianoKeyboard


def get_jdxi_image(digital_font_family=None, current_octave=0, preset_num=1, preset_name="INIT PATCH"):
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
    painter.setFont(QFont("Myriad Pro, Arial", 28, QFont.Bold))
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
    
    # Set up font for digital display
    if digital_font_family:
        display_font = QFont(digital_font_family, 16)
    else:
        display_font = QFont("Consolas", 16)
    painter.setFont(display_font)
    painter.setPen(QPen(QColor("#FF8C00")))  # Orange color for text
    
    # Draw preset number and name
    preset_text = f"{preset_num:03d}:{preset_name}"
    text_y = display_y + 25  # Position for preset text
    painter.drawText(
        display_x + 10,  # Add small margin
        text_y,
        preset_text
    )
    
    # Draw octave display below preset name
    oct_x = display_x + display_width - 60  # Position from right edge
    oct_y = text_y + 25  # Position below preset text
    
    # Format octave text
    if current_octave == 0:
        oct_text = "Octave 0"
    elif current_octave > 0:
        oct_text = f"Octave +{current_octave}"
    else:
        oct_text = f"Octave {current_octave}"
        
    painter.drawText(oct_x, oct_y, oct_text)
    
    # Load/Save buttons in display (without boxes)
    button_width = 70
    button_height = 25
    button_margin = 10
    button_y = display_y + (display_height - button_height*2 - button_margin) / 2
    
    # Load button (text only)
    load_x = display_x + button_margin
    painter.setPen(QPen(QColor("#FF8C00")))
    if digital_font_family:
        painter.setFont(QFont(digital_font_family, 18))
    else:
        painter.setFont(QFont("Consolas", 22))  # Fallback font
 
    
    # Save button (text only)
    save_x = display_x + button_margin

    
    # Keyboard section (moved up and taller)
    keyboard_width = 800
    keyboard_start = width - keyboard_width - margin - 20
    key_width = keyboard_width / 32  # Increased from 25 to 32 keys
    white_keys = 32  # Increased total white keys
    black_key_width = key_width * 0.6
    black_key_height = 80
    white_key_height = 127
    keyboard_y = height - white_key_height - (height * 0.1) + (white_key_height * 0.3)
    
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
    seq_y = keyboard_y - 50  # Keep same distance above keyboard
    seq_height = 30
    seq_width = keyboard_width * 0.5  # Use roughly half keyboard width
    seq_x = width - margin - 20 - seq_width  # Align with right edge of keyboard
    
    # Calculate step dimensions
    step_count = 16
    step_size = 20  # Smaller square size
    total_spacing = seq_width - (step_count * step_size)
    step_spacing = total_spacing / (step_count - 1)
    
    # Draw horizontal measure lines (white)
    painter.setPen(QPen(Qt.white, 1))
    line_y = seq_y - 10  # Move lines above buttons
    measure_width = (step_size + step_spacing) * 4  # Width of 4 steps
    line_spacing = step_size / 3  # Space between lines
    
    beats_list = [2, 3, 4]
    # Draw 4 separate measure lines
    for beats in beats_list:
        for measure in range(beats):
            measure_x = seq_x + measure * measure_width
            for i in range(beats):  # 2, 3 or 4 horizontal lines per measure
                y = line_y - 25 + i * line_spacing
                painter.drawLine(
                    int(measure_x),
                    int(y),
                    int(measure_x + measure_width - step_spacing),  # Stop before next measure
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
        self.setMinimumSize(1000, 400)
        # self.setMaximumSize(1000, 440)
        # Store window dimensions
        self.width = 1000
        self.height = 400
        self.margin = 15
        
        # Store display coordinates as class variables
        self.display_x = 35  # margin + 20
        self.display_y = 50  # margin + 20 + title height
        self.display_width = 180
        self.display_height = 70
        
        # Initialize state variables
        self.current_octave = 0  # Initialize octave tracking first
        self.current_preset_num = 1  # Initialize preset number
        self.current_preset_name = "JD Xi"  # Initialize preset name
        self.midi_in = None
        self.midi_out = None
        self.midi_in_port_name = ""  # Store input port name
        self.midi_out_port_name = ""  # Store output port name
        
        # Initialize MIDI helper
        self.midi_helper = MIDIHelper(parent=self)
        
        # Try to auto-connect to JD-Xi
        self._auto_connect_jdxi()
        
        # Show MIDI config if auto-connect failed
        if not self.midi_helper.current_in_port or not self.midi_helper.current_out_port:
            self._show_midi_config()
        
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
        
        # Load custom font
        self._load_digital_font()
        
        # Create UI
        self._create_menu_bar()
        self._create_central_widget()  # Now current_octave exists when this is called
        self._create_status_bar()
        
        # Load settings
        self.settings = QSettings("jdxi_manager", "settings")
        self._load_settings()
        
        # Show window
        self.show()
        
        # Store references to debug windows
        self.midi_debugger = None
        self.log_viewer = None
        self.midi_message_debug = None
        
        # Add debug menu
        debug_menu = self.menuBar().addMenu("Debug")
        
        # Add MIDI debugger action (SysEx decoder)
        midi_debugger_action = QAction("MIDI SysEx Debugger", self)
        midi_debugger_action.triggered.connect(self._open_midi_debugger)
        debug_menu.addAction(midi_debugger_action)
        
        # Add MIDI message monitor action
        midi_monitor_action = QAction("MIDI Monitor", self)
        midi_monitor_action.triggered.connect(self._open_midi_message_debug)
        debug_menu.addAction(midi_monitor_action)
        
        # Add log viewer action
        log_viewer_action = QAction("Log Viewer", self)
        log_viewer_action.triggered.connect(self._open_log_viewer)
        debug_menu.addAction(log_viewer_action)
        
        # Add preset tracking
        self.current_preset_num = 1
        self.current_preset_name = "INIT PATCH"
        
        # Add piano keyboard at bottom
        keyboard = PianoKeyboard(parent=self)
        self.statusBar().addPermanentWidget(keyboard)
        
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
        
        # Store reference to image label
        self.image_label = QLabel()
        self.image_label.setPixmap(get_jdxi_image(
            self.digital_font_family if hasattr(self, 'digital_font_family') else None,
            self.current_octave
        ))
        self.image_label.setAlignment(Qt.AlignCenter)
        container.layout().addWidget(self.image_label)
        
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
        
        # Add Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        # Add Patch Name action
        edit_name_action = QAction("Edit Patch Name", self)
        edit_name_action.triggered.connect(self._edit_patch_name)
        edit_menu.addAction(edit_name_action)
        
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
        try:
            # Get available ports using instance method
            input_ports = self.midi_helper.get_input_ports()  # Use instance method
            output_ports = self.midi_helper.get_output_ports()  # Use instance method
            
            dialog = MIDIConfigDialog(
                input_ports,
                output_ports,
                self.midi_helper.current_in_port,
                self.midi_helper.current_out_port,
                parent=self
            )
            
            if dialog.exec():
                in_port = dialog.get_input_port()
                out_port = dialog.get_output_port()
                
                # Open selected ports using instance methods
                if in_port:
                    self.midi_helper.open_input_port(in_port)
                if out_port:
                    self.midi_helper.open_output_port(out_port)
                    
        except Exception as e:
            logging.error(f"Error showing MIDI configuration: {str(e)}")
            self.show_error("MIDI Configuration Error", str(e))
        
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
        try:
            if hasattr(self, 'settings'):
                # Load MIDI port settings
                input_port = self.settings.value("midi_in", "")
                output_port = self.settings.value("midi_out", "")
                
                # Load window geometry
                geometry = self.settings.value("geometry")
                if geometry:
                    self.restoreGeometry(geometry)
                    
                # Load preset info
                self.current_preset_num = int(self.settings.value("preset_num", 1))
                self.current_preset_name = self.settings.value("preset_name", "INIT PATCH")
                
                # Try to open MIDI ports if they were saved
                if input_port and output_port:
                    self._set_midi_ports(input_port, output_port)
                    
                logging.debug("Settings loaded successfully")
                
        except Exception as e:
            logging.error(f"Error loading settings: {str(e)}")

    def _show_editor(self, title, editor_class, **kwargs):
        """Show editor window"""
        try:
            # Create editor with proper initialization
            if editor_class in [DigitalSynthEditor, DrumEditor, AnalogSynthEditor]:
                editor = editor_class(
                    midi_helper=self.midi_helper,
                    parent=self,
                    **kwargs
                )
            else:
                # For other editors, use existing initialization
                editor = editor_class(midi_out=self.midi_out, **kwargs)
                
            # Set window title
            editor.setWindowTitle(title)
            
            # Store reference and show
            if title == "Digital Synth 1":
                self.digital_synth1 = editor
            elif title == "Digital Synth 2":
                self.digital_synth2 = editor
            elif title == "Analog Synth":
                self.analog_synth = editor
            elif title == "Drum Kit":
                self.drum_kit = editor
            elif title == "Effects":
                self.effects = editor
                
            # Show editor
            editor.show()
            editor.raise_()
            
        except Exception as e:
            logging.error(f"Error showing {title} editor: {str(e)}")
        
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
        self._show_drums_editor()
        
    def _open_arpeggiator(self):
        """Show the arpeggiator editor window"""
        try:
            if not hasattr(self, 'arpeggiator'):
                self.arpeggiator = ArpeggioEditor(parent=self)
            self.arpeggiator.show()
            self.arpeggiator.raise_()
            
        except Exception as e:
            logging.error(f"Error showing Arpeggiator editor: {str(e)}")
        
    def _open_effects(self):
        """Show the effects editor window"""
        try:
            if not hasattr(self, 'effects_editor'):
                self.effects_editor = EffectsEditor(
                    midi_helper=self.midi_helper,  # Pass midi_helper instead of midi_out
                    parent=self
                )
            self.effects_editor.show()
            self.effects_editor.raise_()
            
        except Exception as e:
            logging.error(f"Error showing Effects editor: {str(e)}")
        
    def _load_patch(self):
        """Show patch manager for loading"""
        try:
            dialog = PatchManager(self)
            if dialog.exec_():
                # Get selected patch info
                patch_num = dialog.selected_patch_number
                patch_name = dialog.selected_patch_name
                
                # Update display
                self.update_preset_display(patch_num, patch_name)
                
                # Send MIDI message to load patch
                if self.midi_out:
                    # Create patch load message
                    msg = MIDIHelper.create_patch_load_message(patch_num)
                    self.midi_out.send_message(msg)
                    logging.debug(f"Loaded patch {patch_num}: {patch_name}")
                    
                    # Blink indicator
                    if hasattr(self, 'midi_out_indicator'):
                        self.midi_out_indicator.blink()
                        
        except Exception as e:
            logging.error(f"Error loading patch: {str(e)}")

    def _save_patch(self):
        """Show patch manager for saving"""
        try:
            dialog = PatchManager(self, save_mode=True)
            if dialog.exec_():
                # Get target patch number and name
                patch_num = dialog.selected_patch_number
                patch_name = dialog.patch_name
                
                # Update display
                self.update_preset_display(patch_num, patch_name)
                
                # Send MIDI message to save patch
                if self.midi_out:
                    # Create patch save message
                    msg = MIDIHelper.create_patch_save_message(patch_num)
                    self.midi_out.send_message(msg)
                    logging.debug(f"Saved patch {patch_num} as: {patch_name}")
                    
                    # Blink indicator
                    if hasattr(self, 'midi_out_indicator'):
                        self.midi_out_indicator.blink()
                        
        except Exception as e:
            logging.error(f"Error saving patch: {str(e)}")

    def _apply_patch(self, patch_data):
        """Apply loaded patch data"""
        # TODO: Implement patch loading
        pass
        
    def closeEvent(self, event):
        """Handle window close event"""
        try:
            # Properly delete MIDI ports
            if self.midi_in:
                self.midi_in.delete()  # Use delete() instead of close()
            if self.midi_out:
                self.midi_out.delete()  # Use delete() instead of close()
            
            # Save settings
            self._save_settings()
            
            # Accept the event
            event.accept()
            
        except Exception as e:
            logging.error(f"Error during close event: {str(e)}")
            event.ignore()
        
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
                font-family: "Myriad Pro", Arial;
                font-size: 13px;
                color: #00A0E9;  /* Blue for Analog */
                font-weight: bold;
            """)
        else:
            label.setStyleSheet("""
                font-family: "Myriad Pro", Arial;
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

    def add_arpeggiator_buttons(self, widget):
        """Add arpeggiator up/down buttons to the interface"""
        # Create container
        arpeggiator_buttons_container = QWidget(widget)

        # Position to align with sequencer but 25% higher (increased from 20%)
        seq_y = self.height - 50 - self.height * 0.1  # Base sequencer Y position
        offset_y = self.height * 0.25  # 25% of window height (increased from 0.2)
        arpeggiator_x = self.width - self.width * 0.8 - 60  # Position left of sequencer

        # Apply the height offset to the Y position
        arpeggiator_buttons_container.setGeometry(
            arpeggiator_x,
            seq_y - 60 - offset_y,  # Move up by offset_y (now 25% instead of 20%)
            100,
            100
        )

        arpeggiator_layout = QVBoxLayout(arpeggiator_buttons_container)
        arpeggiator_layout.setSpacing(5)

        # Add "ARPEGGIO" label at the top
        arpeggiator_label = QLabel("ARPEGGIO")
        arpeggiator_label.setStyleSheet("""
            font-family: "Myriad Pro", Arial;
            font-size: 14px;
            color: #d51e35;
            font-weight: bold;
            background: transparent;
        """)
        arpeggiator_label.setAlignment(Qt.AlignCenter)
        arpeggiator_layout.addWidget(arpeggiator_label)

        # Create horizontal layout for Down/Up labels
        labels_row = QHBoxLayout()
        labels_row.setSpacing(20)  # Space between labels

        # On label
        on_label = QLabel("On")
        on_label.setStyleSheet("""
            font-family: "Myriad Pro", Arial;
            font-size: 13px;
            color: #d51e35;
            font-weight: bold;
        """)
        labels_row.addWidget(on_label)

        # Add labels row
        arpeggiator_layout.addLayout(labels_row)

        # Create horizontal layout for buttons
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(20)  # Space between buttons

        # Down label
        key_hold_label = QLabel("Key Hold")
        key_hold_label.setStyleSheet("""
            font-family: "Myriad Pro", Arial;
            font-size: 13px;
            color: #d51e35;
            font-weight: bold;
        """)
        labels_row.addWidget(key_hold_label)

        # Create and store arpeggiator  button
        self.arpeggiator_button = QPushButton()
        self.arpeggiator_button.setFixedSize(30, 30)
        self.arpeggiator_button.setCheckable(True)
        self.arpeggiator_button.clicked.connect(
            lambda checked: self._send_arp_on_off(checked)
        )
        self.arpeggiator_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                border: 4px solid #d51e35;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #1A1A1A;
                border-color: #ff4d4d;
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: #333333;
                border-color: #ff6666;
            }
        """)
        buttons_row.addWidget(self.arpeggiator_button)

        # Create and store octave down button
        self.key_hold = QPushButton()
        self.key_hold.setFixedSize(30, 30)
        self.key_hold.setCheckable(True)
        self.key_hold.clicked.connect(
            lambda checked: self._send_arp_key_hold(checked)
        )
        self.key_hold.setStyleSheet("""
            QPushButton {
                background-color: black;
                border: 4px solid #d51e35;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #1A1A1A;
                border-color: #ff4d4d;
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: #333333;
                border-color: #ff6666;
            }
        """)
        buttons_row.addWidget(self.key_hold)

        # Add buttons row
        arpeggiator_layout.addLayout(buttons_row)

        # Make container transparent
        arpeggiator_buttons_container.setStyleSheet("background: transparent;")

    def add_octave_buttons(self, widget):
        """Add octave up/down buttons to the interface"""
        # Create container
        octave_buttons_container = QWidget(widget)
        
        # Position to align with sequencer but 25% higher (increased from 20%)
        seq_y = self.height - 50 - self.height * 0.1  # Base sequencer Y position
        offset_y = self.height * 0.25  # 25% of window height (increased from 0.2)
        octave_x = self.width - self.width * 0.8 - 150  # Position left of sequencer
        
        # Apply the height offset to the Y position
        octave_buttons_container.setGeometry(
            octave_x, 
            seq_y - 60 - offset_y,  # Move up by offset_y (now 25% instead of 20%)
            100, 
            100
        )
        
        octave_layout = QVBoxLayout(octave_buttons_container)
        octave_layout.setSpacing(5)


        # Create horizontal layout for Down/Up labels
        labels_row = QHBoxLayout()
        labels_row.setSpacing(20)  # Space between labels

        # Add "OCTAVE" label at the top
        octave_label = QLabel("OCTAVE")
        octave_label.setStyleSheet("""
            font-family: "Myriad Pro", Arial;
            font-size: 14px;
            color: #d51e35;
            font-weight: bold;
            background: transparent;
        """)
        octave_label.setAlignment(Qt.AlignCenter)
        octave_layout.addWidget(octave_label)
        
        # Down label
        down_label = QLabel("Down")
        down_label.setStyleSheet("""
            font-family: "Myriad Pro", Arial;
            font-size: 13px;
            color: #d51e35;
            font-weight: bold;
        """)
        labels_row.addWidget(down_label)

        # Up label
        up_label = QLabel("Up")
        up_label.setStyleSheet("""
            font-family: "Myriad Pro", Arial;
            font-size: 13px;
            color: #d51e35;
            font-weight: bold;
        """)
        labels_row.addWidget(up_label)
        
        # Add labels row
        octave_layout.addLayout(labels_row)

        # Create horizontal layout for buttons
        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(20)  # Space between buttons
        
        # Create and store octave down button
        self.octave_down = QPushButton()
        self.octave_down.setFixedSize(30, 30)
        self.octave_down.setCheckable(True)
        self.octave_down.clicked.connect(lambda: self._send_octave(-1))
        self.octave_down.setStyleSheet("""
            QPushButton {
                background-color: black;
                border: 4px solid #d51e35;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #1A1A1A;
                border-color: #ff4d4d;
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: #333333;
                border-color: #ff6666;
            }
        """)
        buttons_row.addWidget(self.octave_down)
        
        # Create and store octave up button
        self.octave_up = QPushButton()
        self.octave_up.setFixedSize(30, 30)
        self.octave_up.setCheckable(True)
        self.octave_up.clicked.connect(lambda: self._send_octave(1))
        self.octave_up.setStyleSheet("""
            QPushButton {
                background-color: black;
                border: 4px solid #d51e35;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #1A1A1A;
                border-color: #ff4d4d;
            }
            QPushButton:pressed, QPushButton:checked {
                background-color: #333333;
                border-color: #ff6666;
            }
        """)
        buttons_row.addWidget(self.octave_up)

        # Add buttons row
        octave_layout.addLayout(buttons_row)

        # Make container transparent
        octave_buttons_container.setStyleSheet("background: transparent;")

    def _add_overlaid_controls(self, widget):
        """Add interactive controls overlaid on the JD-Xi image"""
        # Create absolute positioning layout
        widget.setLayout(QVBoxLayout())
        
        # Parts Select section with Arpeggiator
        parts_container = QWidget(widget)
        parts_x = self.display_x + self.display_width + 30
        parts_y = self.display_y - (self.height * 0.15)  # Move up by 20% of window height
        
        parts_container.setGeometry(parts_x, parts_y, 220, 250)
        parts_layout = QVBoxLayout(parts_container)
        parts_layout.setSpacing(15)  # Increased from 5 to 15 for more vertical spacing
        
        # Add Parts Select label
        parts_label = QLabel("Parts Select")
        parts_label.setStyleSheet("""
            font-family: "Myriad Pro", Arial;
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

        self.add_octave_buttons(widget)
        self.add_arpeggiator_buttons(widget)

        # Effects button in top row
        fx_container = QWidget(widget)
        fx_container.setGeometry(self.width - 200, self.margin + 25, 150, 50)
        fx_layout = QHBoxLayout(fx_container)
        
        effects_row = self._create_button_row("Effects", self._open_effects)
        fx_layout.addLayout(effects_row)
        
        # Make containers transparent
        parts_container.setStyleSheet("background: transparent;")
        fx_container.setStyleSheet("background: transparent;") 
        
        # Calculate keyboard dimensions
        key_width = self.width * 0.8 / 25  # keyboard_width/25
        key_height = 127  # white_key_height
        keyboard_y = self.height - key_height - (self.height * 0.1) + (key_height * 0.3)
        keyboard_start = self.width - (self.width * 0.8) - self.margin - 20
        
        # Add white keys C1 to F5
        white_notes = [
            36, 38, 40, 41, 43, 45, 47,  # C1 to B1
            48, 50, 52, 53, 55, 57, 59,  # C2 to B2
            60, 62, 64, 65, 67, 69, 71,  # C3 to B3
            72, 74, 76, 77, 79, 81, 83,  # C4 to B4
            84, 86, 88, 89              # C5 to F5
        ]
        
        for i, note in enumerate(white_notes):
            x_pos = keyboard_start + i * key_width
            self._add_piano_key(widget, False, note, x_pos, keyboard_y, key_width, key_height)
            
        # Add black keys
        black_notes = [
            37, 39, None, 42, 44, 46,     # C#1 to B1
            49, 51, None, 54, 56, 58,     # C#2 to B2
            61, 63, None, 66, 68, 70,     # C#3 to B3
            73, 75, None, 78, 80, 82,     # C#4 to B4
            85, 87, None, 90              # C#5 to F#5
        ]
        
        black_positions = [0, 1, 3, 4, 5, 7, 8, 10, 11, 12, 14, 15, 17, 18, 19, 
                         21, 22, 24, 25, 26, 28, 29, 31, 32]  # Extended positions
        
        for pos, note in zip(black_positions, [n for n in black_notes if n is not None]):
            x_pos = keyboard_start + pos * key_width + key_width/2
            self._add_piano_key(widget, True, note, x_pos, keyboard_y, key_width, key_height)
        
    def _add_piano_key(self, widget, is_black, note_number, x_pos, keyboard_y, key_width, key_height):
        """Helper to create a piano key button"""
        button = QPushButton(widget)
        
        if is_black:
            width = key_width * 0.6
            height = 80
            style = """
                QPushButton {
                    background-color: black;
                    border: 1px solid black;
                    border-radius: 0px;
                }
                QPushButton:hover {
                    background-color: #1a1a1a;
                }
                QPushButton:pressed {
                    background-color: #333333;
                }
            """
        else:
            width = key_width - 1
            height = key_height
            style = """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                    border-radius: 0px;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                }
                QPushButton:pressed {
                    background-color: #e0e0e0;
                }
            """
            
        button.setGeometry(
            int(x_pos),
            int(keyboard_y),
            int(width),
            int(height)
        )
        button.setStyleSheet(style)
        
        def key_pressed():
            if self.midi_out:
                self.midi_out.send_message([0x90, note_number, 1])  # Note On
                logging.debug(f"Sent MIDI Note On {note_number} velocity 1")
        
        def key_released():
            if self.midi_out:
                self.midi_out.send_message([0x80, note_number, 5])  # Note Off
                logging.debug(f"Sent MIDI Note Off {note_number} velocity 5")
        
        # Connect to mouse events instead of clicked
        button.pressed.connect(key_pressed)
        button.released.connect(key_released) 
        
    def _send_octave(self, direction):
        """Send octave change MIDI message"""
        if self.midi_out:
            # Update octave tracking
            self.current_octave = max(-3, min(3, self.current_octave + direction))
            
            # Update button states
            self.octave_down.setChecked(self.current_octave < 0)
            self.octave_up.setChecked(self.current_octave > 0)
            
            # Update display
            self._update_display()
            
            # Map octave value to correct SysEx value
            # -3 = 0x3D, -2 = 0x3E, -1 = 0x3F, 0 = 0x40, +1 = 0x41, +2 = 0x42, +3 = 0x43
            octave_value = 0x40 + self.current_octave  # 0x40 is center octave
            
            # Calculate checksum
            checksum = (0x19 + 0x01 + 0x00 + 0x15 + octave_value)
            checksum = (0x80 - (checksum & 0x7F)) & 0x7F
            
            # Create SysEx message
            sysex_msg = [
                0xF0,   # Start of SysEx
                0x41,   # Roland ID
                0x10,   # Device ID
                0x00, 0x00, 0x00, 0x0E,  # Model ID
                0x12,   # Command ID (DT1)
                0x19,   # Address 1
                0x01,   # Address 2
                0x00,   # Address 3
                0x15,   # Address 4
                octave_value,  # Parameter value
                checksum,  # Checksum
                0xF7    # End of SysEx
            ]
            
            self.midi_out.send_message(sysex_msg)
            logging.debug(f"Sent octave change SysEx, new octave: {self.current_octave} (value: {hex(octave_value)})")

    def _create_other(self):
        """Create other controls section"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        
        # Create buttons for Effects and Vocal FX
        others = [
            ("Effects", self._open_effects),
            ("Vocal FX", self._open_vocal_fx),
        ]
        
        for text, slot in others:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            btn.clicked.connect(slot)
            layout.addWidget(btn)
        
        # Create horizontal layout for Arpeggiator
        arp_row = QHBoxLayout()
        
        # Arpeggiator button
        arp_btn = QPushButton("Arpeggio")
        arp_btn.setFixedHeight(40)
        arp_btn.clicked.connect(self._open_arpeggio)
        arp_row.addWidget(arp_btn)
        
        # Add the horizontal row to the main layout
        layout.addLayout(arp_row)
        
        # Add stretch at the bottom
        layout.addStretch()
        
        return frame 

    def _update_display(self):
        """Update the JD-Xi display image"""
        pixmap = get_jdxi_image(
            digital_font_family=self.digital_font_family if hasattr(self, 'digital_font_family') else None,
            current_octave=self.current_octave,
            preset_num=self.current_preset_num,
            preset_name=self.current_preset_name
        )
        if hasattr(self, 'image_label'):
            self.image_label.setPixmap(pixmap) 

    def _load_digital_font(self):
        """Load the digital LCD font for the display"""
        import os
        font_name = "JdLCD.ttf"
        font_path = os.path.join(os.path.dirname(__file__), "..", "..", "resources", "fonts", font_name)
        if os.path.exists(font_path):
            logging.debug(f"Found file, Loading {font_name}font from {font_path}")
            try:
                font_id = QFontDatabase.addApplicationFont(font_path)
                if font_id < 0:
                    logging.debug("Error loading {font_name} font")
                font_families = QFontDatabase.applicationFontFamilies(font_id)
                if font_families:
                    self.digital_font_family = font_families[0]
                    logging.debug(f"Successfully loaded font family: {self.digital_font_family}")
                else:
                    logging.debug("No font families found after loading font")
            except Exception as e:
                logging.exception(f"Error loading {font_name} font from {font_path}: {e}")
        else:
            logging.debug(f"File not found: {font_path}") 

    def _send_arp_key_hold(self, state):
        """Send arpeggiator key hold (latch) command"""
        try:
            if self.midi_helper:
                # Value: 0 = OFF, 1 = ON
                value = 0x01 if state else 0x00
                
                # Create SysEx message using constants
                sysex_msg = [
                    START_OF_SYSEX,
                    ROLAND_ID,
                    DEVICE_ID,
                    MODEL_ID_1, MODEL_ID_2, MODEL_ID, JD_XI_ID,
                    DT1_COMMAND_12,
                    0x15,   # Arpeggio area
                    0x00,   # Subgroup
                    0x00,   # Part
                    0x02,   # Key Hold parameter
                    value,  # Parameter value
                ]
                
                # Calculate checksum (sum all data bytes)
                checksum = sum(sysex_msg[8:-1]) & 0x7F  # From address to value
                checksum = (128 - checksum) & 0x7F
                
                # Add checksum and end of sysex
                sysex_msg.extend([checksum, END_OF_SYSEX])
                
                # Send message
                self.midi_helper.send_message(bytes(sysex_msg))
                logging.debug(f"Sent arpeggiator key hold: {'ON' if state else 'OFF'}")
                
        except Exception as e:
            logging.error(f"Error sending arp key hold: {str(e)}")

    def _send_arp_on_off(self, state):
        """Send arpeggiator on/off command"""
        try:
            if self.midi_helper:
                # Value: 0 = OFF, 1 = ON
                value = 0x01 if state else 0x00
                
                # Create SysEx message using constants
                sysex_msg = [
                    START_OF_SYSEX,
                    ROLAND_ID,
                    DEVICE_ID,
                    MODEL_ID_1, MODEL_ID_2, MODEL_ID, JD_XI_ID,
                    DT1_COMMAND_12,
                    0x15,   # Arpeggio area
                    0x00,   # Subgroup
                    0x00,   # Part
                    0x00,   # On/Off parameter
                    value,  # Parameter value
                ]
                
                # Calculate checksum (sum all data bytes)
                checksum = sum(sysex_msg[8:-1]) & 0x7F  # From address to value
                checksum = (128 - checksum) & 0x7F
                
                # Add checksum and end of sysex
                sysex_msg.extend([checksum, END_OF_SYSEX])
                
                # Send message
                self.midi_helper.send_message(bytes(sysex_msg))
                logging.debug(f"Sent arpeggiator on/off: {'ON' if state else 'OFF'}")
                
        except Exception as e:
            logging.error(f"Error sending arp on/off: {str(e)}")

    def _open_midi_debugger(self):
        """Open MIDI debugger window"""
        if not self.midi_helper:
            logging.error("MIDI helper not initialized")
            return
        """    
        if not self.midi_helper.midi_out:
            logging.warning("No MIDI output port set")
            # Show MIDI config dialog
            self._show_midi_config()
            return
        """    
        if not self.midi_debugger:
            self.midi_debugger = MIDIDebugger(self.midi_helper)
            # Clean up reference when window is closed
            self.midi_debugger.setAttribute(Qt.WA_DeleteOnClose)
            self.midi_debugger.destroyed.connect(self._midi_debugger_closed)
            logging.debug("Created new MIDI debugger window")
        self.midi_debugger.show()
        self.midi_debugger.raise_()
        
    def _midi_debugger_closed(self):
        """Handle MIDI debugger window closure"""
        self.midi_debugger = None
        
    def _open_log_viewer(self):
        """Open log viewer window"""
        if not self.log_viewer:
            self.log_viewer = LogViewer()
            # Clean up reference when window is closed
            self.log_viewer.setAttribute(Qt.WA_DeleteOnClose)
            self.log_viewer.destroyed.connect(self._log_viewer_closed)
        self.log_viewer.show()
        self.log_viewer.raise_()  # Bring to front if already open
        
    def _log_viewer_closed(self):
        """Handle log viewer window closure"""
        self.log_viewer = None 

    def _set_midi_ports(self, in_port, out_port):
        """Set MIDI input and output ports"""
        try:
            # Close existing ports
            if self.midi_in:
                self.midi_in.delete()  # Use delete() instead of close()
            if self.midi_out:
                self.midi_out.delete()  # Use delete() instead of close()
            
            # Open new ports
            self.midi_in = MIDIHelper.open_input(in_port, self)
            self.midi_out = MIDIHelper.open_output(out_port, self)
            
            # Store port names
            self.midi_in_port_name = in_port
            self.midi_out_port_name = out_port
            
            # Initialize singleton connection
            MIDIConnection().initialize(self.midi_in, self.midi_out, self)
            
            # Update MIDI helper
            self.midi_helper.midi_in = self.midi_in
            self.midi_helper.midi_out = self.midi_out
            
            # Set up MIDI input callback
            if self.midi_in:
                self.midi_in.set_callback(self._handle_midi_message)
            
            # Update indicators
            self.midi_in_indicator.set_active(self.midi_in is not None)
            self.midi_out_indicator.set_active(self.midi_out is not None)
            
            # Save settings
            if self.midi_in and self.midi_out:
                self.settings.setValue("midi_in", in_port)
                self.settings.setValue("midi_out", out_port)
                logging.info(f"MIDI ports configured - In: {in_port}, Out: {out_port}")
            else:
                logging.warning("Failed to configure MIDI ports")
                
        except Exception as e:
            logging.error(f"Error setting MIDI ports: {str(e)}")

    def _open_midi_message_debug(self):
        """Open MIDI message debug window"""
        if not self.midi_message_debug:
            self.midi_message_debug = MIDIMessageDebug()
            self.midi_message_debug.setAttribute(Qt.WA_DeleteOnClose)
            self.midi_message_debug.destroyed.connect(self._midi_message_debug_closed)
        self.midi_message_debug.show()
        self.midi_message_debug.raise_()
        
    def _midi_message_debug_closed(self):
        """Handle MIDI message debug window closure"""
        self.midi_message_debug = None 

    def _handle_midi_message(self, message, timestamp):
        """Handle incoming MIDI message"""
        data = message[0]  # Get the raw MIDI data
        
        # Check if it's a SysEx message
        if data[0] == START_OF_SYSEX and len(data) > 8:
            # Verify it's a Roland message for JD-Xi
            if (data[1] == DEVICE_ID and  # Roland ID
                data[4:8] == bytes([MODEL_ID_1, MODEL_ID_2, MODEL_ID, JD_XI_ID])):  # JD-Xi ID
                # Blink the input indicator
                if hasattr(self, 'midi_in_indicator'):
                    self.midi_in_indicator.blink()
                
                # Forward to MIDI helper
                if hasattr(self, 'midi_helper'):
                    self.midi_helper.handle_midi_message(message, timestamp)

    def _send_midi_message(self, message):
        """Send MIDI message and blink indicator"""
        if self.midi_out:
            self.midi_out.send_message(message)
            # Blink the output indicator
            if hasattr(self, 'midi_out_indicator'):
                self.midi_out_indicator.blink() 

    def _show_drums_editor(self):
        """Show the drum editor window"""
        try:
            if not hasattr(self, 'drums_editor'):
                self.drums_editor = DrumEditor(parent=self)  # Only pass parent
            self.drums_editor.show()
            self.drums_editor.raise_()
            
        except Exception as e:
            logging.error(f"Error showing Drums editor: {str(e)}") 

    def update_preset_display(self, preset_num, preset_name):
        """Update the current preset display"""
        self.current_preset_num = preset_num
        self.current_preset_name = preset_name
        self._update_display() 

    def _edit_patch_name(self):
        """Edit current patch name"""
        try:
            dialog = PatchNameEditor(self.current_preset_name, self)
            if dialog.exec_():
                new_name = dialog.get_name()
                
                # Update display
                self.update_preset_display(self.current_preset_num, new_name)
                
                # Send MIDI message to update patch name
                if self.midi_out:
                    msg = MIDIHelper.create_patch_name_message(
                        self.current_preset_num, 
                        new_name
                    )
                    self.midi_out.send_message(msg)
                    logging.debug(f"Updated patch {self.current_preset_num} name to: {new_name}")
                    
                    # Blink indicator
                    if hasattr(self, 'midi_out_indicator'):
                        self.midi_out_indicator.blink()
                        
        except Exception as e:
            logging.error(f"Error editing patch name: {str(e)}") 

    def _save_settings(self):
        """Save application settings"""
        try:
            # Save MIDI port settings
            if hasattr(self, 'settings'):
                self.settings.setValue("midi_in", self.midi_in_port_name)
                self.settings.setValue("midi_out", self.midi_out_port_name)
                
                # Save window geometry
                self.settings.setValue("geometry", self.saveGeometry())
                
                # Save current preset info
                self.settings.setValue("preset_num", self.current_preset_num)
                self.settings.setValue("preset_name", self.current_preset_name)
                
                logging.debug("Settings saved successfully")
                
        except Exception as e:
            logging.error(f"Error saving settings: {str(e)}") 

    def show_error(self, title: str, message: str):
        """Show error message dialog
        
        Args:
            title: Dialog title
            message: Error message
        """
        QMessageBox.critical(self, title, message)

    def show_warning(self, title: str, message: str):
        """Show warning message dialog
        
        Args:
            title: Dialog title
            message: Warning message
        """
        QMessageBox.warning(self, title, message)

    def show_info(self, title: str, message: str):
        """Show info message dialog
        
        Args:
            title: Dialog title
            message: Info message
        """
        QMessageBox.information(self, title, message) 

    def _auto_connect_jdxi(self):
        """Attempt to automatically connect to JD-Xi MIDI ports"""
        try:
            # Get available ports
            input_ports = self.midi_helper.get_input_ports()
            output_ports = self.midi_helper.get_output_ports()
            
            # Look for JD-Xi in port names (case insensitive)
            jdxi_names = ['jd-xi', 'jdxi', 'roland jd-xi']
            
            # Find input port
            for port in input_ports:
                if any(name in port.lower() for name in jdxi_names):
                    self.midi_helper.open_input_port(port)
                    logging.info(f"Auto-connected to JD-Xi input: {port}")
                    break
                
            # Find output port
            for port in output_ports:
                if any(name in port.lower() for name in jdxi_names):
                    self.midi_helper.open_output_port(port)
                    logging.info(f"Auto-connected to JD-Xi output: {port}")
                    break
                
            # Verify connection
            if self.midi_helper.current_in_port and self.midi_helper.current_out_port:
                # Send identity request to confirm it's a JD-Xi
                self._verify_jdxi_connection()
                return True
                
        except Exception as e:
            logging.error(f"Error auto-connecting to JD-Xi: {str(e)}")
            
        return False

    def _verify_jdxi_connection(self):
        """Verify connected device is a JD-Xi by sending identity request"""
        try:
            # Create identity request message
            identity_request = [
                START_OF_SYSEX,
                ROLAND_ID,
                DEVICE_ID,
                0x7E,  # Universal System Exclusive
                0x7F,  # All channels
                0x06,  # Identity Request
                0x01,  # Identity Request command
                END_OF_SYSEX
            ]
            
            # Send request
            if self.midi_helper:
                self.midi_helper.send_message(bytes(identity_request))
                logging.debug("Sent identity request to verify JD-Xi connection")
                
        except Exception as e:
            logging.error(f"Error verifying JD-Xi connection: {str(e)}") 

    def show_digital_synth_editor(self, synth_num=1):
        """Show digital synth editor window"""
        try:
            if not hasattr(self, f'digital_synth_{synth_num}_editor'):
                # Create new editor instance
                editor = DigitalSynthEditor(
                    synth_num=synth_num,
                    midi_helper=self.midi_helper,
                    parent=self
                )
                setattr(self, f'digital_synth_{synth_num}_editor', editor)
            
            # Get editor instance
            editor = getattr(self, f'digital_synth_{synth_num}_editor')
            
            # Show editor window
            editor.show()
            editor.raise_()
            editor.activateWindow()
            
            logging.debug(f"Showing Digital Synth {synth_num} editor")
            
        except Exception as e:
            logging.error(f"Error showing Digital Synth {synth_num} editor: {str(e)}")
            self.show_error("Editor Error", str(e)) 

    def _handle_piano_note_on(self, note_num):
        """Handle piano key press"""
        if self.midi_helper:
            # Note on message: 0x90 (Note On, channel 1), note number, velocity 100
            msg = [0x90, note_num, 100]
            self.midi_helper.send_message(msg)
            logging.debug(f"Sent Note On: {note_num}")

    def _handle_piano_note_off(self, note_num):
        """Handle piano key release"""
        if self.midi_helper:
            # Note off message: 0x80 (Note Off, channel 1), note number, velocity 0
            msg = [0x80, note_num, 0]
            self.midi_helper.send_message(msg)
            logging.debug(f"Sent Note Off: {note_num}") 

    def _create_midi_indicators(self):
        """Create MIDI activity indicators"""
        # Create indicators
        self.midi_in_indicator = MIDIIndicator()
        self.midi_out_indicator = MIDIIndicator()
        
        # Create labels
        in_label = QLabel("MIDI IN")
        out_label = QLabel("MIDI OUT")
        in_label.setStyleSheet("color: white; font-size: 10px;")
        out_label.setStyleSheet("color: white; font-size: 10px;")
        
        # Create container widget
        indicator_widget = QWidget(self)
        indicator_layout = QVBoxLayout(indicator_widget)
        indicator_layout.setSpacing(4)
        indicator_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add indicators with labels
        for label, indicator in [(in_label, self.midi_in_indicator), 
                               (out_label, self.midi_out_indicator)]:
            row = QHBoxLayout()
            row.addWidget(label)
            row.addWidget(indicator)
            indicator_layout.addLayout(row)
        
        # Position the container - moved right by 20px and down by 50px from original position
        indicator_widget.move(self.width() - 80, 120)  # Original was (self.width() - 100, 70)
        
        return indicator_widget 