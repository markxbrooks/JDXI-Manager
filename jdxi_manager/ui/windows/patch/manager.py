from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFileDialog, QLineEdit
)
from PySide6.QtCore import Qt
import logging

from jdxi_manager.midi.io import MIDIHelper
from jdxi_manager.ui.style import Style


class PatchManager(QMainWindow):
    def __init__(self, midi_helper=Optional[MIDIHelper], parent=None, save_mode=False):
        super().__init__(parent)
        self.midi_helper = midi_helper
        self.save_mode = save_mode
        
        # Set window properties
        self.setWindowTitle("Save Patch" if save_mode else "Load Patch")
        self.setMinimumSize(400, 200)
        
        # Apply dark theme styling
        self.setStyleSheet(Style.JDXI_PATCH_MANAGER)
        
        # Create central widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        # Create file path row
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select file location...")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self._browse_file)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        layout.addLayout(path_layout)
        
        # Create action buttons
        button_layout = QHBoxLayout()
        action_button = QPushButton("Save" if save_mode else "Load")
        action_button.clicked.connect(self._handle_action)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(action_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        # Set central widget
        self.setCentralWidget(main_widget)
    
    def _browse_file(self):
        """Open file dialog for selecting patch file"""
        try:
            if self.save_mode:
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Patch File",
                    "",
                    "Patch Files (*.syx);;All Files (*.*)"
                )
            else:
                file_path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Load Patch File",
                    "",
                    "Patch Files (*.syx);;All Files (*.*)"
                )
                
            if file_path:
                self.path_input.setText(file_path)
                
        except Exception as e:
            logging.error(f"Error browsing for file: {str(e)}")
    
    def _handle_action(self):
        """Handle save/load action"""
        try:
            file_path = self.path_input.text()
            if not file_path:
                return
                
            if self.save_mode:
                # Handle save
                if self.midi_helper:
                    self.midi_helper.save_patch(file_path)
                    logging.info(f"Patch saved to {file_path}")
            else:
                # Handle load
                if self.midi_helper:
                    self.midi_helper.load_patch(file_path)
                    logging.info(f"Patch loaded from {file_path}")
                    
            self.close()
            
        except Exception as e:
            logging.error(f"Error {'saving' if self.save_mode else 'loading'} patch: {str(e)}")