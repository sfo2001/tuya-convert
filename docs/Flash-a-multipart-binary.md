# Flashing a Multipart Binary

**Last Updated:** 2025-11-06
**Status:** ✅ Complete

## Overview

This guide explains how to combine multiple firmware binaries into a single binary file for flashing with tuya-convert. Some third-party firmware projects require flashing multiple files to different locations in flash memory. Since tuya-convert requires a single binary file (with a 512KB limit for first upload), you need to assemble the individual files into one combined binary before flashing.

**Note:** This method is deprecated for esp-HomeKit-devices as they now use a combined binary, but the technique can be applied to other projects requiring multiple binary files.

## Prerequisites

- Linux/Unix environment (or WSL on Windows)
- `truncate` utility (typically pre-installed)
- `cat` utility (typically pre-installed)
- Hex editor (optional, for verification)
- tuya-convert installed and configured
- Individual firmware binary files from your third-party firmware project
- Knowledge of the flash memory offsets for each binary

## Understanding Flash Memory Layout

When a firmware project asks you to flash multiple files, each file must be placed at a specific memory address (offset) in the ESP chip's flash memory. For example:

- `bootloader.bin` at offset `0x0` (start of flash)
- `config.bin` at offset `0x1000` (4KB from start)
- `firmware.bin` at offset `0x2000` (8KB from start)

To create a single binary, we need to ensure each file segment ends exactly where the next segment should begin.

## Example: esp-homekit-devices

This example follows the original installation instructions from [esp-homekit-devices](https://github.com/RavenSystem/esp-homekit-devices/wiki/Installation), which requires three separate binaries:

1. **[rboot.bin](https://github.com/SuperHouse/esp-open-rtos/raw/master/bootloader/firmware_prebuilt/rboot.bin)** - Bootloader to be flashed at `0x0`
2. **[blank_config.bin](https://github.com/SuperHouse/esp-open-rtos/raw/master/bootloader/firmware_prebuilt/blank_config.bin)** - Configuration to be flashed at `0x1000`
3. **[haaboot.bin](https://github.com/RavenSystem/haa_ota/releases/latest/download/haaboot.bin)** - Main firmware to be flashed at `0x2000`

### Step 1: Download the Firmware Files

Download all required binary files to a working directory:

```bash
wget https://github.com/SuperHouse/esp-open-rtos/raw/master/bootloader/firmware_prebuilt/rboot.bin
wget https://github.com/SuperHouse/esp-open-rtos/raw/master/bootloader/firmware_prebuilt/blank_config.bin
wget https://github.com/RavenSystem/haa_ota/releases/latest/download/haaboot.bin
```

### Step 2: Calculate Required Padding

For each file (except the last one), we need to pad it to end at the offset where the next file should begin:

- `rboot.bin` must end at `0x1000` (4KB)
- `blank_config.bin` must end at `0x2000` (8KB from start, so 4KB in size)
- `haaboot.bin` doesn't need padding (it's the last file)

### Step 3: Pad the Files

Use the `truncate` command to pad files to the correct size:

**Pad rboot.bin to 4KB (0x1000 bytes):**
```bash
truncate -s 4k rboot.bin
```

**Pad blank_config.bin to 4KB:**
```bash
truncate -s 4k blank_config.bin
```

**Note:** We don't pad `haaboot.bin` as there are no files after it.

### Step 4: Concatenate the Files

Combine all padded files into a single binary:

```bash
cat rboot.bin blank_config.bin haaboot.bin > thirdparty.bin
```

This creates `thirdparty.bin` with the correct memory layout.

### Step 5: Verify the Binary (Optional)

Open `thirdparty.bin` in a hex editor and verify that each segment is at the correct offset within the file:

- First segment starts at `0x0000`
- Second segment starts at `0x1000`
- Third segment starts at `0x2000`

### Step 6: Flash with tuya-convert

1. Copy `thirdparty.bin` to your tuya-convert `files/` directory:
   ```bash
   cp thirdparty.bin ~/tuya-convert/files/
   ```

2. Run the standard tuya-convert flashing process:
   ```bash
   cd ~/tuya-convert
   ./start_flash.sh
   ```

3. When prompted, select `thirdparty.bin` as your custom firmware

**Code Reference:** See `scripts/firmware_picker.sh` for firmware selection

## Converting Flash Offsets to File Sizes

Common flash offset conversions:

| Hex Offset | Decimal | Size for truncate |
|------------|---------|-------------------|
| 0x1000 | 4096 | 4k |
| 0x2000 | 8192 | 8k |
| 0x4000 | 16384 | 16k |
| 0x8000 | 32768 | 32k |
| 0x10000 | 65536 | 64k |

Use an online hex to decimal converter or the `printf` command:

```bash
printf "%d\n" 0x1000
# Output: 4096
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Device won't boot after flashing | Incorrect offsets or padding | Verify flash offsets in the firmware documentation and re-create the binary |
| Flash fails with "file too large" error | Combined binary exceeds 512KB | Check firmware sizes; initial OTA flash is limited to 512KB |
| Device boots but doesn't work properly | Files concatenated in wrong order | Verify the order matches the flash memory layout |
| truncate command not found | Missing coreutils package | Install coreutils: `sudo apt-get install coreutils` |
| Hex editor shows gaps or overlaps | Incorrect truncate size | Recalculate padding: next_offset minus current_offset |

## Related Pages

- [Installation Guide](Installation) - Initial tuya-convert setup
- [Quick Start Guide](Quick-Start-Guide) - Standard flashing procedure
- [Using a Raspberry Pi](Using-a-Raspberry-Pi) - Raspberry Pi setup for tuya-convert
- [Troubleshooting](Troubleshooting) - Common issues and solutions

## References

- [esp-homekit-devices Installation Guide](https://github.com/RavenSystem/esp-homekit-devices/wiki/Installation)
- [ESP8266 Flash Layout](https://arduino-esp8266.readthedocs.io/en/latest/filesystem.html#flash-layout)
- [esptool.py Documentation](https://github.com/espressif/esptool)
- Internal code: `scripts/firmware_picker.sh` - Firmware selection interface
- Internal code: `scripts/flash_esp.sh` - ESP flashing logic

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
