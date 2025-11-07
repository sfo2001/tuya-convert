# ADR 001: Configuration Management for tuya-convert

**Status**: Proposed
**Date**: 2025-11-07
**Deciders**: Development Team
**Context**: Phase 4.3 - Configuration Management Evaluation

---

## Context and Problem Statement

The tuya-convert project currently has configuration values scattered across multiple files and formats:
1. Shell scripts read from `config.txt` (bash-style KEY=value)
2. Python scripts have hardcoded defaults with CLI overrides
3. Smartconfig has hardcoded values in `main.py`

We need to determine if a unified configuration management approach is needed and, if so, what format to use.

---

## Survey of Current Configuration Values

### Network Configuration
**Currently configured via:**
- `config.txt` (for shell scripts)
- Tornado `define()` (for fake-registration-server.py)
- Python constants (for psk-frontend.py, mq_pub_15.py)

| Value | Current Location | Default | Purpose |
|-------|------------------|---------|---------|
| Gateway IP | Multiple files | 10.42.42.1 | Network gateway for fake AP |
| HTTP Port | fake-registration-server.py | 80 | Fake cloud API server |
| HTTPS Port | psk-frontend.py | 443 | TLS-PSK proxy |
| MQTT Port | psk-frontend.py | 1883 | MQTT broker |
| MQTT-TLS Port | psk-frontend.py | 8886 | MQTT TLS-PSK proxy |
| MQTT Broker | mq_pub_15.py | 127.0.0.1 | MQTT broker address |
| WLAN Interface | config.txt | wlan0 | Wi-Fi interface name |
| AP SSID | config.txt, main.py | vtrust-flash | Access point name |

### Smartconfig Configuration
**Currently hardcoded in:** `scripts/smartconfig/main.py`

| Value | Current Value | Purpose | Flexibility Needed |
|-------|---------------|---------|-------------------|
| ssid | "vtrust-flash" | AP SSID | LOW - Must match AP |
| passwd | "" (empty) | Wi-Fi password | LOW - Must match AP |
| region | "US" | Tuya region code | LOW - Protocol requirement |
| token | "00000000" | Device token | LOW - Dummy value |
| secret | "0101" | Device secret | LOW - Dummy value |

### Protocol Constants
**Currently hardcoded in:** Multiple Python modules

| Value | Location | Purpose | Flexibility Needed |
|-------|----------|---------|-------------------|
| UDP ports 6666/6667 | tuya-discovery.py | Tuya UDP discovery | NONE - Protocol fixed |
| UDP_KEY_MAGIC | tuya-discovery.py | Decryption key | NONE - Protocol fixed |
| PSK_HINT | psk-frontend.py | TLS-PSK hint | NONE - Protocol fixed |
| IDENTITY_PREFIX | psk-frontend.py | Device ID validation | NONE - Protocol fixed |
| TUYA_SEQUENCE_NUMBER | mq_pub_15.py | MQTT protocol 15 | NONE - Protocol fixed |
| Protocol versions 2.1/2.2 | mq_pub_15.py | Encryption modes | NONE - Protocol fixed |

### Security Configuration
**Currently configured via:** CLI arguments and defaults

| Value | Current Location | Default | Flexibility Needed |
|-------|------------------|---------|-------------------|
| secKey | fake-registration-server.py | "0000000000000000" | LOW - Dummy key |
| localKey | mq_pub_15.py | "0000000000000000" | MEDIUM - Device-specific |

---

## Decision Drivers

### Current State Analysis

**Strengths:**
1. ✅ **Shell scripts already use config.txt** - Working configuration mechanism exists
2. ✅ **Python CLI overrides work well** - tornado `define()` provides flexibility
3. ✅ **Protocol constants are correctly hardcoded** - These should never change
4. ✅ **Single-purpose tool** - tuya-convert has one specific use case
5. ✅ **Packaged execution** - Usually run via `start_flash.sh` wrapper

**Weaknesses:**
1. ⚠️ **Inconsistency** - Shell uses config.txt, Python uses constants/CLI
2. ⚠️ **Smartconfig values hardcoded** - No way to override without editing code
3. ⚠️ **No validation** - Invalid values not caught early

### Use Case Analysis

**Primary use case:** Device firmware flashing via `start_flash.sh`
- Users run a single command: `./start_flash.sh`
- Script orchestrates all components automatically
- Configuration changes are rare (only for non-standard networks)

**Secondary use case:** Development and testing
- Developers may need to test individual components
- CLI arguments already provide necessary flexibility

---

## Considered Options

### Option 1: Keep Current Approach (Recommended) ✅

**Status Quo with Minor Improvements:**
- Keep `config.txt` for shell scripts (already working)
- Keep tornado `define()` for fake-registration-server.py (already working)
- Keep Python constants with CLI overrides (already working)
- **ONLY CHANGE:** Extract smartconfig hardcoded values to config.txt

**Pros:**
- ✅ Minimal changes required
- ✅ Proven to work in production
- ✅ Each component remains self-contained
- ✅ CLI overrides still available for development
- ✅ No new dependencies
- ✅ Simple for users (one config file for rare changes)

**Cons:**
- ⚠️ Slight inconsistency between shell and Python configuration
- ⚠️ No centralized validation

**Implementation:**
```python
# scripts/smartconfig/main.py - Read from config.txt if available
import os
config_path = "../../config.txt"
ssid = "vtrust-flash"  # defaults
# ... parse config.txt to override defaults
```

### Option 2: Unified Config File (YAML/JSON)

**Create config.yaml for all components**

**Pros:**
- ✅ Single source of truth
- ✅ Structured validation possible
- ✅ Easy to extend

**Cons:**
- ❌ Breaking change - requires rewriting working shell scripts
- ❌ New dependency (PyYAML)
- ❌ Overkill for current needs
- ❌ More complex than needed
- ❌ Users would need to learn new format

### Option 3: Environment Variables

**Use ENV vars for all configuration**

**Pros:**
- ✅ Standard approach
- ✅ Works for both shell and Python

**Cons:**
- ❌ Poor user experience - many variables to set
- ❌ Not persistent (unless exported in shell)
- ❌ Harder to version control
- ❌ Breaks existing config.txt workflow
- ❌ More complex for users than editing one file

---

## Decision

**Chosen Option: Option 1 - Keep Current Approach with Minor Improvements**

### Rationale

1. **"If it ain't broke, don't fix it"** - The current system works well for 99% of users
2. **User experience** - `config.txt` editing is simple and working
3. **Development flexibility** - CLI overrides provide needed flexibility
4. **Minimal risk** - Only change is making smartconfig read config.txt
5. **Principle of least change** - After major refactoring, avoid unnecessary changes

### Recommended Improvements

#### Immediate (Low effort, high value):
1. **Make smartconfig read config.txt** - Eliminate hardcoded values in main.py
2. **Add config.txt.example** - Document all available options
3. **Add validation** - Catch invalid IPs/ports early with clear error messages

#### Future (Optional):
1. **Centralized defaults** - Create `scripts/config_defaults.py` with all defaults
2. **Validation module** - Validate IP addresses, port ranges, etc.
3. **Config documentation** - Add section to README explaining configuration

---

## Implementation Plan

### Phase 1: Extract Smartconfig Hardcoded Values (Recommended Now)

```bash
# config.txt - Add smartconfig values
SMARTCONFIG_SSID=vtrust-flash
SMARTCONFIG_PASSWORD=
SMARTCONFIG_REGION=US
SMARTCONFIG_TOKEN=00000000
SMARTCONFIG_SECRET=0101
```

```python
# scripts/smartconfig/main.py - Read from config
def load_config():
    """Load configuration from config.txt with fallback to defaults."""
    config = {
        'ssid': 'vtrust-flash',
        'passwd': '',
        'region': 'US',
        'token': '00000000',
        'secret': '0101'
    }

    config_path = os.path.join(os.path.dirname(__file__), '../../config.txt')
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key == 'SMARTCONFIG_SSID':
                            config['ssid'] = value
                        # ... etc
    return config

config = load_config()
ssid = config['ssid']
passwd = config['passwd']
# ... use config values
```

### Phase 2: Create config.txt.example (Documentation)

Document all available configuration options in a template file.

### Phase 3: Add Basic Validation (Optional)

Add simple validation for IP addresses and port numbers.

---

## Consequences

### Positive
- ✅ Maintains working system
- ✅ Improves smartconfig flexibility without breaking changes
- ✅ Clear path for future enhancements
- ✅ Simple for users to understand
- ✅ No new dependencies

### Negative
- ⚠️ Slight inconsistency remains (acceptable trade-off)
- ⚠️ No centralized validation (can be added later if needed)

### Neutral
- Configuration management complexity stays manageable
- Future enhancements can build on this foundation

---

## Notes

### Why Not More Sophisticated Config Management?

tuya-convert is a **single-purpose tool** with a **well-defined use case**:
1. User runs `./start_flash.sh`
2. Tool creates fake AP with fixed name
3. Device connects and gets flashed
4. Done

This is NOT a long-running service with complex deployment scenarios. The configuration needs are minimal:
- Most values MUST be hardcoded (protocol requirements)
- Most users never change defaults
- Rare changes (different network) are easily handled by config.txt

### Configuration Philosophy

**Good configuration management means:**
- ✅ Making common cases simple (defaults work out of box)
- ✅ Making rare customization possible (config.txt)
- ✅ Making development flexible (CLI overrides)
- ❌ NOT adding complexity without clear benefit
- ❌ NOT over-engineering for hypothetical future needs

---

## References

- Existing `config.txt` mechanism
- Tornado options system: `tornado.options.define()`
- Python argparse: Command-line interfaces
- [12-Factor App Config](https://12factor.net/config) (considered but not applicable here)

---

## Review History

- 2025-11-07: Initial evaluation and decision
