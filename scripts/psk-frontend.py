#!/usr/bin/env python3
"""TLS-PSK (Pre-Shared Key) Frontend Proxy for Tuya Device Flashing.

This module implements a TLS-PSK frontend proxy that intercepts encrypted
connections from Tuya IoT devices during the flashing process. It acts as a
man-in-the-middle, decrypting TLS-PSK connections and forwarding them to the
fake registration server over plain HTTP.

What is TLS-PSK?
    TLS-PSK (Pre-Shared Key) is a TLS cipher suite that uses symmetric keys
    instead of certificates for authentication. Tuya devices use PSK-TLS to
    encrypt communication with the cloud, deriving the PSK from device
    identity and hint using AES-CBC encryption.

How It Works:
    1. Device connects to port 443 (HTTPS) or 8886 (MQTT-TLS)
    2. TLS-PSK handshake occurs using device identity
    3. PSK is derived from identity and hint using AES-CBC + MD5
    4. Decrypted traffic is forwarded to local HTTP/MQTT server
    5. Responses are encrypted and sent back to device

Architecture:
    ┌──────────┐   TLS-PSK    ┌───────────┐   Plain    ┌───────────┐
    │  Device  │──────────────▶│ PSK Proxy │───────────▶│ Fake API  │
    │  (443)   │◀──────────────│ (this)    │◀───────────│ (80/1883) │
    └──────────┘              └───────────┘            └───────────┘

Proxied Connections:
    - Port 443 (HTTPS) → Port 80 (HTTP) - API requests
    - Port 8886 (MQTT-TLS) → Port 1883 (MQTT) - Device telemetry

PSK Derivation:
    1. Extract identity from client hello (minus first byte)
    2. Validate identity prefix matches expected value
    3. Generate AES key: MD5(last 16 bytes of hint)
    4. Generate AES IV: MD5(identity)
    5. PSK = AES-CBC-Encrypt(first 32 bytes of identity)

Typical Usage:
    Run as standalone proxy:
        $ sudo ./psk-frontend.py

    The proxy binds to 10.42.42.1 (gateway) and listens on ports 443 and 8886.
    Devices connecting via TLS-PSK are automatically decrypted and proxied.

Example:
    >>> from psk_frontend import gen_psk
    >>> identity = b'\\x00' + b'BAohbmd6aG91IFR1' + b'...'  # Device identity
    >>> hint = b'1dHRsc2NjbHltbGx3eWh5' b'0000000000000000'
    >>> psk = gen_psk(identity, hint)
    PSK: a1b2c3d4e5f6...

Security Note:
    This proxy is designed for local device flashing only. It performs
    intentional man-in-the-middle decryption of device traffic to enable
    firmware replacement. Only use on networks you control.

Created by VTRUST team for tuya-convert project.
"""

import select
import socket
import ssl
from binascii import hexlify, unhexlify
from hashlib import md5
from typing import List, Tuple

from Cryptodome.Cipher import AES
from sslpsk3 import SSLPSKContext

# Network constants
DEFAULT_GATEWAY = "10.42.42.1"
HTTPS_PORT = 443
HTTP_PORT = 80
MQTT_ALT_PORT = 8886
MQTT_PORT = 1883

# PSK constants
IDENTITY_PREFIX = b"BAohbmd6aG91IFR1"
PSK_HINT = b"1dHRsc2NjbHltbGx3eWh5" b"0000000000000000"

# Crypto constants
MD5_KEY_LENGTH = 16
AES_BLOCK_SIZE = 32

# Socket constants
SOCKET_LISTEN_BACKLOG = 1
SOCKET_BUFFER_SIZE = 4096


def listener(host: str, port: int) -> socket.socket:
    """Create a TCP listening socket on the specified host and port.

    Creates a server socket that listens for incoming connections. The socket
    is configured with SO_REUSEADDR to allow immediate rebinding after restart,
    which is useful for development and testing.

    Args:
        host: The IP address to bind to. Use "0.0.0.0" for all interfaces,
            or a specific IP like "10.42.42.1" for the gateway.
        port: The TCP port number to listen on (e.g., 443 for HTTPS,
            8886 for MQTT-TLS).

    Returns:
        A listening socket object ready to accept client connections.
        Call accept() on this socket to receive incoming connections.

    Example:
        >>> sock = listener("10.42.42.1", 443)
        >>> client_sock, addr = sock.accept()
        >>> print(f"Connection from {addr}")
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(SOCKET_LISTEN_BACKLOG)
    return sock


def client(host: str, port: int) -> socket.socket:
    """Create a TCP client socket and connect to the specified host and port.

    Creates an outbound TCP connection to a backend server. This is used by the
    proxy to forward decrypted traffic to the local fake registration server
    or MQTT broker.

    Args:
        host: The hostname or IP address to connect to. Typically "10.42.42.1"
            for the local gateway running the fake services.
        port: The TCP port number to connect to (e.g., 80 for HTTP,
            1883 for MQTT).

    Returns:
        A connected socket object ready for sending and receiving data.

    Raises:
        OSError: If the connection fails (e.g., service not running).

    Example:
        >>> sock = client("10.42.42.1", 80)
        >>> sock.send(b"GET / HTTP/1.1\\r\\n\\r\\n")
        >>> response = sock.recv(4096)
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def gen_psk(identity: bytes, hint: bytes) -> bytes:
    """Generate pre-shared key from device identity and hint using AES-CBC.

    Derives the TLS-PSK key using the Tuya-specific algorithm:
    1. Strip first byte from identity (TLS encoding byte)
    2. Validate identity prefix matches expected value
    3. Generate AES key from MD5 of last 16 bytes of hint
    4. Generate AES IV from MD5 of identity
    5. Encrypt first 32 bytes of identity using AES-CBC

    This algorithm is hardcoded in Tuya device firmware and must be replicated
    exactly for the TLS-PSK handshake to succeed.

    Args:
        identity: The device identity bytes from TLS-PSK client hello.
            First byte is TLS encoding, followed by base64-like prefix,
            then device-specific data. Typically 33+ bytes.
        hint: The PSK hint bytes, typically the concatenation of a base64
            string and device key. Last 16 bytes are used for key derivation.

    Returns:
        The 32-byte pre-shared key used for TLS-PSK encryption.

    Example:
        >>> identity = b'\\x00BAohbmd6aG91IFR1' + b'X' * 16
        >>> hint = b'1dHRsc2NjbHltbGx3eWh5' + b'0' * 16
        >>> psk = gen_psk(identity, hint)
        ID: 004241...
        PSK: a1b2c3...
        >>> len(psk)
        32

    Note:
        - Prints identity and PSK in hex for debugging
        - Validates identity prefix to detect unexpected devices
        - PSK length must be exactly 32 bytes for AES-CBC
    """
    print("ID: %s" % hexlify(identity).decode())
    identity = identity[1:]
    if identity[:MD5_KEY_LENGTH] != IDENTITY_PREFIX:
        print("Prefix: %s" % identity[:MD5_KEY_LENGTH])  # type: ignore[str-bytes-safe]
    key = md5(hint[-MD5_KEY_LENGTH:]).digest()
    iv = md5(identity).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    psk = cipher.encrypt(identity[:AES_BLOCK_SIZE])
    print("PSK: %s" % hexlify(psk).decode())
    return psk


class PskFrontend:
    """TLS-PSK frontend proxy that decrypts and forwards device connections.

    Implements a transparent proxy that:
    1. Accepts TLS-PSK encrypted connections from Tuya devices
    2. Performs TLS-PSK handshake using device identity
    3. Decrypts incoming traffic
    4. Forwards plaintext to backend server (HTTP/MQTT)
    5. Encrypts responses and sends back to device

    Each PskFrontend instance handles one port mapping (e.g., 443→80 or 8886→1883).
    Multiple sessions can be active simultaneously, tracked in the sessions list.

    Attributes:
        listening_host: IP address to listen on (e.g., "10.42.42.1")
        listening_port: Port to accept TLS-PSK connections (e.g., 443, 8886)
        host: Backend server IP to forward to (e.g., "10.42.42.1")
        port: Backend server port to forward to (e.g., 80, 1883)
        server_sock: The listening socket accepting new connections
        sessions: List of (client_ssl_socket, backend_socket) tuples for active connections
        hint: PSK hint bytes used for key derivation during handshake

    Example:
        >>> # Create HTTPS→HTTP proxy
        >>> proxy = PskFrontend("10.42.42.1", 443, "10.42.42.1", 80)
        >>> # In event loop:
        >>> readables = proxy.readables()
        >>> r, _, _ = select.select(readables, [], [])
        >>> for s in r:
        ...     proxy.data_ready_cb(s)
    """

    def __init__(self, listening_host: str, listening_port: int, host: str, port: int) -> None:
        """Initialize PSK frontend proxy with listening and backend addresses.

        Args:
            listening_host: IP address to bind the TLS-PSK listener (gateway IP)
            listening_port: Port for TLS-PSK connections (443 or 8886)
            host: Backend server IP to forward decrypted traffic
            port: Backend server port (80 for HTTP, 1883 for MQTT)
        """
        self.listening_port: int = listening_port
        self.listening_host: str = listening_host
        self.host: str = host
        self.port: int = port

        self.server_sock: socket.socket = listener(listening_host, listening_port)
        self.sessions: List[Tuple[socket.socket, socket.socket]] = []
        self.hint: bytes = PSK_HINT

    def readables(self) -> List[socket.socket]:
        """Return list of all sockets to monitor for readable data.

        Collects sockets from:
        - The listening socket (for new client connections)
        - All client SSL sockets (encrypted data from devices)
        - All backend sockets (plaintext data from local servers)

        This list is used with select.select() to implement non-blocking I/O.

        Returns:
            List of socket objects to monitor for incoming data.

        Example:
            >>> proxy = PskFrontend("10.42.42.1", 443, "10.42.42.1", 80)
            >>> sockets = proxy.readables()
            >>> len(sockets) >= 1  # At minimum, the server socket
            True
        """
        readables = [self.server_sock]
        for s1, s2 in self.sessions:
            readables.append(s1)
            readables.append(s2)
        return readables

    def new_client(self, s1: socket.socket) -> None:
        """Handle new client connection by setting up TLS-PSK and backend connection.

        Performs TLS-PSK handshake with the device and creates a corresponding
        connection to the backend server. The two sockets are paired as a session
        for bidirectional data forwarding.

        Process:
        1. Create TLS-PSK context with TLSv1.2 and PSK-AES128-CBC-SHA256 cipher
        2. Set PSK callback to derive key from device identity
        3. Perform TLS handshake with device
        4. Connect to backend server (HTTP/MQTT)
        5. Add socket pair to sessions list

        Args:
            s1: The accepted client socket from the device. Will be wrapped with
                TLS-PSK encryption.

        Side Effects:
            - Adds (ssl_socket, backend_socket) tuple to self.sessions
            - Prints connection info and any errors to stdout

        Note:
            SSL errors are caught and logged but don't crash the proxy. Common
            errors like NO_SHARED_CIPHER often come from phones/browsers and
            can be safely ignored.

        Example:
            >>> proxy = PskFrontend("10.42.42.1", 443, "10.42.42.1", 80)
            >>> client_sock, addr = proxy.server_sock.accept()
            >>> proxy.new_client(client_sock)
            new client on port 443 from 192.168.1.100:54321
            ID: 004241...
            PSK: a1b2c3...
        """
        try:
            # Create SSLPSKContext for TLS-PSK connection
            context = SSLPSKContext(ssl.PROTOCOL_TLS_SERVER)
            context.maximum_version = ssl.TLSVersion.TLSv1_2
            context.set_ciphers("PSK-AES128-CBC-SHA256")
            context.set_psk_server_callback(
                lambda identity: gen_psk(identity, self.hint), identity_hint=self.hint
            )

            ssl_sock = context.wrap_socket(s1, server_side=True)

            s2 = client(self.host, self.port)
            self.sessions.append((ssl_sock, s2))
        except ssl.SSLError as e:
            print("could not establish sslpsk socket:", e)
            if e and (
                "NO_SHARED_CIPHER" in e.reason
                or "WRONG_VERSION_NUMBER" in e.reason
                or "WRONG_SSL_VERSION" in e.reason
            ):
                print("don't panic this is probably just your phone!")
        except Exception as e:
            print(e)

    def data_ready_cb(self, s: socket.socket) -> None:
        """Handle readable data on a socket (new connection or data transfer).

        Called when select.select() indicates a socket has readable data. This
        method handles two cases:
        1. New connection on server socket - accepts and sets up TLS-PSK session
        2. Data on session socket - forwards data to the paired socket

        Data Flow:
            Device → SSL Socket → Decrypt → Backend Socket → Local Server
            Device ← SSL Socket ← Encrypt ← Backend Socket ← Local Server

        Connection Lifecycle:
        - Empty recv() (0 bytes) indicates graceful close - both sockets shut down
        - Socket errors (OSError, BrokenPipeError) indicate abrupt close - session removed
        - Session is removed from sessions list on any closure

        Args:
            s: The socket that has readable data (from select.select() result).
                Can be the server socket (new connection) or a session socket (data).

        Side Effects:
            - Accepts new connections and creates sessions
            - Forwards data between socket pairs
            - Removes closed sessions from sessions list
            - Prints connection info and errors to stdout

        Example:
            >>> proxy = PskFrontend("10.42.42.1", 443, "10.42.42.1", 80)
            >>> readables = proxy.readables()
            >>> r, _, _ = select.select(readables, [], [])
            >>> for sock in r:
            ...     proxy.data_ready_cb(sock)
            new client on port 443 from 192.168.1.100:54321
        """
        if s == self.server_sock:
            _s, frm = s.accept()
            print("new client on port %d from %s:%d" % (self.listening_port, frm[0], frm[1]))
            self.new_client(_s)

        for s1, s2 in self.sessions:
            if s == s1 or s == s2:
                c = s1 if s == s2 else s2
                try:
                    buf = s.recv(SOCKET_BUFFER_SIZE)
                    if len(buf) > 0:
                        c.send(buf)
                    else:
                        s1.shutdown(socket.SHUT_RDWR)
                        s2.shutdown(socket.SHUT_RDWR)
                        self.sessions.remove((s1, s2))
                except (OSError, ValueError, BrokenPipeError) as e:
                    # Handle socket errors, connection issues, and session removal errors
                    print(f"Session error: {e}")
                    try:
                        self.sessions.remove((s1, s2))
                    except ValueError:
                        # Session already removed
                        pass


def main() -> None:
    """Run PSK frontend proxies for TLS-PSK HTTPS and MQTT connections.

    Creates and runs two concurrent TLS-PSK proxy instances:
    1. HTTPS proxy: 10.42.42.1:443 → 10.42.42.1:80
       - Decrypts device API requests and forwards to fake registration server
    2. MQTT-TLS proxy: 10.42.42.1:8886 → 10.42.42.1:1883
       - Decrypts device telemetry and forwards to local MQTT broker

    Uses select() for multiplexed I/O, allowing both proxies to run concurrently
    in a single-threaded event loop. The loop runs indefinitely until interrupted.

    Proxies:
        - HTTPS (443→80): Device activation, token requests, upgrade checks
        - MQTT-TLS (8886→1883): Device status updates, command acknowledgments

    Usage:
        Run as root (required for binding to privileged ports):
            $ sudo ./psk-frontend.py

        The proxies will run indefinitely. Press Ctrl+C to stop.

    Side Effects:
        - Binds to ports 443 and 8886 (requires root/CAP_NET_BIND_SERVICE)
        - Runs infinite event loop
        - Prints connection info and errors to stdout

    Note:
        This function never returns under normal operation. It must be
        interrupted (Ctrl+C) or killed to stop.

    Example:
        >>> # This would run forever, so we don't actually call it in tests
        >>> # main()  # Runs until Ctrl+C
    """
    gateway = DEFAULT_GATEWAY
    proxies = [
        PskFrontend(gateway, HTTPS_PORT, gateway, HTTP_PORT),
        PskFrontend(gateway, MQTT_ALT_PORT, gateway, MQTT_PORT),
    ]

    while True:
        readables: List[socket.socket] = []
        for p in proxies:
            readables = readables + p.readables()
        r, _, _ = select.select(readables, [], [])
        for s in r:
            for p in proxies:
                p.data_ready_cb(s)


if __name__ == "__main__":
    main()
