# Testing Guide for Virtual Environment Fix (Issue #1159)

This document describes how to test the virtual environment implementation that fixes the "externally managed environment" error on modern Linux distributions.

## Related Issue

This fix addresses [upstream issue #1159](https://github.com/ct-Open-Source/tuya-convert/issues/1159) - "error: This environment is externally managed"

## Overview

The fix implements Python virtual environment (venv) support to comply with PEP 668, which is enforced on:
- Debian 12+ (Bookworm)
- Ubuntu 23.04+
- Fedora 38+
- Raspberry Pi OS (latest)
- Other modern Linux distributions

## Testing Levels

### Level 1: Basic Syntax Validation (Automated)

These tests verify that the bash scripts have no syntax errors:

```bash
# Test install_prereq.sh syntax
bash -n install_prereq.sh
echo "install_prereq.sh syntax: $?"

# Test start_flash.sh syntax
bash -n start_flash.sh
echo "start_flash.sh syntax: $?"

# Test activate_venv.sh syntax
bash -n activate_venv.sh
echo "activate_venv.sh syntax: $?"
```

Expected output: All return codes should be 0 (success)

### Level 2: Installation Testing

Test the installation process on target distributions:

#### Prerequisites
- Fresh installation or clean VM/container of target OS
- Internet connection
- Git installed

#### Test Steps

1. **Clone the repository**
   ```bash
   git clone <your-fork-url>
   cd tuya-convert
   git checkout <your-branch>
   ```

2. **Run installation script**
   ```bash
   ./install_prereq.sh
   ```

3. **Verify virtual environment creation**
   ```bash
   # Check if venv directory exists
   ls -la venv/

   # Check if Python is in venv
   ls -la venv/bin/python*

   # Check if pip is in venv
   ls -la venv/bin/pip*
   ```

4. **Verify Python packages are installed in venv**
   ```bash
   source venv/bin/activate
   pip list | grep -E 'paho-mqtt|tornado|pycryptodomex|sslpsk'
   deactivate
   ```

   Expected packages:
   - paho-mqtt
   - tornado
   - pycryptodomex
   - sslpsk

5. **Test manual activation helper**
   ```bash
   source ./activate_venv.sh
   which python3
   # Should point to ./venv/bin/python3
   deactivate
   ```

### Level 3: Start Script Testing

Test that start_flash.sh properly activates the virtual environment:

1. **Check venv auto-activation**
   ```bash
   # This will fail at network configuration (expected)
   # but should successfully activate venv
   ./start_flash.sh
   ```

   Expected output:
   - "Activating Python virtual environment..."
   - No "WARNING: Virtual environment not found!" message

2. **Verify Python scripts can find dependencies**
   ```bash
   source venv/bin/activate

   # Test imports
   python3 -c "import paho.mqtt.client; print('paho-mqtt: OK')"
   python3 -c "import tornado; print('tornado: OK')"
   python3 -c "import Cryptodome; print('pycryptodomex: OK')"
   python3 -c "import sslpsk; print('sslpsk: OK')"

   deactivate
   ```

   Expected output: All imports should succeed with "OK" messages

### Level 4: Integration Testing (Full System)

**WARNING:** This requires compatible hardware and a Tuya device. Only perform if you have the proper setup.

1. Follow the normal tuya-convert procedure
2. Run `./start_flash.sh`
3. Verify all services start correctly (AP, web server, MQTT, PSK, discovery)
4. Verify Python scripts can communicate with the device

Expected behavior:
- No Python import errors
- All services start successfully
- Device flashing works as expected

## Test Matrix

| Distribution | Version | Install Test | Start Test | Full Test | Status |
|--------------|---------|--------------|------------|-----------|--------|
| Debian       | 12 (Bookworm) | ⏳ Needed | ⏳ Needed | ⏳ Needed | Untested |
| Ubuntu       | 23.04+ | ⏳ Needed | ⏳ Needed | ⏳ Needed | Untested |
| Ubuntu Server| 22.04 LTS | ⏳ Needed | ⏳ Needed | ⏳ Needed | Untested |
| Raspberry Pi OS | Latest | ⏳ Needed | ⏳ Needed | ⏳ Needed | Untested |
| Fedora       | 38+ | ⏳ Needed | ⏳ Needed | ⏳ Needed | Untested |
| Kali Linux   | 2024+ | ⏳ Needed | ⏳ Needed | ⏳ Needed | Untested |
| Arch Linux   | Rolling | ⏳ Needed | ⏳ Needed | ⏳ Needed | Untested |

Legend:
- ✅ Passed
- ❌ Failed
- ⏳ Needed
- ⚠️ Partially working

## Backward Compatibility Testing

Test that the fix doesn't break existing installations:

### Test on Older Distributions (Pre-PEP 668)

Distributions like Debian 11, Ubuntu 20.04, Raspberry Pi OS Buster should continue to work:

1. Run `./install_prereq.sh`
2. Verify venv is created (new behavior)
3. Verify scripts still work (no regression)

### Test Docker Installation

Docker installation should be unaffected:

1. Follow Docker instructions in README
2. Verify container builds successfully
3. Verify tuya-convert works in container

## Reporting Test Results

If you test this implementation, please report your results by:

1. Creating an issue in the repository with:
   - Distribution name and version
   - Test level performed (1-4)
   - Results (pass/fail)
   - Any errors or warnings encountered
   - Relevant log snippets

2. Or submitting a PR that updates the Test Matrix above

## Known Limitations

1. The virtual environment adds ~50MB of disk space usage
2. Users must ensure venv is activated if running Python scripts manually
3. Some system monitoring tools may not detect the venv-installed packages

## Rollback Procedure

If the virtual environment causes issues, you can roll back:

```bash
# Remove virtual environment
rm -rf venv/

# Install packages system-wide (old method, may fail on modern distros)
sudo python3 -m pip install --user paho-mqtt tornado pycryptodomex
sudo python3 -m pip install --user git+https://github.com/drbild/sslpsk.git

# Or use --break-system-packages flag (not recommended)
python3 -m pip install --break-system-packages --user paho-mqtt tornado pycryptodomex
python3 -m pip install --break-system-packages --user git+https://github.com/drbild/sslpsk.git
```

## Questions or Issues

If you encounter issues during testing:
1. Check the TROUBLESHOOTING section in README.md
2. Verify all test steps were followed correctly
3. Open an issue with detailed information about your environment and error messages
