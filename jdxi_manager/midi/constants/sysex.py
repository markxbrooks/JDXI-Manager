"""Roland-specific MIDI constants"""

# SysEx Headers
START_OF_SYSEX = 0xF0
END_OF_SYSEX = 0xF7
ROLAND_ID = 0x41
DEVICE_ID = 0x10

# Model ID bytes
MODEL_ID_1 = 0x00  # Manufacturer ID extension
MODEL_ID_2 = 0x00  # Device family code MSB
MODEL_ID_3 = 0x00  # Device family code LSB
MODEL_ID_4 = 0x0E  # JD-XI Product code

PROGRAM_COMMON = 0x00

# Roland Commands
DT1_COMMAND_12 = 0x12  # Data Set 1
RQ1_COMMAND_11 = 0x11  # Data Request 1

# Full Model ID array
MODEL_ID = [MODEL_ID_1, MODEL_ID_2, MODEL_ID_3, MODEL_ID_4]

# Device Identification
JD_XI_ID_LIST = [ROLAND_ID, DEVICE_ID, MODEL_ID_1, MODEL_ID_2, MODEL_ID_3, MODEL_ID_4]
JD_XI_HEADER_LIST = [START_OF_SYSEX] + JD_XI_ID_LIST

# SysEx Commands
DT1_COMMAND = 0x12  # Data Set 1
RQ1_COMMAND = 0x11  # Data Request 1
COMMAND_IDS = [DT1_COMMAND, RQ1_COMMAND]  # Roland Exclusive messages

# Memory Areas
TEMPORARY_PROGRAM_AREA = 0x18  # Temporary Program area
TEMPORARY_TONE_AREA = 0x19  # Temporary Digital Synth area
TEMPORARY_DIGITAL_SYNTH_1_AREA = 0x19  # Digital synth 1 area
TEMPORARY_DIGITAL_SYNTH_2_AREA = 0x1A  # Digital synth 2 area
TEMPORARY_ANALOG_SYNTH_AREA = 0x1B  # Analog synth area
TEMPORARY_DRUM_KIT_AREA = 0x1C  # Drum kit area
DRUM_KIT_AREA = 0x70 # Determined empirically
EFFECTS_AREA = 0x16  # Effects area
ARPEGGIO_AREA = 0x15  # Arpeggiator area
VOCAL_FX_AREA = 0x14  # Vocal effects area
TEMPORARY_SETUP_AREA = 0x01  # Settings area
TEMPORARY_SYSTEM_AREA = 0x02  # System area
TEMPORARY_AREAS = [
    TEMPORARY_PROGRAM_AREA,
    TEMPORARY_TONE_AREA,
    TEMPORARY_DIGITAL_SYNTH_1_AREA,
    TEMPORARY_DIGITAL_SYNTH_2_AREA,
    TEMPORARY_ANALOG_SYNTH_AREA,
    TEMPORARY_DRUM_KIT_AREA,
    EFFECTS_AREA,
    ARPEGGIO_AREA,
    VOCAL_FX_AREA,
    TEMPORARY_SETUP_AREA,
    TEMPORARY_SYSTEM_AREA,
]


# Part Numbers AKA "Temporary Tone"
DIGITAL_PART_1 = 0x01  # Digital synth 1 address
DIGITAL_PART_2 = 0x02  # Digital synth 2 address
ANALOG_PART = 0x00  # Analog synth address
DRUM_PART = 0x00  # Drum address
VOCAL_PART = 0x00  # Vocal address
SYSTEM_PART = 0x00  # System address
TEMPORARY_TONES = [
    DIGITAL_PART_1,
    DIGITAL_PART_2,
    ANALOG_PART,
    DRUM_PART,
    VOCAL_PART,
    SYSTEM_PART,
]

# Parameter Groups
PROGRAM_GROUP = 0x00
COMMON_GROUP = 0x10
PARTIAL_GROUP = 0x20
EFFECTS_GROUP = 0x30

# Bank Select
BANK_MSB = 0x55  # 85 (0x55) for all JD-Xi banks
