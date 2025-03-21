"""
Module: preset_handler
======================

This module defines the `PresetHandler` class, which extends `PresetHelper` to manage
preset selection and navigation for a MIDI-enabled synthesizer.

Classes:
--------
- `PresetHandler`: Handles preset loading, switching, and signaling for UI updates.

Dependencies:
-------------
- `PySide6.QtCore` (Signal, QObject) for event-driven UI interaction.
- `jdxi_manager.midi.data.presets.type.PresetType` for managing preset types.
- `jdxi_manager.midi.preset.loader.PresetLoader` as the base class for preset loading.

Functionality:
--------------
- Loads presets via MIDI.
- Emits signals when a preset changes (`preset_changed`).
- Supports navigation through available presets (`next_tone`, `previous_tone`).
- Retrieves current preset details (`get_current_preset`).

Usage:
------
This class is typically used within a larger MIDI control application to handle
preset changes and communicate them to the UI and MIDI engine.

"""

from PySide6.QtCore import Signal

from jdxi_editor.midi.preset.type import SynthType
from jdxi_editor.midi.preset.helper import PresetHelper


class PresetHandler(PresetHelper):
    """ Preset Loading Class """
    preset_changed = Signal(int, int)  # Signal emitted when preset changes

    def __init__(self, midi_helper, presets, device_number=0, channel=1, preset_type=SynthType.DIGITAL_1):
        super().__init__(midi_helper, device_number)  # Call PresetLoader's constructor
        self.presets = presets
        self.channel = channel
        self.type = preset_type
        self.current_preset_zero_based = 0

    def next_tone(self):
        """Increase the tone index and return the new preset."""
        if self.current_preset_zero_based < len(self.presets) - 1:
            self.current_preset_zero_based += 1
            self.preset_changed.emit(self.current_preset_zero_based_index, self.channel)
            # self.update_display.emit(self.type, self.current_preset_zero_based_index, self.channel)  # convert to 1-based index
        return self.get_current_preset()

    def previous_tone(self):
        """Decrease the tone index and return the new preset."""
        if self.current_preset_zero_based > 0:
            self.current_preset_zero_based -= 1
            self.preset_changed.emit(self.current_preset_zero_based, self.channel)
            # self.update_display.emit(self.type, self.current_preset_zero_based_index, self.channel)  # convert to 1-based index
        return self.get_current_preset()

    def get_current_preset(self):
        """Get the current preset details."""
        return {
            "index": self.current_preset_zero_based,
            "preset": self.presets[self.current_preset_zero_based],
            "channel": self.channel,
        }

    def get_available_presets(self):
        """Get the available presets."""
        return self.presets

    def save_preset(self, program_number: int, params):
        """Save the current preset to the preset list."""
        name = self.presets[program_number]
        print(f"name: \t{name}")
        print(f"params: \t{params}")
        self.preset_changed.emit(self.current_preset_zero_based, self.channel)
        self.update_display.emit(self.type, self.current_preset_zero_based, self.channel)
        return self.get_current_preset()


