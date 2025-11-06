# Analysis of Issue #1167: Virtual Environment PATH Not Honored in Screen Sessions

**Issue**: Ubuntu non-docker deps issue
**Reporter**: mitchcapper
**Date**: October 15, 2025
**Status**: Open, Unaddressed
**Upstream**: https://github.com/ct-Open-Source/tuya-convert/issues/1167

---

## Executive Summary

Issue #1167 reports that despite the project implementing virtual environment support (to comply with PEP 668), the virtual environment PATH is not properly preserved when launching Python scripts through screen sessions with sudo. This causes Python scripts to fail finding their dependencies (particularly `sslpsk`, which has no system package equivalent on Ubuntu).

## Problem Description

### Context
Modern Linux distributions implement PEP 668 ("Marking Python base environments as 'externally managed'"), preventing `pip install` on system Python without `--break-system-packages` flag. The tuya-convert project addressed this by implementing virtual environment support.

### The Core Issue
The reporter discovered that even with a working virtual environment:
1. System packages exist for `tornado` and `pycryptodome` (as `python3-tornado`, `python3-pycrypto`)
2. **No system package exists for `sslpsk`** - it must come from the venv
3. The current implementation fails to preserve the venv PATH when launching processes via `sudo screen`

### User's Findings
The reporter attempted to use a virtual environment (the proper approach) but found:
- The venv PATH is not honored when scripts launch through screen sessions
- This occurs specifically with sudo screen invocations
- Virtual environment activation doesn't persist through the sudo boundary

---

## Technical Analysis

### Current Implementation

#### 1. Virtual Environment Setup (`install_prereq.sh`)
```bash
setupPythonVenv() {
    echo "Creating Python virtual environment..."
    python3 -m venv venv

    echo "Installing Python packages into virtual environment..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
}
```
✓ Correctly creates venv and installs dependencies

#### 2. PATH Preservation Attempt (`start_flash.sh:69-82`)
```bash
if [ -d "venv" ]; then
    echo "Activating Python virtual environment..."
    source venv/bin/activate
    # Set VENV_PATH for use in screen sessions
    VENV_PATH="$PWD/venv/bin:$PATH"
else
    VENV_PATH="$PATH"
fi
```
⚠️ **CRITICAL BUG**: `VENV_PATH` is set but **NOT exported**

#### 3. Screen Session Launching (`start_flash.sh:93-96, 115`)
```bash
# Detect screen version
if [ "$screen_minor" -gt 5 ]; then
    screen_with_log="sudo screen -L -Logfile"
else
    screen_with_log="./old_screen_with_log.sh ${screen_minor}"
fi

# Later: Launch Python script
$screen_with_log smarthack-web.log -S smarthack-web -m -d \
    env PATH="$VENV_PATH" ./fake-registration-server.py
```

**For modern screen (4.6+)**: Expands to:
```bash
sudo screen -L -Logfile smarthack-web.log -S smarthack-web -m -d \
    env PATH="$VENV_PATH" ./fake-registration-server.py
```

**For older screen (<4.6)**: Expands to:
```bash
./old_screen_with_log.sh 5 smarthack-web.log -S smarthack-web -m -d \
    env PATH="$VENV_PATH" ./fake-registration-server.py
```

---

## Root Causes Identified

### Bug #1: VENV_PATH Not Exported
**Location**: `start_flash.sh:75`

The variable `VENV_PATH` is set but never exported:
```bash
VENV_PATH="$PWD/venv/bin:$PATH"  # Set but not exported
```

**Impact**: When `old_screen_with_log.sh` is invoked as a separate script (subprocess), it cannot access the `$VENV_PATH` variable. The shell substitution `env PATH="$VENV_PATH"` evaluates to `env PATH=""`, causing Python scripts to use system PATH without venv.

**Affected Scenarios**:
- Systems with screen version < 4.6 (uses `old_screen_with_log.sh` wrapper)
- Any subprocess that references `$VENV_PATH`

### Bug #2: Sudo Environment Preservation Not Guaranteed
**Location**: All `sudo screen` invocations

When `sudo` is invoked, it typically resets the environment for security. The `env PATH="..."` command comes AFTER sudo, but sudo's environment policy varies by system configuration (`/etc/sudoers`).

**Default sudo behavior**:
- Resets most environment variables
- Preserves only "safe" variables (HOME, USER, PATH from secure_path)
- Custom variables like VENV_PATH are stripped

**Current mitigation**: Using `env PATH="..."` inside the screen command works around this, but only if:
1. VENV_PATH is accessible (fails due to Bug #1)
2. The env command successfully overrides PATH for the screen session

### Bug #3: old_screen_with_log.sh Doesn't Preserve Environment
**Location**: `scripts/old_screen_with_log.sh:18`

The wrapper script runs:
```bash
${screen_with_log} ${screen_logfile_name} \
    -c ${screen_logfile_name}.screenrc ${screen_other_options}
```

It properly passes through `${screen_other_options}` (which includes the `env PATH=...` command), but since `$VENV_PATH` isn't exported from the parent, it evaluates to empty string.

---

## Why sslpsk is Critical

From `requirements.txt`:
```
tornado>=6.1
pycryptodomex>=3.9.8
sslpsk3>=1.0.0
```

**System package availability (Ubuntu/Debian)**:
- ✓ `python3-tornado` - Available
- ✓ `python3-pycryptodomex` - Available (as python3-pycryptodome)
- ✗ `python3-sslpsk3` - **NOT AVAILABLE**

The `sslpsk3` package (Python 3.12+ compatible SSL PSK library) is essential for the PSK frontend server (`psk-frontend.py`) which handles Pre-Shared Key encryption for device communication. Without it, the entire flashing process fails.

**Import chain**:
1. `psk-frontend.py` imports `sslpsk3`
2. Python searches PATH for `python3` executable
3. That python3 searches its sys.path for modules
4. If wrong python3 is found (system instead of venv), import fails

---

## Proposed Solution

### Fix #1: Export VENV_PATH (Critical)
**File**: `start_flash.sh:75`

```bash
# Current (BROKEN):
VENV_PATH="$PWD/venv/bin:$PATH"

# Fixed:
export VENV_PATH="$PWD/venv/bin:$PATH"
```

**Rationale**: Makes VENV_PATH available to all subprocesses, including `old_screen_with_log.sh`

### Fix #2: Add Explicit Python Venv Activation in Screen Commands (Recommended)
**File**: `start_flash.sh:115, 124, 129`

Instead of relying on PATH manipulation alone, explicitly activate venv within screen:

```bash
# Current (FRAGILE):
$screen_with_log smarthack-web.log -S smarthack-web -m -d \
    env PATH="$VENV_PATH" ./fake-registration-server.py

# Improved (ROBUST):
$screen_with_log smarthack-web.log -S smarthack-web -m -d \
    bash -c "source $PWD/venv/bin/activate && exec ./fake-registration-server.py"
```

**Rationale**:
- Explicitly activates venv within the screen session
- Sets all venv environment variables (PATH, VIRTUAL_ENV, etc.)
- More robust than PATH manipulation
- Works regardless of sudo configuration
- `exec` replaces bash with Python process (no extra parent)

### Fix #3: Update old_screen_with_log.sh for Venv Support (Optional Enhancement)
**File**: `scripts/old_screen_with_log.sh`

Add venv awareness to the wrapper:

```bash
#!/usr/bin/env bash
screen_minor=${1}
screen_logfile_name=${2}
screen_other_options=${@:3}

# Detect and preserve venv activation
if [ -n "${VIRTUAL_ENV:-}" ]; then
    venv_activate="source $VIRTUAL_ENV/bin/activate &&"
else
    venv_activate=""
fi

# Version-specific screen command...
# (existing logic)

# Modified execution with venv support:
${screen_with_log} ${screen_logfile_name} \
    -c ${screen_logfile_name}.screenrc \
    bash -c "${venv_activate} ${screen_other_options}"
```

---

## Testing Strategy

### Prerequisites
- Ubuntu 24.04 or similar with PEP 668 enforcement
- Screen version < 4.6 (to test old_screen_with_log.sh path)
- Clean venv without --break-system-packages

### Test Cases

**Test 1: Verify VENV_PATH Export**
```bash
./start_flash.sh &
sleep 2
cat scripts/smarthack-web.log | grep -i "ModuleNotFoundError\|sslpsk"
# Should show no import errors
```

**Test 2: Verify Python Version in Screen Session**
```bash
sudo screen -S test -m -d bash -c "source venv/bin/activate && which python3"
sudo screen -r test
# Should show /path/to/tuya-convert/venv/bin/python3
```

**Test 3: Verify sslpsk3 Import**
```bash
sudo screen -S test -m -d bash -c "source $PWD/venv/bin/activate && python3 -c 'import sslpsk3; print(sslpsk3.__version__)'"
# Should print version number without error
```

**Test 4: Full Integration Test**
```bash
# After applying fixes, run complete flash process
./start_flash.sh
# Monitor logs in scripts/*.log for import errors
```

---

## Implementation Priority

**CRITICAL (Must Fix)**:
- ✓ Fix #1: Export VENV_PATH

**HIGH (Strongly Recommended)**:
- ✓ Fix #2: Explicit venv activation in screen commands

**MEDIUM (Nice to Have)**:
- ✓ Fix #3: Update old_screen_with_log.sh wrapper

---

## Related Issues

- **#1159**: "error: This environment is externally managed" - Resolved with venv support
- **#1153**: "AttributeError: module 'ssl' has no attribute 'wrap_socket'" - Resolved with sslpsk3 migration
- **#1143**: "install_prereq.sh needs --break-system-packages" - Resolved with venv support

This issue (#1167) represents the remaining edge case where venv support exists but fails under specific conditions (sudo screen with old screen versions).

---

## Conclusion

Issue #1167 is a **valid, reproducible bug** affecting users on:
- Modern Linux distributions with PEP 668 enforcement
- Systems with older screen versions (<4.6)
- Non-Docker installations

The root cause is a missing `export` statement combined with fragile PATH manipulation through sudo boundaries. The proposed fixes are minimal, low-risk, and align with the project's existing venv architecture.

**Recommendation**: Implement all three fixes for maximum compatibility and robustness.
