#!/usr/bin/env python3
# encoding: utf-8
"""Tuya IoT Device Discovery via UDP Broadcast Protocol.

This module listens for and decodes UDP broadcast messages from Tuya IoT devices
on the local network. Devices broadcast their presence, capabilities, and status
information when they boot up, connect to Wi-Fi, or periodically as heartbeats.

How Tuya Discovery Works:
    1. Tuya devices broadcast UDP packets on ports 6666 (unencrypted) and 6667 (encrypted)
    2. Broadcasts contain JSON payloads with device info: gwId, IP, version, capabilities
    3. Encrypted broadcasts use MD5-derived key from magic string "yGAdlopoPVldABfn"
    4. Messages have 20-byte header and 8-byte footer that must be stripped

UDP Broadcast Format:
    [20-byte header][encrypted/plain JSON payload][8-byte footer]

Decryption Process:
    1. Strip 20-byte header and 8-byte footer from packet
    2. Derive key: MD5("yGAdlopoPVldABfn")
    3. Decrypt payload using AES with derived key
    4. Parse resulting JSON

Device Detection:
    - ESP82xx devices: Broadcast contains "ability" (correct spelling)
    - Non-ESP devices: Broadcast contains "ablilty" (typo in SDK)
    - The typo is used to warn users about incompatible (non-ESP) devices

Typical JSON Payload:
    {
        "ip": "192.168.1.100",
        "gwId": "43511212112233445566",
        "active": 2,
        "ablilty": 0,        # Typo indicates non-ESP device
        "encrypt": true,
        "productKey": "keycb42ktnmcxxxx",
        "version": "3.3"
    }

Typical Usage:
    Run as a standalone discovery tool:
        $ ./tuya-discovery.py
        Listening for Tuya broadcast on UDP 6666
        Listening for encrypted Tuya broadcast on UDP 6667
        192.168.1.100 {"ip":"192.168.1.100","gwId":"43511212..."}

    Use in another script:
        >>> import asyncio
        >>> from tuya_discovery import TuyaDiscovery
        >>> loop = asyncio.get_event_loop()
        >>> listener = loop.create_datagram_endpoint(
        ...     TuyaDiscovery, local_addr=("0.0.0.0", 6666)
        ... )
        >>> loop.run_until_complete(listener)

Example Output:
    $ ./tuya-discovery.py
    Listening for Tuya broadcast on UDP 6666
    Listening for encrypted Tuya broadcast on UDP 6667
    192.168.1.100 {"ip":"192.168.1.100","gwId":"eb12345678...","active":2}
    WARNING: it appears this device does not use an ESP82xx...

Use Cases:
    - Enumerate Tuya devices on network before flashing
    - Verify device is broadcasting after smartconfig
    - Identify non-ESP devices that can't be flashed
    - Monitor device heartbeats during tuya-convert process

Created by kueblc on 2019-11-13.
Part of the tuya-convert project.
"""

import asyncio
import json
from hashlib import md5
from typing import Tuple

from crypto_utils import decrypt

# Network constants
UDP_BROADCAST_PORT = 6666  # Unencrypted Tuya device broadcasts
UDP_ENCRYPTED_PORT = 6667  # Encrypted Tuya device broadcasts
BIND_ALL_INTERFACES = "0.0.0.0"

# Protocol constants
UDP_KEY_MAGIC = b"yGAdlopoPVldABfn"  # Magic string for deriving UDP decryption key
MESSAGE_FRAME_HEADER_SIZE = 20  # Bytes to skip at start of message
MESSAGE_FRAME_FOOTER_SIZE = 8  # Bytes to skip at end of message

# Tuya SDK typo indicators
TUYA_ESP_ABILITY_KEY = "ability"  # Correct spelling in ESP SDK
TUYA_NON_ESP_ABILITY_KEY = "ablilty"  # Typo in non-ESP SDK (used to detect non-ESP devices)

# Derived constants
udpkey = md5(UDP_KEY_MAGIC).digest()
decrypt_udp = lambda msg: decrypt(msg, udpkey)

devices_seen = set()


class TuyaDiscovery(asyncio.DatagramProtocol):
    """AsyncIO DatagramProtocol for discovering Tuya devices via UDP broadcasts.

    Implements the asyncio DatagramProtocol interface to process incoming UDP
    packets from Tuya devices. Each packet is decoded, decrypted (if encrypted),
    parsed as JSON, and analyzed to determine device type.

    The protocol maintains a global set of seen device broadcasts to avoid
    processing duplicates, as devices broadcast periodically.

    Protocol Flow:
        1. Receive UDP datagram
        2. Check if already seen (deduplicate)
        3. Strip 20-byte header and 8-byte footer
        4. Attempt decryption (fall back to plaintext if fails)
        5. Parse JSON payload
        6. Check for ESP/non-ESP indicator
        7. Print device info and warnings

    Thread Safety:
        This class is designed to run in an asyncio event loop. All methods
        are called from the event loop thread.

    Example:
        >>> import asyncio
        >>> loop = asyncio.get_event_loop()
        >>> listener = loop.create_datagram_endpoint(
        ...     TuyaDiscovery, local_addr=("0.0.0.0", 6666)
        ... )
        >>> transport, protocol = loop.run_until_complete(listener)
        >>> # Protocol will now receive datagrams via datagram_received()
    """

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        """Handle received UDP datagram from Tuya device.

        Processes incoming broadcast packets by:
        1. Deduplicating based on raw packet data
        2. Stripping protocol framing (header/footer)
        3. Decrypting encrypted payloads
        4. Parsing JSON device information
        5. Detecting non-ESP devices via SDK typo

        Args:
            data: Raw UDP datagram bytes including header/footer framing.
                Format: [20-byte header][payload][8-byte footer]
            addr: Tuple of (ip_address, port) from which datagram was sent.

        Side Effects:
            - Adds raw datagram to global devices_seen set for deduplication
            - Prints device IP and JSON payload to stdout
            - Prints warning if non-ESP device detected

        Device Type Detection:
            - "ablilty" in JSON → Non-ESP device (can't flash ESP firmware)
            - "ability" in JSON → ESP82xx device (compatible with tuya-convert)

        Example:
            >>> # Called automatically by asyncio when UDP packet arrives
            >>> # protocol.datagram_received(packet_data, ("192.168.1.100", 12345))
            192.168.1.100 {"ip":"192.168.1.100","gwId":"eb12345...","active":2}

        Note:
            - Silently ignores duplicate packets (same raw data)
            - Uses bare except to gracefully handle decryption/parsing failures
            - Prints to stdout for real-time monitoring during device setup
        """
        # ignore devices we've already seen
        if data in devices_seen:
            return
        devices_seen.add(data)
        # remove message frame
        data = data[MESSAGE_FRAME_HEADER_SIZE:-MESSAGE_FRAME_FOOTER_SIZE]
        # decrypt if encrypted
        try:
            data = decrypt_udp(data)  # type: ignore[assignment]
        except:
            data = data.decode()  # type: ignore[assignment]
        print(addr[0], data)
        # parse json
        try:
            data = json.loads(data)
            # there is a typo present only in Tuya SDKs for non-ESP devices ("ablilty")
            # it is spelled correctly in the Tuya SDK for the ESP ("ability")
            # we can use this as a clue to report unsupported devices
            if TUYA_NON_ESP_ABILITY_KEY in data:  # type: ignore[operator]
                print(
                    "WARNING: it appears this device does not use an ESP82xx and therefore cannot install ESP based firmware"
                )
        except:
            pass


def main() -> None:
    """Start UDP listeners for Tuya device discovery on ports 6666 and 6667.

    Creates two asyncio UDP listeners to monitor Tuya device broadcasts:
    1. Port 6666: Unencrypted device broadcasts (older devices, initial setup)
    2. Port 6667: Encrypted device broadcasts (newer devices, post-activation)

    The listeners run concurrently in an asyncio event loop, processing packets
    as they arrive. Each packet is deduplicated, decrypted (if needed), and
    displayed with device information.

    Ports:
        6666: Plain JSON broadcasts from devices
        6667: AES-encrypted broadcasts (most common)

    Event Loop:
        The function sets up listeners and runs the event loop indefinitely
        until interrupted with Ctrl+C (KeyboardInterrupt).

    Usage:
        Run as standalone script:
            $ ./tuya-discovery.py
            Listening for Tuya broadcast on UDP 6666
            Listening for encrypted Tuya broadcast on UDP 6667
            192.168.1.100 {"ip":"192.168.1.100"...}
            ^C

        The script will print device information as broadcasts are received.
        Press Ctrl+C to stop.

    Side Effects:
        - Binds to UDP ports 6666 and 6667 on all interfaces (0.0.0.0)
        - Runs infinite event loop until KeyboardInterrupt
        - Prints listener status and device info to stdout

    Example Output:
        Listening for Tuya broadcast on UDP 6666
        Listening for encrypted Tuya broadcast on UDP 6667
        192.168.1.100 {"ip":"192.168.1.100","gwId":"eb12...","active":2}
        192.168.1.101 {"ip":"192.168.1.101","gwId":"ab34...","active":1}
        WARNING: it appears this device does not use an ESP82xx...

    Note:
        - Requires no special privileges (ports >1024)
        - Listens on all network interfaces
        - Safe to run alongside other tuya-convert components
        - Gracefully handles Ctrl+C shutdown
    """
    loop = asyncio.get_event_loop()
    listener = loop.create_datagram_endpoint(TuyaDiscovery, local_addr=(BIND_ALL_INTERFACES, UDP_BROADCAST_PORT))
    encrypted_listener = loop.create_datagram_endpoint(TuyaDiscovery, local_addr=(BIND_ALL_INTERFACES, UDP_ENCRYPTED_PORT))
    loop.run_until_complete(listener)
    print(f"Listening for Tuya broadcast on UDP {UDP_BROADCAST_PORT}")
    loop.run_until_complete(encrypted_listener)
    print(f"Listening for encrypted Tuya broadcast on UDP {UDP_ENCRYPTED_PORT}")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()


if __name__ == "__main__":
    main()
