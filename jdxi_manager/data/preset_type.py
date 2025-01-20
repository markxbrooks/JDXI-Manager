class PresetType:
    """Preset types and their MIDI area codes"""
    ANALOG = "Analog"
    DIGITAL_1 = "Digital 1"  # Main digital synth
    DIGITAL_2 = "Digital 2"  # Second digital synth
    DRUMS = "Drums"

    @staticmethod
    def get_area_code(preset_type: str) -> int:
        """Get MIDI area code for preset type"""
        area_codes = {
            PresetType.ANALOG: 0x22,
            PresetType.DIGITAL_1: 0x20,
            PresetType.DIGITAL_2: 0x19,
            PresetType.DRUMS: 0x23
        }
        return area_codes.get(preset_type) 