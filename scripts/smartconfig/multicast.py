#!/usr/bin/env python3
# encoding: utf-8
"""
multicast.py
Created by kueblc on 2019-01-25.
Encode data for Tuya smartconfig via multicast
multicast strategy reverse engineered by kueblc
"""

import os
import sys
from typing import List

try:
    from .constants import (
        BYTE_MASK,
        CRC32_LE_SHIFTS,
        MULTICAST_BASE_IP,
        MULTICAST_HEADER_SEQUENCE,
        MULTICAST_PASSWORD_SEQUENCE,
        MULTICAST_SSID_SEQUENCE,
        MULTICAST_TOKEN_SEQUENCE,
        SMARTCONFIG_AES_KEY,
    )
    from .crc import crc_32
except ImportError:
    from constants import (  # type: ignore[import-not-found]
        BYTE_MASK,
        CRC32_LE_SHIFTS,
        MULTICAST_BASE_IP,
        MULTICAST_HEADER_SEQUENCE,
        MULTICAST_PASSWORD_SEQUENCE,
        MULTICAST_SSID_SEQUENCE,
        MULTICAST_TOKEN_SEQUENCE,
        SMARTCONFIG_AES_KEY,
    )
    from crc import crc_32  # type: ignore[import-not-found]

# Add parent directory to path to import crypto_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto_utils import encrypt


def encrypt_smartconfig(data: str) -> bytes:
    """
    Encrypt data for smartconfig with the fixed Tuya key.

    Args:
        data: String data to encrypt

    Returns:
        Encrypted bytes using AES-128 with the Tuya protocol key
    """
    return encrypt(data, SMARTCONFIG_AES_KEY)


def encode_pw(pw: str) -> List[int]:
    """
    Encode password with encryption for multicast transmission.

    Args:
        pw: WiFi password to encode

    Returns:
        List of bytes: [len, len, crc32_le (4 bytes), encrypted_payload]
    """
    r: List[int] = []
    pw_bytes: List[int] = [ord(c) for c in pw]
    encrypted_pw: bytes = encrypt_smartconfig(pw)

    # CRC and length are from plaintext (for verification)
    crc: int = crc_32(pw_bytes)

    # Encode length twice (for redundancy)
    r.append(len(pw))
    r.append(len(pw))

    # Encode CRC-32 in little-endian byte order
    r.extend([(crc >> i) & BYTE_MASK for i in CRC32_LE_SHIFTS])

    # Append encrypted payload
    r.extend(encrypted_pw)

    return r


def encode_plain(s: str) -> List[int]:
    """
    Encode plaintext string for multicast transmission.

    Args:
        s: String to encode (SSID or token group)

    Returns:
        List of bytes: [len, len, crc32_le (4 bytes), plaintext_payload]
    """
    r: List[int] = []
    s_bytes: List[int] = [ord(c) for c in s]
    crc: int = crc_32(s_bytes)

    # Encode length twice (for redundancy)
    r.append(len(s))
    r.append(len(s))

    # Encode CRC-32 in little-endian byte order
    r.extend([(crc >> i) & BYTE_MASK for i in CRC32_LE_SHIFTS])

    # Append plaintext payload
    r.extend(s_bytes)

    return r


def bytes_to_ips(data: List[int], sequence: int) -> List[str]:
    """
    Convert byte list to multicast IP addresses.

    Encodes two bytes per IP address in format: 226.{sequence}.{byte1}.{byte0}
    The sequence number increments for each IP address.

    Args:
        data: List of bytes to encode (will be padded if odd length)
        sequence: Starting sequence number (becomes 2nd octet)

    Returns:
        List of IP address strings in the 226.x.y.z format
    """
    r: List[str] = []

    # Pad data to even length if necessary
    if len(data) & 1:
        data.append(0)

    # Encode two bytes per IP: 226.{seq}.{byte1}.{byte0}
    for i in range(0, len(data), 2):
        ip: str = (
            MULTICAST_BASE_IP
            + "."
            + str(sequence)
            + "."
            + str(data[i + 1])
            + "."
            + str(data[i])
        )
        r.append(ip)
        sequence += 1

    return r


# Protocol header: "TYST01" encoded as multicast IPs starting at sequence 120
multicast_head: List[str] = bytes_to_ips(
    [ord(c) for c in "TYST01"], MULTICAST_HEADER_SEQUENCE
)


def encode_multicast_body(password: str, ssid: str, token_group: str) -> List[str]:
    """
    Encode complete multicast body for Tuya smartconfig protocol.

    Args:
        password: WiFi password (encrypted)
        ssid: WiFi SSID (plaintext)
        token_group: Combined region + token + secret (plaintext)

    Returns:
        List of multicast IP addresses to send in order
    """
    r: List[str] = []

    # Encode SSID at sequence 64
    ssid_encoded: List[int] = encode_plain(ssid)
    r.extend(bytes_to_ips(ssid_encoded, MULTICAST_SSID_SEQUENCE))

    # Encode password (encrypted) at sequence 0
    password_encoded: List[int] = encode_pw(password)
    r.extend(bytes_to_ips(password_encoded, MULTICAST_PASSWORD_SEQUENCE))

    # Encode token group at sequence 32
    token_group_encoded: List[int] = encode_plain(token_group)
    r.extend(bytes_to_ips(token_group_encoded, MULTICAST_TOKEN_SEQUENCE))

    return r
