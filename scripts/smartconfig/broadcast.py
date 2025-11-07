#!/usr/bin/env python3
# encoding: utf-8
"""
broadcast.py
Created by kueblc on 2019-01-25.
Encode data for Tuya smartconfig via broadcast
broadcast strategy ported from https://github.com/tuyapi/link
"""

from typing import List

try:
    from .constants import (
        CRC_HIGH_NIBBLE_MARKER,
        CRC_LOW_NIBBLE_MARKER,
        CRC_MASK,
        DATA_BYTE_MARKER,
        LENGTH_HIGH_NIBBLE_MARKER,
        LENGTH_LOW_NIBBLE_MARKER,
        NIBBLE_MASK,
        SEQUENCE_MARKER,
        SHIFT_4_BITS,
    )
    from .crc import crc_8
except ImportError:
    from constants import (  # type: ignore[import-not-found]
        CRC_HIGH_NIBBLE_MARKER,
        CRC_LOW_NIBBLE_MARKER,
        CRC_MASK,
        DATA_BYTE_MARKER,
        LENGTH_HIGH_NIBBLE_MARKER,
        LENGTH_LOW_NIBBLE_MARKER,
        NIBBLE_MASK,
        SEQUENCE_MARKER,
        SHIFT_4_BITS,
    )
    from crc import crc_8  # type: ignore[import-not-found]

broadcast_head: List[int] = [1, 3, 6, 10]


def encode_broadcast_body(password: str, ssid: str, token_group: str) -> List[int]:
    """
    Encode broadcast body for Tuya smartconfig protocol.

    Args:
        password: WiFi password
        ssid: WiFi SSID
        token_group: Combined region + token + secret string

    Returns:
        List of integers representing packet lengths to send via UDP broadcast.
        Each integer indicates the length of a UDP packet to send.
    """
    # Build raw data buffer: [pw_len, pw_bytes..., token_len, token_bytes..., ssid_bytes...]
    r: List[int] = []
    r.append(len(password))
    r.extend([ord(l) for l in password])
    r.append(len(token_group))
    r.extend([ord(l) for l in token_group])
    r.extend([ord(l) for l in ssid])

    # Encode the data with length/CRC header and sequence numbers
    e: List[int] = []
    length: int = len(r)
    length_crc: int = crc_8([length])

    # Encode length as two nibbles with markers
    e.append((length >> SHIFT_4_BITS) | LENGTH_HIGH_NIBBLE_MARKER)
    e.append((length & NIBBLE_MASK) | LENGTH_LOW_NIBBLE_MARKER)

    # Encode length CRC as two nibbles with markers
    e.append((length_crc >> SHIFT_4_BITS) | CRC_HIGH_NIBBLE_MARKER)
    e.append((length_crc & NIBBLE_MASK) | CRC_LOW_NIBBLE_MARKER)

    # Encode data in 4-byte groups with sequence numbers and CRC
    sequence: int = 0
    for i in range(0, length, 4):
        # Build group: [sequence, up to 4 data bytes, padding if needed]
        group: List[int] = []
        group.append(sequence)
        group.extend(r[i : i + 4])
        group.extend([0] * (5 - len(group)))  # Pad to 5 bytes

        # Calculate CRC of group
        group_crc: int = crc_8(group)

        # Encode: CRC (with marker), sequence (with marker), data bytes (with marker)
        e.append((group_crc & CRC_MASK) | SEQUENCE_MARKER)
        e.append(sequence | SEQUENCE_MARKER)
        e.extend([b | DATA_BYTE_MARKER for b in r[i : i + 4]])

        sequence += 1

    # Pad remaining length with marker value
    e.extend([DATA_BYTE_MARKER] * (length - i))

    return e
