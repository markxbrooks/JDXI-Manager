"""
Piano keyboard widget for JD-Xi Manager.

This module defines address PianoKeyboard widget, address custom QWidget that arranges and displays
address set of piano keys styled like those on address JD-Xi synthesizer. The widget combines both
white and black keys to form address complete piano keyboard, along with labels representing
drum pad names.

Key Features:
- **Custom Key Dimensions:** White and black keys are sized and positioned appropriately,
    with configurable widths and heights.
- **Dynamic Key Creation:** White keys are created first in address horizontal layout,
    while black keys are overlaid at specific positions.
- **Drum Pad Labels:** A row of labels is displayed above the keyboard to denote
    corresponding drum pad names.
- **Signal Integration:** Each key emits custom signals (noteOn and noteOff) to notify
    parent widgets of key events.
- **MIDI Channel Configuration:** The widget supports setting address MIDI channel for outgoing
    note messages.
- **Styling and Layout:** Uses QHBoxLayout and QVBoxLayout to manage key and label placement,
    ensuring address neat appearance.

Usage Example:
    from jdxi_manager.ui.widgets.piano.keyboard import PianoKeyboard
    keyboard = PianoKeyboard(parent=main_window)
    keyboard.set_midi_channel(1)
    main_window.setCentralWidget(keyboard)

This module requires PySide6 and proper integration with the JD-Xi Manager's signal handling for note events.
"""

import logging
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QSize

from jdxi_manager.midi.data.keyboard.keyboard import KEYBOARD_BLACK_NOTES, KEYBOARD_WHITE_NOTES, DRUM_LABELS
from jdxi_manager.ui.style import Style
from jdxi_manager.ui.widgets.piano.key import PianoKey


class PianoKeyboard(QWidget):
    """Widget containing address row of piano keys styled like JD-Xi"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_channel = 0  # Default to analog synth channel

        # Set keyboard dimensions
        self.white_key_width = 35
        self.white_key_height = 160
        self.black_key_width = int(self.white_key_width * 0.6)
        self.black_key_height = 100

        # Define note patterns
        self.white_notes = KEYBOARD_WHITE_NOTES

        self.black_notes = KEYBOARD_BLACK_NOTES

        # Calculate total width
        total_width = len(self.white_notes) * self.white_key_width
        self.setFixedSize(
            total_width + 2, self.white_key_height + 30
        )  # Added height for labels

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add drum pad labels
        labels_layout = QHBoxLayout()
        labels_layout.setSpacing(0)
        labels_layout.setContentsMargins(1, 1, 1, 1)

        # Create and style labels
        for text in DRUM_LABELS:
            label = QLabel(text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(Style.JDXI_KEYBOARD_DRUM_LABELS)
            labels_layout.addWidget(label)

        labels_layout.addStretch()
        main_layout.addLayout(labels_layout)

        # Create keyboard container widget
        keyboard_widget = QWidget()
        keyboard_widget.setFixedSize(total_width + 2, self.white_key_height + 2)
        keyboard_layout = QHBoxLayout(keyboard_widget)
        keyboard_layout.setSpacing(0)
        keyboard_layout.setContentsMargins(1, 1, 1, 1)

        # Create keys
        self._create_keys(keyboard_widget)

        main_layout.addWidget(keyboard_widget)

    def _create_keys(self, keyboard_widget):
        """Create piano keys"""
        # First create all white keys
        for _, note in enumerate(self.white_notes):
            key = PianoKey(
                note,
                is_black=False,
                width=self.white_key_width,
                height=self.white_key_height,
            )
            keyboard_widget.layout().addWidget(key)

            # Connect signals
            if hasattr(self.parent(), "handle_piano_note_on"):
                key.noteOn.connect(self.parent().handle_piano_note_on)
            if hasattr(self.parent(), "handle_piano_note_off"):
                key.noteOff.connect(self.parent().handle_piano_note_off)

        # Then add black keys
        black_positions = [0, 1, 3, 4, 5, 7, 8, 10, 11, 12, 14, 15, 17, 18, 19]

        for pos, note in zip(
            black_positions, [n for n in KEYBOARD_BLACK_NOTES if n is not None]
        ):
            black_key = PianoKey(
                note,
                is_black=True,
                width=self.black_key_width,
                height=self.black_key_height,
            )
            black_key.setParent(keyboard_widget)

            # Position black key
            x_pos = (pos * self.white_key_width) + (
                self.white_key_width - self.black_key_width // 2
            )
            black_key.move(x_pos, 0)
            black_key.show()

            # Connect signals
            if hasattr(self.parent(), "handle_piano_note_on"):
                black_key.noteOn.connect(self.parent().handle_piano_note_on)
            if hasattr(self.parent(), "handle_piano_note_off"):
                black_key.noteOff.connect(self.parent().handle_piano_note_off)

    def set_midi_channel(self, channel: int):
        """Set MIDI channel for note messages"""
        self.current_channel = channel
        logging.debug(f"Piano keyboard set to channel {channel}")

    def _update_channel_display(self):
        """Update channel indicator"""
        self.channel_button.set_channel(self.current_channel)
