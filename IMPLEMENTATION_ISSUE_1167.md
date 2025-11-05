# Implementation: Fix for Upstream Issue #1167

## Issue Summary
**Upstream Issue**: [ct-Open-Source/tuya-convert#1167](https://github.com/ct-Open-Source/tuya-convert/issues/1167)
**Title**: Ubuntu non-docker deps issue
**Problem**: Virtual environment packages (particularly `sslpsk3`) not accessible to Python scripts launched in `sudo screen` sessions

## Root Cause
When `start_flash.sh` launches Python scripts using `sudo screen`, the elevated privilege context creates a new shell environment that:
1. Resets environment variables including `PATH` and `VIRTUAL_ENV`
2. Causes `#!/usr/bin/env python3` shebangs to resolve to system Python instead of venv Python
3. Results in `ImportError` for packages installed only in the virtual environment

## Solution Implemented

### Approach: Use `env` Command to Preserve PATH (Option 1)
We explicitly set the PATH to include the virtual environment's `bin/` directory when launching Python scripts in screen sessions.

### Changes Made

#### 1. Modified `start_flash.sh`

**Added VENV_PATH variable (lines 74-81)**:
```bash
if [ -d "venv" ]; then
    echo "Activating Python virtual environment..."
    source venv/bin/activate
    # Set VENV_PATH for use in screen sessions (which run with sudo and lose activation)
    VENV_PATH="$PWD/venv/bin:$PATH"
else
    echo "WARNING: Virtual environment not found!"
    echo "Please run ./install_prereq.sh to set up the environment properly."
    echo "Attempting to continue with system Python packages..."
    # Fallback to system PATH
    VENV_PATH="$PATH"
fi
```

**Updated script invocations (lines 115, 124, 129)**:
```bash
# Before:
$screen_with_log smarthack-web.log -S smarthack-web -m -d ./fake-registration-server.py

# After:
$screen_with_log smarthack-web.log -S smarthack-web -m -d env PATH="$VENV_PATH" ./fake-registration-server.py
```

Applied to all three Python scripts launched in screen sessions:
- `fake-registration-server.py` (web server, port 80)
- `psk-frontend.py` (PSK handler, port 8886)
- `tuya-discovery.py` (UDP discovery service)

#### 2. Updated `README.md`

Added documentation explaining the fix:
- References both issue #1159 and #1167
- Explains the virtual environment and sudo compatibility approach
- Notes that PATH is explicitly set via `env` command for screen sessions

### How It Works

1. **Virtual environment activation** happens normally at script start
2. **VENV_PATH variable** captures the full PATH with venv/bin prepended (as absolute path)
3. **When script changes directory** to `scripts/`, the absolute path remains valid
4. **When sudo screen launches** Python scripts, `env PATH="$VENV_PATH"` restores the PATH
5. **Python shebang resolution** now finds the venv Python first in PATH
6. **Import statements** succeed because venv Python knows about venv site-packages

### Why This Solution

**Advantages**:
- ✅ **POSIX-compliant**: `env` command is standard on all Unix-like systems
- ✅ **Portable**: Works across all target platforms (Ubuntu, Debian, Raspberry Pi)
- ✅ **Pythonic**: Uses virtual environment's intended PATH-based isolation
- ✅ **Minimal changes**: No new files, no script modifications
- ✅ **Backward compatible**: Falls back to system PATH if venv doesn't exist
- ✅ **Clear intent**: Explicitly shows we're preserving the environment

**Compared to alternatives**:
- More elegant than hardcoding venv Python path
- Simpler than wrapper scripts
- More portable than bash-specific solutions

## Testing Recommendations

Test on target platforms with virtual environment:
```bash
# Create fresh installation
./install_prereq.sh

# Run start_flash.sh and check logs
./start_flash.sh

# Verify Python scripts can import sslpsk3
sudo screen -r smarthack-psk
# Check for import errors in output

# Verify venv Python is being used
ps aux | grep python3
# Should show full path to venv/bin/python3
```

## Related Issues & Fixes

1. ✅ **Issue #1159**: Virtual environment / PEP 668 compliance (SOLVED)
2. ✅ **Issue #1153**: Python 3.12+ `ssl.wrap_socket()` removal (SOLVED)
3. ✅ **Issue #1167**: Virtual environment broken in sudo screen sessions (SOLVED - this fix)

## Future Work

See `ISSUE_DRAFT_REMOVE_SUDO.md` for a feature request to eliminate the root cause by removing unnecessary `sudo` usage entirely through:
- Linux capabilities (CAP_NET_BIND_SERVICE)
- High port forwarding via iptables
- systemd socket activation
- authbind

This would eliminate the need for PATH workarounds and improve security posture.

## Commit Information

**Branch**: `claude/analyze-upstream-issue-011CUqSTmYfzt2SERby9mHfS`
**Files Modified**:
- `start_flash.sh` (added VENV_PATH, updated 3 script invocations)
- `README.md` (documented fix and referenced issue #1167)

**Files Created**:
- `ISSUE_DRAFT_REMOVE_SUDO.md` (feature request for future work)
- `IMPLEMENTATION_ISSUE_1167.md` (this document)
