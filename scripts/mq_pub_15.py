#!/usr/bin/env python3
# encoding: utf-8
"""MQTT Protocol 15 Message Publisher for Tuya IoT Devices.

This module publishes MQTT messages to Tuya IoT devices using protocol version 15.
It supports both protocol 2.1 (MD5 signature) and protocol 2.2 (CRC32 signature)
encryption schemes.

The publisher encrypts device commands using AES encryption with a device-specific
local key, then publishes the encrypted message to the device's MQTT topic. This
is typically used to trigger firmware upgrades during the tuya-convert flashing
process.

Protocol Differences:
    - Protocol 2.1: Uses MD5-based signature verification, base64 encoding
    - Protocol 2.2: Uses CRC32 checksums, timestamp-based encoding

Typical Usage:
    Basic device activation with default settings:
        $ ./mq_pub_15.py -i 43511212112233445566

    With custom local key and protocol version:
        $ ./mq_pub_15.py -i 43511212112233445566 -l a1b2c3d4e5f67788 -p 2.2

    Specify custom MQTT broker:
        $ ./mq_pub_15.py -i 43511212112233445566 -b 192.168.1.100

Example:
    >>> from mq_pub_15 import iot_enc, iot_dec
    >>> message = '{"data":{"gwId":"test123"},"protocol":15,"s":1523715,"t":1234567890}'
    >>> encrypted = iot_enc(message, "0000000000000000", "2.1")
    >>> decrypted = iot_dec(encrypted.decode(), "0000000000000000")

Note:
    This module is part of the tuya-convert project and is designed to work
    with the fake registration server to flash alternative firmware to Tuya
    devices.

Created by nano on 2018-11-22.
Copyright (c) 2018 VTRUST. All rights reserved.
"""
import base64
import binascii
import getopt
import sys
import time
from hashlib import md5
from typing import List, Optional

import paho.mqtt.publish as publish

help_message = """USAGE:
	"-i"/"--deviceID"
	"-l"/"--localKey" [default=0000000000000000]
	"-b"/"--broker" [default=127.0.0.1]
	"-p"/"--protocol" [default=2.1]
iot:	
%s -i 43511212112233445566 -l a1b2c3d4e5f67788""" % (
    sys.argv[0].split("/")[-1]
)

from crypto_utils import decrypt, encrypt

# Protocol constants
PROTOCOL_VERSION_21 = "2.1"
PROTOCOL_VERSION_22 = "2.2"
PROTOCOL_NUMBER = 15

# Default configuration
DEFAULT_BROKER = "127.0.0.1"
DEFAULT_LOCAL_KEY = "0000000000000000"
DEFAULT_PROTOCOL = PROTOCOL_VERSION_21

# Message format constants
MESSAGE_PREFIX_LENGTH = 19
SIGNATURE_START_OFFSET = 8
SIGNATURE_LENGTH = 16
TIMESTAMP_MODULO = 100000000
TIMESTAMP_MULTIPLIER = 100
CRC_BYTE_SIZE = 4

# Validation constants
MIN_KEY_LENGTH = 10
MIN_DEVICE_ID_LENGTH = 10

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR = 2

# Tuya IoT constants
TUYA_SEQUENCE_NUMBER = 1523715  # Appears to be a fixed sequence number for protocol 15


def iot_dec(message: str, local_key: str) -> str:
    """Decrypt IoT message from base64-encoded format.

    Decrypts a Tuya IoT protocol message by removing the protocol prefix,
    base64-decoding the payload, and decrypting using AES encryption with
    the device's local key.

    The message format is: <protocol_version><signature><base64_payload>
    This function strips the first 19 characters (prefix), then decodes and
    decrypts the remaining payload.

    Args:
        message: The encrypted message string including protocol prefix and
            base64-encoded ciphertext. Format: "2.1" + 16-char signature + base64 data
        local_key: The device's local encryption key (typically 16 characters).
            This key is unique to each device and used for AES decryption.

    Returns:
        The decrypted message as a UTF-8 string, typically JSON format containing
        device commands or status information.

    Example:
        >>> encrypted = "2.1abc123...base64data..."
        >>> key = "0000000000000000"
        >>> decrypted = iot_dec(encrypted, key)
        >>> print(decrypted)
        {"data":{"gwId":"test123"},"protocol":15}

    Note:
        This function prints the decrypted message to stdout as a side effect
        for debugging purposes during the tuya-convert flashing process.
    """
    message_clear = decrypt(base64.b64decode(message[MESSAGE_PREFIX_LENGTH:]), local_key.encode())
    print(message_clear)
    return message_clear


def iot_enc(message: str, local_key: str, protocol: str) -> bytes:
    """Encrypt IoT message with protocol-specific formatting.

    Encrypts a message using AES encryption and formats it according to either
    protocol 2.1 or 2.2 specifications. The two protocols use different signature
    and encoding schemes for backwards compatibility with different device firmware.

    Protocol 2.1 Format:
        <protocol_version> + <md5_signature> + <base64_encrypted_data>
        - Signature: MD5 hash of "data=<encrypted>||pv=<protocol>||<key>"
        - Uses middle 16 characters of MD5 hash (offset 8-24)
        - Data is base64-encoded after AES encryption

    Protocol 2.2 Format:
        <protocol_version> + <crc32_checksum> + <timestamp> + <encrypted_data>
        - CRC32: 4-byte big-endian checksum of timestamp + encrypted data
        - Timestamp: 8-digit timestamp (current time * 100 % 100000000)
        - Data is raw encrypted bytes (no base64 encoding)

    Args:
        message: The plaintext message to encrypt, typically JSON format with
            device commands. Example: '{"data":{"gwId":"123"},"protocol":15}'
        local_key: The device's local encryption key (typically 16 characters).
            Must match the key stored on the device.
        protocol: Protocol version string, either "2.1" or "2.2". Determines
            the signature scheme and encoding format.

    Returns:
        The encrypted and formatted message as bytes, ready to publish via MQTT.
        The exact format depends on the protocol version specified.

    Example:
        >>> message = '{"data":{"gwId":"test123"},"protocol":15,"s":1523715,"t":1234567890}'
        >>> key = "0000000000000000"
        >>> encrypted_21 = iot_enc(message, key, "2.1")
        >>> encrypted_22 = iot_enc(message, key, "2.2")
        >>> len(encrypted_21) != len(encrypted_22)  # Different formats
        True

    Note:
        This function prints the encrypted message to stdout as a side effect
        for debugging purposes during the tuya-convert flashing process.
    """
    messge_enc = encrypt(message, local_key.encode())
    if protocol == PROTOCOL_VERSION_21:
        messge_enc = base64.b64encode(messge_enc)
        signature = (
            b"data=" + messge_enc + b"||pv=" + protocol.encode() + b"||" + local_key.encode()
        )
        signature = md5(signature).hexdigest()[SIGNATURE_START_OFFSET : SIGNATURE_START_OFFSET + SIGNATURE_LENGTH].encode()
        messge_enc = protocol.encode() + signature + messge_enc
    else:
        timestamp = b"%08d" % ((int(time.time() * TIMESTAMP_MULTIPLIER) % TIMESTAMP_MODULO))
        messge_enc = timestamp + messge_enc
        crc = binascii.crc32(messge_enc).to_bytes(CRC_BYTE_SIZE, byteorder="big")
        messge_enc = protocol.encode() + crc + messge_enc
    print(messge_enc)
    return messge_enc


class Usage(Exception):
    """Exception raised for command-line usage errors.

    This exception is raised when invalid command-line arguments are provided
    or when required arguments are missing. It carries a help message that
    explains the correct usage of the script.

    Attributes:
        msg: A help message string explaining the correct usage and available
            command-line options.

    Example:
        >>> raise Usage("Invalid arguments provided")
        Traceback (most recent call last):
        ...
        Usage: Invalid arguments provided
    """

    def __init__(self, msg: str) -> None:
        """Initialize Usage exception with a help message.

        Args:
            msg: The help message to display to the user.
        """
        self.msg = msg


def main(argv: Optional[List[str]] = None) -> int:
    """Main entry point for MQTT protocol 15 publisher.

    Parses command-line arguments, constructs an encrypted protocol 15 message,
    and publishes it to the specified device's MQTT topic. This triggers the
    device to check for firmware upgrades during the tuya-convert flashing process.

    The message contains:
    - gwId: Gateway/device ID
    - protocol: Protocol number (always 15)
    - s: Sequence number (fixed at 1523715)
    - t: Current timestamp

    Command-line Options:
        -i, --deviceID: (Required) Device ID (gwId), minimum 10 characters
        -l, --localKey: Local encryption key (default: "0000000000000000")
        -b, --broker: MQTT broker address (default: "127.0.0.1")
        -p, --protocol: Protocol version, "2.1" or "2.2" (default: "2.1")
        -h, --help: Display help message

    Args:
        argv: Command-line arguments list. If None, uses sys.argv.
            Typically provided for testing purposes.

    Returns:
        Exit code integer. Returns 0 (EXIT_SUCCESS) on success,
        2 (EXIT_ERROR) on error.

    Raises:
        Usage: If invalid arguments are provided or required arguments are missing.

    Example:
        Command-line usage:
            $ ./mq_pub_15.py -i 43511212112233445566 -p 2.2

        Programmatic usage:
            >>> result = main(["-i", "43511212112233445566", "-l", "mykey123"])
            >>> result == 0
            True

    Note:
        The device ID and local key must be at least 10 characters long.
        The MQTT topic format is: smart/device/in/<deviceID>
    """
    broker = DEFAULT_BROKER
    localKey = DEFAULT_LOCAL_KEY
    deviceID = ""
    protocol = DEFAULT_PROTOCOL
    if argv is None:
        argv = sys.argv
    try:  # getopt
        try:
            opts, args = getopt.getopt(
                argv[1:], "hl:i:vb:p:", ["help", "localKey=", "deviceID=", "broker=", "protocol="]
            )
        except getopt.GetoptError as err:
            # Invalid command-line arguments
            print(f"Error: {err}", file=sys.stderr)
            raise Usage(help_message)

        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-l", "--localKey"):
                localKey = value
            if option in ("-i", "--deviceID"):
                deviceID = value
            if option in ("-b", "--broker"):
                broker = value
            if option in ("-p", "--protocol"):
                protocol = value

        if len(localKey) < MIN_KEY_LENGTH:
            raise Usage(help_message)
        if len(deviceID) < MIN_DEVICE_ID_LENGTH:
            raise Usage(help_message)
    except Usage:
        print(sys.argv[0].split("/")[-1] + ": ")
        print("\t for help use --help")
        print(help_message)
        return EXIT_ERROR

    if protocol == PROTOCOL_VERSION_21:
        message = '{"data":{"gwId":"%s"},"protocol":%d,"s":%d,"t":%d}' % (
            deviceID,
            PROTOCOL_NUMBER,
            TUYA_SEQUENCE_NUMBER,
            time.time(),
        )
    else:
        message = '{"data":{"gwId":"%s"},"protocol":%d,"s":"%d","t":"%d"}' % (
            deviceID,
            PROTOCOL_NUMBER,
            TUYA_SEQUENCE_NUMBER,
            time.time(),
        )
    print("encoding", message, "using protocol", protocol)
    m1 = iot_enc(message, localKey, protocol)

    publish.single("smart/device/in/%s" % (deviceID), m1, hostname=broker)
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
