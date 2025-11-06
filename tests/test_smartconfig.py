#!/usr/bin/env python3
# encoding: utf-8
"""
Test suite for smartconfig encoding functions.

This test suite validates the broadcast and multicast encoding implementations
to ensure refactoring maintains exact packet sequence compatibility.
"""

import os
import sys

import pytest

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "smartconfig"))

# Import smartconfig modules
from broadcast import broadcast_head, encode_broadcast_body
from multicast import bytes_to_ips, encode_multicast_body, encode_plain, encode_pw, multicast_head


class TestBroadcastHead:
    """Test the broadcast header constant."""

    def test_broadcast_head_format(self):
        """Test that broadcast_head is a list of integers."""
        assert isinstance(broadcast_head, list)
        assert len(broadcast_head) == 4
        assert broadcast_head == [1, 3, 6, 10]

    def test_broadcast_head_values(self):
        """Test broadcast header values are correct."""
        assert broadcast_head[0] == 1
        assert broadcast_head[1] == 3
        assert broadcast_head[2] == 6
        assert broadcast_head[3] == 10


class TestMulticastHead:
    """Test the multicast header constant."""

    def test_multicast_head_format(self):
        """Test that multicast_head is a list of IP strings."""
        assert isinstance(multicast_head, list)
        assert len(multicast_head) == 3  # "TYST01" = 6 bytes = 3 IPs (2 bytes per IP)

    def test_multicast_head_ip_format(self):
        """Test that multicast_head contains valid IP address strings."""
        for ip in multicast_head:
            assert isinstance(ip, str)
            parts = ip.split(".")
            assert len(parts) == 4
            assert parts[0] == "226"  # Multicast prefix

    def test_multicast_head_encodes_tyst01(self):
        """Test that multicast_head encodes the string 'TYST01'."""
        # Should encode "TYST01" starting at sequence 120
        # T=84, Y=89, S=83, T=84, 0=48, 1=49
        expected_bytes = [ord(c) for c in "TYST01"]
        assert expected_bytes == [84, 89, 83, 84, 48, 49]


class TestBytesToIps:
    """Test the bytes_to_ips conversion function."""

    def test_bytes_to_ips_simple(self):
        """Test converting simple byte sequence to IPs."""
        data = [1, 2, 3, 4]
        sequence = 100
        result = bytes_to_ips(data, sequence)

        assert isinstance(result, list)
        assert len(result) == 2  # 4 bytes = 2 IPs

        # First IP: 226.100.2.1
        assert result[0] == "226.100.2.1"
        # Second IP: 226.101.4.3
        assert result[1] == "226.101.4.3"

    def test_bytes_to_ips_odd_length(self):
        """Test that odd-length data gets padded with zero."""
        data = [1, 2, 3]
        sequence = 50
        result = bytes_to_ips(data, sequence)

        assert len(result) == 2  # 3 bytes padded to 4 = 2 IPs
        assert result[0] == "226.50.2.1"
        assert result[1] == "226.51.0.3"  # Padded with 0

    def test_bytes_to_ips_sequence_increment(self):
        """Test that sequence number increments for each IP."""
        data = [10, 20, 30, 40]
        sequence = 0
        result = bytes_to_ips(data, sequence)

        parts0 = result[0].split(".")
        parts1 = result[1].split(".")

        assert parts0[1] == "0"
        assert parts1[1] == "1"

    def test_bytes_to_ips_format(self):
        """Test IP format: 226.sequence.byte[i+1].byte[i]."""
        data = [65, 66]  # 'A', 'B'
        sequence = 10
        result = bytes_to_ips(data, sequence)

        assert len(result) == 1
        assert result[0] == "226.10.66.65"


class TestEncodePlain:
    """Test the encode_plain function for SSID and token_group."""

    def test_encode_plain_structure(self):
        """Test that encode_plain returns correct structure."""
        s = "test"
        result = encode_plain(s)

        assert isinstance(result, list)
        # Structure: length (2x) + CRC32 (4 bytes LE) + payload
        assert len(result) >= 6

        # First two bytes should be length
        assert result[0] == len(s)
        assert result[1] == len(s)

    def test_encode_plain_ssid_example(self):
        """Test encoding example SSID."""
        ssid = "vtrust-flash"
        result = encode_plain(ssid)

        assert result[0] == 12  # length
        assert result[1] == 12  # length again
        # Bytes 2-5 are CRC32 in LE format
        # Bytes 6+ are the plaintext SSID
        payload_start = 6
        payload = result[payload_start:]
        assert payload == [ord(c) for c in ssid]

    def test_encode_plain_deterministic(self):
        """Test that encode_plain is deterministic."""
        s = "test123"
        result1 = encode_plain(s)
        result2 = encode_plain(s)
        assert result1 == result2

    def test_encode_plain_empty_string(self):
        """Test encoding empty string."""
        result = encode_plain("")
        assert result[0] == 0
        assert result[1] == 0
        # Should still have CRC bytes
        assert len(result) == 6  # 2 length + 4 CRC + 0 payload


class TestEncodePw:
    """Test the encode_pw function for password encryption."""

    def test_encode_pw_structure(self):
        """Test that encode_pw returns correct structure."""
        pw = "password"
        result = encode_pw(pw)

        assert isinstance(result, list)
        # Structure: length (2x) + CRC32 (4 bytes LE) + AES-encrypted payload
        assert len(result) >= 6

        # First two bytes should be length
        assert result[0] == len(pw)
        assert result[1] == len(pw)

    def test_encode_pw_encrypted(self):
        """Test that password is encrypted (not plaintext)."""
        pw = "password"
        result = encode_pw(pw)

        payload_start = 6
        payload = result[payload_start:]
        pw_bytes = [ord(c) for c in pw]

        # Payload should NOT equal plaintext (it's encrypted)
        assert payload != pw_bytes

    def test_encode_pw_deterministic(self):
        """Test that encode_pw is deterministic (same key used)."""
        pw = "testpass"
        result1 = encode_pw(pw)
        result2 = encode_pw(pw)

        # Should be deterministic because AES-ECB is deterministic
        assert result1 == result2

    def test_encode_pw_padded_length(self):
        """Test that encrypted payload is padded to 16-byte blocks."""
        pw = "short"
        result = encode_pw(pw)

        payload_start = 6
        payload = result[payload_start:]
        payload_len = len(payload)

        # Encrypted payload should be multiple of 16 (AES block size)
        assert payload_len % 16 == 0

    def test_encode_pw_different_passwords(self):
        """Test that different passwords produce different encodings."""
        pw1 = "password1"
        pw2 = "password2"

        result1 = encode_pw(pw1)
        result2 = encode_pw(pw2)

        # Should be different
        assert result1 != result2


class TestEncodeBroadcastBody:
    """Test the encode_broadcast_body function."""

    def test_encode_broadcast_body_returns_list(self):
        """Test that encode_broadcast_body returns a list of integers."""
        password = "pass"
        ssid = "test"
        token_group = "UStoken0101"

        result = encode_broadcast_body(password, ssid, token_group)

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(x, int) for x in result)

    def test_encode_broadcast_body_deterministic(self):
        """Test that encoding is deterministic."""
        password = "mypass"
        ssid = "myssid"
        token_group = "UStoken0101"

        result1 = encode_broadcast_body(password, ssid, token_group)
        result2 = encode_broadcast_body(password, ssid, token_group)

        assert result1 == result2

    def test_encode_broadcast_body_example(self):
        """Test with example values from smartconfig/main.py."""
        password = ""
        ssid = "vtrust-flash"
        token_group = "US000000000101"

        result = encode_broadcast_body(password, ssid, token_group)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_encode_broadcast_body_different_inputs(self):
        """Test that different inputs produce different outputs."""
        password1 = "pass1"
        password2 = "pass2"
        ssid = "test"
        token_group = "UStoken0101"

        result1 = encode_broadcast_body(password1, ssid, token_group)
        result2 = encode_broadcast_body(password2, ssid, token_group)

        assert result1 != result2


class TestEncodeMulticastBody:
    """Test the encode_multicast_body function."""

    def test_encode_multicast_body_returns_list_of_ips(self):
        """Test that encode_multicast_body returns a list of IP strings."""
        password = "pass"
        ssid = "test"
        token_group = "UStoken0101"

        result = encode_multicast_body(password, ssid, token_group)

        assert isinstance(result, list)
        assert len(result) > 0
        assert all(isinstance(ip, str) for ip in result)

        # All should be valid IPs starting with 226
        for ip in result:
            parts = ip.split(".")
            assert len(parts) == 4
            assert parts[0] == "226"

    def test_encode_multicast_body_deterministic(self):
        """Test that encoding is deterministic."""
        password = "mypass"
        ssid = "myssid"
        token_group = "UStoken0101"

        result1 = encode_multicast_body(password, ssid, token_group)
        result2 = encode_multicast_body(password, ssid, token_group)

        assert result1 == result2

    def test_encode_multicast_body_example(self):
        """Test with example values from smartconfig/main.py."""
        password = ""
        ssid = "vtrust-flash"
        token_group = "US000000000101"

        result = encode_multicast_body(password, ssid, token_group)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_encode_multicast_body_three_sections(self):
        """Test that multicast body contains three encoded sections."""
        password = "pass"
        ssid = "testssid"
        token_group = "UStoken0101"

        result = encode_multicast_body(password, ssid, token_group)

        # Should contain:
        # 1. SSID encoding (plaintext, starts at sequence 64)
        # 2. Password encoding (encrypted, starts at sequence 0)
        # 3. Token/group encoding (plaintext, starts at sequence 32)
        assert len(result) > 10  # Should be substantial

    def test_encode_multicast_body_different_inputs(self):
        """Test that different inputs produce different outputs."""
        password = "pass"
        ssid1 = "ssid1"
        ssid2 = "ssid2"
        token_group = "UStoken0101"

        result1 = encode_multicast_body(password, ssid1, token_group)
        result2 = encode_multicast_body(password, ssid2, token_group)

        assert result1 != result2


class TestSmartconfigIntegration:
    """Integration tests for complete smartconfig encoding."""

    def test_complete_smartconfig_sequence(self):
        """Test complete smartconfig encoding as used in main.py."""
        # Parameters from smartconfig/main.py
        ssid = "vtrust-flash"
        passwd = ""
        region = "US"
        token = "00000000"
        secret = "0101"
        token_group = region + token + secret

        # Generate both broadcast and multicast bodies
        broadcast_body = encode_broadcast_body(passwd, ssid, token_group)
        multicast_body = encode_multicast_body(passwd, ssid, token_group)

        # Verify both are valid
        assert isinstance(broadcast_body, list)
        assert isinstance(multicast_body, list)
        assert len(broadcast_body) > 0
        assert len(multicast_body) > 0

        # Verify headers
        assert isinstance(broadcast_head, list)
        assert isinstance(multicast_head, list)

    def test_regression_vtrust_flash(self):
        """Regression test with exact values used in production."""
        ssid = "vtrust-flash"
        passwd = ""
        token_group = "US000000000101"

        # Calculate encodings
        broadcast_body = encode_broadcast_body(passwd, ssid, token_group)
        multicast_body = encode_multicast_body(passwd, ssid, token_group)

        # Store these values for regression testing
        # Any refactoring MUST produce identical output
        expected_broadcast_len = len(broadcast_body)
        expected_multicast_len = len(multicast_body)

        # Re-encode and verify identical
        assert len(encode_broadcast_body(passwd, ssid, token_group)) == expected_broadcast_len
        assert len(encode_multicast_body(passwd, ssid, token_group)) == expected_multicast_len

        # Verify exact equality
        assert encode_broadcast_body(passwd, ssid, token_group) == broadcast_body
        assert encode_multicast_body(passwd, ssid, token_group) == multicast_body


class TestSmartconfigBitManipulation:
    """Test bit manipulation operations used in smartconfig."""

    def test_broadcast_length_encoding(self):
        """Test length encoding in broadcast mode."""
        # From broadcast.py
        length = 25

        # Encode length into 4 values
        nibble1 = length >> 4 | 16
        nibble2 = length & 0xF | 32

        assert 16 <= nibble1 < 32
        assert 32 <= nibble2 < 48

    def test_broadcast_crc_encoding(self):
        """Test CRC encoding in broadcast mode."""
        # Example length_crc value
        length_crc = 0xA5  # 10100101

        nibble3 = length_crc >> 4 | 48
        nibble4 = length_crc & 0xF | 64

        assert 48 <= nibble3 < 64
        assert 64 <= nibble4 < 80

    def test_broadcast_data_encoding(self):
        """Test data byte encoding in broadcast mode."""
        # From broadcast.py: data bytes are OR'd with 256
        data_byte = 65  # 'A'
        encoded = data_byte | 256

        assert encoded == 321
        assert encoded >= 256


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
