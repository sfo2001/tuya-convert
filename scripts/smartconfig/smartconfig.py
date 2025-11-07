#!/usr/bin/env python3
# encoding: utf-8
"""
smartconfig.py
Created by kueblc on 2019-01-25.
Configure Tuya devices via smartconfig without the Tuya cloud or app
broadcast strategy ported from https://github.com/tuyapi/link
multicast strategy reverse engineered by kueblc
"""

from socket import AF_INET, IPPROTO_IP, IPPROTO_UDP, SO_BROADCAST, SO_REUSEADDR
from socket import IP_MULTICAST_TTL, SOCK_DGRAM, SOL_SOCKET, socket
from time import sleep
from typing import List

try:
    from .broadcast import broadcast_head, encode_broadcast_body
    from .constants import (
        BODY_REPEAT_COUNT,
        BROADCAST_PORT,
        DEFAULT_BIND_ADDRESS,
        DEFAULT_PACKET_GAP_SECONDS,
        HEADER_REPEAT_COUNT,
        MULTICAST_PORT,
        MULTICAST_TTL,
    )
    from .multicast import encode_multicast_body, multicast_head
except ImportError:
    from broadcast import broadcast_head, encode_broadcast_body  # type: ignore[import-not-found]
    from constants import (  # type: ignore[import-not-found]
        BODY_REPEAT_COUNT,
        BROADCAST_PORT,
        DEFAULT_BIND_ADDRESS,
        DEFAULT_PACKET_GAP_SECONDS,
        HEADER_REPEAT_COUNT,
        MULTICAST_PORT,
        MULTICAST_TTL,
    )
    from multicast import encode_multicast_body, multicast_head  # type: ignore[import-not-found]


class SmartConfigSocket(object):
    """
    UDP socket for sending smartconfig packets.

    Configured for both broadcast and multicast transmission with appropriate
    socket options for local network smartconfig protocol.
    """

    def __init__(
        self, address: str = DEFAULT_BIND_ADDRESS, gap: float = DEFAULT_PACKET_GAP_SECONDS
    ):
        """
        Initialize smartconfig socket.

        Args:
            address: Local IP address to bind to (typically AP gateway)
            gap: Time in seconds to sleep between packets (default 0.005s / 5ms)
        """
        self._socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self._socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self._socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self._socket.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, MULTICAST_TTL)
        self._socket.bind((address, 0))
        self._gap: float = gap

    def send_broadcast(self, data: List[int]) -> None:
        """
        Send broadcast packets with specified lengths.

        Each integer in data represents the length of a UDP packet to send.
        The actual payload is null bytes of that length.

        Args:
            data: List of packet lengths to send
        """
        for length in data:
            self._socket.sendto(b"\0" * length, ("255.255.255.255", BROADCAST_PORT))
            sleep(self._gap)

    def send_multicast(self, data: List[str]) -> None:
        """
        Send multicast packets to specified IP addresses.

        Sends a single null byte to each IP address on the multicast port.

        Args:
            data: List of multicast IP addresses (226.x.y.z format)
        """
        for ip in data:
            self._socket.sendto(b"\0", (ip, MULTICAST_PORT))
            sleep(self._gap)


def smartconfig(password: str, ssid: str, region: str, token: str, secret: str) -> None:
    """
    Send smartconfig packets to configure Tuya device with WiFi credentials.

    Combines region, token, and secret into a token group, then sends both
    broadcast and multicast encoded packets repeatedly to ensure device receives
    the configuration.

    Args:
        password: WiFi password
        ssid: WiFi SSID
        region: Region code (e.g., "US", "EU", "CN")
        token: 8-character token string
        secret: 4-character secret string

    Returns:
        None - prints progress dots to stdout
    """
    sock: SmartConfigSocket = SmartConfigSocket()
    token_group: str = region + token + secret

    # Encode configuration data
    broadcast_body: List[int] = encode_broadcast_body(password, ssid, token_group)
    multicast_body: List[str] = encode_multicast_body(password, ssid, token_group)

    # Send header repeatedly to signal start of configuration
    for i in range(HEADER_REPEAT_COUNT):  # 40 times
        sock.send_multicast(multicast_head)
        sock.send_broadcast(broadcast_head)

    # Send complete body repeatedly for reliability
    for i in range(BODY_REPEAT_COUNT):  # 10 times
        print(".", end="", flush=True)  # Progress indicator
        sock.send_multicast(multicast_head)
        sock.send_multicast(multicast_body)
        sock.send_broadcast(broadcast_body)
