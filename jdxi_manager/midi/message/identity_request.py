"""
MIDI Identity Request Message Module

This module defines the `IdentityRequestMessage` class, which represents a MIDI Identity Request message.
MIDI Identity Request messages are used to query a device for its identity, typically to retrieve information such as its model or manufacturer.

Classes:
    - IdentityRequestMessage: Represents a MIDI Identity Request message used to query a device's identity.

Features:
    - Inherits from the base `Message` class, utilizing SysEx message structure.
    - Includes device identification information, such as device ID and fixed SysEx parameters.
    - Provides a method for converting the message into a list of bytes for sending via MIDI.

Constants Used:
    - START_OF_SYSEX: The start byte for a SysEx message.
    - ID_NUMBER, DEVICE, SUB_ID_1, SUB_ID_2: Fixed SysEx identifiers for the identity request.
    - END_OF_SYSEX: The end byte for a SysEx message.

Usage Example:
    >>> identity_msg = IdentityRequestMessage()
    >>> identity_msg.to_list()
    [0xF0, 0x7E, 0x00, 0x01, 0x02, 0xF7]

"""

from dataclasses import dataclass
from typing import List

from jdxi_manager.midi.data.constants.sysex import START_OF_SYSEX, ID_NUMBER, DEVICE, SUB_ID_1, SUB_ID_2, END_OF_SYSEX
from jdxi_manager.midi.message.midi import MidiMessage


@dataclass
class IdentityRequestMessage(MidiMessage):
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
