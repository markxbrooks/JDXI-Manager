from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple

DRUM_PARTIAL_NAMES = [
    "COM",
    "BD1",
    "RIM",
    "BD2",
    "CLAP",
    "BD3",
    "SD1",
    "CHH",
    "SD2",
    "PHH",
    "SD3",
    "OHH",
    "SD4",
    "TOM1",
    "PRC1",
    "TOM2",
    "PRC2",
    "TOM3",
    "PRC3",
    "CYM1",
    "PRC4",
    "CYM2",
    "PRC5",
    "CYM3",
    "HIT",
    "OTH1",
    "OTH2",
    "D4",
    "Eb4",
    "E4",
    "F4",
    "F#4",
    "G4",
    "G#4",
    "A4",
    "Bb4",
    "B4",
    "C5",
    "C#5",
]

DRUM_ADDRESSES = (
    b"\x19\x70\x00\x00",
    b"\x19\x70\x2E\x00",
    b"\x19\x70\x30\x00",
    b"\x19\x70\x32\x00",
    b"\x19\x70\x34\x00",
    b"\x19\x70\x36\x00",
    b"\x19\x70\x38\x00",
    b"\x19\x70\x3A\x00",
    b"\x19\x70\x3C\x00",
    b"\x19\x70\x3E\x00",
    b"\x19\x70\x40\x00",
    b"\x19\x70\x42\x00",
    b"\x19\x70\x44\x00",
    b"\x19\x70\x46\x00",
    b"\x19\x70\x48\x00",
    b"\x19\x70\x4A\x00",
    b"\x19\x70\x4C\x00",
    b"\x19\x70\x4E\x00",
    b"\x19\x70\x50\x00",
    b"\x19\x70\x52\x00",
    b"\x19\x70\x54\x00",
    b"\x19\x70\x56\x00",
    b"\x19\x70\x58\x00",
    b"\x19\x70\x5A\x00",
    b"\x19\x70\x5C\x00",
    b"\x19\x70\x5E\x00",
    b"\x19\x70\x60\x00",
    b"\x19\x70\x62\x00",
    b"\x19\x70\x64\x00",
    b"\x19\x70\x66\x00",
    b"\x19\x70\x68\x00",
    b"\x19\x70\x6A\x00",
    b"\x19\x70\x6C\x00",
    b"\x19\x70\x6E\x00",
    b"\x19\x70\x70\x00",
    b"\x19\x70\x72\x00",
    b"\x19\x70\x74\x00",
    b"\x19\x70\x76\x00",
    b"\x19\x70\x78\x00",
)


def get_address_for_partial(partial_num: int) -> Tuple[int, int]:
    """Get parameter group and address adjusted for partial number"""
    LO = DRUM_ADDRESSES[partial_num][
        2
    ]  # Skip the first row (common area), then extract the 3rd byte (zero-based index)
    HI = LO + 1
    return int(f"{LO:02X}", 16), int(f"{HI:02X}", 16)


# Drum parameter offsets and ranges
DR = {
    "common": {
        "level": (0x00, 0, 127),
        "pan": (0x01, 0, 127),
        "reverb_send": (0x02, 0, 127),
        "delay_send": (0x03, 0, 127),
        "fx_send": (0x04, 0, 127),
    },
    "pad": {
        "wave": (0x00, 0, 127),
        "level": (0x01, 0, 127),
        "pan": (0x02, 0, 127),
        "tune": (0x03, -50, 50),
        "decay": (0x04, 0, 127),
        "mute_group": (0x05, 0, 31),
        "reverb_send": (0x06, 0, 127),
        "delay_send": (0x07, 0, 127),
        "fx_send": (0x08, 0, 127),
    },
}

# Drum part categories
DRUM_PARTS = {
    "KICK": ["Kick 1", "Kick 2", "Kick 3", "TR-808 Kick", "TR-909 Kick"],
    "SNARE": ["Snare 1", "Snare 2", "Rim Shot", "TR-808 Snare", "TR-909 Snare"],
    "HI_HAT": ["Closed HH", "Open HH", "Pedal HH", "TR-808 CH", "TR-808 OH"],
    "CYMBAL": ["Crash 1", "Crash 2", "Ride", "China", "Splash"],
    "TOM": ["Tom Hi", "Tom Mid", "Tom Low", "TR-808 Tom Hi", "TR-808 Tom Low"],
    "PERCUSSION": ["Conga Hi", "Conga Low", "Bongo Hi", "Bongo Low", "Timbale"],
}


class MuteGroup(Enum):
    """Drum pad mute groups"""

    OFF = 0
    GROUPS = range(1, 32)  # Groups 1-31


class Note(Enum):
    """MIDI note numbers for drum pads"""

    PAD_1 = 36  # C1
    PAD_2 = 37  # C#1
    PAD_3 = 38  # D1
    PAD_4 = 39  # D#1
    PAD_5 = 40  # E1
    PAD_6 = 41  # F1
    PAD_7 = 42  # F#1
    PAD_8 = 43  # G1
    PAD_9 = 44  # G#1
    PAD_10 = 45  # A1
    PAD_11 = 46  # A#1
    PAD_12 = 47  # B1
    PAD_13 = 48  # C2
    PAD_14 = 49  # C#2
    PAD_15 = 50  # D2
    PAD_16 = 51  # D#2


class DrumPad:
    """Represents a single drum pad's settings"""
    
    # Parameter offsets within each pad
    PARAM_OFFSET = 0x10  # Each pad takes 16 bytes of parameter space
    
    # Parameter addresses within pad
    WAVE = 0x00
    LEVEL = 0x01 
    PAN = 0x02
    MUTE_GROUP = 0x03
    TUNE = 0x04
    DECAY = 0x05
    REVERB_SEND = 0x06
    DELAY_SEND = 0x07
    FX_SEND = 0x08

    def __init__(self):
        self.wave = 0
        self.level = 100
        self.pan = 64  # Center
        self.mute_group = 0
        self.tune = 0
        self.decay = 64
        self.reverb_send = 0
        self.delay_send = 0 
        self.fx_send = 0


@dataclass
class DrumPadSettings:
    """Settings for a single drum pad"""

    wave: int = 0
    level: int = 100
    pan: int = 64  # Center
    tune: int = 0
    decay: int = 64
    mute_group: int = 0  # OFF
    reverb_send: int = 0
    delay_send: int = 0
    fx_send: int = 0


@dataclass
class DrumKitPatch:
    """Complete drum kit patch data"""

    # Common parameters
    level: int = 100
    pan: int = 64  # Center
    reverb_send: int = 0
    delay_send: int = 0
    fx_send: int = 0
    
    # Individual pad settings
    pads: Dict[int, DrumPadSettings] = None
    
    def __post_init__(self):
        """Initialize pad settings"""
        if self.pads is None:
            self.pads = {i: DrumPadSettings() for i in range(16)} 


# SuperNATURAL drum kit presets
SN_PRESETS = [
    "001: Studio Standard",
    "002: Studio Rock",
    "003: Studio Jazz",
    "004: Studio Dance",
    "005: Studio R&B",
    "006: Studio Latin",
    "007: Power Kit",
    "008: Rock Kit",
    "009: Jazz Kit",
    "010: Brush Kit",
    "011: Orchestra Kit",
    "012: Dance Kit",
    "013: House Kit",
    "014: Hip Hop Kit",
    "015: R&B Kit",
    "016: Latin Kit",
    "017: World Kit",
    "018: Electronic Kit",
    "019: TR-808 Kit",
    "020: TR-909 Kit",
    "021: CR-78 Kit",
    "022: TR-606 Kit",
    "023: TR-707 Kit",
    "024: TR-727 Kit",
    "025: Percussion Kit",
    "026: SFX Kit",
    "027: User Kit 1",
    "028: User Kit 2",
    "029: User Kit 3",
    "030: User Kit 4",
] 

# Drum kit presets
DRUM_PRESETS: Tuple[str, ...] = (
    "001: TR-909 Kit 1",
    "002: TR-808 Kit 1",
    "003: 707&727 Kit1",
    "004: CR-78 Kit 1",
    "005: TR-606 Kit 1",
    "006: TR-626 Kit 1",
    "007: EDM Kit 1",
    "008: Drum&Bs Kit1",
    "009: Techno Kit 1",
    "010: House Kit 1",
    "011: Hiphop Kit 1",
    "012: R&B Kit 1",
    "013: TR-909 Kit 2",
    "014: TR-909 Kit 3",
    "015: TR-808 Kit 2",
    "016: TR-808 Kit 3",
    "017: TR-808 Kit 4",
    "018: 808&909 Kit1",
    "019: 808&909 Kit2",
    "020: 707&727 Kit2",
    "021: 909&7*7 Kit1",
    "022: 808&7*7 Kit1",
    "023: EDM Kit 2",
    "024: Techno Kit 2",
    "025: Hiphop Kit 2",
    "026: 80's Kit 1",
    "027: 90's Kit 1",
    "028: Noise Kit 1",
    "029: Pop Kit 1",
    "030: Pop Kit 2",
    "031: Rock Kit",
    "032: Jazz Kit",
    "033: Latin Kit",
)

# Drum kit categories
DRUM_CATEGORIES: Dict[str, list] = {
    "VINTAGE ROLAND": [
        "001: TR-909 Kit 1",
        "002: TR-808 Kit 1",
        "003: 707&727 Kit1",
        "004: CR-78 Kit 1",
        "005: TR-606 Kit 1",
        "006: TR-626 Kit 1",
        "013: TR-909 Kit 2",
        "014: TR-909 Kit 3",
        "015: TR-808 Kit 2",
        "016: TR-808 Kit 3",
        "017: TR-808 Kit 4",
    ],
    "HYBRID": [
        "018: 808&909 Kit1",
        "019: 808&909 Kit2",
        "020: 707&727 Kit2",
        "021: 909&7*7 Kit1",
        "022: 808&7*7 Kit1",
    ],
    "ELECTRONIC": [
        "007: EDM Kit 1",
        "008: Drum&Bs Kit1",
        "009: Techno Kit 1",
        "023: EDM Kit 2",
        "024: Techno Kit 2",
        "028: Noise Kit 1",
    ],
    "MODERN": [
        "010: House Kit 1",
        "011: Hiphop Kit 1",
        "012: R&B Kit 1",
        "025: Hiphop Kit 2",
        "026: 80's Kit 1",
        "027: 90's Kit 1",
    ],
    "ACOUSTIC": [
        "029: Pop Kit 1",
        "030: Pop Kit 2",
        "031: Rock Kit",
        "032: Jazz Kit",
        "033: Latin Kit",
    ],
}


def _on_tva_level_velocity_sens_slider_changed(self, value: int):
    """Handle TVA Level Velocity Sens change"""
    if self.midi_helper:
        # Convert -63 to +63 range to MIDI value (0 to 127)
        midi_value = value + 63  # Center at 63
        self.midi_helper.send_parameter(
            area=DRUM_KIT_AREA,
            part=DRUM_PART,
            group=DRUM_LEVEL,
            param=0x137,  # Address for TVA Level Velocity Sens
            value=midi_value,
        )
        logging.info(f"TVA Level Velocity Sens changed to {midi_value}")
