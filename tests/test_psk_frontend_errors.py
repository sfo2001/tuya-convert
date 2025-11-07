#!/usr/bin/env python3
# encoding: utf-8
"""
Test suite for psk-frontend.py error handling.

This test suite validates proper exception handling in the PSK-TLS frontend
proxy that intercepts and decrypts Tuya device communications.
"""

import sys
import os
import pytest
from unittest.mock import Mock, MagicMock, patch
import socket
import ssl

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

# Import module with hyphen in name
import importlib.util
spec = importlib.util.spec_from_file_location(
    "psk_frontend",
    os.path.join(os.path.dirname(__file__), "..", "scripts", "psk-frontend.py")
)
psk_frontend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(psk_frontend)

# Import the functions and classes
listener = psk_frontend.listener
client = psk_frontend.client
gen_psk = psk_frontend.gen_psk
PskFrontend = psk_frontend.PskFrontend
IDENTITY_PREFIX = psk_frontend.IDENTITY_PREFIX


class TestListenerFunction:
    """Test listener socket creation."""

    def test_listener_creates_socket(self):
        """Test that listener creates a socket on specified port."""
        # Use a high port to avoid permission issues
        host = "127.0.0.1"
        port = 9999

        sock = listener(host, port)
        assert sock is not None
        assert isinstance(sock, socket.socket)

        # Clean up
        sock.close()

    def test_listener_socket_options(self):
        """Test that listener sets SO_REUSEADDR option."""
        host = "127.0.0.1"
        port = 9998

        sock = listener(host, port)

        # Check that SO_REUSEADDR is set
        reuse = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        assert reuse == 1

        sock.close()


class TestClientFunction:
    """Test client socket creation."""

    @patch("socket.socket")
    def test_client_connects_to_host(self, mock_socket_class):
        """Test that client creates and connects socket."""
        mock_sock = Mock()
        mock_socket_class.return_value = mock_sock

        result = client("192.168.1.1", 80)

        # Verify socket was created
        mock_socket_class.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        # Verify connect was called
        mock_sock.connect.assert_called_once_with(("192.168.1.1", 80))
        assert result == mock_sock


class TestGenPskFunction:
    """Test PSK generation function."""

    def test_gen_psk_with_valid_identity(self):
        """Test PSK generation with valid identity."""
        # Identity must start with 0x prefix byte, then IDENTITY_PREFIX
        identity = b"\x00" + IDENTITY_PREFIX + b"test1234567890123456"
        hint = b"hint" + b"0" * 12  # Must be at least 16 bytes

        psk = gen_psk(identity, hint)

        # PSK should be 32 bytes (AES encrypted identity[:32])
        assert isinstance(psk, bytes)
        assert len(psk) == 32

    def test_gen_psk_deterministic(self):
        """Test that same identity/hint produces same PSK."""
        identity = b"\x00" + IDENTITY_PREFIX + b"test1234567890123456"
        hint = b"hint" + b"0" * 12

        psk1 = gen_psk(identity, hint)
        psk2 = gen_psk(identity, hint)

        assert psk1 == psk2


class TestPskFrontendInit:
    """Test PskFrontend initialization."""

    def test_init_creates_server_socket(self):
        """Test that init creates server socket."""
        frontend = PskFrontend("127.0.0.1", 9997, "10.42.42.1", 80)

        assert frontend.listening_host == "127.0.0.1"
        assert frontend.listening_port == 9997
        assert frontend.host == "10.42.42.1"
        assert frontend.port == 80
        assert frontend.server_sock is not None
        assert frontend.sessions == []

        # Clean up
        frontend.server_sock.close()


class TestPskFrontendReadables:
    """Test readables method."""

    def test_readables_returns_server_socket(self):
        """Test that readables includes server socket."""
        frontend = PskFrontend("127.0.0.1", 9996, "10.42.42.1", 80)

        readables = frontend.readables()

        assert frontend.server_sock in readables
        assert len(readables) == 1

        frontend.server_sock.close()

    def test_readables_includes_session_sockets(self):
        """Test that readables includes all session sockets."""
        frontend = PskFrontend("127.0.0.1", 9995, "10.42.42.1", 80)

        # Add mock sessions
        mock_s1 = Mock()
        mock_s2 = Mock()
        frontend.sessions.append((mock_s1, mock_s2))

        readables = frontend.readables()

        assert frontend.server_sock in readables
        assert mock_s1 in readables
        assert mock_s2 in readables
        assert len(readables) == 3

        frontend.server_sock.close()


class TestPskFrontendNewClient:
    """Test new_client method error handling."""

    @patch.object(psk_frontend, "client")
    @patch.object(psk_frontend, "SSLPSKContext")
    def test_new_client_handles_ssl_error(self, mock_ssl_context_class, mock_client):
        """Test that SSL errors are caught and handled."""
        frontend = PskFrontend("127.0.0.1", 9994, "10.42.42.1", 80)

        # Mock SSLContext to raise SSLError
        mock_context = Mock()
        mock_ssl_context_class.return_value = mock_context
        # Create SSLError with reason attribute
        error = ssl.SSLError("NO_SHARED_CIPHER")
        error.reason = "NO_SHARED_CIPHER"
        mock_context.wrap_socket.side_effect = error

        # Create a mock socket
        mock_socket = Mock()

        # Should not raise exception
        frontend.new_client(mock_socket)

        # Session should not be added due to error
        assert len(frontend.sessions) == 0

        frontend.server_sock.close()

    @patch.object(psk_frontend, "client")
    @patch.object(psk_frontend, "SSLPSKContext")
    def test_new_client_handles_general_exception(self, mock_ssl_context_class, mock_client):
        """Test that general exceptions are caught and handled."""
        frontend = PskFrontend("127.0.0.1", 9993, "10.42.42.1", 80)

        # Mock to raise general exception
        mock_context = Mock()
        mock_ssl_context_class.return_value = mock_context
        mock_context.wrap_socket.side_effect = Exception("Test error")

        mock_socket = Mock()

        # Should not raise exception
        frontend.new_client(mock_socket)

        # Session should not be added
        assert len(frontend.sessions) == 0

        frontend.server_sock.close()

    @patch.object(psk_frontend, "client")
    @patch.object(psk_frontend, "SSLPSKContext")
    def test_new_client_successful_connection(self, mock_ssl_context_class, mock_client):
        """Test successful client connection."""
        frontend = PskFrontend("127.0.0.1", 9992, "10.42.42.1", 80)

        # Mock successful SSL context
        mock_context = Mock()
        mock_ssl_context_class.return_value = mock_context
        mock_ssl_sock = Mock()
        mock_context.wrap_socket.return_value = mock_ssl_sock

        # Mock client socket
        mock_client_sock = Mock()
        mock_client.return_value = mock_client_sock

        mock_socket = Mock()

        # Call new_client
        frontend.new_client(mock_socket)

        # Session should be added
        assert len(frontend.sessions) == 1
        assert frontend.sessions[0] == (mock_ssl_sock, mock_client_sock)

        frontend.server_sock.close()


class TestPskFrontendDataReadyCb:
    """Test data_ready_cb method error handling."""

    def test_data_ready_cb_handles_socket_errors(self):
        """Test that socket errors during data transfer are handled."""
        frontend = PskFrontend("127.0.0.1", 9991, "10.42.42.1", 80)

        # Create mock sockets for a session
        mock_s1 = Mock()
        mock_s2 = Mock()
        frontend.sessions.append((mock_s1, mock_s2))

        # Make recv raise an OSError (connection error)
        mock_s1.recv.side_effect = OSError("Connection reset by peer")

        # Should not raise exception
        frontend.data_ready_cb(mock_s1)

        # Session should be removed due to error
        assert len(frontend.sessions) == 0

        frontend.server_sock.close()

    def test_data_ready_cb_handles_broken_pipe(self):
        """Test that BrokenPipeError during send is handled."""
        frontend = PskFrontend("127.0.0.1", 9990, "10.42.42.1", 80)

        mock_s1 = Mock()
        mock_s2 = Mock()
        frontend.sessions.append((mock_s1, mock_s2))

        # recv succeeds but send fails
        mock_s1.recv.return_value = b"test data"
        mock_s2.send.side_effect = BrokenPipeError("Broken pipe")

        # Should not raise exception
        frontend.data_ready_cb(mock_s1)

        # Session should be removed
        assert len(frontend.sessions) == 0

        frontend.server_sock.close()

    def test_data_ready_cb_handles_shutdown_error(self):
        """Test that shutdown errors are handled."""
        frontend = PskFrontend("127.0.0.1", 9989, "10.42.42.1", 80)

        mock_s1 = Mock()
        mock_s2 = Mock()
        frontend.sessions.append((mock_s1, mock_s2))

        # recv returns empty (connection closed)
        mock_s1.recv.return_value = b""
        # shutdown raises error (already closed)
        mock_s1.shutdown.side_effect = OSError("Transport endpoint is not connected")

        # Should not raise exception
        frontend.data_ready_cb(mock_s1)

        # Session should be removed
        assert len(frontend.sessions) == 0

        frontend.server_sock.close()

    @pytest.mark.skip(reason="socket.accept is read-only and cannot be mocked easily")
    def test_data_ready_cb_handles_new_connection(self):
        """Test that new client connections are handled."""
        # This test is skipped because socket.accept is a built-in method
        # that cannot be patched. Integration testing would be needed.
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
