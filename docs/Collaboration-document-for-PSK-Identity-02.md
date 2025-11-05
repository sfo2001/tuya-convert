# PSK Identity 02 Protocol

**Last Updated:** 2025-11-05
**Status:** 🔄 Research In Progress
**Implementation:** `scripts/psk-frontend.py`
**Related:** [Research Procedures](PSK-Research-Procedures.md) | [Affected Devices](PSK-Identity-02-Affected-Devices.md)

## Overview

This document consolidates community research into the PSK Identity 02 protocol used by newer Tuya devices. This protocol prevents OTA flashing via tuya-convert.

**Original research discussion:** [Issue #483](https://github.com/ct-Open-Source/tuya-convert/issues/483)

## Does output in your smarthack-psk.log look like this?
```
new client on port 443 from 10.42.42.25:3694
ID: 0242416f68626d6436614739314946523126e9b5b5bdabbb170482e008c373d879b5d1540ec094d09bb7d53fa3fc9645df
PSK: 2a9cf84b7a1b6bf1ede712edb7ee53c04b065f673e600f43627a67fea9a9d05d
could not establish sslpsk socket: [SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC] decryption failed or bad record mac (_ssl.c:1056)
```
If so, you are in the right place. This is where we aim to fix the issue with `ID: 02` and we need your help!

# The Goal
- Derive the PSK from the PSK identity or other known information, if that is even possible with the information we can obtain before a TLS connection is established.

## How can you help?
 1. Grab a pcap (see below)
 1. Compare to other pcap signatures in this wiki
 1. Flag if different

## Why this is hard?
The challenge of this issue is mapping known information (ie `gwId`) to the PSK (`pskKey`), which as mentioned before is indeed unique to every device. This is not possible to extract from the firmware, because to obtain the firmware would require we already know the PSK (or open the device at which point OTA becomes moot).

The previous implementation leaked information through the PSK ID (the MD5 of the `auzKey`), but this latest implementation uses already public information (the SHA256 of the `gwId`) as the PSK ID.

It may be that the `pskKey` is totally random and only stored on Tuya servers and the smart device. If this turns out to be the case, there is no solution to our challenge and this strategy of flashing firmware OTA is no longer viable.
§
> The `prod_idx` is used to compute the PSK identity. This is handed to the server by the client during the handshake, so it is not secret information.

> `prod_idx` is not secret information, it is the first part of the `gwId`. The `gwId` is what is being hashed here, which is `prod_idx` + `mac`.

> The point is that the previous implementation *did* leak secret information through the PSK identity, which we could use to compute the PSK. Now that it does not, our job is harder.

# Open questions
- How is pskKey used to decrypt identity 02 TLS sessions
- Where does pskKey get stored on devices that have been updated from pre-pskKey versions?
- What is with pskKey being 37 characters long? And why does it consist of a-zA-Z0-9 (like base64 but without '+' and '/')
  - If it's base62, then this would be a (16+12) 28-byte value, which are 224 bits. Maybe it's a SHA-224 hash?
- How can we encourage people to check back in this section for things to help with?
  - I would 1) suggest creating a discussion thread than is pinned, much like #483 was and posting any useful information that comes out of it here. 2) rather than pin issue #483, it would be better to pin a link directly to this wiki.  Maybe create a new issue that is closed/locked that only contains a link to this wiki if pinning the wiki itself isn't possible.

# Implementation Details

The PSK Identity 02 protocol is implemented in tuya-convert:

**Code Reference:** `scripts/psk-frontend.py`
- **Line 12:** Identity prefix constant: `IDENTITY_PREFIX = b"BAohbmd6aG91IFR1"`
- **Lines 26-36:** `gen_psk()` function - PSK generation algorithm
- **Lines 48-49:** Hint value used in PSK calculation
- **Lines 61-66:** TLS-PSK setup with cipher suite `PSK-AES128-CBC-SHA256`

**Key Technical Details from Code:**
- PSK Identity format: `\x02` + prefix + SHA256(gwId)
- Cipher suite: `PSK-AES128-CBC-SHA256`
- PSK derivation: AES-CBC with key=MD5(hint[-16:]), IV=MD5(identity)

See the implementation for full algorithm details.

# Findings (and comments that need to be edited into findings)
- firmware ESP8266 RTOS SDK version did not change, but the hash and build time did
  - versions before PSK change are:
    - `OS SDK ver: 2.0.0(898b733) compiled @ May 27 2019 18:49:04`
    - `OS SDK ver: 2.0.0(e8c5810) compiled @ Jan 25 2019 14:26:04`
  - versions after PSK change are:
    - `OS SDK ver: 2.0.0(29f7e05) compiled @ Sep 30 2019 11:19:12`
      - interesting that this build date corresponds with the release of tuya-convert 2.0, coincidence?
    - `OS SDK ver: 2.1.1(317e50f) compiled @ Dec 10 2019 11:05:04`
    - `OS SDK ver: 2.1.1(8d30f72) compiled @ Jul 28 2020 12:33:05`
- Tuya version also is changed.
  - versions before PSK change are:
  - versions after PSK change are:
    - `tuya sdk compiled at Jan  4 2020 18:50:11` (oem_esp_plug)
    - `tuya sdk compiled at Mar  6 2020 20:27:48`
    - `tuya sdk compiled at Apr  8 2020 11:36:25` (oem_esp_switch)
    - `tuya sdk compiled at Apr  9 2020 02:33:43` (oem_esp_light_tuya)
    - `tuya sdk compiled at Apr  9 2020 04:37:24` (oem_esp_light)
    - `tuya sdk compiled at Apr 10 2020 14:44:10` (oem_esp_dltj)
    - `tuya sdk compiled at Apr 12 2020 09:45:06` (oem_esp_plug)
    - `tuya sdk compiled at Apr 13 2020 20:17:41` (oem_esp_light1_pwm_e2l_jbt_onoff)
    - `tuya sdk compiled at Mar 19 2020 17:08:43` (smart_lamp_test2)
- PSK ID begins with:
  - `01` tuya-convert handles these nicely
  - `02` This is the problem at hand
    - derivation:
      - '\x02' + 'BAohbmd6aG91IFR1' + sha256(gwId)
        - where gwId = prod_idx + mac_addr
          - where prod_idx is an 8 digit ASCII numeric identifier for that device model
          - where mac_addr is the lowercase hex representation of the device MAC address
        - where 'BAohbmd6aG91IFR1' is base64 of a chunk of "Hangzhou Tuya Information Technology Co." (base64(0x04,0x0a,"!ngzhou Tu"))
      - Example: 0242416f68626d6436614739314946523126e9b5b5bdabbb170482e008c373d879b5d1540ec094d09bb7d53fa3fc9645df
        - '\x02' + 'BAohbmd6aG91IFR1' is hex 0242416f68626d64366147393149465231
          - many smarthack-psk.log files have repeating f3 in this section; firmware bug?
        - sha256('81550705c82b9615a3f2') is hex 26e9b5b5bdabbb170482e008c373d879b5d1540ec094d09bb7d53fa3fc9645df
          - prod_idx = '81550705'
          - mac_addr = 'c82b9615a3f2'
  - `03` On OHLUX bulbs
    - is this device using certificate pinning?
- disabled most of the serial debugging output
  - unfortunate as this was a useful reverse engineering resource
  - system_uart_swap() is called, switching uart over to GPIO2 (at least for LSC devices). There, the debug output is still shown.
- did not respond to our `smartconfig` procedure
  - it may use a new mechanism or additional restrictions have been imposed
- MAC address in flash appears to be compared with actual device MAC
  - likely to foil reverse engineering attempts by running firmware on a dev board
  - this means that a given firmware backup will only run on the original device
  - MAC address is stored at several places in flash:
    - shuffled at 0x79060: the MAC address 11:22:33:44:55:66 is seen here as 55 44 00 B2 33 22 11 66
    - 0xFB000 in the json string
    - 0xFE484, this is a part of the boot- and network settings (0xFE000)
     - 0xFD484,which contains a copy of the boot- and network settings
       - the sector at 0xFE000 is identical to 0xFD000, except when settings are changed during the last session
- new factory written key found in flash, `"pskKey"`
  - the app never has access to the PSK, it is only used between the IoT device and the cloud
  - once written to flash it is never transmitted, period.
  - stored in JSON blob at 0xFB000
    - from factory only; updated devices do not have pskKey at 0xFB000
      - so where is pskKey stored on field updated devices?
  - this is indeed the PSK key, unencrypted
    - this means if you have a firmware backup you can use this to decrypt captures from the same device
    - since obtaining the firmware requires a working hack or physically opening the device, this doesn't help us for OTA purposes
  - the PSK key does not change with each new session
    - previously the PSK key changed each session, computed using the PSK ID (fixed) and PSK hint from the server (variable)
    - the previous implementation leaked information via the PSK ID while 02 does not
  - this may mean the encryption key will no longer be derived deterministically, big bummer
  - only found in @rsbob's backup, looks like @Farfar's was updated to this firmware and thus lacks this factory written key
    - this may mean there is still hope for devices that came with a lower firmware, since updating to this firmware would require fetching the key
    - this is a very interesting new endpoint: `tuya.device.uuid.pskkey.get`
      - if we can figure out the format of this call, we could try faking it and seeing what it returns after multiple calls
      - to do this, we'll need to capture network traffic from a device upgrading to this firmware from an older one without PSK 02
- The device can request the server downgrade to the old authentication, but the server cannot ask the device to downgrade
  - Since we emulate the server, the downgrade path doesn't help us.
- outside of updating a vulnerable device to the new firmware, the PSK never leaves Tuya's servers
  - Since this communication is encrypted by the highest version of the encryption scheme that the device supports, this isn't too helpful. Currently we can only decrypt that communication if the device is on the old firmware or we have a firmware dumps from that particular device.
- the PSK is unique to each device, not shared among an entire model
- there is currently unused code for what I think is certificate pinning in the Tuya SDK (the one on the device)
  - why do they use PSK, why not do the certificate pinning to the cloud?
    - likely answer is that the public key cryptography necessary to validate a certificate or chain is too slow on the ESP8266
- the server cannot tell Tuya devices to turn off encryption
  - The devices will reject any connection not secured with the TLS_PSK_WITH_AES_128_CBC_SHA256 cipher suite.
- The alphabet for both auz_key and pskKey seem to be (a-z, A-Z, 0-9)
  - We know that is it likely not base64, as we have plenty of samples and no instances of the `+/` characters
  - It is possible that it is base62, but it seems more likely that this is a random string generated at the factory and stored only on the device and the cloud.
    - That would lead me to the guess, that they are not the result of any computation (like hashing the mac_addr or the like), because converting the binary result of such a computation into the above format is not straight forward.
    - If it's base62, then this would be a (2*8) 24-byte value, which are 192 bits. Maybe it's an AES key?
  - Does anybody have an idea, why the length of the pskKey is 37? That sounds rather random.

## Research Procedures

Detailed procedures for capturing and analyzing PSK data have been moved to a dedicated page:

**👉 [PSK Research Procedures](PSK-Research-Procedures.md)**

This includes:
- Decrypting network captures with known PSK
- Creating network captures and firmware backups
- Step-by-step experimental procedures
- Requirements and known issues
- Tools and setup instructions

# Data

## Known Affected Devices

A comprehensive list of devices confirmed to use PSK Identity 02 has been moved to a dedicated page:

**👉 [PSK Identity 02 Affected Devices](PSK-Identity-02-Affected-Devices.md)**

This page includes:
- Alphabetical device list with purchase dates and models
- Identification methods (smarthack-psk.log error patterns)
- Device purchase timeline (pre/post September 2019)
- Community-contributed test results

**Quick check:** If your `smarthack-psk.log` shows `ID: 02...` with a `DECRYPTION_FAILED_OR_BAD_RECORD_MAC` error, see the [affected devices list](PSK-Identity-02-Affected-Devices.md).

## Firmware
🔢 | pcap | SDK_ver_A | SDK_ver_B | mac | mac_addr | prod_idx | auz_key | pskKey
-- | ---- | --------- | --------- | --- | -------- | -------- | ------- | ------
 [1](https://github.com/ct-Open-Source/tuya-convert/files/4021684/BSD34--image1M.zip) |  | 🔴29f7e05 |  |  | c44f33bc1794 | 65046664 | tKzPU69mMe3ns8PmA5M2cAuUUDOtrTeA | yhULg57DUA3Uo1xTP5xhoI0C1kRpWQOwqjMO8
 [2](https://github.com/ct-Open-Source/tuya-convert/files/4052386/Deltaco_SH-P01E_20200110_image1M.zip) |  | 🟢e8c5810 | 🟡29f7e05 | 5e1 |  | 84067851 | iyTIVyDnqiMiMfzWf5KZZsZIcn7gfvMI | 
 [3](https://github.com/ct-Open-Source/tuya-convert/files/4287008/moeshouse_downlight_1m.zip) |  | 🔴29f7e05 |  |  | 98f4abc96ac3 | 06402221 | Yw0VAIvFe3aWlvdKEZfmBPg8xfQ3Jg4Q | kPJ6yZaAbTUqlk5fHrCN6DyWY2Flz9LLI49un
 [4](https://github.com/ct-Open-Source/tuya-convert/files/4303944/BSD29_firmware_1M.zip) |  | 🔴29f7e05 |  |  | d8f15bd5c898 | 83203175 | JQ1YB6PV5AHHLttPZwkKDs9plRFSWpoY | x8rMeGHKE4KVEQiNyUUSyvWxc561vIIN82PMt
 [5](https://github.com/ct-Open-Source/tuya-convert/files/4338606/module1.zip) | ✅ | 🔴29f7e05 |  |  | 2462ab3989fe | 08488420 | diI5mLzLQx5GBNCQQZsZ8J0dQLYMaAeT | Z9ir6z2hsTlRVJKwEZyqpfyIzfLyzkMBkwyGd
 [6b](https://github.com/ct-Open-Source/tuya-convert/files/4360647/tuya_pairing.zip#before4.bin) |  | 🔴29f7e05 |  |  | 98f4abc96ab3 | 06402221 | L14IZWNkHhToWQR60Q8cC2BOMSEQ42DF | ynYDVOPHIhOH7oBHvcbAIbTrlvAar8slGyNBv
 [6a](https://github.com/ct-Open-Source/tuya-convert/files/4360647/tuya_pairing.zip#after4.bin) | ✅ | 🔴29f7e05 |  |  | 98f4abc96ab3 | 06402221 | L14IZWNkHhToWQR60Q8cC2BOMSEQ42DF | ynYDVOPHIhOH7oBHvcbAIbTrlvAar8slGyNBv
 [7b2](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#before2.bin) |  | 🔴29f7e05 |  |  | 98f4abc96ac8 | 06402221 | dhDirFfJylXSWmkpdXUhcVlY5XK97YtW | sLPbe7MDpYMdaQzEYID8gX3flbuUuUHxmQ3Mz
 [7a2](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#after2.bin) | ✅ | 🔴29f7e05 |  |  | 98f4abc96ac8 | 06402221 | dhDirFfJylXSWmkpdXUhcVlY5XK97YtW | sLPbe7MDpYMdaQzEYID8gX3flbuUuUHxmQ3Mz
 [7b3](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#before3.bin) |  | 🔴29f7e05 |  |  | 98f4abc96bde | 06402221 | lpb6dZ9qFwE4beS6SYepUQtPAUOdBmlI | f0xlg6wbkihLXju2ZVaXmbwJlf2qzsGvxBlqX
 [7a3](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#after3.bin) | ✅ | 🔴29f7e05 |  |  | 98f4abc96bde | 06402221 | lpb6dZ9qFwE4beS6SYepUQtPAUOdBmlI | f0xlg6wbkihLXju2ZVaXmbwJlf2qzsGvxBlqX
 [7b4](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#before4.bin) |  | 🔴29f7e05 |  |  | 98f4abc96ab3 | 06402221 | L14IZWNkHhToWQR60Q8cC2BOMSEQ42DF | ynYDVOPHIhOH7oBHvcbAIbTrlvAar8slGyNBv
 [7a4](https://github.com/ct-Open-Source/tuya-convert/files/4364709/tuya_pairing.zip#after4.bin) | ✅ | 🔴29f7e05 |  |  | 98f4abc96ab3 | 06402221 | L14IZWNkHhToWQR60Q8cC2BOMSEQ42DF | ynYDVOPHIhOH7oBHvcbAIbTrlvAar8slGyNBv
 [8](https://github.com/ct-Open-Source/tuya-convert/files/4732853/AOFO_ZLD-44EU-W_20200604_image1M.bin.gz) |  | 🔴29f7e05 |  |  | 600194facb50 | 02063503 | oDg2MkXuvbyxqNEp1Uz1myBAyQarmnUf | 6CJRAyEyBuUzueuVBCItKRnQMfOJhdBWm4BvO
 [9](https://github.com/ct-Open-Source/tuya-convert/files/4732914/firmware-backup.zip) |  | 🔴29f7e05 |  |  | 500291e8f141 | 26636676 | wg7xdxUcsi7W0EmnPUlEtuwoyZwcF2W2 | GUKgTWzsxGCn8UR5tIFFluuKD2qA8FYmaZwY2
[10b](https://github.com/ct-Open-Source/tuya-convert/files/4743192/gosund_sp112_capture.zip#gosund_sp112_firmware_orig.bin) |  | 🟢e8c5810 | 🟡29f7e05 | b60 |  | 10801581 | qxm7SD7sgStYPZUBfIjlUgtDVAN6AoGP | 
[10a](https://github.com/ct-Open-Source/tuya-convert/files/4743192/gosund_sp112_capture.zip#fw_after_onboarding_1.bin.bin) | ✅ | 🟢e8c5810 | 🟡29f7e05 | b60 |  | 10801581 | qxm7SD7sgStYPZUBfIjlUgtDVAN6AoGP | 
[11](https://github.com/ct-Open-Source/tuya-convert/files/4755710/Merkaryv3.3.zip) |  | 🟡29f7e05 |  |  | c44f33b5ed3e | 22885450 | fMFu4XqaRa8f1HLzI9QDm7DJXSdGqJzf | 
[12b](https://github.com/ct-Open-Source/tuya-convert/files/4812333/gosund-WB4.zip#gosund_pre_wb4.bin) |  | 🔴29f7e05 |  |  | c82b9615a3f2 | 81550705 | DWH2FCFhYROGKFyFrflC3hNAUc0HlPdX | rgHG2E1ToDyRq1d4rB1fsSaZJQn3fArLFmTGE
[12a](https://github.com/ct-Open-Source/tuya-convert/files/4812333/gosund-WB4.zip#gosund_post_wb4.bin) | ✅ | 🔴29f7e05 |  |  | c82b9615a3f2 | 81550705 | DWH2FCFhYROGKFyFrflC3hNAUc0HlPdX | rgHG2E1ToDyRq1d4rB1fsSaZJQn3fArLFmTGE
[13](https://github.com/ct-Open-Source/tuya-convert/files/4875072/dxpow_WP1_original_fw.zip) |  | 🟢23fbe10 |  | 2c3ae838e6e4 |  | 01200101 | opTcwaOCLL2nhutEvmdqJMgspspjiAA7 | 
[14](https://github.com/ct-Open-Source/tuya-convert/files/4903594/backup_20200709_112518.zip) |  | 🔴29f7e05 |  |  | c82b96580af8 | 54354408 | AA8tiO3d0Mm8L1tXxVrvjxUrC4ecwjg4 | 2ncs17NzxeXXlu0rdSVuWBy1PH9CQvvhtFWPK
[15](https://github.com/ct-Open-Source/tuya-convert/files/4907683/backup_20200711_210602.zip) |  | 🔴? |  |  | a4cf12e5b2ec | 62531570 | DAuwPH9PaBKgFzBg7Zq4CpUhYDzG4rDQ | y5Vsp5b5OTWUqLjp6kOLYxu0Z0PBByRTYuYym
[16d1](https://github.com/ct-Open-Source/tuya-convert/files/4981803/firmware-backup-devices.zip#firmware-backup-device1.bin) |  | 🔴29f7e05 |  |  | c82b964e3b29 | 64785071 | eDOnWtAUy5gJOiKtcXkNplBMqOMjJmM3 | ggD99i71cC7R7MTVnHadCtjaK28H2f6fOJLrG
[16d2](https://github.com/ct-Open-Source/tuya-convert/files/4981803/firmware-backup-devices.zip#firmware-backup-device2.bin) |  | 🔴29f7e05 |  |  | c82b964e3b22 | 64785071 | in18hm8DJch2NzlkjkSVHVuFJ3kpUo6k | hcXNpRfvnob0zqZWQ4zL4oxa0BHHRzC6jns3X
[17](https://github.com/ct-Open-Source/tuya-convert/files/5011017/tuya1way_flash_1M.zip) |  | 🔴317e50f |  |  | f4cfa209f296 | 02017786 | XAQxizdPqgrnvQbOIghkjPVfKfucx57H | jJ0OviSFn83XvHf8mkcqxtDPupbv9ahGcMMOk
[18](https://github.com/ct-Open-Source/tuya-convert/files/5015727/firmware-baf0cc.bin.zip) |  | 🟢e8c5810 |  | 0cc |  | 66058212 | lUYMJPQn6rXCboADiborfnCqTUreKyAT | 
[19b1](https://github.com/ct-Open-Source/tuya-convert/files/5016179/Backup.zip#Backup1_20200803_140803.bin) |  | 🔴317e50f |  |  | 600194fa3ee6 | 62520020 | ra6mACgWjH95YpxmYKGOY8lBJrBOApq0 | 2addWd7o1Qv9duggcFeklHqI3A3oSaKMJMrYx
[19b2](https://github.com/ct-Open-Source/tuya-convert/files/5016179/Backup.zip#Backup2_20200803_142458.bin) |  | 🔴317e50f |  |  | d8f15bb9ce4d | 62520020 | 54SbITkxFzL2bUPjFqijQJH3AxRdaT6e | 92JWevlzWoAHtlYEOHkX4LsCsQPGyqIWW3bEm
[20](https://github.com/ct-Open-Source/tuya-convert/files/5018720/Tuya_Backup_20200803_134931.zip) |  | 🔴29f7e05 | 🔴317e50f |  | 2462ab3d3499 | 80340470 | yXbeuWdxJyD8IVYCvukoSvKrApH4fOaf | Tln7d8Uou2pp8TtJbe5JTfdw3b7SYj2YOkmfY
[21](https://github.com/ct-Open-Source/tuya-convert/files/5037513/old-original-fw.zip) |  | 🟢898b733 |  | b4e |  | 27080852 | mJOBHtZuvzvAK0g8JiRaqyYHn2FOS5Cb | 
[22](https://github.com/ct-Open-Source/tuya-convert/files/5059741/backup_BW-LT29.zip) |  | 🔴29f7e05 |  |  | 50029178b020 | 54436323 | AG1rTspXIeEv0VIciXnD8kAcGu8QUR4c | bPzGF9hhpAOCzTZ1bnyEPcLtFXnQlMJSxF1A0
[23](https://github.com/ct-Open-Source/tuya-convert/files/5067474/backup_20200812_163954.zip) |  | 🟢898b733 |  | 133 |  | 06847238 | iL4ePi4zaV1V7TjAgOWKcyzBkdI34e2r | 
[24](https://github.com/ct-Open-Source/tuya-convert/files/5069154/MoesGarageDoor.zip) |  | 🟢e8c5810 |  | 6ac |  | 03733058 | rlPU5cNvqskvc5TpT6tA2AfupOyLrlYl | 
[25](https://github.com/ct-Open-Source/tuya-convert/files/5071350/firmware-backup.zip) |  | 🔴317e50f |  |  | fcf5c4800682 | 40426764 | UOLjYJbk07gHZO0VBHaZshkxW65HsW0d | WgWAqXlPnX8qAdaD8GU2Ljoa8TYaTcD65r6Ur
[26](https://github.com/ct-Open-Source/tuya-convert/files/5080563/firmware-backup.zip) |  | 🔴317e50f |  |  | c82b96ccd0e2 | 68116280 | 3KEWyyZHNAOzqyZ8gHpu1IqLasrMlOJZ | pfQ9jVNRUArItWV4qaSUuP3ojC5vsXY0L6SIB
[27](https://github.com/Elkropac/esp-firmware-backup/blob/master/aofo_socket/firmware-backup.bin) |  | 🔴29f7e05 |  |  | d8f15bdf7e98 | 20432477 | 5RpboSdogNamQInfsrpMeVbr01fvAd9V | eH3eYWXmNxaAxTJXPLhJSCucK0N8VkPwCxp24
[28](https://github.com/Elkropac/esp-firmware-backup/blob/master/zemismart_downlight/firmware-backup.bin) |  | 🔴317e50f |  |  | fcf5c4800682 | 40426764 | UOLjYJbk07gHZO0VBHaZshkxW65HsW0d | WgWAqXlPnX8qAdaD8GU2Ljoa8TYaTcD65r6Ur
[29](https://drive.google.com/file/d/1VtKJz6VznqlBdR5x_OySgMEKB6OoGbIR/view?usp=sharing) |  | 🔴317e50f |  |  | 50029117b5d0 | 07045557 | CTuF4WV3hKInKYPt6QrJPgX9LaK9M4Bk | gibTC21CwXiuH4S3Wjg2wOOqj0Tx1PTtnCknc
[30](https://github.com/ct-Open-Source/tuya-convert/files/4881063/firmware-9c52d8.bin.gz) |  | 🟢e8c5810 |  | 2d8 |  | 56435352 | ZJO0QadxOoDTlPFbwW8Larh2r7L8AOBW | 
[31](https://github.com/ct-Open-Source/tuya-convert/files/4881064/firmware-52a6fb.bin.gz) |  | 🟢898b733 |  | 6fb |  | 04453323 | yzCEW1vz7Y1ZvoCEeEynhxO36JVdZcKA | 
[32](https://github.com/ct-Open-Source/tuya-convert/files/4881065/firmware-a068f4.bin.gz) |  | 🟢898b733 |  | 8f4 |  | 78677700 | HkXr1p695mO3YpjniaFqhR7PFd3XDHpB | 
[33](https://github.com/ct-Open-Source/tuya-convert/files/4881066/firmware-a0709d.bin.gz) |  | 🟢898b733 |  | 09d |  | 78677700 | DAY0eL57GnmVALIvgqDm7YUVkzsWuAEh | 
[34b](https://drive.google.com/file/d/1hp39MsYcBcs9J3TP-fvSbwExhxE9OTQ0/view?usp=sharing) |  | 🟢e8c5810 |  | 610 |  | 50135502 | 0Pefl6UBLqtAvamfrPBimHvM7Oy2AOek | 
[34a1](https://drive.google.com/file/d/1qoh6I7l_Pod-Mqlm6ueOxtrMb65UBbuy/view?usp=sharing) | [✅](https://drive.google.com/file/d/1cHvrW2p7CmO9tF1GvJ1RZ2mUXha_Al3y/view?usp=sharing) | 🟢e8c5810 | 🟡8d30f72 | 610 |  | 50135502 | 0Pefl6UBLqtAvamfrPBimHvM7Oy2AOek | 
[34a2](https://drive.google.com/file/d/1vauElr2v8wzsW5nsNx5cC8XmKP_pxqJl/view?usp=sharing) |  | 🟢e8c5810 | 🟡8d30f72 | 610 |  | 50135502 | 0Pefl6UBLqtAvamfrPBimHvM7Oy2AOek | 
[34a3](https://drive.google.com/file/d/1CbihDyMF9bwTVEcM-JBJJPWg54fkCA57/view?usp=sharing) |  | 🟢e8c5810 | 🟡8d30f72 | 610 |  | 50135502 | 0Pefl6UBLqtAvamfrPBimHvM7Oy2AOek | 
[35](https://drive.google.com/file/d/1Im1MXfnPsr1JYGHsrD_wbz3NYd8o1ve_/view?usp=sharing) |  | 🔴317e50f | |  | 8caab5e5a280 | 87860851 | fCAAa6f5iNYRj7NzCZGPWpnzMq4cOizF | WSWCRf3nG93ttY4j90V3HGXjB1sDeCXYBoVVa
[36](https://drive.google.com/file/d/1ilAbKvsUMM1mAl-XiT2gJPrUJWhU03xM/view?usp=sharing) |  | 🔴317e50f | | | c82b966b3de4 | 05653062 | IG95zG4NOs4hKNtLHxAGz1Mu9h9UiEj1 | PeB57pbhtNUVANIstnaGUFBGWyWjwLqWf1uBk
[37](https://github.com/ct-Open-Source/tuya-convert/files/6470124/wp5_02.bin.gz) |  | 🔴317e50f | | | 70039f8968a6 | 22057624 | x9cW1Vg3FEr6s7RKoys8FmTj5SgGHGqO | k8WTEIHdy0VBeqovXFdSo2WxwuvlwTLbMZJt1
[38](https://github.com/ct-Open-Source/tuya-convert/files/6470144/wp5_03.bin.gz) |  | 🔴317e50f | | | 24a16016e177 | 00080070 | whhqiFzXBinHg33dheVvwyWhRJBBcFV4 | gIjRhFwGBgSibk8czel34IsYoWmImUi2lnjwQ
[39](https://drive.google.com/file/d/1nlIC8da5J0kvIZijlKlHp2ajeqAtyuEY/view?usp=sharing) | [✅] | 🔴29f7e05| | | e09806009aed | 35558538 | CRiNIby4WavZFUX7enncDcFK0M43WQRM | fJNQuzsUEBT8TIY88fpATIdaSka3dfZ0hp1Bu
[40](https://we.tl/t-TKAB7wSbwM) | [✅] | 🔴29f7e05| | | d8f15bad691d | 40014435 | KLeaREf1DijkQ5uFmPidcE0gv0A4VfQG | YR0fEdw2QVwyhCCqwJDBd4WiU1G8BhQPzd9bC


- There can be two firmware builds in a single 1MB image if the device has been updated; listed as SDK_ver_A and SDK_ver_B
- 🟢 build doesn't know about pskKey (Tuya-Convert probably works)
- 🟡 build knows about pskKey but doesn't appear to have one set
- 🔴 build knows about pskKey and has one set in 0xfb000 JSON blob
- 11 is interesting because it is not upgraded and a build known to use pskKey elsewhere, but doesn't include the string literal pskKey
- 13 is an older SDK ver (1.4.2 compiled @ Sep 22 2016 13:09:03) and has full MAC address as mac rather than mac_addr
- 15 is missing the "OS SDK ver:" string
- 34 are the following firmwares: Original + 3 different upgrades (from the same device) via reflashing original and then upgrading. Hope this helps. I'm available on digiBlur's discord channel @jschwalbe#6176 - hit me up if any questions or something you need that I missed.
- The pcap from 34a1 shows a spurious retransmit of a "change cipher spec" which prevents wireshark/tshark from decoding the response to the `tuya.device.uuid.pskkey.get` call.  Ignoring that packet allows it to be decoded, yielding the following JSON: `{"result":"EqY/PCRBZBAhkpujEEx/X9NrCDCOWuqpmCBIXztwprnMeDhTV4cd9flrbszbTDFlmQ99FJWjDwwrsjr9uDBjKGJ76hlBrDLSxPXMJvFfyMrM6sQezfgCpkIpys5lOBK7","sign":"5dd1747ae9294467","t":1599425271}`
- 35 are images of 2 identical devices, one booted original firmware and tryed wifi flashing, other never booted original fw.
- None of the images captured so far of a Tuya-Convert compatible build that are updated to an incompatible pskKey build include the pskKey in the JSON blob at 0xfb000

## Additional Network Captures
- https://github.com/ct-Open-Source/tuya-convert/files/4142919/bakibo_bulp_pcap.zip
- https://github.com/ct-Open-Source/tuya-convert/files/4205411/bakiboT22Y.pcap.zip

## Strings
```
OS SDK ver: 2.0.0(29f7e05) compiled @ Sep 30 2019 11:19:12
[N]%s:%d metedata is without encryption, cover this partition with encrypted data
[N]%s:%d var block [%d] last version is without encryption,now need to encrypt data and cover this partition
[ERR]%s:%d flash_aes128_ecb_encrypt err
[ERR]%s:%d !!!!!!CHIP_MAC:%s FLASH_MAC:%s!!!!!!
aes-internal-dec.c
aes-internal-enc.c
lhttps://a3.tuyacn.com/gw.json
https://a3.tuyaeu.com/gw.json
https://a3-ueaz.tuyaus.com/gw.json
https://a3.tuyaus.com/gw.json
{"mac_addr":"500291e8f141","prod_idx":"26636676","auz_key":"wg7xdxUcsi7W0EmnPUlEtuwoyZwcF2W2","pskKey":"GUKgTWzsxGCn8UR5tIFFluuKD2qA8FYmaZwY2","prod_test":false}
{"ap_ssid":"SmartLife","ap_pwd":null}
{"CC":"CN"}
vtrust-flash
ESP_E8F141
vtrust-flash
```
***

Novostella RBGWC 13W E27
`{"mac_addr":"e098060153ad","prod_idx":"80157022","auz_key":"ksJHynYgCMs7caHDzXtvb8EwtCtFsLxC","pskKey":"eZklnPtc0xuRVn8mf6bj1Hzarr7p7uTBfgKt3","prod_test":false}`
``

## Useful Info/Links
- The [tuyapi library](https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md) has interesting info including developer accounts at https://iot.tuya.com/ and although deprecated, some MITM procedure to get ID and keypairs.
- Tools for reverse engineering of Tuya API signing algo https://github.com/nalajcie/tuya-sign-hacking

## More Investigations in Tuya IoT Platform:
- Cloud tokens are security encryption certificates that Tuya issues to devices. They are credentials for smart devices to connect to Tuya Cloud. Each device shall have a unique token. If you use a Tuya standard module SDK to develop your products, purchase modules and the same number of tokens.
- Also this might be interesting: https://developer.tuya.com/en/docs/iot/device-development/tuya-development-board-kit/tuya-sandwich-evaluation-kits/development-guide/authorization-code-firmware-burning?id=K9br41pefnksv

## Reverse Engineering Tools
maybe this helps someone: https://github.com/xety1337/tuya-reverse

## Using mitmproxy with a rooted Android device and TCP Smart
* It is possible to use mitmproxy to inspect the TLS traffic when pairing one of these devices using the Android TCP Smart application
* The application will note that it is being run on a rooted device, but will permit you to continue
* The mitmproxy certificate must be installed as a system certificate, as pretty much everything on Android will not trust a user certificate and will ignore the cert
* Note that the the smart device will need access to a DHCP server, so this may influence your proxy setup
* The pairing won't complete if the smart device is proxied, as the device won't trust the mitmproxy certificate
* Unless there are alternative methods for configuring pinning, network_security_config.xml suggests that the Android app is not using certificate pinning
* Proxying just the Android device (and not the smart device) allows the pairing process to complete
* When decrypted, the TLS communication between the app and the servers is json encoded and appears to be encrypted and signed (I can understand the latter as an additional authentication step, but not the former)
* Next steps:
  * Find out how the communication between the app and the servers is further encrypted
  * Attempt to build firmware for the smart device that has the mitmproxy embedded?

