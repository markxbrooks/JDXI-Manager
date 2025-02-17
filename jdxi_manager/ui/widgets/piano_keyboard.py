from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor, QPen, QLinearGradient, QPalette
from PySide6.QtCore import Signal
import logging
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPen
from PySide6.QtCore import Qt, QPropertyAnimation, Property, QPointF


from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Signal, QPropertyAnimation, QEasingCurve, Qt, QRect
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPen


class PianoKeyboard(QWidget):
    """Widget containing a row of piano keys styled like JD-Xi"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_channel = 0  # Default to analog synth channel

        # Set keyboard dimensions
        self.white_key_width = 35
        self.white_key_height = 160
        self.black_key_width = int(self.white_key_width * 0.6)
        self.black_key_height = 100

        # Define note patterns
        self.white_notes = [
            36,
            38,
            40,
            41,
            43,
            45,
            47,  # C1 to B1
            48,
            50,
            52,
            53,
            55,
            57,
            59,  # C2 to B2
            60,
            62,
            64,
            65,
            67,
            69,
            71,  # C3 to B3
            72,  # C4
        ]

        self.black_notes = [
            37,
            39,
            None,
            42,
            44,
            46,  # C#1 to B1
            49,
            51,
            None,
            54,
            56,
            58,  # C#2 to B2
            61,
            63,
            None,
            66,
            68,
            70,  # C#3 to B3
        ]

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

        # Drum pad names in order
        drum_labels = [
            "BD1",
            "RIM",
            "BD2",
            "CLP",
            "BD3",
            "SD1",
            "CHH",
            "SD2",
            "PHH",
            "SD3",
            "OHH",
            "SD4",
            "TM1",
            "PC1",
            "TM2",
            "PC2",
            "TM3",
            "PC3",
            "CY1",
            "PC4",
            "CY2",
            "PC5",
            "CY3",
            "HIT",
            "OT1",
            "OT2",
            "   ",
            "   ",
            "   ",
            "   ",
            "   ",
            "   ",
            "   ",
            "   ",
            "   ",
            "   ",
            "  ",
            " ",
        ]

        # Create and style labels
        for text in drum_labels:
            label = QLabel(text)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet(
                """
                QLabel {
                    color: #808080;
                    font-size: 7px;
                    font-family: monospace;
                    padding: 2px;
                    min-width: 30px;
                }
            """
            )
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
        for i, note in enumerate(self.white_notes):
            key = JDXiKey(
                note,
                is_black=False,
                width=self.white_key_width,
                height=self.white_key_height,
            )
            keyboard_widget.layout().addWidget(key)

            # Connect signals
            if hasattr(self.parent(), "_handle_piano_note_on"):
                key.noteOn.connect(self.parent()._handle_piano_note_on)
            if hasattr(self.parent(), "_handle_piano_note_off"):
                key.noteOff.connect(self.parent()._handle_piano_note_off)

        # Then add black keys
        black_positions = [0, 1, 3, 4, 5, 7, 8, 10, 11, 12, 14, 15, 17, 18, 19]

        for pos, note in zip(
            black_positions, [n for n in self.black_notes if n is not None]
        ):
            black_key = JDXiKey(
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
            if hasattr(self.parent(), "_handle_piano_note_on"):
                black_key.noteOn.connect(self.parent()._handle_piano_note_on)
            if hasattr(self.parent(), "_handle_piano_note_off"):
                black_key.noteOff.connect(self.parent()._handle_piano_note_off)

    def set_midi_channel(self, channel: int):
        """Set MIDI channel for note messages"""
        self.current_channel = channel
        logging.debug(f"Piano keyboard set to channel {channel}")

    def _update_channel_display(self):
        """Update channel indicator"""
        self.channel_button.set_channel(self.current_channel)


class ChannelButton(QPushButton):
    """Channel indicator button with synth-specific styling"""

    CHANNEL_STYLES = {
        0: ("ANALOG", "#FF8C00"),  # Orange for Analog
        1: ("DIGI 1", "#00FF00"),  # Green for Digital 1
        2: ("DIGI 2", "#00FFFF"),  # Cyan for Digital 2
        9: ("DRUMS", "#FF00FF"),  # Magenta for Drums
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 160)  # Same height as white keys
        self.setFlat(True)
        self.current_channel = 0
        self._update_style()

    def set_channel(self, channel: int):
        """Set channel and update appearance"""
        self.current_channel = channel
        self._update_style()

    def _update_style(self):
        """Update button appearance based on channel"""
        style, color = self.CHANNEL_STYLES.get(
            self.current_channel, (f"CH {self.current_channel + 1}", "#FFFFFF")
        )

        # Create gradient background
        gradient = f"""
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {color}33,
                stop:0.5 {color}22,
                stop:1 {color}33
            );
        """

        # Set button style
        self.setStyleSheet(
            f"""
            QPushButton {{
                {gradient}
                border: 1px solid {color};
                border-radius: 3px;
                color: {color};
                font-size: 10px;
                font-weight: bold;
                padding: 2px;
                text-align: center;
            }}
            QPushButton:pressed {{
                background: {color}44;
            }}
        """
        )

        # Set text
        self.setText(style)

    def paintEvent(self, event):
        """Custom paint event for vertical text"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Save current state
        painter.save()

        # Rotate text
        painter.translate(self.width(), 0)
        painter.rotate(90)

        # Draw text
        painter.drawText(0, 0, self.height(), self.width(), Qt.AlignCenter, self.text())

        # Restore state
        painter.restore()


from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, Signal
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen


from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, Signal
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen


class JDXiKey(QPushButton):
    """Piano key styled like JD-Xi keys with animations"""

    noteOn = Signal(int)
    noteOff = Signal(int)

    def __init__(self, note_num, is_black=False, width=22, height=160, parent=None):
        super().__init__(parent)
        self.note_num = note_num
        self.is_black = is_black
        self.is_pressed = False
        self.setFixedSize(width, height)
        self.setFlat(True)

        # Animation setup
        self.press_animation = QPropertyAnimation(self, b"geometry")
        self.press_animation.setDuration(50)

        self.release_animation = QPropertyAnimation(self, b"geometry")
        self.release_animation.setDuration(100)

    def paintEvent(self, event):
        """Custom paint for JD-Xi style keys"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())

        if self.is_black:
            if self.is_pressed:
                gradient.setColorAt(0, QColor(80, 80, 80))
                gradient.setColorAt(1, QColor(40, 40, 40))
            else:
                gradient.setColorAt(0, QColor(40, 40, 40))
                gradient.setColorAt(1, QColor(10, 10, 10))
        else:
            if self.is_pressed:
                gradient.setColorAt(0, QColor(200, 200, 200))
                gradient.setColorAt(1, QColor(180, 180, 180))
            else:
                gradient.setColorAt(0, QColor(255, 255, 255))
                gradient.setColorAt(1, QColor(220, 220, 220))

        painter.fillRect(0, 0, self.width(), self.height(), gradient)

        if self.is_pressed:
            painter.fillRect(
                0, self.height() - 4, self.width(), 4, QColor(255, 0, 0, 100)
            )

        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = True
            self.noteOn.emit(self.note_num)
            self.update()

            # Adjust movement amount based on key type
            move_amount = 3 if not self.is_black else 2  # Black keys move less

            self.press_animation.setStartValue(self.geometry())
            self.press_animation.setEndValue(
                QRect(
                    self.x(),
                    self.y() + move_amount,
                    self.width(),
                    self.height() - move_amount,
                )
            )
            self.press_animation.start()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_pressed = False
            self.noteOff.emit(self.note_num)
            self.update()

            move_amount = 3 if not self.is_black else 2  # Restore position

            self.release_animation.setStartValue(self.geometry())
            self.release_animation.setEndValue(
                QRect(
                    self.x(),
                    self.y() - move_amount,
                    self.width(),
                    self.height() + move_amount,
                )
            )
            self.release_animation.start()


class JDXiKeyOld(QPushButton):
    """Piano key styled like JD-Xi keys"""

    noteOn = Signal(int)
    noteOff = Signal(int)

    def __init__(self, note_num, is_black=False, width=22, height=160, parent=None):
        super().__init__(parent)
        self.note_num = note_num
        self.is_black = is_black
        self.is_pressed = False
        self.setFixedSize(width, height)

        # Remove border and set flat style
        self.setFlat(True)

    def paintEvent(self, event):
        """Custom paint for JD-Xi style keys"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.is_black:
            # Black key gradient
            if self.is_pressed:
                # Lighter gradient when pressed
                gradient = QLinearGradient(0, 0, 0, self.height())
                gradient.setColorAt(0, QColor(80, 80, 80))  # Lighter top
                gradient.setColorAt(1, QColor(40, 40, 40))  # Lighter bottom
            else:
                # Normal gradient when not pressed
                gradient = QLinearGradient(0, 0, 0, self.height())
                gradient.setColorAt(0, QColor(40, 40, 40))
                gradient.setColorAt(1, QColor(10, 10, 10))

            painter.fillRect(0, 0, self.width(), self.height(), gradient)

            # Thinner red glow when pressed
            if self.is_pressed:
                painter.fillRect(
                    0, self.height() - 4, self.width(), 4, QColor(255, 0, 0, 100)
                )
        else:
            # White key gradient
            gradient = QLinearGradient(0, 0, 0, self.height())
            if self.is_pressed:
                # Darker gradient when pressed
                gradient.setColorAt(0, QColor(200, 200, 200))  # Darker white
                gradient.setColorAt(1, QColor(180, 180, 180))  # Even darker at bottom
            else:
                gradient.setColorAt(0, QColor(255, 255, 255))
                gradient.setColorAt(1, QColor(220, 220, 220))
            painter.fillRect(0, 0, self.width(), self.height(), gradient)

            # Thinner red glow when pressed
            if self.is_pressed:
                painter.fillRect(
                    0, self.height() - 4, self.width(), 4, QColor(255, 0, 0, 100)
                )

        # Draw border
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_pressed = True
            self.noteOn.emit(self.note_num)
            self.update()
            logging.debug(f"Note On: {self.note_num}")

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_pressed = False
            self.noteOff.emit(self.note_num)
            self.update()
            logging.debug(f"Note Off: {self.note_num}")
