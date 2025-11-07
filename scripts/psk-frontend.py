#!/usr/bin/env python3

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
    """Create a listening socket on the specified host and port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(SOCKET_LISTEN_BACKLOG)
    return sock


def client(host: str, port: int) -> socket.socket:
    """Create a client socket connected to the specified host and port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def gen_psk(identity: bytes, hint: bytes) -> bytes:
    """Generate pre-shared key from identity and hint using AES-CBC."""
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
    """TLS-PSK frontend that proxies connections to a backend server."""

    def __init__(self, listening_host: str, listening_port: int, host: str, port: int) -> None:
        self.listening_port: int = listening_port
        self.listening_host: str = listening_host
        self.host: str = host
        self.port: int = port

        self.server_sock: socket.socket = listener(listening_host, listening_port)
        self.sessions: List[Tuple[socket.socket, socket.socket]] = []
        self.hint: bytes = PSK_HINT

    def readables(self) -> List[socket.socket]:
        """Return list of sockets to monitor for readable data."""
        readables = [self.server_sock]
        for s1, s2 in self.sessions:
            readables.append(s1)
            readables.append(s2)
        return readables

    def new_client(self, s1: socket.socket) -> None:
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
        """Handle readable data on a socket."""
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
    """Run PSK frontend proxies for TLS-PSK and MQTT connections."""
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
