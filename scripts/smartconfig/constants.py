#!/usr/bin/env python3
# encoding: utf-8
"""
constants.py
Protocol constants for Tuya smartconfig.

These constants define the protocol-level values used in broadcast and
multicast smartconfig encoding. They are hardcoded in the Tuya device
firmware and must not be changed.

Created: 2025-11-07
Purpose: Centralize magic numbers and improve code readability
"""

# =============================================================================
# Broadcast Protocol Encoding Constants
# =============================================================================
#
# The broadcast protocol encodes data by OR'ing each nibble with a specific
# marker value to identify its purpose in the protocol stream.
#

# Length nibble markers - Used to encode the total payload length
LENGTH_HIGH_NIBBLE_MARKER = 0x10  # 16 - Marks high nibble of length byte
LENGTH_LOW_NIBBLE_MARKER = 0x20  # 32 - Marks low nibble of length byte

# CRC nibble markers - Used to encode CRC8 checksum of length
CRC_HIGH_NIBBLE_MARKER = 0x30  # 48 - Marks high nibble of CRC8
CRC_LOW_NIBBLE_MARKER = 0x40  # 64 - Marks low nibble of CRC8

# Data encoding markers
DATA_BYTE_MARKER = 0x100  # 256 - OR'd with data payload bytes
SEQUENCE_MARKER = 0x80  # 128 - OR'd with sequence numbers
CRC_MARKER = 0x80  # 128 - OR'd with CRC bytes in data groups

# Bit masks for extracting values
NIBBLE_MASK = 0x0F  # 15 - Extracts lower 4 bits (one nibble)
CRC_MASK = 0x7F  # 127 - Extracts lower 7 bits for CRC values


# =============================================================================
# Multicast Protocol Constants
# =============================================================================
#
# The multicast protocol encodes data as IP addresses in the 226.x.y.z range.
# Each section of data (header, SSID, password, token) starts at a specific
# sequence number which becomes the second octet of the IP address.
#

# Multicast IP addressing
MULTICAST_BASE_IP = "226"  # First octet for all multicast IPs

# Multicast sequence numbers for different data sections
MULTICAST_HEADER_SEQUENCE = 120  # Sequence start for "TYST01" header
MULTICAST_SSID_SEQUENCE = 64  # Sequence start for SSID encoding
MULTICAST_TOKEN_SEQUENCE = 32  # Sequence start for token group encoding
MULTICAST_PASSWORD_SEQUENCE = 0  # Sequence start for password encoding


# =============================================================================
# Network Port Constants
# =============================================================================

BROADCAST_PORT = 30011  # UDP port for broadcast packets
MULTICAST_PORT = 30012  # UDP port for multicast packets


# =============================================================================
# Timing Constants
# =============================================================================

# Time to sleep between packets (milliseconds and seconds)
DEFAULT_PACKET_GAP_MS = 5  # Milliseconds between packets
DEFAULT_PACKET_GAP_SECONDS = DEFAULT_PACKET_GAP_MS / 1000.0  # 0.005 seconds

# Repetition counts for reliability
# These values ensure devices have enough time to receive the full config
HEADER_REPEAT_COUNT = 40  # Send header 40 times before body
BODY_REPEAT_COUNT = 10  # Send complete body 10 times


# =============================================================================
# Multicast Network Constants
# =============================================================================

MULTICAST_TTL = 1  # Time-to-live for multicast packets (local network only)


# =============================================================================
# Cryptography Constants
# =============================================================================

# Fixed AES key for smartconfig multicast encryption
# This key is hardcoded in the Tuya protocol specification and cannot be changed
SMARTCONFIG_AES_KEY = b"a3c6794oiu876t54"  # 16 bytes for AES-128

AES_BLOCK_SIZE = 16  # AES block size in bytes (128 bits)


# =============================================================================
# CRC Algorithm Constants
# =============================================================================

# CRC-8 polynomial and initial value
# Used for checksumming in broadcast protocol
CRC8_POLYNOMIAL = 0x18  # CRC-8 polynomial (x^4 + x^3 + 1)
CRC8_INIT = 0x80  # CRC-8 initial value (MSB set)

# CRC-32 constants
CRC32_INIT = -1  # Initial value for CRC-32 algorithm
CRC32_FINAL_XOR = -1  # XOR value applied to final CRC-32 result
CRC32_MASK = 0xFFFFFFFF  # Mask to keep CRC-32 as 32-bit unsigned
CRC32_TABLE_INDEX_MASK = 0xFF  # Mask for CRC-32 table lookup (255)


# =============================================================================
# Bit Shift Constants
# =============================================================================

# Common bit shift values used in encoding
SHIFT_4_BITS = 4  # Shift to extract high nibble
SHIFT_8_BITS = 8  # Shift for byte operations
SHIFT_BYTE = 8  # Shift one byte (for multi-byte encoding)

# Bit shifts for CRC32 little-endian encoding (0, 8, 16, 24 bits)
CRC32_LE_SHIFTS = [0, 8, 16, 24]  # Little-endian byte order shifts
BYTE_MASK = 0xFF  # 255 - Mask for extracting a single byte


# =============================================================================
# Default Configuration Values
# =============================================================================

# Default bind address for smartconfig socket
DEFAULT_BIND_ADDRESS = "10.42.42.1"  # Typically the AP gateway address
