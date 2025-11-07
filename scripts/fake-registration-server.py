#!/usr/bin/env python3
# encoding: utf-8
"""Fake Tuya Registration Server for Device Firmware Flashing.

This module implements a fake Tuya cloud registration server used for flashing
alternative firmware to Tuya-based IoT devices. It intercepts device activation
and upgrade requests, simulating the official Tuya cloud API endpoints.

The server supports both encrypted (protocol 2.2) and unencrypted (protocol 2.1)
communication modes, using AES-ECB encryption with a configurable secret key.

How It Works:
    1. Device connects to fake AP created by tuya-convert
    2. Device sends smartconfig credentials → Server stores token
    3. Device requests activation → Server responds with fake cloud URLs
    4. Device checks for firmware upgrade → Server offers custom firmware
    5. Device downloads and flashes alternative firmware

Protocol Flow Diagram:
    ┌────────┐                          ┌─────────────┐
    │ Device │                          │ Fake Server │
    └───┬────┘                          └──────┬──────┘
        │                                      │
        │  s.gw.token.get (gwId, token)       │
        │─────────────────────────────────────▶│
        │◀─────────────────────────────────────│
        │  {gwApiUrl, mqttUrl, ...}            │
        │                                      │
        │  [smartconfig killed]                │
        │                                      │
        │  s.gw.dev.pk.active (encrypted)     │
        │─────────────────────────────────────▶│
        │◀─────────────────────────────────────│
        │  {schema, secKey, localKey, ...}    │
        │                                      │
        │  [mq_pub_15.py triggered]           │
        │                                      │
        │  s.gw.upgrade.get (2.2) or          │
        │  s.gw.upgrade (2.1)                 │
        │─────────────────────────────────────▶│
        │◀─────────────────────────────────────│
        │  {url, md5, hmac, version: 9.0.0}   │
        │                                      │
        │  HTTP GET /files/upgrade.bin         │
        │─────────────────────────────────────▶│
        │◀─────────────────────────────────────│
        │  [firmware binary]                   │
        │                                      │
        │  s.gw.upgrade.updatestatus          │
        │─────────────────────────────────────▶│
        │◀─────────────────────────────────────│
        │  {success: true}                     │
        │                                      │
        │  [Device reboots with new firmware] │
        └─────────────────────────────────────┘

Main API Endpoints:
    - s.gw.token.get: Token retrieval, returns fake cloud URLs
    - s.gw.dev.pk.active: Device activation, triggers upgrade
    - s.gw.upgrade.get: Upgrade check (protocol 2.2)
    - s.gw.upgrade: Upgrade check (protocol 2.1)
    - tuya.device.upgrade.get: Alternative upgrade endpoint
    - s.gw.upgrade.updatestatus: Upgrade status reporting
    - s.gw.log: Log submission endpoint
    - s.gw.timer: Timer configuration endpoint
    - s.gw.dev.config.get: Dynamic configuration endpoint

Encryption (Protocol 2.2):
    Request: data parameter contains hex-encoded AES-ECB encrypted JSON
    Response: {
        "result": base64(AES-ECB-encrypt(JSON)),
        "t": timestamp,
        "sign": MD5("result=<encrypted>||t=<timestamp>||<secKey>")[8:24]
    }

Plain (Protocol 2.1):
    Request: JSON parameters in query string or body
    Response: {
        "result": <data>,
        "t": timestamp,
        "e": false,
        "success": true
    }

Main Features:
    - Device activation and token generation endpoints
    - Firmware upgrade endpoints with MD5/SHA256/HMAC verification
    - Dynamic configuration and timer management
    - Support for both ESP82xx-based devices and others
    - Automatic smartconfig process termination after token retrieval
    - Automatic firmware upgrade trigger after device activation

Typical Usage:
    Run as part of tuya-convert:
        $ sudo ./start_flash.sh

    Run standalone for testing:
        $ ./fake-registration-server.py --port=80 --addr=10.42.42.1

    Custom secret key:
        $ ./fake-registration-server.py --secKey=mysecretkey123

Command-line Options:
    --port: HTTP server port (default: 80)
    --addr: Server IP address (default: 10.42.42.1)
    --secKey: Secret key for encrypted communication (default: 0000000000000000)
    --debug: Enable debug mode (default: True)

Example:
    >>> from tornado.ioloop import IOLoop
    >>> from fake_registration_server import JSONHandler
    >>> # Server runs automatically when executed as script
    >>> # Access at http://10.42.42.1/gw.json?a=s.gw.token.get

Security Note:
    This server intentionally bypasses Tuya cloud security to enable local
    firmware flashing. It should only be run on isolated networks you control.
    Never expose this server to the internet.

Created by nano on 2018-11-22.
Copyright (c) 2018 VTRUST. All rights reserved.
"""

from typing import Any, Dict, Optional, Union

import tornado.locks
import tornado.web
from tornado.options import define, options, parse_command_line

define("port", default=80, help="run on the given port", type=int)
define("addr", default="10.42.42.1", help="run on the given ip", type=str)
define("debug", default=True, help="run in debug mode")
define("secKey", default="0000000000000000", help="key used for encrypted communication")

import os
import signal
import subprocess
import threading
from types import FrameType


def exit_cleanly(signum: int, frame: Optional[FrameType]) -> None:
    """
    Handle SIGINT signal for clean server shutdown.

    Args:
            signum: Signal number received
            frame: Current stack frame at the time of signal
    """
    print("Received SIGINT, exiting...")
    exit(0)


signal.signal(signal.SIGINT, exit_cleanly)

import binascii
import hashlib
import hmac
import json
from base64 import b64encode

# Import shared cryptographic utilities
from crypto_utils import decrypt, encrypt, pad, unpad


def jsonstr(j: Union[Dict, list, Any]) -> str:
    """
    Convert a Python object to a compact JSON string.

    Args:
            j: Python object (dict, list, etc.) to serialize

    Returns:
            Compact JSON string without extra whitespace
    """
    return json.dumps(j, separators=(",", ":"))


def file_as_bytes(file_name: str) -> bytes:
    """
    Read a file and return its contents as bytes.

    Args:
            file_name: Path to the file to read

    Returns:
            File contents as bytes
    """
    with open(file_name, "rb") as file:
        return file.read()


# Global variables storing firmware file metadata
# These are calculated once at startup and used for upgrade responses
file_md5: str = ""  # MD5 hash of the firmware file
file_sha256: str = ""  # SHA256 hash of the firmware file
file_hmac: str = ""  # HMAC signature of the SHA256 hash
file_len: str = ""  # Size of the firmware file in bytes


def get_file_stats(file_name: str) -> None:
    """
    Calculate and store cryptographic hashes and size of the firmware file.

    This function populates global variables with MD5, SHA256, HMAC, and file size
    information for the firmware upgrade file. These values are used in upgrade
    endpoint responses to allow devices to verify firmware integrity.

    Args:
            file_name: Path to the firmware file to analyze

    Side Effects:
            Updates global variables: file_md5, file_sha256, file_hmac, file_len
    """
    global file_md5
    global file_sha256
    global file_hmac
    global file_len
    file = file_as_bytes(file_name)
    file_md5 = hashlib.md5(file).hexdigest()
    file_sha256 = hashlib.sha256(file).hexdigest().upper()
    file_hmac = (
        hmac.HMAC(options.secKey.encode(), file_sha256.encode(), "sha256").hexdigest().upper()
    )
    file_len = str(os.path.getsize(file_name))


from time import time


def timestamp() -> int:
    """
    Get current Unix timestamp as an integer.

    Returns:
            Current time as seconds since epoch (January 1, 1970)
    """
    return int(time())


class FilesHandler(tornado.web.StaticFileHandler):
    """
    Custom static file handler that serves firmware files with automatic index.html fallback.

    This handler serves files from the ../files/ directory and automatically serves
    index.html when the URL path is empty or ends with a slash.
    """

    def parse_url_path(self, url_path: str) -> str:
        """
        Parse and modify the URL path to add index.html for directory requests.

        Args:
                url_path: The requested URL path

        Returns:
                Modified URL path with index.html appended if needed
        """
        if not url_path or url_path.endswith("/"):
            url_path = url_path + str("index.html")
        return url_path


class MainHandler(tornado.web.RequestHandler):
    """
    Handler for the root endpoint that displays a simple connection confirmation.
    """

    def get(self) -> None:
        """
        Handle GET requests to the root endpoint.

        Sends a simple text response confirming connection to the fake server.
        """
        self.write("You are connected to vtrust-flash")


class JSONHandler(tornado.web.RequestHandler):
    """
    Main request handler for Tuya API endpoints.

    This handler processes all device registration, activation, and firmware upgrade
    requests. It supports both encrypted (protocol 2.2) and unencrypted (protocol 2.1)
    communication modes.

    Attributes:
            activated_ids: Dictionary tracking which gateway IDs have been activated to
                          determine schema complexity in responses
    """

    activated_ids: Dict[str, bool] = {}

    def get(self) -> None:
        """
        Handle GET requests by delegating to the POST handler.

        Some Tuya devices may send GET requests to endpoints, so we redirect
        them to use the same logic as POST requests.
        """
        self.post()

    def reply(
        self, result: Optional[Union[Dict, bool, Any]] = None, encrypted: bool = False
    ) -> None:
        """
        Send a JSON response to the device with optional encryption.

        For encrypted responses (protocol 2.2), the result is encrypted with AES and
        signed with MD5. For unencrypted responses (protocol 2.1), the result is
        returned in plain JSON.

        Args:
                result: Response data to send (dict, bool, or None)
                encrypted: Whether to use encrypted protocol (2.2) or plain (2.1)

        Side Effects:
                Sends HTTP response with appropriate headers and JSON body
        """
        ts = timestamp()
        if encrypted:
            answer = {"result": result, "t": ts, "success": True}
            answer = jsonstr(answer)
            payload = b64encode(encrypt(answer, options.secKey.encode())).decode()
            signature = "result=%s||t=%d||%s" % (payload, ts, options.secKey)
            signature = hashlib.md5(signature.encode()).hexdigest()[8:24]
            answer = {"result": payload, "t": ts, "sign": signature}
        else:
            answer = {"t": ts, "e": False, "success": True}
            if result:
                answer["result"] = result
        answer = jsonstr(answer)
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.set_header("Content-Length", str(len(answer)))
        self.set_header("Content-Language", "zh-CN")
        self.write(answer)
        print("reply", answer)

    def post(self) -> None:
        """
        Handle POST requests to Tuya API endpoints.

        This method processes all device API requests including:
        - Token retrieval (s.gw.token.get)
        - Device activation (.active endpoints)
        - Firmware upgrade checks and downloads (.upgrade endpoints)
        - Log submission (.log)
        - Timer configuration (.timer)
        - Dynamic configuration (.config.get)

        The method extracts request parameters, attempts to decrypt the payload if
        encrypted, and routes to the appropriate response handler based on the 'a'
        (action) parameter.

        Request Parameters:
                a: API action/endpoint being called
                et: Encryption type (1 for encrypted, 0 for plain)
                gwId: Gateway device ID

        Side Effects:
                - Prints request details and payload to console
                - Triggers firmware upgrade via mq_pub_15.py after activation
                - Kills smartconfig process after token retrieval
        """
        uri = str(self.request.uri)
        a = str(self.get_argument("a", 0))
        encrypted = str(self.get_argument("et", 0)) == "1"
        gwId = str(self.get_argument("gwId", 0))
        payload = self.request.body[5:]
        print()
        print(self.request.method, uri)
        print(self.request.headers)
        if payload:
            try:
                decrypted_payload = decrypt(binascii.unhexlify(payload), options.secKey.encode())
                if decrypted_payload[0] != "{":
                    raise ValueError("payload is not JSON")
                print("payload", decrypted_payload)
            except (binascii.Error, ValueError, UnicodeDecodeError) as e:
                # Failed to decrypt or decode payload - log error and display raw payload
                print(f"Failed to decrypt payload: {e}")
                print("payload", payload.decode())

        if gwId == "0":
            print(
                "WARNING: it appears this device does not use an ESP82xx and therefore cannot install ESP based firmware"
            )

        # Activation endpoints
        if a == "s.gw.token.get":
            print("Answer s.gw.token.get")
            answer = {
                "gwApiUrl": "http://" + options.addr + "/gw.json",
                "stdTimeZone": "-05:00",
                "mqttRanges": "",
                "timeZone": "-05:00",
                "httpsPSKUrl": "https://" + options.addr + "/gw.json",
                "mediaMqttUrl": options.addr,
                "gwMqttUrl": options.addr,
                "dstIntervals": [],
            }
            if encrypted:
                answer["mqttsUrl"] = options.addr
                answer["mqttsPSKUrl"] = options.addr
                answer["mediaMqttsUrl"] = options.addr
                answer["aispeech"] = options.addr
            self.reply(answer)
            # Kill smartconfig process using subprocess (safer than os.system)
            subprocess.run(["pkill", "-f", "smartconfig/main.py"], check=False)

        elif ".active" in a:
            print("Answer s.gw.dev.pk.active")
            # first try extended schema, otherwise minimal schema
            schema_key_count = 1 if gwId in self.activated_ids else 20
            # record that this gwId has been seen
            self.activated_ids[gwId] = True
            schema = jsonstr(
                [{"mode": "rw", "property": {"type": "bool"}, "id": 1, "type": "obj"}]
                * schema_key_count
            )
            answer = {
                "schema": schema,
                "uid": "00000000000000000000",
                "devEtag": "0000000000",
                "secKey": options.secKey,
                "schemaId": "0000000000",
                "localKey": "0000000000000000",
            }
            self.reply(answer)
            print("TRIGGER UPGRADE IN 10 SECONDS")
            protocol = "2.2" if encrypted else "2.1"

            # Use threading and subprocess for safe background execution
            # This prevents shell injection attacks via gwId parameter
            def trigger_upgrade():
                import time
                time.sleep(10)
                subprocess.run(
                    ["./mq_pub_15.py", "-i", gwId, "-p", protocol],
                    check=False
                )

            upgrade_thread = threading.Thread(target=trigger_upgrade, daemon=True)
            upgrade_thread.start()

        # Upgrade endpoints
        elif ".updatestatus" in a:
            print("Answer s.gw.upgrade.updatestatus")
            self.reply(None, encrypted)

        elif (".upgrade" in a) and encrypted:
            print("Answer s.gw.upgrade.get")
            answer = {
                "auto": 3,
                "size": file_len,
                "type": 0,
                "pskUrl": "http://" + options.addr + "/files/upgrade.bin",
                "hmac": file_hmac,
                "version": "9.0.0",
            }
            self.reply(answer, encrypted)

        elif ".device.upgrade" in a:
            print("Answer tuya.device.upgrade.get")
            answer = {
                "auto": True,
                "type": 0,
                "size": file_len,
                "version": "9.0.0",
                "url": "http://" + options.addr + "/files/upgrade.bin",
                "md5": file_md5,
            }
            self.reply(answer, encrypted)

        elif ".upgrade" in a:
            print("Answer s.gw.upgrade")
            answer = {
                "auto": 3,
                "fileSize": file_len,
                "etag": "0000000000",
                "version": "9.0.0",
                "url": "http://" + options.addr + "/files/upgrade.bin",
                "md5": file_md5,
            }
            self.reply(answer, encrypted)

        # Misc endpoints
        elif ".log" in a:
            print("Answer atop.online.debug.log")
            answer = True
            self.reply(answer, encrypted)

        elif ".timer" in a:
            print("Answer s.gw.dev.timer.count")
            answer = {"devId": gwId, "count": 0, "lastFetchTime": 0}
            self.reply(answer, encrypted)

        elif ".config.get" in a:
            print("Answer tuya.device.dynamic.config.get")
            answer = {"validTime": 1800, "time": timestamp(), "config": {}}
            self.reply(answer, encrypted)

        # Catchall
        else:
            print("Answer generic ({})".format(a))
            self.reply(None, encrypted)


def main() -> None:
    """
    Initialize and start the fake Tuya registration server.

    This function:
    1. Parses command-line options (port, address, debug mode, secKey)
    2. Calculates firmware file hashes for upgrade responses
    3. Configures Tornado web application with routes:
       - / : Connection confirmation
       - /gw.json, /d.json : API endpoints
       - /files/* : Static firmware file serving
       - /* : Catch-all redirect to root
    4. Starts the HTTP server on the specified address and port
    5. Enters the Tornado event loop

    Command-line Options:
            --port: Server port (default: 80)
            --addr: Server IP address (default: 10.42.42.1)
            --debug: Enable debug mode (default: True)
            --secKey: AES encryption key for protocol 2.2 (default: "0000000000000000")

    Raises:
            OSError: If the server cannot bind to the specified port (e.g., EADDRINUSE)
    """
    parse_command_line()
    get_file_stats("../files/upgrade.bin")
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/gw.json", JSONHandler),
            (r"/d.json", JSONHandler),
            ("/files/(.*)", FilesHandler, {"path": str("../files/")}),
            (
                r".*",
                tornado.web.RedirectHandler,
                {"url": "http://" + options.addr + "/", "permanent": False},
            ),
        ],
        # template_path=os.path.join(os.path.dirname(__file__), "templates"),
        # static_path=os.path.join(os.path.dirname(__file__), "templates"),
        debug=options.debug,
    )
    try:
        app.listen(options.port, options.addr)
        print("Listening on " + options.addr + ":" + str(options.port))
        tornado.ioloop.IOLoop.current().start()
    except OSError as err:
        print("Could not start server on port " + str(options.port))
        if err.errno == 98:  # EADDRINUSE
            print("Close the process on this port and try again")
        else:
            print(err)


if __name__ == "__main__":
    main()
