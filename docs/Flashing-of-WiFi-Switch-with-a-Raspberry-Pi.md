# Flashing WiFi Switch with Raspberry Pi via Serial

**Last Updated:** 2025-11-06
**Status:** ✅ Complete

## Overview

This guide covers manual serial flashing of Tuya devices using a Raspberry Pi when OTA flashing with tuya-convert is not possible. This method requires opening the device, connecting directly to the ESP chip's test points, and flashing via serial connection. This is an advanced procedure that requires hardware skills including soldering and circuit tracing.

**Important:** This method is necessary for devices manufactured after early 2020, as the tuya-convert OTA vulnerability was fixed (see [issue #483](https://github.com/ct-Open-Source/tuya-convert/issues/483)).

## Prerequisites

### Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- Tuya device to be flashed (already opened)
- Soldering iron and solder
- Multimeter (for continuity testing)
- 3.3V/5V power source or voltage converter
- Jumper wires
- Magnifying glass or microscope (recommended)
- **Warning:** Risk of device damage and electric shock

### Software Requirements

- Raspberry Pi OS (Raspbian) configured
- esptool.py installed
- Tasmota firmware binary (tasmota.bin)
- Basic knowledge of serial communication
- ESP chip datasheet for reference

### Knowledge Requirements

- Basic understanding of electronics and circuit boards
- Ability to read circuit board traces
- Soldering skills
- Understanding of serial communication (UART)
- Knowledge of ESP8266/ESP8285 pinout

## Background: Why Manual Serial Flashing?

### The Tuya Cloud Ecosystem

Many smart home devices are manufactured by Tuya and rebranded by third-party companies (Sonoff, AVATTO, etc.). These devices are natively integrated with the Tuya cloud, which can:

- Operate devices remotely
- Upload new firmware via OTA
- Collect usage data

### Security and Privacy Concerns

The cloud integration may be considered:
- A security risk in your home network
- A privacy concern due to data collection
- A reliability issue if cloud services are unavailable

### The Alternative: Local Control

By flashing open-source firmware (like Tasmota), you can:
- Operate devices locally without cloud dependency
- Integrate with home automation systems (Home Assistant, Domoticz, Alexa, Google)
- Maintain privacy and security
- Ensure continued functionality regardless of cloud service status

## Configure Raspberry Pi Serial

### Enable Hardware Serial Port

The Raspberry Pi 3 and 4 have two serial ports that need to be properly configured:

**Follow one of these guides to edit `/boot/config.txt` and `/boot/cmdline.txt`:**
- [Configuring GPIO Serial Port on Raspbian Jessie](https://spellfoundry.com/2016/05/29/configuring-gpio-serial-port-raspbian-jessie-including-pi-3-4/)
- [Enable Serial Port on Raspberry Pi](https://hallard.me/enable-serial-port-on-raspberry-pi/)

**Alternative:** Use any USB-to-Serial adapter or Arduino serial interface instead of GPIO pins.

**Code Reference:** Serial configuration affects GPIO UART at `/dev/ttyS0` or `/dev/ttyAMA0`

## Install esptool

esptool.py is required for flashing ESP chips via serial connection.

**Follow the installation procedure:**
[Tasmota esptool Download Guide](https://tasmota.github.io/docs/Esptool/#download-esptool)

**Quick install:**
```bash
sudo pip3 install esptool
```

Verify installation:
```bash
esptool.py version
```

## Reverse Engineering: Identifying Test Points

This section applies to a specific device example but the principles apply to any Tuya device.

### Understanding Test Points

Test points are connection pads on the circuit board used by manufacturers for:
- Flashing firmware during production
- Quality control testing
- Debug access

**What you need to find (6 test points typical):**
1. **VCC (3.3V)** - Power supply
2. **GND (0V)** - Ground
3. **TX** - Serial transmit from ESP
4. **RX** - Serial receive to ESP
5. **GPIO0** - Flash mode enable (must be grounded during boot)
6. **Button GPIO** - Optional, usually connected to physical button

### Step 1: Visual Inspection

![Example Device Board](https://user-images.githubusercontent.com/4344157/93678312-5294ef80-faad-11ea-891a-99ed5893b5c9.png)

**Identify the ESP chip:**
- Look for a black square IC (typically ESP8266 or ESP8285)
- Locate test points (circular pads, usually in a row)
- Note component markings and labels

### Step 2: Identify the Test Points

![Test Points Close-up](https://user-images.githubusercontent.com/4344157/93675825-570cd880-faac-11ea-86db-cab972c76687.jpg)

**Typical test point layout (labeled A, B, C, D, E, F in this example):**
- Usually located near the ESP chip
- May be on the same side or opposite side of the board
- Connected to ESP pins via traces or through-holes

### Step 3: Trace Connections

![Board Traces](https://user-images.githubusercontent.com/4344157/93675832-57a56f00-faac-11ea-8e5b-db9c40ab4bd1.jpg)

**How to trace connections:**
1. Use multimeter in continuity mode
2. Check connections between test points and ESP pins
3. Follow board traces (may require flipping board)
4. Look for through-holes connecting front to back

**Tracing tips:**
- GND is typically connected to large copper areas
- VCC often has bypass capacitors nearby
- TX/RX are direct connections to ESP U0TXD/U0RXD pins
- Button typically connects to a GPIO through a pull-up resistor

### Step 4: Map Test Points to ESP Pins

![Connection Scheme](https://user-images.githubusercontent.com/4344157/93706962-70089e80-fb2b-11ea-91fe-259753d1a660.png)

**For this example device, the mapping is:**
- **Pin A:** ESP GPIO (button control)
- **Pin B:** U0RXD (Serial receive)
- **Pin C:** U0TXD (Serial transmit)
- **Pin D:** GPIO0 (Flash mode enable)
- **Pin E:** VDDA (3.3V power)
- **Pin F:** GND (Ground)

**Verification methods:**
- Check continuity with multimeter
- Compare with ESP datasheet pinout
- Look for voltage levels (3.3V on VCC, 0V on GND)

### ESP Chip Datasheets

Download the appropriate datasheet for your chip:

**ESP8266:**
- [ESP8266EX Datasheet (PDF)](https://www.espressif.com/sites/default/files/documentation/0a-esp8266ex_datasheet_en.pdf)

**ESP8285:**
- [ESP8285 Datasheet (PDF)](https://www.espressif.com/sites/default/files/documentation/0a-esp8285_datasheet_en.pdf)

## Connection to Raspberry Pi

### Connection Scheme

![Raspberry Pi Connection](https://user-images.githubusercontent.com/4344157/93675839-583e0580-faac-11ea-99dc-b309b40f227c.jpg)

**Basic wiring:**
- Raspberry Pi GPIO TX → ESP RX (Serial receive)
- Raspberry Pi GPIO RX → ESP TX (Serial transmit)
- Raspberry Pi GND → ESP GND
- Power source → ESP VCC (3.3V)

### Power Considerations

**⚠️ Important:** Raspberry Pi 3.3V output typically cannot provide enough current for ESP chips during flashing.

**Solutions:**
1. **Use external 3.3V power supply** (recommended)
2. **Use Raspberry Pi 5V with voltage converter** (if device has onboard regulator)
3. **Power through device's power converter** (e.g., AMS1117)

**For this example device:**
- Connect Raspberry Pi 5V to the device's internal voltage converter (AMS1117 Vin pin)
- Do NOT connect Raspberry Pi 3.3V directly to ESP VDDA
- See [AMS1117 Datasheet](http://www.advanced-monolithic.com/pdf/ds1117.pdf) for voltage regulator details

### Wiring Table

| Raspberry Pi GPIO | ESP Chip Pin | Test Point | Notes |
|-------------------|--------------|------------|-------|
| TX (GPIO 14) | U0RXD | Pin B | Cross connection |
| RX (GPIO 15) | U0TXD | Pin C | Cross connection |
| GND | GND | Pin F | Common ground required |
| (External 3.3V) | VDDA | Pin E | Or use device power supply |
| - | GPIO0 | Pin D | Ground during boot to enable flash mode |

## Validate Setup: ESP Communication Test

Before flashing, verify the connection is working.

**Test command:**
```bash
esptool.py --port /dev/ttyS0 chip_id
```

**Expected output:**
```
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
Crystal is 26MHz
MAC: xx:xx:xx:xx:xx:xx
Uploading stub...
Running stub...
Stub running...
Chip ID: 0x00xxxxxx
```

If this works, your connections are correct and you can proceed to flashing.

## Flash Procedure

### Step 1: Enable Flash Mode

**Ground GPIO0 during boot:**
- Hold the device button (if connected to GPIO0), or
- Connect GPIO0 test point to GND with jumper wire

**Power cycle the device:**
- Disconnect power
- Ensure GPIO0 is grounded
- Reconnect power
- ESP enters flash mode (ready to receive firmware)

### Step 2: Erase Flash

**Clear the existing firmware:**
```bash
esptool.py --port /dev/ttyS0 erase_flash
```

**Expected output:**
```
Erasing flash (this may take a while)...
Chip erase completed successfully in X.Xs
```

### Step 3: Flash Tasmota Firmware

**Write the Tasmota binary:**
```bash
esptool.py --port /dev/ttyS0 write_flash -fm dout 0x0 tasmota.bin
```

**Parameters explained:**
- `--port /dev/ttyS0` - Serial port (may be `/dev/ttyAMA0` depending on configuration)
- `write_flash` - Flash writing command
- `-fm dout` - Flash mode (Dual Output)
- `0x0` - Starting address (beginning of flash)
- `tasmota.bin` - Firmware file

**Expected output:**
```
Writing at 0x00000000... (x %)
...
Hash of data verified.
Leaving...
Hard resetting via RTS pin...
```

### Step 4: Test the Device

1. Disconnect GPIO0 from GND
2. Power cycle the device
3. Device should boot into Tasmota
4. Look for Tasmota WiFi access point (tasmota-XXXX)

**Code Reference:** See `scripts/flash_esp.sh` for automated flashing logic

## Post-Flashing Configuration

After successfully flashing Tasmota, you need to configure the GPIO mapping to match your device hardware.

### Configure Device Template

The device needs to know which GPIO pins control which functions (relay, LED, button, etc.).

**For this specific example device:**
```json
{"NAME":"Switch","GPIO":[0,0,0,0,0,17,0,0,21,0,0,0,0],"FLAG":0,"BASE":18}
```

**How to apply template:**
1. Connect to Tasmota WiFi AP
2. Configure WiFi settings
3. Access web interface at device IP
4. Go to Configuration → Configure Template
5. Paste the template JSON
6. Save and reboot

**Creating templates for new devices:**
- Follow the [Tasmota Configuration Guide](https://tasmota.github.io/docs/Configuration-Procedure-for-New-Devices/)
- Test each GPIO pin to determine its function
- Create template for future use
- Share on [Tasmota Device Templates Repository](https://templates.blakadder.com/)

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| esptool cannot detect chip | Wrong serial port or bad connections | Try `/dev/ttyAMA0` instead of `/dev/ttyS0`, check continuity of all connections |
| Device won't enter flash mode | GPIO0 not grounded during boot | Ensure GPIO0 is connected to GND before powering on |
| Flash operation fails midway | Power supply insufficient or unstable | Use external 3.3V power supply with adequate current (250mA+) |
| Device doesn't boot after flash | Wrong flash mode or corrupted binary | Reflash with `-fm dout` mode, verify tasmota.bin file integrity |
| TX/RX reversed | Common mistake | Swap TX and RX connections between Raspberry Pi and ESP |
| Serial communication errors | Baud rate mismatch | esptool auto-detects baud rate, but ensure no interference on serial lines |
| Cannot find test points | Points on opposite side or hidden | Check both sides of PCB, look near ESP chip and power regulator |

## Related Pages

- [Using a Raspberry Pi](Using-a-Raspberry-Pi) - Standard Raspberry Pi setup for tuya-convert
- [Installation Guide](Installation) - Initial tuya-convert setup
- [Quick Start Guide](Quick-Start-Guide) - OTA flashing method (when available)
- [Compatible Devices](Compatible-devices) - Check device compatibility
- [Troubleshooting](Troubleshooting) - General troubleshooting

## References

- [NodeMCU Flash Documentation](https://nodemcu.readthedocs.io/en/master/flash/)
- [Tasmota Installation Guide](https://tasmota.github.io/docs/Getting-Started/)
- [esptool.py GitHub Repository](https://github.com/espressif/esptool)
- [ESP8266 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp8266-technical_reference_en.pdf)
- [Tasmota Device Configuration](https://tasmota.github.io/docs/Configuration-Procedure-for-New-Devices/)
- [Tasmota Templates Repository](https://templates.blakadder.com/)

## Safety Warning

**⚠️ WARNING:**
- Working with mains voltage devices can be dangerous
- Always disconnect from power before opening devices
- Use appropriate safety equipment
- Understand the risks of hardware modification
- Proceed at your own risk
- Device warranty will be voided

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
