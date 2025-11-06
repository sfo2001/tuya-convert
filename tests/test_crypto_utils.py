#!/usr/bin/env python3
# encoding: utf-8
"""
Test suite for the refactored crypto_utils module.

This test suite validates that the new crypto_utils module produces
identical output to the original lambda-based implementations.
"""

import os
import sys

import pytest

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

# Import the new crypto_utils module
from crypto_utils import decrypt, encrypt, pad, unpad


class TestCryptoUtilsModule:
    """Test the refactored crypto_utils module."""

    def test_module_exports(self):
        """Test that all expected functions are exported."""
        import crypto_utils

        assert hasattr(crypto_utils, "pad")
        assert hasattr(crypto_utils, "unpad")
        assert hasattr(crypto_utils, "encrypt")
        assert hasattr(crypto_utils, "decrypt")

    def test_pad_function(self):
        """Test pad function from crypto_utils."""
        assert pad("") == chr(16) * 16
        assert pad("A") == "A" + chr(15) * 15
        assert pad("A" * 16) == ("A" * 16) + (chr(16) * 16)

    def test_unpad_function(self):
        """Test unpad function from crypto_utils."""
        padded = "Hello" + chr(11) * 11
        assert unpad(padded) == "Hello"

    def test_encrypt_decrypt_roundtrip(self):
        """Test encrypt/decrypt roundtrip with crypto_utils."""
        key = b"0000000000000000"
        test_messages = [
            "Hello World",
            "Test Message",
            '{"data":{"gwId":"test"},"protocol":15}',
        ]

        for msg in test_messages:
            encrypted = encrypt(msg, key)
            decrypted = decrypt(encrypted, key)
            assert decrypted == msg

    def test_encrypt_validates_key_length(self):
        """Test that encrypt validates key length."""
        with pytest.raises(ValueError, match="AES key must be exactly 16 bytes"):
            encrypt("test", b"short")

        with pytest.raises(ValueError, match="AES key must be exactly 16 bytes"):
            encrypt("test", b"this_is_too_long_for_aes")

    def test_decrypt_validates_key_length(self):
        """Test that decrypt validates key length."""
        with pytest.raises(ValueError, match="AES key must be exactly 16 bytes"):
            decrypt(b"x" * 16, b"short")

    def test_decrypt_validates_message_length(self):
        """Test that decrypt validates message length is multiple of 16."""
        key = b"0000000000000000"
        with pytest.raises(ValueError, match="must be multiple of 16 bytes"):
            decrypt(b"not_16_bytes", key)

    def test_backward_compatibility_with_original(self):
        """
        Test that crypto_utils produces identical output to the original
        lambda-based implementation.
        """
        # Original lambda implementation
        from Cryptodome.Cipher import AES

        pad_orig = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        encrypt_orig = lambda msg, key: AES.new(key, AES.MODE_ECB).encrypt(pad_orig(msg).encode())

        # Test data
        key = b"0000000000000000"
        test_messages = [
            "Hello World",
            "Test",
            "A" * 15,
            "A" * 16,
            "A" * 17,
            '{"data":{"gwId":"43511212112233445566"},"protocol":15,"s":1523715,"t":1234567890}',
        ]

        for msg in test_messages:
            # Both implementations should produce identical output
            original_encrypted = encrypt_orig(msg, key)
            new_encrypted = encrypt(msg, key)
            assert (
                original_encrypted == new_encrypted
            ), f"Encryption output differs for message: {msg}"

    def test_deterministic_encryption(self):
        """Test that encryption is deterministic (ECB property)."""
        key = b"0000000000000000"
        msg = "Test Message"

        result1 = encrypt(msg, key)
        result2 = encrypt(msg, key)
        result3 = encrypt(msg, key)

        assert result1 == result2 == result3

    def test_different_keys_different_output(self):
        """Test that different keys produce different ciphertext."""
        msg = "Test Message"
        key1 = b"0000000000000000"
        key2 = b"1111111111111111"

        result1 = encrypt(msg, key1)
        result2 = encrypt(msg, key2)

        assert result1 != result2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
