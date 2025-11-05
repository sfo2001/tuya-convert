# API Reference

**Last Updated:** 2025-11-05
**Status:** ✅ Complete
**Implementation:** `scripts/fake-registration-server.py`, `scripts/mq_pub_15.py`

## Overview

This document provides technical reference for the HTTP and MQTT APIs used by tuya-convert to intercept device activation and firmware upgrade processes. The fake registration server mimics official Tuya cloud endpoints to redirect devices to custom firmware.

---

## Table of Contents

1. [HTTP/HTTPS API Endpoints](#httphttps-api-endpoints)
2. [MQTT Topics and Messages](#mqtt-topics-and-messages)
3. [Encryption Protocols](#encryption-protocols)
4. [Request/Response Examples](#requestresponse-examples)
5. [Error Handling](#error-handling)

---

## HTTP/HTTPS API Endpoints

### Base Configuration

**Server Address:** `10.42.42.1` (configurable via `--addr`)
**Default Port:** `80` (configurable via `--port`)
**Protocol Support:** HTTP and HTTPS (with TLS-PSK)

**Implementation:** `scripts/fake-registration-server.py`

---

### Gateway Configuration Endpoints

#### GET `/gw.json`
**Purpose:** Gateway API configuration endpoint
**Used By:** Devices requesting gateway/cloud URLs

**Response Format:**
```json
{
  "t": 1636200000,
  "success": true,
  "result": {...}
}
```

**Code Reference:** `fake-registration-server.py:439` (route configuration)

---

#### GET/POST `/d.json`
**Purpose:** Main device API endpoint (catches all Tuya API calls)
**Used By:** All device registration, activation, and upgrade requests

**Query Parameters:**
- `a` - API action/endpoint name (e.g., `s.gw.token.get`)
- `et` - Encryption type (`1` = encrypted, `0` = plain)
- `gwId` - Gateway device ID
- `v` - API version
- `t` - Timestamp

**Code Reference:** `fake-registration-server.py:439` (route configuration)

---

### Device Activation & Token APIs

#### API: `s.gw.token.get`
**Purpose:** Retrieve gateway token and MQTT URLs during device activation

**Request:**
- Method: `POST /d.json?a=s.gw.token.get&et=0&gwId={gwId}`
- Body: Device identification payload

**Response (Unencrypted - Protocol 2.1):**
```json
{
  "t": 1636200000,
  "e": false,
  "success": true,
  "result": {
    "gwApiUrl": "http://10.42.42.1/gw.json",
    "stdTimeZone": "-05:00",
    "mqttRanges": "",
    "timeZone": "-05:00",
    "httpsPSKUrl": "https://10.42.42.1/gw.json",
    "mediaMqttUrl": "10.42.42.1",
    "gwMqttUrl": "10.42.42.1",
    "dstIntervals": []
  }
}
```

**Response (Encrypted - Protocol 2.2):**
```json
{
  "t": 1636200000,
  "success": true,
  "sign": "a1b2c3d4e5f67890",
  "result": "<base64_encrypted_payload>"
}
```

**Side Effects:**
- Kills smartconfig process after token is retrieved
- Directs device to use fake MQTT broker

**Code Reference:** `fake-registration-server.py:325-342`

---

#### API: `s.gw.dev.pk.active` / `*.active`
**Purpose:** Device activation and schema retrieval

**Request:**
- Method: `POST /d.json?a=s.gw.dev.pk.active&et={0|1}&gwId={gwId}`
- Body: Device activation payload

**Response:**
```json
{
  "t": 1636200000,
  "success": true,
  "result": {
    "schema": "[{\"mode\":\"rw\",\"property\":{\"type\":\"bool\"},\"id\":1,\"type\":\"obj\"}]",
    "uid": "00000000000000000000",
    "devEtag": "0000000000",
    "secKey": "0000000000000000",
    "schemaId": "0000000000",
    "localKey": "0000000000000000"
  }
}
```

**Schema Complexity:**
- First activation: 20 schema keys (extended schema)
- Subsequent activations: 1 schema key (minimal schema)
- Tracks activated devices in `JSONHandler.activated_ids`

**Side Effects:**
- Records device as activated
- Triggers firmware upgrade after 10 seconds via `mq_pub_15.py`

**Code Reference:** `fake-registration-server.py:344-362`

---

### Firmware Upgrade APIs

#### API: `s.gw.upgrade.get` (Encrypted Only)
**Purpose:** Firmware upgrade information for encrypted protocol devices

**Request:**
- Method: `POST /d.json?a=s.gw.upgrade.get&et=1&gwId={gwId}`
- Requires: `et=1` (encrypted communication)

**Response:**
```json
{
  "t": 1636200000,
  "success": true,
  "result": {
    "auto": 3,
    "size": 512000,
    "type": 0,
    "pskUrl": "http://10.42.42.1/files/upgrade.bin",
    "hmac": "1234567890abcdef1234567890abcdef",
    "version": "9.0.0"
  }
}
```

**Fields:**
- `auto`: Automatic upgrade mode (3 = auto upgrade)
- `size`: Firmware file size in bytes
- `type`: Upgrade type (0 = full firmware)
- `pskUrl`: HTTPS URL for PSK-encrypted download
- `hmac`: HMAC-SHA256 of firmware file
- `version`: Firmware version string

**Code Reference:** `fake-registration-server.py:369-378`

---

#### API: `tuya.device.upgrade.get`
**Purpose:** Firmware upgrade information (alternative endpoint)

**Request:**
- Method: `POST /d.json?a=tuya.device.upgrade.get&et={0|1}&gwId={gwId}`

**Response:**
```json
{
  "t": 1636200000,
  "success": true,
  "result": {
    "auto": true,
    "type": 0,
    "size": 512000,
    "version": "9.0.0",
    "url": "http://10.42.42.1/files/upgrade.bin",
    "md5": "1234567890abcdef1234567890abcdef"
  }
}
```

**Code Reference:** `fake-registration-server.py:380-389`

---

#### API: `s.gw.upgrade` (Generic)
**Purpose:** Generic firmware upgrade endpoint (unencrypted fallback)

**Request:**
- Method: `POST /d.json?a=s.gw.upgrade&et=0&gwId={gwId}`

**Response:**
```json
{
  "t": 1636200000,
  "success": true,
  "result": {
    "auto": 3,
    "fileSize": 512000,
    "etag": "0000000000",
    "version": "9.0.0",
    "url": "http://10.42.42.1/files/upgrade.bin",
    "md5": "1234567890abcdef1234567890abcdef"
  }
}
```

**Code Reference:** `fake-registration-server.py:391-400`

---

#### API: `s.gw.upgrade.updatestatus`
**Purpose:** Report firmware upgrade status

**Request:**
- Method: `POST /d.json?a=s.gw.upgrade.updatestatus&et={0|1}&gwId={gwId}`
- Body: Upgrade status payload

**Response:**
```json
{
  "t": 1636200000,
  "success": true
}
```

**Code Reference:** `fake-registration-server.py:365-367`

---

### Miscellaneous APIs

#### API: `atop.online.debug.log` / `*.log`
**Purpose:** Device log submission

**Request:**
- Method: `POST /d.json?a=atop.online.debug.log&et={0|1}&gwId={gwId}`
- Body: Log data payload

**Response:**
```json
{
  "t": 1636200000,
  "success": true,
  "result": true
}
```

**Code Reference:** `fake-registration-server.py:403-406`

---

#### API: `s.gw.dev.timer.count` / `*.timer`
**Purpose:** Device timer configuration count

**Request:**
- Method: `POST /d.json?a=s.gw.dev.timer.count&et={0|1}&gwId={gwId}`

**Response:**
```json
{
  "t": 1636200000,
  "success": true,
  "result": {
    "devId": "0123456789abcdef",
    "count": 0,
    "lastFetchTime": 0
  }
}
```

**Code Reference:** `fake-registration-server.py:408-414`

---

#### API: `tuya.device.dynamic.config.get` / `*.config.get`
**Purpose:** Retrieve dynamic device configuration

**Request:**
- Method: `POST /d.json?a=tuya.device.dynamic.config.get&et={0|1}&gwId={gwId}`

**Response:**
```json
{
  "t": 1636200000,
  "success": true,
  "result": {
    "validTime": 1800,
    "time": 1636200000,
    "config": {}
  }
}
```

**Code Reference:** `fake-registration-server.py:416-422`

---

### Static File Endpoints

#### GET `/files/upgrade.bin`
**Purpose:** Serve custom firmware file to devices

**Implementation:** Static file handler
**Location:** `files/upgrade.bin` (stage 1 firmware)

**Verification:**
- MD5 hash calculated and provided in upgrade response
- HMAC-SHA256 calculated for encrypted protocol
- SHA256 checksum for integrity verification

**Code Reference:** `fake-registration-server.py:177-196` (FilesHandler), `142-173` (file hash calculation)

---

## MQTT Topics and Messages

**Broker:** Mosquitto (configured in `start_flash.sh`)
**Default Port:** `1883`
**Implementation:** `scripts/mq_pub_15.py`

---

### Topic: `smart/device/in/{deviceID}`
**Purpose:** Send commands to device (firmware upgrade trigger)

**Message Format (Protocol 2.1):**
```
2.1<signature><base64_encrypted_payload>
```

**Message Format (Protocol 2.2):**
```
2.2<crc32><timestamp><encrypted_payload>
```

**Payload (Decrypted):**
```json
{
  "data": {
    "gwId": "0123456789abcdef"
  },
  "protocol": 15,
  "s": 1523715,
  "t": 1636200000
}
```

**Protocol Field:**
- `15`: Firmware upgrade trigger command

**Encryption:**
- AES-ECB mode with PKCS#7 padding
- Key: `localKey` (16 bytes, default: `0000000000000000`)
- Base64 encoded for protocol 2.1
- Raw binary with timestamp for protocol 2.2

**Code Reference:** `mq_pub_15.py:88-95`

---

### Topic: `smart/device/out/{deviceID}`
**Purpose:** Device responses and status updates

**Message Format:** Same encryption as `smart/device/in/{deviceID}`

**Usage:** Devices publish responses to commands and status updates

---

## Encryption Protocols

### Protocol 2.1 (Unencrypted/Lightly Encrypted)

**Characteristics:**
- Base64-encoded encrypted payloads (HTTP API)
- MD5 signature for message integrity
- AES-ECB encryption with 16-byte key

**Response Format:**
```json
{
  "t": 1636200000,
  "e": false,
  "success": true,
  "result": {...}
}
```

**MQTT Message Format:**
```
2.1<16_byte_md5_signature><base64_encrypted_payload>
```

**Signature Calculation:**
```python
signature = md5(b'data=' + encrypted + b'||pv=2.1||' + localKey).hexdigest()[8:24]
```

**Code Reference:** `mq_pub_15.py:31-37`

---

### Protocol 2.2 (Fully Encrypted)

**Characteristics:**
- Fully encrypted payloads with CRC32 verification
- HMAC-SHA256 for firmware integrity
- Binary message format (no Base64)

**Response Format:**
```json
{
  "result": "<base64_encrypted_payload>",
  "t": 1636200000,
  "sign": "<16_char_md5_signature>"
}
```

**MQTT Message Format:**
```
2.2<4_byte_crc32><8_byte_timestamp><encrypted_payload>
```

**Signature Calculation (HTTP):**
```python
signature = md5(f'result={encrypted_result}||t={timestamp}||{secKey}').hexdigest()[8:24]
```

**Code Reference:**
- HTTP: `fake-registration-server.py:251-263`
- MQTT: `mq_pub_15.py:38-42`

---

### AES Encryption/Decryption

**Algorithm:** AES-ECB
**Padding:** PKCS#7 (pad to 16-byte boundary)
**Key Size:** 16 bytes (128-bit)

**Encryption:**
```python
def encrypt(msg, key):
    return AES.new(key, AES.MODE_ECB).encrypt(pad(msg).encode())
```

**Decryption:**
```python
def decrypt(msg, key):
    return unpad(AES.new(key, AES.MODE_ECB).decrypt(msg)).decode()
```

**Code Reference:** `fake-registration-server.py:52-100`

---

## Request/Response Examples

### Example 1: Device Token Retrieval

**Request:**
```
POST /d.json?a=s.gw.token.get&et=0&v=4.0&gwId=0123456789abcdef&t=1636200000 HTTP/1.1
Host: 10.42.42.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 123

<encrypted_or_plain_payload>
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Content-Length: 234
Content-Language: zh-CN

{
  "t": 1636200000,
  "e": false,
  "success": true,
  "result": {
    "gwApiUrl": "http://10.42.42.1/gw.json",
    "stdTimeZone": "-05:00",
    "mqttRanges": "",
    "timeZone": "-05:00",
    "httpsPSKUrl": "https://10.42.42.1/gw.json",
    "mediaMqttUrl": "10.42.42.1",
    "gwMqttUrl": "10.42.42.1",
    "dstIntervals": []
  }
}
```

---

### Example 2: Device Activation

**Request:**
```
POST /d.json?a=s.gw.dev.pk.active&et=1&v=4.0&gwId=0123456789abcdef&t=1636200000 HTTP/1.1
Host: 10.42.42.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 256

data=<hex_encoded_encrypted_payload>
```

**Response (Encrypted):**
```http
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Content-Length: 178
Content-Language: zh-CN

{
  "result": "SGVsbG8gV29ybGQhIFRoaXMgaXMgYmFzZTY0IGVuY29kZWQgZW5jcnlwdGVkIGRhdGE=",
  "t": 1636200000,
  "sign": "a1b2c3d4e5f67890"
}
```

**Decrypted Result:**
```json
{
  "schema": "[{\"mode\":\"rw\",\"property\":{\"type\":\"bool\"},\"id\":1,\"type\":\"obj\"}]",
  "uid": "00000000000000000000",
  "devEtag": "0000000000",
  "secKey": "0000000000000000",
  "schemaId": "0000000000",
  "localKey": "0000000000000000"
}
```

---

### Example 3: Firmware Upgrade Trigger (MQTT)

**MQTT Publish:**
```python
# Topic: smart/device/in/0123456789abcdef
# Message (Protocol 2.1):
"2.1a1b2c3d4e5f6789SGVsbG8gV29ybGQhIFRoaXMgaXMgYmFzZTY0IGVuY29kZWQgZW5jcnlwdGVkIGRhdGE="

# Decrypted payload:
{
  "data": {
    "gwId": "0123456789abcdef"
  },
  "protocol": 15,
  "s": 1523715,
  "t": 1636200000
}
```

**Device Response:** Device requests firmware upgrade via HTTP API

---

## Error Handling

### HTTP Error Responses

**Format:**
```json
{
  "t": 1636200000,
  "success": false,
  "errorCode": "ERROR_CODE",
  "errorMsg": "Error description"
}
```

**Note:** Current implementation always returns `success: true` for compatibility

---

### Common Issues

#### Issue: Device doesn't recognize gwId=0

**Log Message:**
```
WARNING: it appears this device does not use an ESP82xx and therefore cannot install ESP based firmware
```

**Cause:** Device is not ESP8266/ESP8285 based
**Solution:** Cannot flash ESP-based firmware; device is incompatible

**Code Reference:** `fake-registration-server.py:321-322`

---

#### Issue: Decryption failed

**Cause:** Incorrect `secKey` for encrypted protocol
**Solution:** Verify `secKey` parameter matches device expectation (default: `0000000000000000`)

---

#### Issue: Device doesn't request upgrade

**Causes:**
1. PSK Identity 02 blocking (newer devices)
2. Activation failed
3. MQTT message not received

**Debugging:**
- Check `smarthack-psk.log` for PSK errors
- Verify MQTT broker is running (`mosquitto -p 1883`)
- Confirm activation endpoint was called

---

## Command-Line Options

### fake-registration-server.py

```bash
python3 fake-registration-server.py [options]

Options:
  --port=80              Server port (default: 80)
  --addr=10.42.42.1      Server IP address (default: 10.42.42.1)
  --debug=True           Enable debug mode (default: True)
  --secKey=0000000000000000  AES encryption key for protocol 2.2 (16 bytes)
```

**Code Reference:** `fake-registration-server.py:28-31`

---

### mq_pub_15.py

```bash
python3 mq_pub_15.py -i <deviceID> [options]

Options:
  -i, --deviceID        Device/gateway ID (required)
  -l, --localKey        AES encryption key (default: 0000000000000000)
  -b, --broker          MQTT broker address (default: 127.0.0.1)
  -p, --protocol        Protocol version (2.1 or 2.2, default: 2.1)
```

**Code Reference:** `mq_pub_15.py:13-19`

---

## Related Pages

- [Protocol Overview](Protocol-Overview.md) - Overview of all protocols used by tuya-convert
- [System Architecture](System-Architecture.md) - Complete system architecture
- [PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md) - PSK encryption details
- [Troubleshooting](Troubleshooting.md) - Common issues and solutions

---

## External References

- **Tuya IoT Platform API:** https://developer.tuya.com/en/docs/iot
- **TuyAPI Library:** https://github.com/codetheweb/tuyapi - Tuya device control reference
- **MQTT Protocol:** https://mqtt.org/ - MQTT specification

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
