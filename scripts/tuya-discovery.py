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

udpkey = md5(b"yGAdlopoPVldABfn").digest()
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
        data = data[20:-8]
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
            if "ablilty" in data:  # type: ignore[operator]
                print(
                    "WARNING: it appears this device does not use an ESP82xx and therefore cannot install ESP based firmware"
                )
        except:
            pass


def main() -> None:
    """Start UDP listeners for Tuya device discovery on ports 6666 and 6667."""
    loop = asyncio.get_event_loop()
    listener = loop.create_datagram_endpoint(TuyaDiscovery, local_addr=("0.0.0.0", 6666))
    encrypted_listener = loop.create_datagram_endpoint(TuyaDiscovery, local_addr=("0.0.0.0", 6667))
    loop.run_until_complete(listener)
    print("Listening for Tuya broadcast on UDP 6666")
    loop.run_until_complete(encrypted_listener)
    print("Listening for encrypted Tuya broadcast on UDP 6667")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()


if __name__ == "__main__":
    main()
