from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, Signal

class ValueDisplay(QWidget):
    valueChanged = Signal(int)
    
    def __init__(self, name, min_val, max_val, format_str="{}", parent=None):
        super().__init__(parent)
        self.min_val = min_val
        self.max_val = max_val
        self.format_str = format_str
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        self.name_label = QLabel(name)
        self.value_label = QLabel(self.format_str.format(0))
        self.value_label.setAlignment(Qt.AlignRight)
        self.value_label.setMinimumWidth(45)
        
        layout.addWidget(self.name_label)
        layout.addWidget(self.value_label)
        
    def setValue(self, value):
        clamped = max(self.min_val, min(self.max_val, value))
        self.value_label.setText(self.format_str.format(clamped))
        self.valueChanged.emit(clamped)
        
    def value(self):
        try:
            return int(self.value_label.text())
        except ValueError:
            return 0 