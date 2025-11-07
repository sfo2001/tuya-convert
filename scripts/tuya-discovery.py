#!/usr/bin/env python3
# encoding: utf-8
"""
tuya-discovery.py
Created by kueblc on 2019-11-13.
Discover Tuya devices on the LAN via UDP broadcast
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
    """AsyncIO protocol for discovering Tuya devices via UDP broadcasts."""

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        """Handle received UDP datagram from Tuya device."""
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
    """Start UDP listeners for Tuya device discovery on ports 6666 and 6667."""
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
