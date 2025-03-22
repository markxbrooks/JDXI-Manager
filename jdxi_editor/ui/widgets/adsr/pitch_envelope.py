"""
ADSR Widget for Roland JD-Xi

This widget provides address visual interface for editing ADSR (Attack, Decay, Sustain, Release)
envelope parameters. It includes:
- Interactive sliders for each ADSR parameter
- Visual envelope plot
- Real-time parameter updates
- MIDI parameter integration via SynthParameter objects

The widget supports both analog and digital synth parameters and provides visual feedback
through an animated envelope curve.
"""

import logging
import re

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QGridLayout, QSlider
from typing import Dict, Union
from jdxi_editor.midi.data.parameter.synth import SynthParameter
from jdxi_editor.midi.data.constants.sysex import TEMPORARY_ANALOG_SYNTH_AREA, TEMPORARY_TONE_AREA
from jdxi_editor.midi.message.roland import RolandSysEx
from jdxi_editor.ui.widgets.adsr.plot import ADSRPlot
from jdxi_editor.ui.widgets.slider.slider import Slider
from jdxi_editor.ui.style import Style
from jdxi_editor.midi.data.constants.analog import (
    ANALOG_PART,
    ANALOG_OSC_GROUP,
)
from jdxi_editor.midi.utils.conversions import (
    midi_cc_to_ms,
    ms_to_midi_cc,
)

# Precompile the regex pattern at module level or in the class constructor
ENVELOPE_PATTERN = re.compile(r'(attack|decay|release)', re.IGNORECASE)


class PitchEnvelope(QWidget):
    envelopeChanged = Signal(dict)

    def __init__(self,
                 attack_param: SynthParameter,
                 decay_param: SynthParameter,
                 depth_param: SynthParameter,
                 midi_helper=None,
                 group=None,
                 area=None,
                 part=None,
                 parent=None):
        super().__init__(parent)

        self.controls: Dict[SynthParameter, Slider] = {}
        self.midi_helper = midi_helper
        self.group = group if group else ANALOG_OSC_GROUP
        self.area = area if area else TEMPORARY_TONE_AREA
        self.part = part if part else ANALOG_PART
        self.updating_from_spinbox = False
        self.plot = ADSRPlot(width=300, height=250)

        self.setMinimumHeight(100)  # Adjust height as needed
        self.parameters = {
            'attack': attack_param,
            'decay': decay_param,
            'depth': depth_param,
            'release': 500,
            "sustain_level": 0.8
        }

        self.envelope = {
            "attack_time": 300,
            "decay_time": 800,
            "depth": 64,  # Centered (0-127 range)
            "release_time": 500,
            "sustain_level": 0.8,
            "peak_level": 1,
        }

        self.setMinimumHeight(100)
        self.attack_sb = self.create_spinbox(0, 1000, " ms", self.envelope["attack_time"])
        self.decay_sb = self.create_spinbox(0, 1000, " ms", self.envelope["decay_time"])
        self.depth_sb = self.create_spinbox(-63, 63, " ", self.envelope["depth"])

        self.layout = QGridLayout(self)

        # Create sliders
        self.attack_slider = self._create_parameter_slider(attack_param, "Attack", value=self.envelope["attack_time"])
        self.decay_slider = self._create_parameter_slider(decay_param, "Decay", value=self.envelope["decay_time"])
        self.depth_slider = self._create_parameter_slider(depth_param, "Depth", value=self.envelope["depth"])

        # Add sliders to layout
        self.layout.addWidget(self.attack_slider, 0, 0)
        self.layout.addWidget(self.decay_slider, 0, 1)
        self.layout.addWidget(self.depth_slider, 0, 2)

        self.layout.addWidget(self.attack_sb, 1, 0)
        self.layout.addWidget(self.decay_sb, 1, 1)
        self.layout.addWidget(self.depth_sb, 1, 2)
        self.layout.addWidget(self.plot, 0, 4, 3, 1)

        # Connect signals
        for sb in [self.attack_sb, self.decay_sb, self.depth_sb]:
            sb.valueChanged.connect(self.valueChanged)

        self.setLayout(self.layout)
        self.update_from_envelope()
        self.setStyleSheet(Style.JDXI_EDITOR)

    def update_from_envelope(self):
        """Initialize controls with parameter values"""
        self.update_spinboxes_from_envelope()
        self.update_sliders_from_envelope()
        self.update_controls_from_envelope()

    def update_controls_from_envelope(self):
        """Update slider controls from envelope values."""
        for param, slider in self.controls.items():
            #if param == self.parameters['sustain']:
            #    slider.setValue(int(self.envelope["sustain_level"] * 127))
            #else:
            if match := ENVELOPE_PATTERN.search(param.name):
                key = f"{match.group().lower()}_time"
                slider.setValue(ms_to_midi_cc(self.envelope[key]))

    def _create_parameter_slider_old(self, param, label, value=None):
        slider = QSlider(Qt.Vertical)
        slider.setRange(param.min_val, param.max_val)
        slider.setValue(value)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.valueChanged.connect(lambda v: self._on_parameter_changed(param, v))
        return slider

    def set_envelope(self, envelope: Dict[str, Union[int, float]]):
        """Set envelope values and update controls"""
        self.envelope = envelope
        self.update_controls_from_envelope()
        self.plot.set_values(self.envelope)

    def _create_parameter_slider(self, param: SynthParameter, label: str, value: int = None) -> Slider:
        """Create address slider for address parameter with proper display conversion"""
        if hasattr(param, "get_display_value"):
            display_min, display_max = param.get_display_value()
        else:
            display_min, display_max = param.min_val, param.max_val

        # Create vertical slider
        slider = Slider(label, display_min, display_max, vertical=True, show_value_label=False)
        slider.setValue(value)
        # Connect value changed signal
        slider.valueChanged.connect(lambda v: self._on_parameter_changed(param, v))

        # Store control reference
        self.controls[param] = slider
        return slider

    def valueChanged(self):
        self.envelope["attack_time"] = self.attack_sb.value()
        self.envelope["decay_time"] = self.decay_sb.value()
        self.envelope["depth"] = self.depth_sb.value()
        self.envelope["release_time"] = 500

        self.update_sliders_from_envelope()
        self.envelopeChanged.emit(self.envelope)

    def update_envelope_from_controls(self):
        """Update envelope values from slider controls. @@"""
        for param, slider in self.controls.items():
            if match := ENVELOPE_PATTERN.search(param.name):
                key = f"{match.group().lower()}_time"
                self.envelope[key] = midi_cc_to_ms(slider.value())
                logging.info(f"param: {param} slider value: {slider.value()}")
                logging.info(f'{key}: {self.envelope[key]}')

    def update_spin_box(self, param):
        """Update the corresponding spin box based on the given parameter."""
        # Mapping of parameters to their corresponding spin box and envelope keys
        param_mapping = {
            self.parameters['decay']: (self.decay_sb, "decay_time"),
            self.parameters['attack']: (self.attack_sb, "attack_time"),
            self.parameters['depth']: (self.depth_sb, "depth"),
        }

        # Update the corresponding spin box if the parameter is in the mapping
        if param in param_mapping:
            spin_box, envelope_key = param_mapping[param]
            spin_box.blockSignals(True)
            spin_box.setValue(self.envelope[envelope_key])
            spin_box.blockSignals(False)

    def _on_parameter_changed(self, param: SynthParameter, value: int):
        """Handle parameter value changes and update envelope accordingly."""
        # logging.info(f"_on_parameter_changed param: {param} value: {value}")
        # Update display range if available
        if hasattr(param, "get_display_value"):
            display_min, display_max = param.get_display_value()
        else:
            display_min, display_max = param.min_val, param.max_val
        # Update envelope based on slider values
        self.update_envelope_from_controls()
        self.update_spin_box(param)
        try:
            # Convert display value to MIDI value if needed
            if hasattr(param, "convert_from_display"):
                midi_value = param.convert_from_display(value)
            else:
                midi_value = param.validate_value(value)

            # Send MIDI message
            if not self.send_midi_parameter(param, midi_value):
                logging.warning(f"Failed to send parameter {param.name}")
        except ValueError as ex:
            logging.error(f"Error updating parameter: {ex}")
        self.plot.set_values(self.envelope)
        self.envelopeChanged.emit(self.envelope)

    def _on_parameter_changed_old(self, param, value):
        if param == self.parameters['attack']:
            self.envelope["attack_time"] = value
        elif param == self.parameters['decay']:
            self.envelope["decay_time"] = value
        elif param == self.parameters['depth']:
            self.envelope["depth"] = value
        self.update_spinboxes_from_envelope()
        self.envelopeChanged.emit(self.envelope)

    def update_sliders_from_envelope(self):
        self.attack_slider.setValue(self.envelope["attack_time"])
        self.decay_slider.setValue(self.envelope["decay_time"])
        self.depth_slider.setValue(self.envelope["depth"])

    def update_spinboxes_from_envelope(self):
        self.attack_sb.setValue(self.envelope["attack_time"])
        self.decay_sb.setValue(self.envelope["decay_time"])
        self.depth_sb.setValue(self.envelope["depth"])

    def create_spinbox(self, min_value, max_value, suffix, value):
        sb = QSpinBox()
        sb.setRange(min_value, max_value)
        sb.setSuffix(suffix)
        sb.setValue(value)
        return sb

    def send_midi_parameter(self, param, value) -> bool:
        """Send MIDI parameter with error handling"""
        if not self.midi_helper:
            logging.debug("No MIDI helper available - parameter change ignored")
            return False

        try:
            group = self.group  # Common parameters area
            param_address = param.address
            sysex_message = RolandSysEx(area=self.area,
                                        section=self.part,
                                        group=group,
                                        param=param_address,
                                        value=value)
            return self.midi_helper.send_midi_message(sysex_message)
        except Exception as e:
            logging.error(f"MIDI error setting {param}: {str(e)}")
            return False
