"""Tuya Smartconfig Protocol Implementation.

This package implements the Tuya smartconfig protocol used to provision IoT devices
with Wi-Fi credentials. Smartconfig allows devices to receive SSID, password, and
authentication tokens through specially crafted UDP packets without requiring the
device to host its own access point.

What is Smartconfig?
    Smartconfig is a technique where Wi-Fi credentials are encoded in the lengths
    of UDP packets. Devices in monitor mode can observe packet lengths on the
    network and extract the credentials without being connected to the network.

Tuya Smartconfig Protocol:
    Tuya uses two variants of smartconfig:
    1. Broadcast Mode: Encodes data in UDP broadcast packet lengths
    2. Multicast Mode: Encodes data in multicast IP addresses

How It Works (Broadcast):
    1. Data is AES-encrypted with key "a3c6794oiu876t54"
    2. Each byte is encoded as a UDP packet of specific length
    3. Length encodes nibbles with markers (0x10, 0x20, 0x30, 0x40, 0x100)
    4. Device in monitor mode extracts lengths
    5. Device decodes lengths back to bytes
    6. Device decrypts and connects to Wi-Fi

How It Works (Multicast):
    1. Data is AES-encrypted
    2. Bytes are encoded as multicast IP addresses (226.x.y.z)
    3. Sequence numbers distinguish data sections
    4. Device extracts data from IP addresses
    5. Device decrypts and connects to Wi-Fi

Packet Encoding (Broadcast):
    Length encoding uses markers to identify data:
    - 0x10 | (length >> 4): High nibble of length
    - 0x20 | (length & 0xF): Low nibble of length
    - 0x30 | (crc >> 4): High nibble of CRC8
    - 0x40 | (crc & 0xF): Low nibble of CRC8
    - 0x100 | byte: Actual data bytes
    - 0x80 | seq: Sequence numbers

Multicast Encoding:
    IP addresses encode data:
    - 226.sequence.data1.data2
    - Different sequences for: header, SSID, token, password
    - Header is "TYST01" repeated
    - Each data section uses incrementing sequence numbers

Module Overview:
    - broadcast.py: Broadcast mode packet encoding
    - multicast.py: Multicast mode packet/IP encoding
    - crc.py: CRC8 checksum calculation
    - smartconfig.py: High-level smartconfig orchestration
    - main.py: Command-line entry point

Typical Usage:
    Run smartconfig from command line:
        $ cd scripts/smartconfig
        $ python main.py

    The script reads configuration from ../../config.txt containing:
        WIFI_SSID=MyNetwork
        WIFI_PASS=MyPassword
        SMARTCONFIG_REGION=EU
        SMARTCONFIG_TOKEN=...
        SMARTCONFIG_SECRET=...

    Use in Python:
        >>> from smartconfig.smartconfig import smartconfig
        >>> smartconfig(
        ...     password="MyPassword",
        ...     ssid="MyNetwork",
        ...     region="EU",
        ...     token="aabbccdd...",
        ...     secret="0123456789abcdef"
        ... )

Protocol Flow:
    ┌────────────┐                      ┌────────────┐
    │   Server   │                      │   Device   │
    │  (tuya-    │                      │ (monitor   │
    │  convert)  │                      │   mode)    │
    └─────┬──────┘                      └──────┬─────┘
          │                                    │
          │  Broadcast/Multicast packets       │
          │  with encoded SSID+Password        │
          │───────────────────────────────────▶│
          │                                    │
          │  (Repeated 40x header, 10x body)   │
          │───────────────────────────────────▶│
          │                                    │
          │                                    │ Decode packets
          │                                    │ Extract credentials
          │                                    │ Decrypt with AES
          │                                    │ Connect to Wi-Fi
          │                                    │
          │◀───────────────────────────────────│
          │  UDP broadcast (device discovery)  │
          │                                    │
          └────────────────────────────────────┘

Encryption:
    - Algorithm: AES-128-CBC
    - Key: "a3c6794oiu876t54" (hardcoded in Tuya firmware)
    - IV: MD5(encoded_data_for_iv)
    - Padding: PKCS#7

Example Broadcast Encoding:
    Data: [0xAB, 0xCD]
    Encoded lengths:
    - 0x1A (length high nibble: 0x10 | 0xA)
    - 0x2B (length low nibble: 0x20 | 0xB)
    - 0x3C (CRC high nibble: 0x30 | 0xC)
    - 0x4D (CRC low nibble: 0x40 | 0xD)
    - 0x1AB (data byte: 0x100 | 0xAB)
    - 0x1CD (data byte: 0x100 | 0xCD)

Security Note:
    The AES key is hardcoded and publicly known. Smartconfig provides no
    real security - it's a convenience feature for initial device setup.
    Credentials are observable by anyone on the network in monitor mode.

Performance:
    - Each packet sent with 5ms delay
    - Header repeated 40 times for reliability
    - Body repeated 10 times for reliability
    - Total time: ~5-30 seconds depending on data size

Compatibility:
    - Works with ESP8266 and ESP32 devices
    - Tuya firmware version 3.x and earlier
    - May not work with newer firmware versions

References:
    - Tuya smartconfig reverse engineering
    - ESP8266 smartconfig implementation
    - tuya-convert project documentation

Created for the tuya-convert project.
"""

__version__ = "1.0.0"
__all__ = ["broadcast", "multicast", "smartconfig", "crc"]
