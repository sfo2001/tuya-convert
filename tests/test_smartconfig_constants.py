#!/usr/bin/env python3
# encoding: utf-8
"""
test_smartconfig_constants.py
Tests for smartconfig protocol constants

Verifies that all constants have correct types and reasonable values.
"""

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from smartconfig import constants


class TestBroadcastConstants:
    """Test broadcast protocol encoding constants."""

    def test_nibble_markers_are_integers(self):
        """All nibble markers should be integers."""
        assert isinstance(constants.LENGTH_HIGH_NIBBLE_MARKER, int)
        assert isinstance(constants.LENGTH_LOW_NIBBLE_MARKER, int)
        assert isinstance(constants.CRC_HIGH_NIBBLE_MARKER, int)
        assert isinstance(constants.CRC_LOW_NIBBLE_MARKER, int)

    def test_nibble_markers_have_correct_values(self):
        """Nibble markers should have protocol-specified values."""
        assert constants.LENGTH_HIGH_NIBBLE_MARKER == 0x10
        assert constants.LENGTH_LOW_NIBBLE_MARKER == 0x20
        assert constants.CRC_HIGH_NIBBLE_MARKER == 0x30
        assert constants.CRC_LOW_NIBBLE_MARKER == 0x40

    def test_data_markers_are_integers(self):
        """Data encoding markers should be integers."""
        assert isinstance(constants.DATA_BYTE_MARKER, int)
        assert isinstance(constants.SEQUENCE_MARKER, int)
        assert isinstance(constants.CRC_MARKER, int)

    def test_data_markers_have_correct_values(self):
        """Data markers should have protocol-specified values."""
        assert constants.DATA_BYTE_MARKER == 0x100  # 256
        assert constants.SEQUENCE_MARKER == 0x80  # 128
        assert constants.CRC_MARKER == 0x80  # 128

    def test_bit_masks_are_integers(self):
        """Bit masks should be integers."""
        assert isinstance(constants.NIBBLE_MASK, int)
        assert isinstance(constants.CRC_MASK, int)

    def test_bit_masks_have_correct_values(self):
        """Bit masks should have correct values."""
        assert constants.NIBBLE_MASK == 0x0F  # 15
        assert constants.CRC_MASK == 0x7F  # 127

    def test_nibble_mask_extracts_lower_4_bits(self):
        """NIBBLE_MASK should correctly extract lower 4 bits."""
        # Test with various values
        assert (0x5A & constants.NIBBLE_MASK) == 0x0A
        assert (0xFF & constants.NIBBLE_MASK) == 0x0F
        assert (0x10 & constants.NIBBLE_MASK) == 0x00


class TestMulticastConstants:
    """Test multicast protocol constants."""

    def test_multicast_base_ip_is_string(self):
        """Multicast base IP should be a string."""
        assert isinstance(constants.MULTICAST_BASE_IP, str)

    def test_multicast_base_ip_value(self):
        """Multicast base IP should be '226'."""
        assert constants.MULTICAST_BASE_IP == "226"

    def test_sequence_numbers_are_integers(self):
        """All sequence numbers should be integers."""
        assert isinstance(constants.MULTICAST_HEADER_SEQUENCE, int)
        assert isinstance(constants.MULTICAST_SSID_SEQUENCE, int)
        assert isinstance(constants.MULTICAST_TOKEN_SEQUENCE, int)
        assert isinstance(constants.MULTICAST_PASSWORD_SEQUENCE, int)

    def test_sequence_numbers_have_correct_values(self):
        """Sequence numbers should match protocol specification."""
        assert constants.MULTICAST_HEADER_SEQUENCE == 120
        assert constants.MULTICAST_SSID_SEQUENCE == 64
        assert constants.MULTICAST_TOKEN_SEQUENCE == 32
        assert constants.MULTICAST_PASSWORD_SEQUENCE == 0

    def test_sequence_numbers_are_in_valid_range(self):
        """Sequence numbers should fit in IP address octet (0-255)."""
        assert 0 <= constants.MULTICAST_HEADER_SEQUENCE <= 255
        assert 0 <= constants.MULTICAST_SSID_SEQUENCE <= 255
        assert 0 <= constants.MULTICAST_TOKEN_SEQUENCE <= 255
        assert 0 <= constants.MULTICAST_PASSWORD_SEQUENCE <= 255

    def test_sequence_numbers_dont_overlap(self):
        """Different sections should have distinct sequence ranges."""
        # This ensures sections don't accidentally overlap
        sequences = [
            constants.MULTICAST_HEADER_SEQUENCE,
            constants.MULTICAST_SSID_SEQUENCE,
            constants.MULTICAST_TOKEN_SEQUENCE,
            constants.MULTICAST_PASSWORD_SEQUENCE,
        ]
        assert len(sequences) == len(set(sequences)), "Sequence numbers should be unique"


class TestNetworkConstants:
    """Test network port constants."""

    def test_ports_are_integers(self):
        """Port numbers should be integers."""
        assert isinstance(constants.BROADCAST_PORT, int)
        assert isinstance(constants.MULTICAST_PORT, int)

    def test_ports_have_correct_values(self):
        """Ports should match protocol specification."""
        assert constants.BROADCAST_PORT == 30011
        assert constants.MULTICAST_PORT == 30012

    def test_ports_are_in_valid_range(self):
        """Ports should be valid UDP port numbers."""
        assert 1 <= constants.BROADCAST_PORT <= 65535
        assert 1 <= constants.MULTICAST_PORT <= 65535

    def test_ports_are_different(self):
        """Broadcast and multicast should use different ports."""
        assert constants.BROADCAST_PORT != constants.MULTICAST_PORT

    def test_multicast_ttl_is_integer(self):
        """TTL should be an integer."""
        assert isinstance(constants.MULTICAST_TTL, int)

    def test_multicast_ttl_value(self):
        """TTL should be 1 for local network only."""
        assert constants.MULTICAST_TTL == 1


class TestTimingConstants:
    """Test timing-related constants."""

    def test_packet_gap_ms_is_integer(self):
        """Packet gap in milliseconds should be an integer."""
        assert isinstance(constants.DEFAULT_PACKET_GAP_MS, int)

    def test_packet_gap_ms_value(self):
        """Packet gap should be 5ms."""
        assert constants.DEFAULT_PACKET_GAP_MS == 5

    def test_packet_gap_seconds_is_float(self):
        """Packet gap in seconds should be a float."""
        assert isinstance(constants.DEFAULT_PACKET_GAP_SECONDS, float)

    def test_packet_gap_seconds_value(self):
        """Packet gap in seconds should equal ms/1000."""
        expected = constants.DEFAULT_PACKET_GAP_MS / 1000.0
        assert constants.DEFAULT_PACKET_GAP_SECONDS == expected

    def test_packet_gap_is_reasonable(self):
        """Packet gap should be between 1ms and 100ms."""
        assert 0.001 <= constants.DEFAULT_PACKET_GAP_SECONDS <= 0.1

    def test_repeat_counts_are_integers(self):
        """Repeat counts should be integers."""
        assert isinstance(constants.HEADER_REPEAT_COUNT, int)
        assert isinstance(constants.BODY_REPEAT_COUNT, int)

    def test_repeat_counts_have_correct_values(self):
        """Repeat counts should match protocol specification."""
        assert constants.HEADER_REPEAT_COUNT == 40
        assert constants.BODY_REPEAT_COUNT == 10

    def test_repeat_counts_are_positive(self):
        """Repeat counts should be positive."""
        assert constants.HEADER_REPEAT_COUNT > 0
        assert constants.BODY_REPEAT_COUNT > 0


class TestCryptographyConstants:
    """Test cryptography-related constants."""

    def test_aes_key_is_bytes(self):
        """AES key should be bytes."""
        assert isinstance(constants.SMARTCONFIG_AES_KEY, bytes)

    def test_aes_key_length(self):
        """AES key should be 16 bytes (AES-128)."""
        assert len(constants.SMARTCONFIG_AES_KEY) == 16

    def test_aes_key_value(self):
        """AES key should match protocol specification."""
        assert constants.SMARTCONFIG_AES_KEY == b"a3c6794oiu876t54"

    def test_aes_block_size_is_integer(self):
        """AES block size should be an integer."""
        assert isinstance(constants.AES_BLOCK_SIZE, int)

    def test_aes_block_size_value(self):
        """AES block size should be 16 bytes."""
        assert constants.AES_BLOCK_SIZE == 16


class TestCRCConstants:
    """Test CRC algorithm constants."""

    def test_crc8_constants_are_integers(self):
        """CRC-8 constants should be integers."""
        assert isinstance(constants.CRC8_POLYNOMIAL, int)
        assert isinstance(constants.CRC8_INIT, int)

    def test_crc8_constants_values(self):
        """CRC-8 constants should match protocol specification."""
        assert constants.CRC8_POLYNOMIAL == 0x18
        assert constants.CRC8_INIT == 0x80

    def test_crc32_constants_are_integers(self):
        """CRC-32 constants should be integers."""
        assert isinstance(constants.CRC32_INIT, int)
        assert isinstance(constants.CRC32_FINAL_XOR, int)
        assert isinstance(constants.CRC32_MASK, int)
        assert isinstance(constants.CRC32_TABLE_INDEX_MASK, int)

    def test_crc32_constants_values(self):
        """CRC-32 constants should have correct values."""
        assert constants.CRC32_INIT == -1
        assert constants.CRC32_FINAL_XOR == -1
        assert constants.CRC32_MASK == 0xFFFFFFFF
        assert constants.CRC32_TABLE_INDEX_MASK == 0xFF  # 255

    def test_crc32_mask_is_32bit(self):
        """CRC32_MASK should be maximum 32-bit unsigned value."""
        assert constants.CRC32_MASK == 0xFFFFFFFF
        assert constants.CRC32_MASK == (2**32 - 1)


class TestBitShiftConstants:
    """Test bit shift constants."""

    def test_shift_constants_are_integers(self):
        """Bit shift constants should be integers."""
        assert isinstance(constants.SHIFT_4_BITS, int)
        assert isinstance(constants.SHIFT_8_BITS, int)
        assert isinstance(constants.SHIFT_BYTE, int)

    def test_shift_constants_values(self):
        """Bit shift constants should have correct values."""
        assert constants.SHIFT_4_BITS == 4
        assert constants.SHIFT_8_BITS == 8
        assert constants.SHIFT_BYTE == 8

    def test_crc32_le_shifts_is_list(self):
        """CRC32_LE_SHIFTS should be a list."""
        assert isinstance(constants.CRC32_LE_SHIFTS, list)

    def test_crc32_le_shifts_values(self):
        """CRC32_LE_SHIFTS should contain correct shift values."""
        assert constants.CRC32_LE_SHIFTS == [0, 8, 16, 24]

    def test_crc32_le_shifts_length(self):
        """CRC32_LE_SHIFTS should have 4 elements (4 bytes)."""
        assert len(constants.CRC32_LE_SHIFTS) == 4

    def test_byte_mask_is_integer(self):
        """BYTE_MASK should be an integer."""
        assert isinstance(constants.BYTE_MASK, int)

    def test_byte_mask_value(self):
        """BYTE_MASK should be 0xFF (255)."""
        assert constants.BYTE_MASK == 0xFF
        assert constants.BYTE_MASK == 255

    def test_byte_mask_extracts_single_byte(self):
        """BYTE_MASK should correctly extract a single byte."""
        assert (0x1234 & constants.BYTE_MASK) == 0x34
        assert (0xABCDEF & constants.BYTE_MASK) == 0xEF


class TestDefaultConfiguration:
    """Test default configuration values."""

    def test_default_bind_address_is_string(self):
        """Default bind address should be a string."""
        assert isinstance(constants.DEFAULT_BIND_ADDRESS, str)

    def test_default_bind_address_value(self):
        """Default bind address should be the AP gateway."""
        assert constants.DEFAULT_BIND_ADDRESS == "10.42.42.1"

    def test_default_bind_address_format(self):
        """Default bind address should be a valid IP format."""
        parts = constants.DEFAULT_BIND_ADDRESS.split(".")
        assert len(parts) == 4
        for part in parts:
            assert part.isdigit()
            assert 0 <= int(part) <= 255


class TestConstantsImmutability:
    """Test that constants are not accidentally mutable."""

    def test_aes_key_is_immutable_bytes(self):
        """AES key should be immutable bytes, not bytearray."""
        assert type(constants.SMARTCONFIG_AES_KEY) is bytes
        assert not isinstance(constants.SMARTCONFIG_AES_KEY, bytearray)

    def test_all_integer_constants_are_int(self):
        """All integer constants should be int type (not float or other)."""
        integer_constants = [
            constants.LENGTH_HIGH_NIBBLE_MARKER,
            constants.LENGTH_LOW_NIBBLE_MARKER,
            constants.CRC_HIGH_NIBBLE_MARKER,
            constants.CRC_LOW_NIBBLE_MARKER,
            constants.DATA_BYTE_MARKER,
            constants.SEQUENCE_MARKER,
            constants.CRC_MARKER,
            constants.NIBBLE_MASK,
            constants.CRC_MASK,
            constants.BROADCAST_PORT,
            constants.MULTICAST_PORT,
            constants.MULTICAST_TTL,
            constants.HEADER_REPEAT_COUNT,
            constants.BODY_REPEAT_COUNT,
            constants.AES_BLOCK_SIZE,
            constants.CRC8_POLYNOMIAL,
            constants.CRC8_INIT,
            constants.CRC32_MASK,
            constants.CRC32_TABLE_INDEX_MASK,
        ]

        for const in integer_constants:
            assert type(const) is int, f"Constant {const} should be int, got {type(const)}"


class TestConstantsDocumentation:
    """Test that constants module has proper documentation."""

    def test_module_has_docstring(self):
        """Module should have a docstring."""
        assert constants.__doc__ is not None
        assert len(constants.__doc__) > 0

    def test_module_docstring_mentions_protocol(self):
        """Module docstring should mention 'protocol'."""
        assert "protocol" in constants.__doc__.lower()
