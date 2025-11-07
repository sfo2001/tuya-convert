#!/usr/bin/env python3
# encoding: utf-8
"""
Test suite for smartconfig socket operations.

This test suite validates the SmartConfigSocket class and smartconfig()
function to ensure proper socket configuration and packet transmission.
"""

import os
import sys
from unittest.mock import MagicMock, Mock, call, patch

import pytest

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "scripts", "smartconfig")
)

# Import smartconfig modules
from smartconfig import GAP, MULTICAST_TTL, SmartConfigSocket, smartconfig


class TestSmartConfigSocketInitialization:
    """Test SmartConfigSocket initialization and configuration."""

    @patch("smartconfig.socket")
    def test_socket_creation(self, mock_socket_func):
        """Test that socket is created with correct parameters."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        # Create SmartConfigSocket
        from socket import AF_INET, IPPROTO_UDP, SOCK_DGRAM

        scs = SmartConfigSocket()

        # Verify socket was created with correct parameters
        mock_socket_func.assert_called_once_with(AF_INET, SOCK_DGRAM, IPPROTO_UDP)

    @patch("smartconfig.socket")
    def test_socket_options(self, mock_socket_func):
        """Test that socket options are configured correctly."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        # Create SmartConfigSocket
        scs = SmartConfigSocket()

        # Verify socket options were set
        from socket import (
            IPPROTO_IP,
            IP_MULTICAST_TTL,
            SOL_SOCKET,
            SO_BROADCAST,
            SO_REUSEADDR,
        )

        calls = mock_sock.setsockopt.call_args_list
        assert len(calls) == 3

        # Check SO_REUSEADDR
        assert call(SOL_SOCKET, SO_REUSEADDR, 1) in calls
        # Check SO_BROADCAST
        assert call(SOL_SOCKET, SO_BROADCAST, 1) in calls
        # Check IP_MULTICAST_TTL
        assert call(IPPROTO_IP, IP_MULTICAST_TTL, MULTICAST_TTL) in calls

    @patch("smartconfig.socket")
    def test_socket_bind_default_address(self, mock_socket_func):
        """Test that socket binds to default address."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        # Create SmartConfigSocket with default address
        scs = SmartConfigSocket()

        # Verify socket was bound to default address
        mock_sock.bind.assert_called_once_with(("10.42.42.1", 0))

    @patch("smartconfig.socket")
    def test_socket_bind_custom_address(self, mock_socket_func):
        """Test that socket binds to custom address."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        # Create SmartConfigSocket with custom address
        custom_address = "192.168.1.100"
        scs = SmartConfigSocket(address=custom_address)

        # Verify socket was bound to custom address
        mock_sock.bind.assert_called_once_with((custom_address, 0))

    @patch("smartconfig.socket")
    def test_gap_default(self, mock_socket_func):
        """Test that default gap is set correctly."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        # Create SmartConfigSocket
        scs = SmartConfigSocket()

        # Verify gap is set to default
        assert scs._gap == GAP

    @patch("smartconfig.socket")
    def test_gap_custom(self, mock_socket_func):
        """Test that custom gap is set correctly."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        # Create SmartConfigSocket with custom gap
        custom_gap = 0.01
        scs = SmartConfigSocket(gap=custom_gap)

        # Verify gap is set to custom value
        assert scs._gap == custom_gap


class TestSmartConfigSocketSendBroadcast:
    """Test SmartConfigSocket send_broadcast method."""

    @patch("smartconfig.sleep")
    @patch("smartconfig.socket")
    def test_send_broadcast_basic(self, mock_socket_func, mock_sleep):
        """Test basic send_broadcast functionality."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        scs = SmartConfigSocket()

        # Send broadcast with simple data
        data = [1, 3, 6, 10]
        scs.send_broadcast(data)

        # Verify sendto was called for each data value
        assert mock_sock.sendto.call_count == 4

        # Verify sleep was called between packets
        assert mock_sleep.call_count == 4

    @patch("smartconfig.sleep")
    @patch("smartconfig.socket")
    def test_send_broadcast_packet_format(self, mock_socket_func, mock_sleep):
        """Test that broadcast packets have correct format."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        scs = SmartConfigSocket()

        # Send broadcast
        data = [100, 200]
        scs.send_broadcast(data)

        # Verify packet format: null bytes of specified length to broadcast address
        calls = mock_sock.sendto.call_args_list

        # First packet: 100 null bytes to 255.255.255.255:30011
        assert calls[0] == call(b"\0" * 100, ("255.255.255.255", 30011))
        # Second packet: 200 null bytes
        assert calls[1] == call(b"\0" * 200, ("255.255.255.255", 30011))

    @patch("smartconfig.sleep")
    @patch("smartconfig.socket")
    def test_send_broadcast_gap_timing(self, mock_socket_func, mock_sleep):
        """Test that gap timing is respected."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        custom_gap = 0.01
        scs = SmartConfigSocket(gap=custom_gap)

        # Send broadcast
        data = [1, 2, 3]
        scs.send_broadcast(data)

        # Verify sleep was called with correct gap
        for call_args in mock_sleep.call_args_list:
            assert call_args == call(custom_gap)

    @patch("smartconfig.sleep")
    @patch("smartconfig.socket")
    def test_send_broadcast_empty_data(self, mock_socket_func, mock_sleep):
        """Test send_broadcast with empty data."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        scs = SmartConfigSocket()

        # Send empty broadcast
        data = []
        scs.send_broadcast(data)

        # Verify no packets sent
        mock_sock.sendto.assert_not_called()
        mock_sleep.assert_not_called()


class TestSmartConfigSocketSendMulticast:
    """Test SmartConfigSocket send_multicast method."""

    @patch("smartconfig.sleep")
    @patch("smartconfig.socket")
    def test_send_multicast_basic(self, mock_socket_func, mock_sleep):
        """Test basic send_multicast functionality."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        scs = SmartConfigSocket()

        # Send multicast with IP addresses
        data = ["226.0.1.2", "226.1.3.4"]
        scs.send_multicast(data)

        # Verify sendto was called for each IP
        assert mock_sock.sendto.call_count == 2

        # Verify sleep was called between packets
        assert mock_sleep.call_count == 2

    @patch("smartconfig.sleep")
    @patch("smartconfig.socket")
    def test_send_multicast_packet_format(self, mock_socket_func, mock_sleep):
        """Test that multicast packets have correct format."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        scs = SmartConfigSocket()

        # Send multicast
        data = ["226.10.20.30", "226.40.50.60"]
        scs.send_multicast(data)

        # Verify packet format: single null byte to each IP:30012
        calls = mock_sock.sendto.call_args_list

        assert calls[0] == call(b"\0", ("226.10.20.30", 30012))
        assert calls[1] == call(b"\0", ("226.40.50.60", 30012))

    @patch("smartconfig.sleep")
    @patch("smartconfig.socket")
    def test_send_multicast_gap_timing(self, mock_socket_func, mock_sleep):
        """Test that gap timing is respected."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        custom_gap = 0.02
        scs = SmartConfigSocket(gap=custom_gap)

        # Send multicast
        data = ["226.0.1.2"]
        scs.send_multicast(data)

        # Verify sleep was called with correct gap
        mock_sleep.assert_called_once_with(custom_gap)

    @patch("smartconfig.sleep")
    @patch("smartconfig.socket")
    def test_send_multicast_empty_data(self, mock_socket_func, mock_sleep):
        """Test send_multicast with empty data."""
        mock_sock = MagicMock()
        mock_socket_func.return_value = mock_sock

        scs = SmartConfigSocket()

        # Send empty multicast
        data = []
        scs.send_multicast(data)

        # Verify no packets sent
        mock_sock.sendto.assert_not_called()
        mock_sleep.assert_not_called()


class TestSmartconfigFunction:
    """Test the smartconfig() orchestration function."""

    @patch("smartconfig.SmartConfigSocket")
    @patch("smartconfig.encode_multicast_body")
    @patch("smartconfig.encode_broadcast_body")
    def test_smartconfig_creates_socket(
        self, mock_encode_broadcast, mock_encode_multicast, mock_socket_class
    ):
        """Test that smartconfig creates a SmartConfigSocket."""
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance
        mock_encode_broadcast.return_value = [1, 2, 3]
        mock_encode_multicast.return_value = ["226.0.1.2"]

        # Call smartconfig
        smartconfig("password", "ssid", "US", "token", "secret")

        # Verify socket was created
        mock_socket_class.assert_called_once()

    @patch("smartconfig.SmartConfigSocket")
    @patch("smartconfig.encode_multicast_body")
    @patch("smartconfig.encode_broadcast_body")
    def test_smartconfig_token_group_formation(
        self, mock_encode_broadcast, mock_encode_multicast, mock_socket_class
    ):
        """Test that token_group is formed correctly."""
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance
        mock_encode_broadcast.return_value = [1, 2, 3]
        mock_encode_multicast.return_value = ["226.0.1.2"]

        region = "US"
        token = "00000000"
        secret = "0101"

        # Call smartconfig
        smartconfig("password", "ssid", region, token, secret)

        # Verify token_group is formed correctly
        expected_token_group = region + token + secret  # "US000000000101"

        # Check that encode functions were called with correct token_group
        mock_encode_broadcast.assert_called_once_with(
            "password", "ssid", expected_token_group
        )
        mock_encode_multicast.assert_called_once_with(
            "password", "ssid", expected_token_group
        )

    @patch("smartconfig.SmartConfigSocket")
    @patch("smartconfig.encode_multicast_body")
    @patch("smartconfig.encode_broadcast_body")
    @patch("smartconfig.broadcast_head", [1, 3, 6, 10])
    @patch("smartconfig.multicast_head", ["226.120.89.84", "226.121.84.83", "226.122.49.48"])
    def test_smartconfig_header_transmission(
        self, mock_encode_broadcast, mock_encode_multicast, mock_socket_class
    ):
        """Test that headers are transmitted at least 40 times."""
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance
        mock_encode_broadcast.return_value = [100, 200]
        mock_encode_multicast.return_value = ["226.0.1.2"]

        # Call smartconfig
        smartconfig("password", "ssid", "US", "token", "secret")

        # Count multicast_head and broadcast_head calls
        # Headers should be sent 40 times initially, plus 10 more during body transmission
        multicast_calls = [
            c
            for c in mock_sock_instance.send_multicast.call_args_list
            if c == call(["226.120.89.84", "226.121.84.83", "226.122.49.48"])
        ]

        broadcast_calls = [
            c
            for c in mock_sock_instance.send_broadcast.call_args_list
            if c == call([1, 3, 6, 10])
        ]

        # Headers sent 40 times in header loop, then multicast_head sent 10 more times in body loop
        assert len(multicast_calls) == 50  # 40 (header loop) + 10 (body loop)
        assert len(broadcast_calls) == 40  # Only in header loop

    @patch("smartconfig.SmartConfigSocket")
    @patch("smartconfig.encode_multicast_body")
    @patch("smartconfig.encode_broadcast_body")
    @patch("smartconfig.broadcast_head", [1, 3, 6, 10])
    @patch("smartconfig.multicast_head", ["226.120.89.84"])
    def test_smartconfig_body_transmission(
        self, mock_encode_broadcast, mock_encode_multicast, mock_socket_class
    ):
        """Test that bodies are transmitted 10 times."""
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance

        broadcast_body = [100, 200, 300]
        multicast_body = ["226.0.1.2", "226.1.2.3"]

        mock_encode_broadcast.return_value = broadcast_body
        mock_encode_multicast.return_value = multicast_body

        # Call smartconfig
        smartconfig("password", "ssid", "US", "token", "secret")

        # Count body calls (should be 10 times)
        multicast_body_calls = [
            c
            for c in mock_sock_instance.send_multicast.call_args_list
            if c == call(multicast_body)
        ]

        broadcast_body_calls = [
            c
            for c in mock_sock_instance.send_broadcast.call_args_list
            if c == call(broadcast_body)
        ]

        assert len(multicast_body_calls) == 10
        assert len(broadcast_body_calls) == 10

    @patch("smartconfig.SmartConfigSocket")
    @patch("smartconfig.encode_multicast_body")
    @patch("smartconfig.encode_broadcast_body")
    def test_smartconfig_with_production_values(
        self, mock_encode_broadcast, mock_encode_multicast, mock_socket_class
    ):
        """Test smartconfig with production values from main.py."""
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance
        mock_encode_broadcast.return_value = [1, 2, 3]
        mock_encode_multicast.return_value = ["226.0.1.2"]

        # Production values from main.py
        ssid = "vtrust-flash"
        passwd = ""
        region = "US"
        token = "00000000"
        secret = "0101"

        # Call smartconfig
        smartconfig(passwd, ssid, region, token, secret)

        # Verify encode functions were called with correct values
        mock_encode_broadcast.assert_called_once_with(passwd, ssid, "US000000000101")
        mock_encode_multicast.assert_called_once_with(passwd, ssid, "US000000000101")

    @patch("smartconfig.SmartConfigSocket")
    @patch("smartconfig.encode_multicast_body")
    @patch("smartconfig.encode_broadcast_body")
    @patch("smartconfig.multicast_head", ["226.0.1.2"])
    def test_smartconfig_progress_output(
        self, mock_encode_broadcast, mock_encode_multicast, mock_socket_class
    ):
        """Test that smartconfig prints progress dots."""
        mock_sock_instance = MagicMock()
        mock_socket_class.return_value = mock_sock_instance
        mock_encode_broadcast.return_value = [1]
        mock_encode_multicast.return_value = ["226.0.1.2"]

        # Capture stdout
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            smartconfig("password", "ssid", "US", "token", "secret")

        output = f.getvalue()

        # Should print 10 dots (one per body iteration)
        assert output.count(".") == 10


class TestSmartconfigConstants:
    """Test smartconfig module constants."""

    def test_gap_value(self):
        """Test that GAP constant is set correctly."""
        assert GAP == 5 / 1000.0
        assert GAP == 0.005

    def test_multicast_ttl_value(self):
        """Test that MULTICAST_TTL constant is set correctly."""
        assert MULTICAST_TTL == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
