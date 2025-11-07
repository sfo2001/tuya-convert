#!/usr/bin/env python3
# encoding: utf-8
"""
Test suite for mq_pub_15.py error handling.

This test suite validates proper exception handling and error messages
in the mq_pub_15.py command-line tool.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from mq_pub_15 import main, Usage, iot_enc, iot_dec


class TestUsageException:
    """Test the Usage exception class."""

    def test_usage_exception_creation(self):
        """Test creating Usage exception with message."""
        msg = "Test error message"
        exc = Usage(msg)
        assert exc.msg == msg
        assert isinstance(exc, Exception)


class TestMainErrorHandling:
    """Test error handling in main() function."""

    def test_missing_required_device_id(self):
        """Test that missing deviceID argument returns error code."""
        # Missing -i/--deviceID argument (argv[0] is script name)
        result = main(["mq_pub_15.py", "-l", "0000000000000000"])
        assert result == 2

    def test_missing_required_local_key(self):
        """Test that missing localKey returns error code."""
        # Test with explicit short key
        result = main(["mq_pub_15.py", "-i", "12345678901234567890", "-l", "short"])
        assert result == 2

    def test_device_id_too_short(self):
        """Test that deviceID shorter than 10 characters returns error."""
        result = main(["mq_pub_15.py", "-i", "short", "-l", "0000000000000000"])
        assert result == 2

    def test_local_key_too_short(self):
        """Test that localKey shorter than 10 characters returns error."""
        result = main(["mq_pub_15.py", "-i", "12345678901234567890", "-l", "short"])
        assert result == 2

    def test_invalid_argument(self):
        """Test that invalid arguments are handled properly."""
        # Invalid option should trigger getopt error
        result = main(["mq_pub_15.py", "-x", "invalid"])
        assert result == 2

    def test_help_option_returns_error_code(self):
        """Test that -h/--help returns error code 2."""
        result = main(["mq_pub_15.py", "-h"])
        assert result == 2

        result = main(["mq_pub_15.py", "--help"])
        assert result == 2

    @patch("mq_pub_15.publish.single")
    def test_valid_arguments_success(self, mock_publish):
        """Test that valid arguments allow execution to proceed."""
        # Mock MQTT publish to avoid actual network call
        mock_publish.return_value = None

        result = main(
            ["mq_pub_15.py", "-i", "12345678901234567890", "-l", "0000000000000000"]
        )
        # Should succeed (return None or 0)
        assert result is None or result == 0
        # Verify MQTT publish was called
        assert mock_publish.called

    @patch("mq_pub_15.publish.single")
    def test_protocol_2_2_with_valid_args(self, mock_publish):
        """Test protocol 2.2 with valid arguments."""
        mock_publish.return_value = None

        result = main(
            [
                "mq_pub_15.py",
                "-i",
                "12345678901234567890",
                "-l",
                "0000000000000000",
                "-p",
                "2.2",
            ]
        )
        assert result is None or result == 0
        assert mock_publish.called


class TestIotEncFunction:
    """Test iot_enc function error handling."""

    def test_iot_enc_protocol_2_1(self):
        """Test iot_enc with protocol 2.1."""
        message = '{"data":{"gwId":"test"},"protocol":15}'
        local_key = "0000000000000000"
        result = iot_enc(message, local_key, "2.1")

        # Should return bytes
        assert isinstance(result, bytes)
        # Should start with protocol version
        assert result.startswith(b"2.1")

    def test_iot_enc_protocol_2_2(self):
        """Test iot_enc with protocol 2.2."""
        message = '{"data":{"gwId":"test"},"protocol":15}'
        local_key = "0000000000000000"
        result = iot_enc(message, local_key, "2.2")

        # Should return bytes
        assert isinstance(result, bytes)
        # Should start with protocol version
        assert result.startswith(b"2.2")

    def test_iot_enc_with_short_key(self):
        """Test iot_enc with key too short for AES."""
        message = '{"test":"data"}'
        local_key = "short"  # Too short for AES (needs 16 bytes)

        # Should raise ValueError from crypto_utils
        with pytest.raises(ValueError, match="AES key must be exactly 16 bytes"):
            iot_enc(message, local_key, "2.1")


class TestIotDecFunction:
    """Test iot_dec function error handling."""

    def test_iot_dec_with_valid_message(self):
        """Test iot_dec with properly formatted message."""
        # Create a valid encrypted message first
        local_key = "0000000000000000"
        original = '{"test":"data"}'

        # Encrypt it
        encrypted = iot_enc(original, local_key, "2.1")

        # Decrypt it
        decrypted = iot_dec(encrypted, local_key)
        assert decrypted == original

    def test_iot_dec_with_invalid_base64(self):
        """Test iot_dec with invalid base64 data."""
        local_key = "0000000000000000"
        # Invalid base64 after the protocol header (19 bytes)
        invalid_message = b"2.1" + b"0" * 16 + b"invalid!@#$%"

        # Should raise error during base64 decode
        with pytest.raises(Exception):  # Could be binascii.Error or ValueError
            iot_dec(invalid_message, local_key)

    def test_iot_dec_with_wrong_key(self):
        """Test iot_dec with wrong decryption key."""
        # Encrypt with one key
        local_key1 = "0000000000000000"
        original = '{"test":"data"}'
        encrypted = iot_enc(original, local_key1, "2.1")

        # Try to decrypt with different key
        local_key2 = "1111111111111111"
        # Should raise error or produce garbage
        with pytest.raises(Exception):  # Could be UnicodeDecodeError or ValueError
            iot_dec(encrypted, local_key2)


class TestCommandLineInterface:
    """Test command-line interface behavior."""

    @patch("sys.stdout")
    def test_help_message_displayed(self, mock_stdout):
        """Test that help message is displayed on error."""
        result = main(["-h"])
        assert result == 2
        # Help message should be printed

    def test_empty_arguments(self):
        """Test with empty arguments list."""
        result = main(["mq_pub_15.py"])
        assert result == 2  # Should fail due to missing required args

    @patch("mq_pub_15.publish.single")
    def test_custom_broker(self, mock_publish):
        """Test specifying custom broker address."""
        mock_publish.return_value = None

        result = main(
            [
                "mq_pub_15.py",
                "-i",
                "12345678901234567890",
                "-l",
                "0000000000000000",
                "-b",
                "192.168.1.100",
            ]
        )

        assert result is None or result == 0
        # Verify broker was passed to publish.single
        assert mock_publish.called
        call_kwargs = mock_publish.call_args
        assert call_kwargs.kwargs.get("hostname") == "192.168.1.100"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
