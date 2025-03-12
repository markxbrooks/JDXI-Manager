from jdxi_manager.midi.data.constants.sysex import DT1_COMMAND_12
from jdxi_manager.midi.sysex.jdxi import JDXiSysEx
# from jdxi_manager.midi.sysex.sysex import DT1_COMMAND_12, RQ1_COMMAND_11
from jdxi_manager.midi.data.constants import (
    DrumKitCC,
    START_OF_SYSEX,
    END_OF_SYSEX,
    ROLAND_ID,
    DIGITAL_SYNTH_1_AREA,
    PART_1,
    OSC_1_GROUP,  # Changed from OSC_PARAM_GROUP
    OSC_WAVE_PARAM,  # Changed from PARAM_NUMBER
    WAVE_SAW,
    ID_NUMBER, DEVICE, SUB_ID_1, SUB_ID_2,
)

from dataclasses import dataclass, field
from typing import List

from jdxi_manager.midi.sysex.parameter_utils import create_parameter_message

# Roland SysEx Constants
# START_OF_SYSEX = 0xF0
# END_OF_SYSEX = 0xF7
# ROLAND_ID = 0x41  # Roland Manufacturer ID
JD_XI_MODEL_ID = [0x00, 0x00, 0x00, 0x0E]  # JD-Xi Model ID
# DT1_COMMAND_12 = 0x12  # Data Set 1 (DT1) command
# RQ1_COMMAND_11 = 0x11  # Data Request 1 (RQs1) command


@dataclass
class IdentityRequest():
    """MIDI Identity Request message"""

    device_id: int = 0x10  # Default device ID

    def to_list(self) -> List[int]:
        """Convert to list of bytes for sending

        Returns:
            List of integers representing the MIDI message
        """
        return [START_OF_SYSEX,
                ID_NUMBER,
                DEVICE,
                SUB_ID_1,
                SUB_ID_2,
                END_OF_SYSEX]

    def to_bytes(self) -> bytes:
        """Convert to bytes for sending

        Returns:
            Bytes object containing the MIDI message
        """
        return bytes(self.to_list())


@dataclass
class ParameterMessage(JDXiSysEx):
    """Base class for parameter messages"""

    command: int = DT1_COMMAND_12

    def __post_init__(self):
        """Handle parameter value conversion"""
        super().__post_init__()

        # Convert parameter value if needed
        if hasattr(self, "convert_value"):
            self.data = self.convert_value(self.value)

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value to data bytes"""
        # Default implementation just returns single byte
        return [value]

    @classmethod
    def from_bytes(cls, data: bytes):
        """Create message from received bytes"""
        msg = super().from_bytes(data)

        # Convert data back to value if needed
        if hasattr(cls, "convert_data"):
            msg.value = cls.convert_data(msg.data)

        return msg

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        # Default implementation just returns first byte
        return data[0] if data else 0


@dataclass
class SystemMessage(ParameterMessage):
    """System parameter message"""

    area: int = 0x02  # System area


@dataclass
class ProgramMessage(ParameterMessage):
    """Program parameter message"""

    area: int = 0x18  # Program area


# Update other message classes to inherit from ParameterMessage
@dataclass
class Effect1Message(ParameterMessage):
    """Effect 1 parameter message"""

    area: int = 0x18  # Program area
    section: int = 0x04  # Effect 1 section


@dataclass
class Effect2Message(ParameterMessage):
    """Effect 2 parameter message"""

    area: int = 0x18  # Program area
    section: int = 0x05  # Effect 2 section


@dataclass
class DelayMessage(ParameterMessage):
    """Delay parameter message"""

    area: int = 0x18  # Program area
    section: int = 0x06  # Delay section


@dataclass
class ReverbMessage(ParameterMessage):
    """Reverb parameter message"""

    area: int = 0x18  # Program area
    section: int = 0x08  # Reverb section


@dataclass
class PartMessage(ParameterMessage):
    """Program Part parameter message"""

    area: int = 0x18  # Program area
    section: int = 0x00  # Part section

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value based on parameter preset_type"""
        # Parameters that need special conversion
        if self.param == 0x0B:  # Part Coarse Tune
            return [value + 64]  # Convert -48/+48 to 16-112
        elif self.param == 0x0C:  # Part Fine Tune
            return [value + 64]  # Convert -50/+50 to 14-114
        elif self.param == 0x13:  # Part Cutoff Offset
            return [value + 64]  # Convert -64/+63 to 0-127
        elif self.param == 0x14:  # Part Resonance Offset
            return [value + 64]  # Convert -64/+63 to 0-127
        elif self.param == 0x15:  # Part Attack Time Offset
            return [value + 64]  # Convert -64/+63 to 0-127
        elif self.param == 0x16:  # Part Decay Time Offset
            return [value + 64]  # Convert -64/+63 to 0-127
        elif self.param == 0x17:  # Part Release Time Offset
            return [value + 64]  # Convert -64/+63 to 0-127
        elif self.param == 0x18:  # Part Vibrato Rate
            return [value + 64]  # Convert -64/+63 to 0-127
        elif self.param == 0x19:  # Part Vibrato Depth
            return [value + 64]  # Convert -64/+63 to 0-127
        elif self.param == 0x1A:  # Part Vibrato Delay
            return [value + 64]  # Convert -64/+63 to 0-127
        elif self.param == 0x1B:  # Part Octave Shift
            return [value + 64]  # Convert -3/+3 to 61-67
        elif self.param == 0x1C:  # Part Velocity Sens Offset
            return [value + 64]  # Convert -63/+63 to 1-127
        elif self.param == 0x11:  # Part Portamento Time (2 bytes)
            if value == 128:  # TONE setting
                return [0x00, 0x80]
            else:
                return [0x00, value & 0x7F]

        # Default handling for other parameters
        return super().convert_value(value)

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        param = cls.param if hasattr(cls, "param") else 0

        # Parameters that need special conversion
        if param == 0x0B:  # Part Coarse Tune
            return data[0] - 64  # Convert 16-112 to -48/+48
        elif param == 0x0C:  # Part Fine Tune
            return data[0] - 64  # Convert 14-114 to -50/+50
        elif param in [0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A]:
            return data[0] - 64  # Convert 0-127 to -64/+63
        elif param == 0x1B:  # Part Octave Shift
            return data[0] - 64  # Convert 61-67 to -3/+3
        elif param == 0x1C:  # Part Velocity Sens Offset
            return data[0] - 64  # Convert 1-127 to -63/+63
        elif param == 0x11:  # Part Portamento Time
            if data[1] & 0x80:  # TONE setting
                return 128
            else:
                return data[1] & 0x7F

        # Default handling for other parameters
        return super().convert_data(data)


@dataclass
class ZoneMessage(ParameterMessage):
    """Program Zone parameter message"""

    area: int = 0x18  # Program area
    section: int = 0x01  # Zone section

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value based on parameter preset_type"""
        # Parameters that need special conversion
        if self.param == 0x19:  # Zone Octave Shift
            return [value + 64]  # Convert -3/+3 to 61-67
        elif self.param == 0x03:  # Arpeggio Switch
            return [value & 0x01]  # Ensure boolean value

        # Default handling for other parameters
        return super().convert_value(value)

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        param = cls.param if hasattr(cls, "param") else 0

        # Parameters that need special conversion
        if param == 0x19:  # Zone Octave Shift
            return data[0] - 64  # Convert 61-67 to -3/+3
        elif param == 0x03:  # Arpeggio Switch
            return data[0] & 0x01  # Ensure boolean value

        # Default handling for other parameters
        return super().convert_data(data)


@dataclass
class ControllerMessage(ParameterMessage):
    """Program Controller parameter message"""

    area: int = 0x18  # Program area
    section: int = 0x40  # Controller section

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value based on parameter preset_type"""
        # Parameters that need special conversion
        if self.param == 0x07:  # Arpeggio Octave Range
            return [value + 64]  # Convert -3/+3 to 61-67

        # Default handling for other parameters
        return super().convert_value(value)

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        param = cls.param if hasattr(cls, "param") else 0

        # Parameters that need special conversion
        if param == 0x07:  # Arpeggio Octave Range
            return data[0] - 64  # Convert 61-67 to -3/+3

        # Default handling for other parameters
        return super().convert_data(data)


@dataclass
class DigitalToneCommonMessage(ParameterMessage):
    """SuperNATURAL Synth Tone Common parameter message"""

    area: int = 0x19  # Temporary area
    section: int = 0x00  # Common section

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value based on parameter preset_type"""
        # Parameters that need special conversion
        if self.param == 0x15:  # Octave Shift
            return [value + 64]  # Convert -3/+3 to 61-67

        # Default handling for other parameters
        return super().convert_value(value)

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        param = cls.param if hasattr(cls, "param") else 0

        # Parameters that need special conversion
        if param == 0x15:  # Octave Shift
            return data[0] - 64  # Convert 61-67 to -3/+3

        # Default handling for other parameters
        return super().convert_data(data)


@dataclass
class DigitalToneModifyMessage(ParameterMessage):
    """SuperNATURAL Synth Tone Modify parameter message"""

    area: int = 0x19  # Temporary area
    section: int = 0x50  # Modify section

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value based on parameter preset_type"""
        # No special conversion needed for modify parameters
        return super().convert_value(value)

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        # No special conversion needed for modify parameters
        return super().convert_data(data)


@dataclass
class DigitalTonePartialMessage(ParameterMessage):
    """SuperNATURAL Synth Tone Partial parameter message"""

    area: int = 0x19  # Temporary area
    section: int = 0x20  # Partial 1 section (0x20, 0x21, 0x22 for Partials 1-3)

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value based on parameter preset_type"""
        # Parameters that need special conversion
        if self.param == 0x00:  # OSC Wave
            return [value & 0x07]  # Ensure 3-bit value (0-7)
        elif self.param == 0x01:  # OSC Wave Variation
            return [value & 0x03]  # Ensure 2-bit value (0-2)

        # Default handling for other parameters
        return super().convert_value(value)

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        param = cls.param if hasattr(cls, "param") else 0

        # Parameters that need special conversion
        if param == 0x00:  # OSC Wave
            return data[0] & 0x07  # Extract 3-bit value
        elif param == 0x01:  # OSC Wave Variation
            return data[0] & 0x03  # Extract 2-bit value

        # Default handling for other parameters
        return super().convert_data(data)


@dataclass
class AnalogToneMessage:
    """Message for analog tone parameters"""

    area: int
    part: int
    group: int
    param: int
    value: int

    def to_sysex(self) -> List[int]:
        """Convert to SysEx message bytes"""
        return [
            0xF0,  # Start of SysEx
            0x41,  # Roland ID
            0x10,  # Device ID
            0x00,
            0x00,
            0x00,
            0x0E,  # Model ID
            0x12,  # DT1 Command
            self.area,
            self.part,
            self.group,
            self.param,
            self.value,
            0x00,  # Checksum placeholder
            0xF7,  # End of SysEx
        ]

    def calculate_checksum(self, data: List[int]) -> int:
        """Calculate Roland checksum

        Args:
            data: List of bytes to checksum

        Returns:
            Checksum value (0-127)
        """
        checksum = 0
        for byte in data[8:-2]:  # Skip header and end bytes
            checksum += byte
        return (128 - (checksum % 128)) & 0x7F


@dataclass
class DrumKitCommonMessage(ParameterMessage):
    """Drum Kit Common parameter message"""

    area: int = 0x19  # Temporary area
    section: int = 0x10  # Drum Kit section
    group: int = 0x00  # Common area

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value based on parameter preset_type"""
        # No special conversion needed for drum kit common parameters
        return super().convert_value(value)

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        # No special conversion needed for drum kit common parameters
        return super().convert_data(data)


@dataclass
class DrumKitPartialMessage(ParameterMessage):
    """Drum Kit Partial parameter message"""

    area: int = 0x19  # Temporary area
    section: int = 0x10  # Drum Kit section
    group: int = 0x01  # Partial area

    def convert_value(self, value: int) -> List[int]:
        """Convert parameter value based on parameter preset_type"""
        # Parameters that need special conversion
        if self.param == 0x10:  # Fine Tune
            return [value + 64]  # Convert -50/+50 to 14-114
        elif self.param == 0x14:  # Alternate Pan
            return [value + 64]  # Convert L63-63R to 1-127

        # Default handling for other parameters
        return super().convert_value(value)

    @classmethod
    def convert_data(cls, data: List[int]) -> int:
        """Convert data bytes back to parameter value"""
        param = cls.param if hasattr(cls, "param") else 0

        # Parameters that need special conversion
        if param == 0x10:  # Fine Tune
            return data[0] - 64  # Convert 14-114 to -50/+50
        elif param == 0x14:  # Alternate Pan
            return data[0] - 64  # Convert 1-127 to L63-63R

        # Default handling for other parameters
        return super().convert_data(data)


@dataclass
class DigitalToneCCMessage:
    """SuperNATURAL Synth Tone Control Change message"""

    channel: int = 0  # MIDI channel (0-15)
    cc: int = 0  # CC number
    value: int = 0  # CC value (0-127)
    is_nrpn: bool = False  # Whether this is an NRPN message

    def to_bytes(self) -> bytes:
        """Convert to MIDI message bytes"""
        if not self.is_nrpn:
            # Standard CC message
            return bytes(
                [
                    0xB0 | self.channel,  # Control Change status
                    self.cc,  # CC number
                    self.value,  # Value
                ]
            )
        else:
            # NRPN message sequence
            return bytes(
                [
                    0xB0 | self.channel,  # CC for NRPN MSB
                    0x63,  # NRPN MSB (99)
                    0x00,  # MSB value = 0
                    0xB0 | self.channel,  # CC for NRPN LSB
                    0x62,  # NRPN LSB (98)
                    self.cc,  # LSB value = parameter
                    0xB0 | self.channel,  # CC for Data Entry
                    0x06,  # Data Entry MSB
                    self.value,  # Value
                ]
            )

    @classmethod
    def from_bytes(cls, data: bytes):
        """Create message from MIDI bytes"""
        if len(data) == 3:
            # Standard CC message
            return cls(channel=data[0] & 0x0F, cc=data[1], value=data[2], is_nrpn=False)
        elif len(data) == 9:
            # NRPN message
            return cls(
                channel=data[0] & 0x0F,
                cc=data[5],  # NRPN parameter number
                value=data[8],  # NRPN value
                is_nrpn=True,
            )
        raise ValueError("Invalid CC message length")


@dataclass
class AnalogToneCCMessage:
    """Analog Synth Tone Control Change message"""

    channel: int = 0  # MIDI channel (0-15)
    cc: int = 0  # CC number
    value: int = 0  # CC value (0-127)
    is_nrpn: bool = False  # Whether this is an NRPN message

    def to_bytes(self) -> bytes:
        """Convert to MIDI message bytes"""
        if not self.is_nrpn:
            # Standard CC message
            return bytes(
                [
                    0xB0 | self.channel,  # Control Change status
                    self.cc,  # CC number
                    self.value,  # Value
                ]
            )
        else:
            # NRPN message sequence
            return bytes(
                [
                    0xB0 | self.channel,  # CC for NRPN MSB
                    0x63,  # NRPN MSB (99)
                    0x00,  # MSB value = 0
                    0xB0 | self.channel,  # CC for NRPN LSB
                    0x62,  # NRPN LSB (98)
                    self.cc,  # LSB value = parameter
                    0xB0 | self.channel,  # CC for Data Entry
                    0x06,  # Data Entry MSB
                    self.value,  # Value
                ]
            )

    @classmethod
    def from_bytes(cls, data: bytes):
        """Create message from MIDI bytes"""
        if len(data) == 3:
            # Standard CC message
            return cls(channel=data[0] & 0x0F, cc=data[1], value=data[2], is_nrpn=False)
        elif len(data) == 9:
            # NRPN message
            return cls(
                channel=data[0] & 0x0F,
                cc=data[5],  # NRPN parameter number
                value=data[8],  # NRPN value
                is_nrpn=True,
            )
        raise ValueError("Invalid CC message length")


@dataclass
class DrumKitCCMessage:
    """Drum Kit Control Change message"""

    channel: int = 0  # MIDI channel (0-15)
    msb: int = 0  # NRPN MSB value
    note: int = 36  # MIDI note number (36-72)
    value: int = 0  # CC value (0-127)

    def __post_init__(self):
        """Validate all parameters"""
        # Validate channel
        if not 0 <= self.channel <= 15:
            raise ValueError(f"Invalid MIDI channel: {self.channel}")

        # Validate MSB
        if not DrumKitCC.validate_msb(self.msb):
            raise ValueError(f"Invalid MSB value: {self.msb}")

        # Validate note
        if not DrumKitCC.validate_note(self.note):
            raise ValueError(f"Invalid drum note: {self.note}")

        # Validate value
        if not DrumKitCC.validate_value(self.value):
            raise ValueError(f"Invalid parameter value: {self.value}")

    def to_bytes(self) -> bytes:
        """Convert to MIDI message bytes"""
        # NRPN message sequence
        return bytes(
            [
                0xB0 | self.channel,  # CC for NRPN MSB
                0x63,  # NRPN MSB (99)
                self.msb,  # MSB value
                0xB0 | self.channel,  # CC for NRPN LSB
                0x62,  # NRPN LSB (98)
                self.note,  # LSB value = note number
                0xB0 | self.channel,  # CC for Data Entry
                0x06,  # Data Entry MSB
                self.value,  # Value
            ]
        )

    @classmethod
    def from_bytes(cls, data: bytes):
        """Create message from MIDI bytes"""
        if len(data) == 9:
            return cls(
                channel=data[0] & 0x0F,
                msb=data[2],  # MSB value
                note=data[5],  # Note number
                value=data[8],  # Parameter value
            )
        raise ValueError("Invalid CC message length")


# Usage example:
msg = create_parameter_message(
    area=DIGITAL_SYNTH_1_AREA,  # 0x19
    part=PART_1,  # 0x01
    group=OSC_1_GROUP,  # 0x20 - Changed from OSC_PARAM_GROUP
    param=OSC_WAVE_PARAM,  # 0x00
    value=WAVE_SAW,  # 0x00
)
# Result: F0 41 10 00 00 00 0E 12 19 01 20 00 00 46 F7

# etc...
