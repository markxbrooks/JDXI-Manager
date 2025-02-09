import logging
import os
import re
import json
from functools import partial
from typing import Optional, Dict, Union

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QScrollArea,
    QComboBox,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
import qtawesome as qta

from jdxi_manager.data.digital import DigitalCommonParameter
from jdxi_manager.data.preset_data import ANALOG_PRESETS, DIGITAL_PRESETS
from jdxi_manager.data.preset_type import PresetType
from jdxi_manager.data.analog import (
    AnalogParameter,
    AnalogCommonParameter,
    get_analog_parameter_by_address,
)
from jdxi_manager.midi import MIDIHelper
from jdxi_manager.midi.conversions import (
    midi_cc_to_ms,
    midi_cc_to_frac,
    frac_to_midi_cc,
    ms_to_midi_cc,
)
from jdxi_manager.midi.preset_loader import PresetLoader
from jdxi_manager.ui.editors.base_editor import BaseEditor
from jdxi_manager.ui.editors.digital import base64_to_pixmap
from jdxi_manager.ui.style import Style
from jdxi_manager.ui.widgets.adsr_widget import ADSRWidget
from jdxi_manager.ui.widgets.analog_waveform import AnalogWaveformButton
from jdxi_manager.ui.widgets.preset_combo_box import PresetComboBox
from jdxi_manager.ui.widgets.slider import Slider
from jdxi_manager.ui.widgets.waveform import (
    WaveformButton,
    upsaw_png,
    triangle_png,
    pwsqu_png,
    adsr_waveform_icon,
)
from jdxi_manager.ui.widgets.switch import Switch
from jdxi_manager.midi.constants.analog import (
    AnalogToneCC,
    Waveform,
    SubOscType,
    ANALOG_SYNTH_AREA,
    ANALOG_PART,
    ANALOG_OSC_GROUP,
)
import base64

instrument_icon_folder = "analog_synths"


class AnalogSynthEditor(BaseEditor):
    """Analog Synth"""

    preset_changed = Signal(int, str, int)

    def __init__(self, midi_helper: Optional[MIDIHelper], parent=None):
        super().__init__(midi_helper, parent)
        self.part = ANALOG_PART
        self.preset_loader = None
        self.setWindowTitle("Analog Synth")

        # Allow resizing
        self.setMinimumSize(800, 400)
        self.resize(1000, 600)
        self.image_label = QLabel()
        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Center align the image
        self.main_window = parent
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.presets = ANALOG_PRESETS
        self.preset_type = PresetType.ANALOG
        # Create scroll area for resizable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # Store parameter controls for easy access
        self.controls: Dict[Union[AnalogParameter, AnalogCommonParameter], QWidget] = {}
        self.updating_from_spinbox = False
        # Create container widget for scroll area
        container = QWidget()
        container_layout = QVBoxLayout()
        container.setLayout(container_layout)

        # Additional styling specific to analog editor
        self.setStyleSheet(
            Style.ANALOG_EDITOR_STYLE
            + "QSlider::groove:vertical { background: #222222; }"
        )
        upper_layout = QHBoxLayout()
        container_layout.addLayout(upper_layout)

        # Title and drum kit selection
        instrument_preset_group = QGroupBox("Analog Synth")
        self.instrument_title_label = QLabel(
            f"Analog Synth:\n {self.presets[0]}" if self.presets else "Analog Synth"
        )
        instrument_preset_group.setStyleSheet(
            """
            QGroupBox {
            width: 300px;
            }
        """
        )
        self.instrument_title_label.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
        """
        )
        instrument_title_group_layout = QVBoxLayout()
        instrument_preset_group.setLayout(instrument_title_group_layout)
        instrument_title_group_layout.addWidget(self.instrument_title_label)

        # Add the "Read Request" button
        self.read_request_button = QPushButton("Send Read Request to Synth")
        self.read_request_button.clicked.connect(self.data_request)
        instrument_title_group_layout.addWidget(self.read_request_button)

        self.instrument_selection_label = QLabel("Select an Analog synth:")
        instrument_title_group_layout.addWidget(self.instrument_selection_label)
        # Synth selection
        self.instrument_selection_combo = PresetComboBox(ANALOG_PRESETS)
        self.instrument_selection_combo.combo_box.setEditable(True)  # Allow text search
        self.instrument_selection_combo.combo_box.currentIndexChanged.connect(
            self.update_instrument_image
        )
        # Connect QComboBox signal to PresetHandler
        self.main_window.analog_preset_handler.preset_changed.connect(
            self.update_combo_box_index
        )
        self.instrument_selection_combo.combo_box.currentIndexChanged.connect(
            self.update_instrument_title
        )
        self.instrument_selection_combo.combo_box.currentIndexChanged.connect(
            self.update_instrument_preset
        )
        instrument_title_group_layout.addWidget(self.instrument_selection_combo)
        upper_layout.addWidget(instrument_preset_group)
        upper_layout.addWidget(self.image_label)
        container_layout.addLayout(upper_layout)
        self.update_instrument_image()
        # Add sections side by side
        container_layout.addWidget(self._create_oscillator_section())
        container_layout.addWidget(self._create_filter_section())
        container_layout.addWidget(self._create_amp_section())
        container_layout.addWidget(self._create_lfo_section())

        # Add container to scroll area
        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        # Connect oscillator controls
        self.coarse.valueChanged.connect(
            lambda v: self._send_cc(AnalogToneCC.OSC_COARSE, v + 64)  # Center at 0
        )
        self.fine.valueChanged.connect(
            lambda v: self._send_cc(AnalogToneCC.OSC_FINE, v + 64)  # Center at 0
        )

        # Connect filter controls
        self.cutoff.valueChanged.connect(
            lambda v: self._send_cc(AnalogToneCC.FILTER_CUTOFF, v)
        )
        self.resonance.valueChanged.connect(
            lambda v: self._send_cc(AnalogToneCC.FILTER_RESO, v)
        )
        self.midi_helper.parameter_received.connect(self._on_parameter_received)
        self.midi_helper.json_sysex.connect(self.update_sliders_from_sysex)
        self.data_request()

    def _create_oscillator_section(self):
        group = QGroupBox("Oscillator")
        layout = QVBoxLayout()
        group.setLayout(layout)

        oscillator_hlayout = QHBoxLayout()
        for icon in [
            "mdi.triangle-wave",
            "mdi.sine-wave",
            "fa5s.wave-square",
            "mdi.cosine-wave",
            "mdi.triangle-wave",
            "mdi.waveform",
        ]:
            oscillator_triangle_label = QLabel()
            icon = qta.icon(icon)
            pixmap = icon.pixmap(30, 30)  # Set the desired size
            oscillator_triangle_label.setPixmap(pixmap)
            oscillator_triangle_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            oscillator_hlayout.addWidget(oscillator_triangle_label)
        layout.addLayout(oscillator_hlayout)

        # Waveform buttons
        wave_layout = QHBoxLayout()
        self.wave_buttons = {}
        for waveform in [Waveform.SAW, Waveform.TRIANGLE, Waveform.PULSE]:
            btn = AnalogWaveformButton(waveform)

            # Set icons for each waveform
            if waveform == Waveform.SAW:
                saw_icon_base64 = upsaw_png("#FFFFFF", 1.0)
                saw_pixmap = self._base64_to_pixmap(saw_icon_base64)
                btn.setIcon(QIcon(saw_pixmap))
            elif waveform == Waveform.TRIANGLE:
                tri_icon_base64 = triangle_png("#FFFFFF", 1.0)
                tri_pixmap = self._base64_to_pixmap(tri_icon_base64)
                btn.setIcon(QIcon(tri_pixmap))
            elif waveform == Waveform.PULSE:
                pulse_icon_base64 = pwsqu_png("#FFFFFF", 1.0)
                pulse_pixmap = self._base64_to_pixmap(pulse_icon_base64)
                btn.setIcon(QIcon(pulse_pixmap))

            btn.waveform_selected.connect(self._on_waveform_selected)
            self.wave_buttons[waveform] = btn
            wave_layout.addWidget(btn)
        layout.addLayout(wave_layout)

        # Tuning controls
        tuning_group = QGroupBox("Tuning")
        tuning_layout = QVBoxLayout()
        tuning_group.setLayout(tuning_layout)

        self.coarse = Slider("Coarse", -24, 24)  # Will be mapped to 40-88
        self.coarse.valueChanged.connect(
            self._on_coarse_changed
        )  # Changed to new method

        self.fine = Slider("Fine", -50, 50)  # Will be mapped to 14-114
        self.fine.valueChanged.connect(self._on_fine_changed)  # Changed to new method

        tuning_layout.addWidget(self.coarse)
        tuning_layout.addWidget(self.fine)
        layout.addWidget(tuning_group)

        # Pulse Width controls
        pw_group = QGroupBox("Pulse Width")
        pw_layout = QVBoxLayout()
        pw_group.setLayout(pw_layout)

        self.pw = self._create_parameter_slider(
            AnalogParameter.OSC_PULSE_WIDTH,
            "Width",
        )
        self.pw_mod = self._create_parameter_slider(
            AnalogParameter.OSC_PULSE_WIDTH_MOD_DEPTH,
            "Mod Depth",
        )

        pw_layout.addWidget(self.pw)
        pw_layout.addWidget(self.pw_mod)
        layout.addWidget(pw_group)

        # Pitch Envelope
        pitch_env_group = QGroupBox("Pitch Envelope")
        pitch_env_layout = QVBoxLayout()
        pitch_env_group.setLayout(pitch_env_layout)

        self.pitch_env_velo = self._create_parameter_slider(
            AnalogParameter.OSC_PITCH_ENV_VELOCITY_SENS, "Mod Depth"
        )
        self.pitch_env_attack = self._create_parameter_slider(
            AnalogParameter.OSC_PITCH_ENV_ATTACK_TIME, "Attack"
        )
        self.pitch_env_decay = self._create_parameter_slider(
            AnalogParameter.OSC_PITCH_ENV_DECAY, "Decay"
        )
        self.pitch_env_depth = self._create_parameter_slider(
            AnalogParameter.OSC_PITCH_ENV_DEPTH, "Depth"
        )

        pitch_env_layout.addWidget(self.pitch_env_velo)
        pitch_env_layout.addWidget(self.pitch_env_attack)
        pitch_env_layout.addWidget(self.pitch_env_decay)
        pitch_env_layout.addWidget(self.pitch_env_depth)
        layout.addWidget(pitch_env_group)

        # Sub Oscillator
        sub_group = QGroupBox("Sub Oscillator")
        sub_layout = QVBoxLayout()
        sub_group.setLayout(sub_layout)

        self.sub_type = Switch(
            "Type",
            [
                SubOscType.OFF.display_name,
                SubOscType.OCT_DOWN_1.display_name,
                SubOscType.OCT_DOWN_2.display_name,
            ],
        )
        self.sub_type.valueChanged.connect(self._on_sub_type_changed)
        sub_layout.addWidget(self.sub_type)
        layout.addWidget(sub_group)

        # Update PW controls enabled state based on current waveform
        self._update_pw_controls_state(Waveform.SAW)  # Initial state

        return group

    def update_combo_box_index(self, preset_number):
        """Updates the QComboBox to reflect the loaded preset."""
        logging.info(f"Updating combo to preset {preset_number}")
        self.instrument_selection_combo.combo_box.setCurrentIndex(preset_number)

    def update_instrument_title(self):
        selected_synth_text = self.instrument_selection_combo.combo_box.currentText()
        logging.info(f"selected_synth_text: {selected_synth_text}")
        self.instrument_title_label.setText(f"Analog Synth:\n {selected_synth_text}")

    def update_instrument_preset(self):
        selected_synth_text = self.instrument_selection_combo.combo_box.currentText()
        if synth_matches := re.search(
            r"(\d{3}): (\S+).+", selected_synth_text, re.IGNORECASE
        ):
            selected_synth_padded_number = (
                synth_matches.group(1).lower().replace("&", "_").split("_")[0]
            )
            preset_index = int(selected_synth_padded_number)
            logging.info(f"preset_index: {preset_index}")
            self.load_preset(preset_index)

    def update_instrument_image(self):
        def load_and_set_image(image_path, secondary_image_path):
            """Helper function to load and set the image on the label."""
            file_to_load = ""
            if os.path.exists(image_path):
                file_to_load = image_path
            elif os.path.exists(secondary_image_path):
                file_to_load = secondary_image_path
            else:
                file_to_load = os.path.join(
                    "resources", instrument_icon_folder, "analog.png"
                )
            pixmap = QPixmap(file_to_load)
            scaled_pixmap = pixmap.scaledToHeight(
                250, Qt.TransformationMode.SmoothTransformation
            )  # Resize to 250px height
            self.image_label.setPixmap(scaled_pixmap)
            return True

        selected_instrument_text = (
            self.instrument_selection_combo.combo_box.currentText()
        )

        # Try to extract synth name from the selected text
        image_loaded = False
        if instrument_matches := re.search(
            r"(\d{3}): (\S+)\s(\S+)+", selected_instrument_text, re.IGNORECASE
        ):
            selected_instrument_name = (
                instrument_matches.group(2).lower().replace("&", "_").split("_")[0]
            )
            selected_instrument_type = (
                instrument_matches.group(3).lower().replace("&", "_").split("_")[0]
            )
            logging.info(f"selected_instrument_type: {selected_instrument_type}")
            specific_image_path = os.path.join(
                "resources",
                instrument_icon_folder,
                f"{selected_instrument_name}.png",
            )
            generic_image_path = os.path.join(
                "resources",
                instrument_icon_folder,
                f"{selected_instrument_type}.png",
            )
            image_loaded = load_and_set_image(specific_image_path, generic_image_path)

        # Fallback to default image if no specific image is found
        if not image_loaded:
            if not load_and_set_image(default_image_path):
                self.image_label.clear()  # Clear label if default image is also missing

    def load_preset(self, preset_index):
        preset_data = {
            "type": self.preset_type,  # Ensure this is a valid type
            "selpreset": preset_index,  # Convert to 1-based index
            "modified": 0,  # or 1, depending on your logic
        }
        if not self.preset_loader:
            self.preset_loader = PresetLoader(self.midi_helper)
        if self.preset_loader:
            self.preset_loader.load_preset(preset_data)

    def _update_pw_controls_state(self, waveform: Waveform):
        """Enable/disable PW controls based on waveform"""
        pw_enabled = waveform == Waveform.PULSE
        self.pw.setEnabled(pw_enabled)
        self.pw_mod.setEnabled(pw_enabled)
        # Update the visual state
        self.pw.setStyleSheet(
            "" if pw_enabled else "QSlider::groove:vertical { background: #222222; }"
        )
        self.pw_mod.setStyleSheet(
            "" if pw_enabled else "QSlider::groove:vertical { background: #222222; }"
        )

    def send_midi_parameter(self, param, value) -> bool:
        """Send MIDI parameter with error handling"""
        if not self.midi_helper:
            logging.debug("No MIDI helper available - parameter change ignored")
            return False

        try:
            # Get parameter group and address with partial offset
            # if isinstance(param, AnalogParameter):
            #    group, param_address = param.get_address_for_partial(self.partial_num)
            # else:
            group = ANALOG_OSC_GROUP  # Common parameters group
            param_address = param.address

            # Ensure value is included in the MIDI message
            return self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=self.part,
                group=group,
                param=param_address,
                value=value,  # Make sure this value is being sent
            )
        except Exception as e:
            logging.error(f"MIDI error setting {param}: {str(e)}")
            return False

    def _on_parameter_changed(
        self, param: Union[AnalogParameter, AnalogCommonParameter], display_value: int
    ):
        """Handle parameter value changes from UI controls"""
        try:
            # Convert display value to MIDI value if needed
            if hasattr(param, "convert_from_display"):
                midi_value = param.convert_from_display(display_value)
            else:
                midi_value = param.validate_value(display_value)

            # Send MIDI message
            if not self.send_midi_parameter(param, midi_value):
                logging.warning(f"Failed to send parameter {param.name}")

        except Exception as e:
            logging.error(f"Error handling parameter {param.name}: {str(e)}")

    def _create_parameter_slider(
        self,
        param: Union[AnalogParameter, AnalogCommonParameter],
        label: str,
        vertical=False,
    ) -> Slider:
        """Create a slider for a parameter with proper display conversion"""
        if hasattr(param, "get_display_value"):
            display_min, display_max = param.get_display_value()
        else:
            display_min, display_max = param.min_val, param.max_val

        # Create horizontal slider (removed vertical ADSR check)
        slider = Slider(label, display_min, display_max, vertical)

        # Connect value changed signal
        slider.valueChanged.connect(lambda v: self._on_parameter_changed(param, v))

        # Store control reference
        self.controls[param] = slider
        return slider

    def on_amp_env_adsr_envelope_changed(self, envelope):
        if not self.updating_from_spinbox:
            self.controls[AnalogParameter.AMP_ENV_ATTACK_TIME].setValue(
                ms_to_midi_cc(envelope["attackTime"], 10, 1000)
            )
            self.controls[AnalogParameter.AMP_ENV_DECAY_TIME].setValue(
                ms_to_midi_cc(envelope["decayTime"], 10, 1000)
            )
            self.controls[AnalogParameter.AMP_ENV_SUSTAIN_LEVEL].setValue(
                ms_to_midi_cc(envelope["sustainAmpl"], 0.1, 1)
            )
            self.controls[AnalogParameter.AMP_ENV_RELEASE_TIME].setValue(
                ms_to_midi_cc(envelope["releaseTime"], 10, 1000)
            )

    def ampEnvAdsrValueChanged(self):
        self.updating_from_spinbox = True
        self.amp_env_adsr_widget.envelope["attackTime"] = (
            self.amp_env_adsr_widget.attackSB.value()
        )
        self.amp_env_adsr_widget.envelope["decayTime"] = (
            self.amp_env_adsr_widget.decaySB.value()
        )
        self.amp_env_adsr_widget.envelope["releaseTime"] = (
            self.amp_env_adsr_widget.releaseSB.value()
        )
        self.amp_env_adsr_widget.envelope["initialAmpl"] = (
            self.amp_env_adsr_widget.initialSB.value()
        )
        self.amp_env_adsr_widget.envelope["peakAmpl"] = (
            self.amp_env_adsr_widget.peakSB.value()
        )
        self.amp_env_adsr_widget.envelope["sustainAmpl"] = (
            self.amp_env_adsr_widget.sustainSB.value()
        )
        self.amp_env_adsr_widget.plot.set_values(self.amp_env_adsr_widget.envelope)
        self.amp_env_adsr_widget.envelopeChanged.emit(self.amp_env_adsr_widget.envelope)
        self.updating_from_spinbox = False

    def _create_filter_section(self):
        group = QGroupBox("Filter")
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 15, 5, 5)
        group.setLayout(layout)

        # prettify with icons
        icon_hlayout = QHBoxLayout()
        for icon in ["mdi.sine-wave", "ri.filter-3-fill", "mdi.waveform"]:
            icon_label = QLabel()
            icon = qta.icon(icon)
            pixmap = icon.pixmap(30, 30)  # Set the desired size
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignHCenter)
            icon_hlayout.addWidget(icon_label)
        layout.addLayout(icon_hlayout)

        # Filter controls
        self.cutoff = Slider("Cutoff", 0, 127)
        self.resonance = Slider("Resonance", 0, 127)
        self.cutoff.valueChanged.connect(self._on_cutoff_changed)
        self.resonance.valueChanged.connect(self._on_resonance_changed)
        layout.addWidget(self.cutoff)
        layout.addWidget(self.resonance)

        # Add spacing
        layout.addSpacing(10)

        # Generate the ADSR waveform icon
        icon_base64 = adsr_waveform_icon("#FFFFFF", 2.0)
        pixmap = base64_to_pixmap(icon_base64)  # Convert to QPixmap

        # Vbox to vertically arrange icons and ADSR(D) Envelope controls
        sub_layout = QVBoxLayout()

        icon_label = QLabel()
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignHCenter)
        icons_hlayout = QHBoxLayout()
        icons_hlayout.addWidget(icon_label)
        sub_layout.addLayout(icons_hlayout)

        # Filter envelope
        env_group = QGroupBox("Envelope")
        env_group.setProperty("adsr", True)  # Mark as ADSR group
        env_layout = QHBoxLayout()
        env_layout.setSpacing(5)

        # Create ADSRWidget
        self.filter_adsr_widget = ADSRWidget()

        adsr_vlayout = QVBoxLayout()
        adsr_vlayout.addLayout(env_layout)
        env_layout.addWidget(self.filter_adsr_widget)
        env_layout.setStretchFactor(self.filter_adsr_widget, 5)

        # ADSR controls
        adsr_layout = QHBoxLayout()
        adsr_vlayout.addLayout(adsr_layout)

        adsr_layout.addWidget(
            self._create_parameter_slider(
                AnalogParameter.FILTER_ENV_ATTACK_TIME, "A", vertical=True
            )
        )
        adsr_layout.addWidget(
            self._create_parameter_slider(
                AnalogParameter.FILTER_ENV_DECAY_TIME, "D", vertical=True
            )
        )
        adsr_layout.addWidget(
            self._create_parameter_slider(
                AnalogParameter.FILTER_ENV_SUSTAIN_LEVEL, "S", vertical=True
            )
        )
        adsr_layout.addWidget(
            self._create_parameter_slider(
                AnalogParameter.FILTER_ENV_RELEASE_TIME, "R", vertical=True
            )
        )
        sub_layout.addWidget(env_group)
        env_group.setLayout(adsr_vlayout)
        layout.addLayout(sub_layout)

        # Mapping ADSR parameters to their corresponding spinboxes
        self.filter_adsr_control_map = {
            AnalogParameter.FILTER_ENV_ATTACK_TIME: self.filter_adsr_widget.attackSB,
            AnalogParameter.FILTER_ENV_DECAY_TIME: self.filter_adsr_widget.decaySB,
            AnalogParameter.FILTER_ENV_SUSTAIN_LEVEL: self.filter_adsr_widget.sustainSB,
            AnalogParameter.FILTER_ENV_RELEASE_TIME: self.filter_adsr_widget.releaseSB,
        }

        # 🔹 Connect ADSR spinboxes to external controls dynamically
        for param, spinbox in self.filter_adsr_control_map.items():
            spinbox.valueChanged.connect(partial(self.update_slider_from_adsr, param))

        # 🔹 Connect external controls to ADSR spinboxes dynamically
        for param, spinbox in self.filter_adsr_control_map.items():
            self.controls[param].valueChanged.connect(
                partial(
                    self.update_filter_adsr_spinbox_from_param,
                    self.filter_adsr_control_map,
                    param,
                )
            )

        return group

    def update_filter_adsr_spinbox_from_param(self, control_map, param, value):
        """Updates an ADSR parameter from an external control, avoiding feedback loops."""
        spinbox = control_map[param]
        if param in [
            AnalogParameter.AMP_ENV_SUSTAIN_LEVEL,
            AnalogParameter.FILTER_ENV_SUSTAIN_LEVEL,
        ]:
            new_value = midi_cc_to_frac(value)
        else:
            new_value = midi_cc_to_ms(value)
        if spinbox.value() != new_value:
            spinbox.blockSignals(True)
            spinbox.setValue(new_value)
            spinbox.blockSignals(False)
            self.filter_adsr_widget.valueChanged()

    def _create_amp_section(self):
        group = QGroupBox("Amplifier")
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(5, 15, 5, 5)
        group.setLayout(layout)

        icons_hlayout = QHBoxLayout()
        for icon in [
            "mdi.volume-variant-off",
            "mdi6.volume-minus",
            "mdi.amplifier",
            "mdi6.volume-plus",
            "mdi.waveform",
        ]:
            icon_label = QLabel()
            icon = qta.icon(icon)
            pixmap = icon.pixmap(
                Style.ICON_SIZE, Style.ICON_SIZE
            )  # Set the desired size
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            icons_hlayout.addWidget(icon_label)
        layout.addLayout(icons_hlayout)

        # Level control
        self.level = Slider("Level", 0, 127)
        self.level.valueChanged.connect(self._on_level_changed)
        layout.addWidget(self.level)

        # Add spacing
        layout.addSpacing(10)

        # Amp envelope
        env_group = QGroupBox("Envelope")
        env_group.setProperty("adsr", True)  # Mark as ADSR group
        amp_env_adsr_vlayout = QVBoxLayout()
        env_layout = QHBoxLayout()
        env_layout.setSpacing(5)
        env_layout.setContentsMargins(5, 15, 5, 5)
        env_group.setLayout(amp_env_adsr_vlayout)

        # Generate the ADSR waveform icon
        icon_base64 = adsr_waveform_icon("#FFFFFF", 2.0)
        pixmap = base64_to_pixmap(icon_base64)  # Convert to QPixmap

        # Vbox to vertically arrange icons and ADSR(D) Envelope controls
        sub_layout = QVBoxLayout()

        icon_label = QLabel()
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        icons_hlayout = QHBoxLayout()
        icons_hlayout.addWidget(icon_label)
        sub_layout.addLayout(icons_hlayout)

        env_layout.addWidget(
            self._create_parameter_slider(
                AnalogParameter.AMP_ENV_ATTACK_TIME, "A", vertical=True
            )
        )
        env_layout.addWidget(
            self._create_parameter_slider(
                AnalogParameter.AMP_ENV_DECAY_TIME, "D", vertical=True
            )
        )
        env_layout.addWidget(
            self._create_parameter_slider(
                AnalogParameter.AMP_ENV_SUSTAIN_LEVEL, "S", vertical=True
            )
        )
        env_layout.addWidget(
            self._create_parameter_slider(
                AnalogParameter.AMP_ENV_RELEASE_TIME, "R", vertical=True
            )
        )
        self.amp_env_adsr_widget = ADSRWidget()
        amp_env_adsr_vlayout.addWidget(self.amp_env_adsr_widget)
        amp_env_adsr_vlayout.addLayout(env_layout)
        sub_layout.addWidget(env_group)
        layout.addLayout(sub_layout)

        # Mapping ADSR parameters to their corresponding spinboxes
        self.adsr_control_map = {
            AnalogParameter.AMP_ENV_ATTACK_TIME: self.amp_env_adsr_widget.attackSB,
            AnalogParameter.AMP_ENV_DECAY_TIME: self.amp_env_adsr_widget.decaySB,
            AnalogParameter.AMP_ENV_SUSTAIN_LEVEL: self.amp_env_adsr_widget.sustainSB,
            AnalogParameter.AMP_ENV_RELEASE_TIME: self.amp_env_adsr_widget.releaseSB,
        }

        # 🔹 Connect ADSR spinboxes to external controls dynamically
        for param, spinbox in self.adsr_control_map.items():
            spinbox.valueChanged.connect(partial(self.update_slider_from_adsr, param))

        # 🔹 Connect external controls to ADSR spinboxes dynamically
        for param, spinbox in self.adsr_control_map.items():
            self.controls[param].valueChanged.connect(
                partial(
                    self.update_adsr_spinbox_from_param, self.adsr_control_map, param
                )
            )

        return group

    def update_adsr_spinbox_from_param(self, control_map, param, value):
        """Updates an ADSR parameter from an external control, avoiding feedback loops."""
        spinbox = control_map[param]
        if param in [
            AnalogParameter.AMP_ENV_SUSTAIN_LEVEL,
            AnalogParameter.FILTER_ENV_SUSTAIN_LEVEL,
        ]:
            new_value = midi_cc_to_frac(value)
        else:
            new_value = midi_cc_to_ms(value)
        if spinbox.value() != new_value:
            spinbox.blockSignals(True)
            spinbox.setValue(new_value)
            spinbox.blockSignals(False)
            self.amp_env_adsr_widget.valueChanged()

    def update_slider_from_adsr(self, param, value):
        """Updates external control from ADSR widget, avoiding infinite loops."""
        control = self.controls[param]
        if param in [
            AnalogParameter.AMP_ENV_SUSTAIN_LEVEL,
            AnalogParameter.FILTER_ENV_SUSTAIN_LEVEL,
        ]:
            new_value = frac_to_midi_cc(value)
        else:
            new_value = ms_to_midi_cc(value)
        if control.value() != new_value:
            control.blockSignals(True)
            control.setValue(new_value)
            control.blockSignals(False)

    def _create_lfo_section(self):
        group = QGroupBox("LFO")
        layout = QVBoxLayout()
        group.setLayout(layout)

        # pimp up the section with some icons
        icons_hlayout = QHBoxLayout()
        for icon in [
            "mdi.triangle-wave",
            "mdi.sine-wave",
            "fa5s.wave-square",
            "mdi.cosine-wave",
            "mdi.triangle-wave",
            "mdi.waveform",
        ]:
            icon_label = QLabel()
            icon = qta.icon(icon)
            pixmap = icon.pixmap(
                Style.ICON_SIZE, Style.ICON_SIZE
            )  # Set the desired size
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignHCenter)
            icons_hlayout.addWidget(icon_label)
        layout.addLayout(icons_hlayout)

        # LFO Shape selector
        shape_row = QHBoxLayout()
        shape_row.addWidget(QLabel("Shape"))
        self.lfo_shape = QComboBox()
        self.lfo_shape.addItems(["TRI", "SIN", "SAW", "SQR", "S&H", "RND"])
        self.lfo_shape.currentIndexChanged.connect(self._on_lfo_shape_changed)
        shape_row.addWidget(self.lfo_shape)
        layout.addLayout(shape_row)

        # Rate and Fade Time
        self.lfo_rate = self._create_parameter_slider(AnalogParameter.LFO_RATE, "Rate")

        self.lfo_fade = self._create_parameter_slider(
            AnalogParameter.LFO_FADE_TIME, "Fade Time"
        )

        # Tempo Sync controls
        sync_row = QHBoxLayout()
        # self.lfo_sync = self._create_parameter_slider(AnalogParameter.LFO_TEMPO_SYNC_SWITCH, "Tempo Sync")
        self.lfo_sync = Switch("Tempo Sync", ["OFF", "ON"])
        self.lfo_sync.valueChanged.connect(self._on_lfo_sync_changed)
        sync_row.addWidget(self.lfo_sync)

        self.sync_note = QComboBox()
        self.sync_note.addItems(
            [
                "16",
                "12",
                "8",
                "4",
                "2",
                "1",
                "3/4",
                "2/3",
                "1/2",
                "3/8",
                "1/3",
                "1/4",
                "3/16",
                "1/6",
                "1/8",
                "3/32",
                "1/12",
                "1/16",
                "1/24",
                "1/32",
            ]
        )
        self.sync_note.currentIndexChanged.connect(self._on_lfo_sync_note_changed)
        sync_row.addWidget(self.sync_note)

        # Depth controls
        self.lfo_pitch = self._create_parameter_slider(
            AnalogParameter.LFO_PITCH_DEPTH, "Pitch Depth"
        )
        # self.lfo_pitch = Slider("Pitch Depth", -63, 63)
        # self.lfo_pitch.valueChanged.connect(self._on_lfo_pitch_changed)

        self.lfo_filter = self._create_parameter_slider(
            AnalogParameter.LFO_FILTER_DEPTH,
            "Filter Depth",
        )
        # self.lfo_filter = Slider("Filter Depth", -63, 63)
        # self.lfo_filter.valueChanged.connect(self._on_lfo_filter_changed)

        self.lfo_amp = self._create_parameter_slider(
            AnalogParameter.LFO_AMP_DEPTH, "Amp Depth"
        )
        # self.lfo_amp.valueChanged.connect(self._on_lfo_amp_changed)

        # Key Trigger switch
        self.key_trig = Switch("Key Trigger", ["OFF", "ON"])
        self.key_trig.valueChanged.connect(self._on_lfo_key_trig_changed)

        # Add all controls to layout
        layout.addWidget(self.lfo_rate)
        layout.addWidget(self.lfo_fade)
        layout.addLayout(sync_row)
        layout.addWidget(self.lfo_pitch)
        layout.addWidget(self.lfo_filter)
        layout.addWidget(self.lfo_amp)
        layout.addWidget(self.key_trig)

        return group

    def _on_waveform_selected(self, waveform: Waveform):
        """Handle waveform button selection"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.OSC_WAVE,
                value=waveform.midi_value,
            )
            self._update_pw_controls_state(waveform)

    def _send_cc(self, cc: AnalogToneCC, value: int):
        """Send MIDI CC message"""
        if self.midi_helper:
            # Convert enum to int if needed
            cc_number = cc.value if isinstance(cc, AnalogToneCC) else cc
            self.midi_helper.send_cc(cc_number, value, channel=ANALOG_PART)

    def _on_sub_type_changed(self, value: int):
        """Handle sub oscillator type change"""
        if self.midi_helper:
            # Convert switch position to SubOscType enum
            sub_type = SubOscType(value)
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.SUB_TYPE,
                value=sub_type.midi_value,
            )

    def _on_coarse_changed(self, value: int):
        """Handle coarse tune change"""
        if self.midi_helper:
            # Convert -24 to +24 range to MIDI value (0x28 to 0x58)
            midi_value = value + 63  # Center at 63 (0x3F)
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.OSC_COARSE,
                value=midi_value,
            )

    def _on_fine_changed(self, value: int):
        """Handle fine tune change"""
        if self.midi_helper:
            # Convert -50 to +50 range to MIDI value
            midi_value = value + 64
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.OSC_FINE,
                value=midi_value,
            )

    def _on_pitch_env_velo_changed(self, value: int):
        """Handle pitch envelope velocity change"""
        if self.midi_helper:
            # Convert -63 to +63 range to 1-127
            midi_value = value + 64 if value >= 0 else abs(value)
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.OSC_PENV_VELO,
                value=midi_value,
            )

    def _on_pitch_env_attack_changed(self, value: int):
        """Handle pitch envelope attack change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.OSC_PENV_A,
                value=value,
            )

    def _on_pitch_env_decay_changed(self, value: int):
        """Handle pitch envelope decay change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.OSC_PENV_D,
                value=value,
            )

    def _on_pitch_env_depth_changed(self, value: int):
        """Handle pitch envelope depth change"""
        if self.midi_helper:
            # Convert -63 to +63 range to 1-127
            midi_value = value + 64 if value >= 0 else abs(value)
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.OSC_PENV_DEPTH,
                value=midi_value,
            )

    def _on_cutoff_changed(self, value: int):
        """Handle cutoff change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.FILTER_CUTOFF,
                value=value,
            )

    def _on_resonance_changed(self, value: int):
        """Handle resonance change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.FILTER_RESO,
                value=value,
            )

    def _on_level_changed(self, value: int):
        """Handle level change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogParameter.AMP_LEVEL.value[0],
                value=value,
            )

    def _on_lfo_shape_changed(self, value: int):
        """Handle LFO shape change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_SHAPE,
                value=value,
            )

    def _on_lfo_rate_changed(self, value: int):
        """Handle LFO rate change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_RATE,
                value=value,
            )

    def _on_lfo_fade_changed(self, value: int):
        """Handle LFO fade time change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_FADE,
                value=value,
            )

    def _on_lfo_sync_changed(self, value: int):
        """Handle LFO sync change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_SYNC,
                value=value,
            )

    def _on_lfo_sync_note_changed(self, value: int):
        """Handle LFO sync note change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_SYNC_NOTE,
                value=value,
            )

    def _on_lfo_pitch_changed(self, value: int):
        """Handle LFO pitch depth change"""
        if self.midi_helper:
            # Convert -63 to +63 range to 1-127
            midi_value = value + 64 if value >= 0 else abs(value)
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_PITCH,
                value=midi_value,
            )

    def _on_lfo_filter_changed(self, value: int):
        """Handle LFO filter depth change"""
        if self.midi_helper:
            # Convert -63 to +63 range to 1-127
            midi_value = value + 64 if value >= 0 else abs(value)
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_FILTER,
                value=midi_value,
            )

    def _on_lfo_amp_changed(self, value: int):
        """Handle LFO amp depth change"""
        if self.midi_helper:
            # Convert -63 to +63 range to 1-127
            midi_value = value + 64 if value >= 0 else abs(value)
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_AMP,
                value=midi_value,
            )

    def _on_lfo_key_trig_changed(self, value: int):
        """Handle LFO key trigger change"""
        if self.midi_helper:
            self.midi_helper.send_parameter(
                area=ANALOG_SYNTH_AREA,
                part=ANALOG_PART,
                group=ANALOG_OSC_GROUP,
                param=AnalogToneCC.LFO_KEY_TRIG,
                value=value,
            )

    def data_request(self):
        """Send data request SysEx messages to the JD-Xi"""
        # Define SysEx messages as byte arrays
        wave_type_request = bytes.fromhex(
            "F0 41 10 00 00 00 0E 11 19 42 00 00 00 00 00 40 65 F7"
        )
        # Send each SysEx message
        self.send_message(wave_type_request)

    def send_message(self, message):
        """Send a SysEx message using the MIDI helper"""
        if self.midi_helper:
            self.midi_helper.send_message(message)
        else:
            logging.error("MIDI helper not initialized")

    def _base64_to_pixmap(self, base64_str):
        """Convert base64 string to QPixmap"""
        image_data = base64.b64decode(base64_str)
        image = QPixmap()
        image.loadFromData(image_data)
        return image

    def _on_parameter_received(self, address, value):
        """Handle parameter updates from MIDI messages."""
        area_code = address[0]
        logging.info(
            f"In analog area_code: {area_code}: ANALOG_SYNTH_AREA: {ANALOG_SYNTH_AREA}"
        )
        if address[0] == ANALOG_SYNTH_AREA:
            # Extract the actual parameter address (80, 0) from [25, 1, 80, 0]
            parameter_address = tuple(address[2:])  # (80, 0)

            # Retrieve the corresponding DigitalParameter
            param = get_analog_parameter_by_address(parameter_address)
            partial_no = address[1]
            if param:
                logging.info(f"param: {param}")
                logging.info(
                    f"Received parameter update: Address={address}, Value={value}"
                )

                # Update the corresponding slider
                if param in self.partial_editors[partial_no].controls:
                    slider = self.partial_editors[partial_no].controls[param]
                    slider.blockSignals(True)  # Prevent feedback loop
                    slider.setValue(value)
                    slider.blockSignals(False)

    def update_sliders_from_sysex(self, json_sysex_data: str):
        """Update sliders and combo boxes based on parsed SysEx data."""
        logging.info("Updating UI components from SysEx data")
        logging.info(json_sysex_data)
        sysex_data = json.loads(json_sysex_data)

        # Mapping for LFO Shape values to combo box indices
        lfo_shape_map = {0: "TRI", 1: "SIN", 2: "SAW", 3: "SQR", 4: "S&H", 5: "RND"}

        # Mapping for Sub Oscillator Type values to switch indices
        sub_osc_type_map = {0: 0, 1: 1, 2: 2}  # Ensure these are integers
        failures = []
        for param_name, param_value in sysex_data.items():
            # Update sliders
            param = AnalogParameter.get_by_name(param_name)
            if param and param in self.controls:
                slider = self.controls[param]
                slider.blockSignals(True)  # Prevent feedback loop
                logging.info(f"Success: \tupdating \t{param} \twith \t{param_value}")
                slider.setValue(param_value)
                slider.blockSignals(False)
            else:
                # Update LFO Shape combo box
                if param_name == "LFO_SHAPE":
                    if param_value in lfo_shape_map:
                        index = self.lfo_shape.findText(lfo_shape_map[param_value])
                        if index != -1:
                            self.lfo_shape.blockSignals(True)
                            self.lfo_shape.setCurrentIndex(index)
                            self.lfo_shape.blockSignals(False)

                # Update Sub Oscillator Type switch
                elif param_name == "SUB_OSCILLATOR_TYPE":
                    if param_value in sub_osc_type_map:
                        index = sub_osc_type_map[param_value]
                        if isinstance(index, int):  # Ensure index is an integer
                            self.sub_type.blockSignals(True)
                            self.sub_type.setValue(index)
                            self.sub_type.blockSignals(False)
                else:
                    failures.append(param_name)
        logging.info(f"failures: {failures}")
