#!/usr/bin/env python3
# encoding: utf-8
"""
Cryptographic utilities for tuya-convert.

This module provides shared cryptographic functions used across the tuya-convert
project for encrypting and decrypting data in communication with Tuya IoT devices.

Security Note:
--------------
This module uses AES-ECB mode, which is generally considered less secure than
CBC or GCM modes because it's deterministic (same plaintext always produces
the same ciphertext). This is the protocol design chosen by Tuya and cannot
be changed without breaking compatibility with Tuya devices.

The PKCS#7 padding implementation follows the standard specification where
padding bytes equal the padding length.

Functions:
---------
- pad(): Apply PKCS#7 padding to a string
- unpad(): Remove PKCS#7 padding from a string
- encrypt(): Encrypt a message using AES-ECB with PKCS#7 padding
- decrypt(): Decrypt a message using AES-ECB and remove PKCS#7 padding

Created by VTRUST for tuya-convert.
Copyright (c) 2018 VTRUST. All rights reserved.
"""

from typing import Union

from Cryptodome.Cipher import AES


def pad(data: str) -> str:
    """
    Apply PKCS#7 padding to a string to make it a multiple of 16 bytes.

    PKCS#7 padding adds N bytes with value N, where N is the number of bytes
    needed to reach the next 16-byte boundary. If the data is already a
    multiple of 16 bytes, a full block of 16 bytes (each with value 0x10)
    is added.

    Args:
        data: String to pad

    Returns:
        Padded string with length as a multiple of 16 bytes

    Examples:
        >>> pad("Hello")  # 5 bytes -> needs 11 bytes padding
        'Hello\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b'

        >>> pad("A" * 16)  # Exactly 16 bytes -> adds full 16-byte padding block
        'AAAAAAAAAAAAAAAA\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10\\x10'
    """
    padding_length = 16 - len(data) % 16
    return data + padding_length * chr(padding_length)


def unpad(data: str) -> str:
    """
    Remove PKCS#7 padding from a string.

    Reads the last byte to determine how many padding bytes to remove.
    This assumes the data was properly padded with PKCS#7.

    Args:
        data: Padded string to unpad

    Returns:
        Original unpadded string

    Examples:
        >>> unpad("Hello\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b\\x0b")
        'Hello'

    Note:
        This function does not validate that the padding is correct.
        Invalid padding will result in incorrect output.
    """
    return data[: -ord(data[len(data) - 1 :])]


def encrypt(message: str, key: bytes) -> bytes:
    """
    Encrypt a message using AES-ECB mode with PKCS#7 padding.

    This function:
    1. Applies PKCS#7 padding to the message
    2. Encodes the padded message to UTF-8 bytes
    3. Encrypts using AES-ECB mode with the provided key

    Security Note:
        AES-ECB mode is deterministic and does not provide semantic security.
        The same plaintext with the same key will always produce the same
        ciphertext. This mode is used for Tuya protocol compatibility.

    Args:
        message: Plain text string to encrypt
        key: AES encryption key (must be exactly 16 bytes for AES-128)

    Returns:
        Encrypted message as bytes

    Raises:
        ValueError: If key length is not 16 bytes
        UnicodeEncodeError: If message contains characters that cannot be
                           encoded to UTF-8

    Examples:
        >>> key = b"0000000000000000"  # 16-byte key
        >>> encrypted = encrypt("Hello World", key)
        >>> isinstance(encrypted, bytes)
        True
        >>> len(encrypted) % 16 == 0  # Always multiple of 16
        True
    """
    if len(key) != 16:
        raise ValueError("AES key must be exactly 16 bytes")

    padded_message = pad(message)
    plaintext_bytes = padded_message.encode("utf-8")
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted: bytes = cipher.encrypt(plaintext_bytes)
    return encrypted


def decrypt(encrypted_message: bytes, key: bytes) -> str:
    """
    Decrypt a message using AES-ECB mode and remove PKCS#7 padding.

    This function:
    1. Decrypts the message using AES-ECB mode
    2. Decodes the decrypted bytes from UTF-8
    3. Removes PKCS#7 padding

    Args:
        encrypted_message: Encrypted message bytes (must be multiple of 16 bytes)
        key: AES decryption key (must be exactly 16 bytes for AES-128)

    Returns:
        Decrypted plain text string

    Raises:
        ValueError: If key length is not 16 bytes or encrypted message length
                   is not a multiple of 16 bytes
        UnicodeDecodeError: If decrypted data is not valid UTF-8

    Examples:
        >>> key = b"0000000000000000"
        >>> encrypted = encrypt("Hello World", key)
        >>> decrypt(encrypted, key)
        'Hello World'
    """
    if len(key) != 16:
        raise ValueError("AES key must be exactly 16 bytes")

    if len(encrypted_message) % 16 != 0:
        raise ValueError("Encrypted message length must be multiple of 16 bytes")

    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(encrypted_message)
    decrypted_str = decrypted_bytes.decode("utf-8")
    return unpad(decrypted_str)


# For backward compatibility with existing lambda-based implementations,
# provide the same interface
__all__ = ["pad", "unpad", "encrypt", "decrypt"]
