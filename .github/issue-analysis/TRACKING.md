# Issue Analysis Tracking

**Repository**: sfo2001/tuya-convert (fork of ct-Open-Source/tuya-convert)
**Last Updated**: 2025-11-06

---

## Legend

- ✅ **Resolved** - Fixed, tested, and merged
- 🔄 **In Progress** - Currently working on
- 📦 **Archived** - Not actionable / Won't fix / Hardware limitation
- 🔍 **Investigating** - Analysis phase
- ⏸️ **Paused** - Blocked or deprioritized

---

## Upstream Issues (ct-Open-Source/tuya-convert)

| Issue | Title | Status | Location | Commits | PR | Notes |
|-------|-------|--------|----------|---------|-----|-------|
| [#1098](https://github.com/ct-Open-Source/tuya-convert/issues/1098) | Endless flash loop | ✅ Resolved | `resolved/1098-endless-flash-loop/` | 59549b1 | #10 | Fixed by sslpsk3 |
| [#1143](https://github.com/ct-Open-Source/tuya-convert/issues/1143) | PEP 668 compliance | ✅ Resolved | `resolved/1143-pep668-compliance/` | 1663d29 | #17 | Virtual env support |
| [#1145](https://github.com/ct-Open-Source/tuya-convert/issues/1145) | SP25 dead after flash | 📦 Archived | `archived/1145-sp25-user-error/` | - | - | User error (wrong MAC) |
| [#1146](https://github.com/ct-Open-Source/tuya-convert/issues/1146) | SC400W won't flash | 📦 Archived | `archived/1146-sc400w-incompatible/` | - | - | Non-ESP chip |
| [#1153](https://github.com/ct-Open-Source/tuya-convert/issues/1153) | sslpsk3 migration | ✅ Resolved | - | 59549b1 | #10 | Python 3.12+ compat |
| [#1157](https://github.com/ct-Open-Source/tuya-convert/issues/1157) | Chip incompatibility | 📦 Archived | `archived/1157-chip-incompatible/` | ea46fb1 | #19 | ECR6600 chip (not ESP) |
| [#1159](https://github.com/ct-Open-Source/tuya-convert/issues/1159) | PEP 668 externally managed | ✅ Resolved | `resolved/1159-pep668-duplicate/` | b8a8291 | #9 | Duplicate of #1143 |
| [#1161](https://github.com/ct-Open-Source/tuya-convert/issues/1161) | Docker files/ mount | ✅ Resolved | - | bb8f12e | #14 | Docker volume fix |
| [#1162](https://github.com/ct-Open-Source/tuya-convert/issues/1162) | SmartConfig loop | 🔍 Investigating | `open/1162-smartconfig-loop/` | - | - | Device won't connect |
| [#1163](https://github.com/ct-Open-Source/tuya-convert/issues/1163) | Nix flake support | ✅ Resolved | `open/1163-nix-flake/` | f78bd4a | - | Reproducible env |
| [#1164](https://github.com/ct-Open-Source/tuya-convert/issues/1164) | Video doorbell telnet | 📦 Archived | `archived/1164-video-doorbell-telnet/` | - | - | Out of scope |
| [#1165](https://github.com/ct-Open-Source/tuya-convert/issues/1165) | Gentoo install support | ✅ Resolved | `resolved/1165-gentoo-install/` | 90547b0 | #13 | emerge + venv |
| [#1167](https://github.com/ct-Open-Source/tuya-convert/issues/1167) | Venv PATH sudo | ✅ Resolved | `resolved/1167-venv-sudo-screen/` | d071bdc, 83db9d2 | - | Screen session venv |

---

## Detailed Status

### ✅ Resolved Issues (8)

#### #1098: Failing to flash smart plug that connects, with an endless loop
- **Status**: ✅ Resolved
- **Date Resolved**: 2025-01-04 (by sslpsk3 migration for #1153)
- **Date Reported**: 2023-07-16
- **Reporter**: AzzieDev
- **Solution**: Migrated from deprecated sslpsk to sslpsk3 for better SSL cipher support
- **Commits**: 59549b1 (sslpsk3 migration)
- **PR**: #10
- **Files**:
  - `resolved/1098-endless-flash-loop/analysis.md`
  - `resolved/1098-endless-flash-loop/summary.md`
  - Updated `requirements.txt` (sslpsk → sslpsk3)
  - Updated `scripts/psk-frontend.py` (import changes)
- **Impact**: Resolves SSL/TLS-PSK handshake failures causing endless loop during device flashing
- **Technical Details**:
  - Error: `[SSL: NO_SHARED_CIPHER] no shared cipher`
  - Device: YTE CZ001 Smart Plug (PSK Identity 02 protocol)
  - Root cause: Old sslpsk library had limited cipher support, Python 3.12 incompatibility
  - Fix: sslpsk3 provides better cipher suite support (PSK-AES128-CBC-SHA256)
  - Same fix resolves #1153 (Python 3.12+ AttributeError)
- **User Symptoms**:
  - SmartConfig succeeds (device connects to fake AP)
  - Initial HTTP/MQTT exchanges work
  - SSL/TLS-PSK handshake fails repeatedly
  - Device enters endless loop: blue LED → pink → red → blue
  - WiFi: repeated connect/disconnect cycles
- **Related**: #1153 (sslpsk3 - same fix), #1162 (similar symptoms), #430, #1058

#### #1143: install_prereq.sh needs --break-system-packages
- **Status**: ✅ Resolved
- **Date Resolved**: 2024-11-12
- **Solution**: Added virtual environment support to comply with PEP 668
- **Commits**: 1663d29
- **PR**: #17
- **Files**: `resolved/1143-pep668-compliance/analysis.md`
- **Impact**: Enables installation on Debian 12+, Ubuntu 24.04+ without breaking system packages

#### #1153: AttributeError: module 'ssl' has no attribute 'wrap_socket'
- **Status**: ✅ Resolved
- **Date Resolved**: 2025-01-04
- **Solution**: Migrated from deprecated `sslpsk` to `sslpsk3` for Python 3.12+ compatibility
- **Commits**: 59549b1
- **PR**: #10
- **Files**: No analysis document (resolved before tracking system)
- **Impact**: Python 3.12+ compatibility

#### #1159: error: This environment is externally managed
- **Status**: ✅ Resolved (Duplicate of #1143)
- **Date Resolved**: 2025-04-01 (reported), resolved by existing venv implementation
- **Solution**: Same as #1143 - Python virtual environment support for PEP 668 compliance
- **Commits**: b8a8291 (primary), 90547b0 (refactoring)
- **PR**: #9
- **Files**:
  - `resolved/1159-pep668-duplicate/analysis.md`
  - `resolved/1159-pep668-duplicate/summary.md`
  - Same implementation files as #1143 (install_prereq.sh, start_flash.sh, requirements.txt, etc.)
- **Impact**: Duplicate report of #1143 - validates that PEP 668 issue is widespread
- **Technical Details**:
  - Identical error message: "externally-managed-environment"
  - Identical root cause: System-wide pip install violates PEP 668
  - Identical solution: Virtual environment support
  - Identical affected systems: Debian 12+, Ubuntu 23.04+, Arch, Fedora 38+
- **User Contribution**: ricardopretrazy attempted `--break-system-packages` workaround
- **Maintainer Response**: Correctly suggested virtual environment solution (already implemented)
- **Related**: #1143 (primary issue), #1167 (venv PATH), #1153 (sslpsk3 in venv)

#### #1161: Docker Tuya Convert unable to see esphome firmware.bin
- **Status**: ✅ Resolved
- **Date Resolved**: 2025-05-12
- **Solution**: Fixed Docker volume mount for `files/` directory
- **Commits**: bb8f12e
- **PR**: #14
- **Files**: No analysis document (resolved before tracking system)
- **Impact**: Custom firmware loading in Docker works

#### #1165: No install option for gentoo
- **Status**: ✅ Resolved
- **Date Resolved**: 2025-11-05
- **Solution**: Added complete Gentoo Linux support with emerge package manager and virtual environment
- **Commits**: 90547b0
- **PR**: #13
- **Files**:
  - `resolved/1165-gentoo-install/analysis.md`
  - Updated `install_prereq.sh` (added gentooInstall() function)
  - Updated `README.md` (listed Gentoo as supported)
- **Impact**: Gentoo users can now use tuya-convert with native package manager support
- **Technical Details**:
  - Added gentooInstall() function using emerge package manager
  - Installs all dependencies with Gentoo package naming (category/package)
  - Creates Python virtual environment (same as Debian/Arch)
  - Includes emerge --sync to update Portage tree
  - Uses --ask --verbose flags (Gentoo best practice)
  - Refactored to extract setupPythonVenv() shared function (DRY principle)
- **User Contribution**: rpruen provided implementation attachment
- **Related**: #1143 (PEP 668 - venv approach), #1167 (venv PATH)

#### #1167: Ubuntu non-docker deps issue (Venv PATH)
- **Status**: ✅ Resolved
- **Date Resolved**: 2025-11-06
- **Solution**: Export VENV_PATH and explicit venv activation in sudo screen sessions
- **Commits**: d071bdc (code), 83db9d2 (docs)
- **PR**: Not yet submitted to upstream
- **Files**:
  - `resolved/1167-venv-sudo-screen/analysis.md`
  - `resolved/1167-venv-sudo-screen/implementation.md`
  - `resolved/1167-venv-sudo-screen/summary.md`
- **Impact**: Virtual environment packages (sslpsk3) accessible in sudo screen sessions
- **Technical Details**:
  - Root cause: VENV_PATH not exported, sudo environment reset
  - Fix: Export VENV_PATH, use `bash -c "source venv/bin/activate && exec script.py"`
  - Affects: Ubuntu 24.04+, Debian 12+, modern Linux with PEP 668

#### #1163: Add nix flake to documentation
- **Status**: ✅ Resolved
- **Date Resolved**: 2025-11-06
- **Solution**: Complete Nix flake implementation with comprehensive documentation
- **Commits**: f78bd4a
- **PR**: Not yet submitted to upstream
- **Files**:
  - `open/1163-nix-flake/analysis.md`
  - `open/1163-nix-flake/summary.md`
  - `flake.nix` (repository root)
  - `docs/Using-Nix.md` (450+ lines)
  - Updated `docs/Installation.md`
  - Updated `docs/Quick-Start-Guide.md`
- **Impact**: Provides third installation method with perfect reproducibility
- **Technical Details**:
  - Custom sslpsk3 package build (Python 3.12+ compatible)
  - All dependencies version-locked via flake.lock
  - Isolated environment in /nix/store/
  - Zero system impact, works on any Linux with Nix
  - Credits: SHU-red (original), seanaye (build fix), mberndt123 (suggestions)
- **Benefits**:
  - One-command setup: `nix develop`
  - Cross-distribution compatibility
  - Reproducible environments (no version drift)
  - Developer-friendly workflow

---

### 🔍 Investigating (1)

#### #1162: Flash process doesn't connect on smart device - repeating: SmartConfig complete. Resending SmartConfig Packets
- **Status**: 🔍 Investigating
- **Started**: 2025-11-06
- **Reporter**: Edu-ST (2025-05-26)
- **Maintainer Response**: RoSk0 linked to #1153 (2025-07-27)
- **Analysis**: Complete, awaiting user diagnostic information
- **Files**: `open/1162-smartconfig-loop/analysis.md`
- **Root Cause Hypothesis**: Likely related to #1153 (Python 3.12+ / sslpsk3 compatibility)
  - User running Kali 2025.1.c (Python 3.12+)
  - SmartConfig completes but device won't connect (SSL handshake likely failing)
  - Possible alternative causes: device incompatibility, newer security protocol, environment issues
- **Next Steps**:
  1. Request user to provide log files (`smarthack-psk.log`, `smarthack-wifi.log`)
  2. Verify sslpsk3 installation status
  3. Determine if device uses ESP chip or alternative (ECR6600, BK7231, etc.)
- **Impact**: Common issue on modern Linux with Python 3.12+ without proper sslpsk3 setup
- **Related**: #1153 (sslpsk3 - resolved), #1157 (chip incompatibility - archived), #1167 (venv activation - resolved)

---

### 📦 Archived Issues (4)

#### #1145: Teckin/Tuya SP25 Plug: dead after post-wifi-reboot
- **Status**: 📦 Archived (User Error - Self-Resolved)
- **Date Archived**: 2025-11-06
- **Date Reported**: 2024-12-05
- **Reporter**: STR4NG3RdotSH
- **Reason**: User error - device was working correctly, user was checking wrong MAC address
- **Files**:
  - `archived/1145-sp25-user-error/analysis.md`
  - `archived/1145-sp25-user-error/summary.md`
- **Device**: Teckin SP25 smart plug (ESP8266-based)
- **What Happened**:
  - User successfully flashed device with tasmota-lite.bin
  - After WiFi config reboot, device appeared "dead"
  - User performed extensive troubleshooting
  - Used fast power cycle recovery (6x power reinsertion) to enter config mode
  - Reconfigured WiFi and rebooted again
  - Discovered device had been connected all along - was checking wrong MAC address
- **Outcome**: ✅ Device working perfectly, tuya-convert functioned correctly
- **Educational Value**:
  - Documents fast power cycle recovery feature usage
  - Shows common post-flash verification confusion
  - Validates Teckin SP25 compatibility with tuya-convert
  - Demonstrates importance of verifying correct MAC address from logs
- **Potential Documentation Improvements**:
  - Add post-flash verification guide
  - Document fast power cycle recovery feature
  - Add troubleshooting section for "device appears dead" scenarios
  - Explain MAC address identification best practices
- **Related**: Common user confusion pattern, not a software issue

#### #1146: my SC400W will not flash with raspberry5
- **Status**: 📦 Archived (Hardware Incompatibility)
- **Date Archived**: 2025-11-06
- **Date Reported**: 2024-12-07
- **Reporter**: HaraldKiessling
- **Reason**: Device does not use ESP82xx chip - tuya-convert detected non-ESP hardware
- **Files**:
  - `archived/1146-sc400w-incompatible/analysis.md`
  - `archived/1146-sc400w-incompatible/summary.md`
- **Device**: Loratap SC400W (Product ID: YWK0ZiumXZGkb8nj, Firmware: 1.0.6)
- **Platform**: Raspberry Pi 5
- **What Happened**:
  - User attempted to flash device using tuya-convert
  - SmartConfig transmission worked
  - Device failed to connect
  - tuya-convert diagnostic reported: "Your device does not use an ESP82xx"
  - Flash process safely aborted
- **Chip Type**: Non-ESP (likely Beken BK7231 or Realtek RTL8710)
- **Why Cannot Be Fixed**: tuya-convert is fundamentally ESP-specific, cannot support other architectures
- **Outcome**: ✅ tuya-convert correctly detected incompatibility and prevented failed flash
- **Alternative Solutions**:
  - CloudCutter (OTA for Beken): https://github.com/tuya-cloudcutter/tuya-cloudcutter
  - ltchiptool (Serial flashing): https://github.com/libretiny-eu/ltchiptool
  - OpenBeken firmware: https://github.com/openshwprojects/OpenBK7231T_App
- **Educational Value**:
  - Demonstrates tuya-convert's chip detection working correctly
  - Highlights trend of Tuya moving from ESP to cheaper chips (post-2020)
  - Provides guidance for non-ESP device alternatives
- **Potential Documentation Improvements**:
  - Add prominent compatibility warning in README (ESP-only)
  - Create compatibility check guide
  - Enhance diagnostic error message with links to alternatives
  - Document chip transition timeline (ESP -> Beken trend)
- **Related**: #1157 (ECR6600 incompatibility), #1164 (video doorbell - similar pattern of non-ESP devices)

#### #1157: new tuya smart plug 20A convert failed attempt
- **Status**: 📦 Archived (Hardware Incompatibility)
- **Date Archived**: 2025-11-06
- **Reason**: Device uses Eswin ECR6600 chip (not ESP8266/ESP32), no custom firmware available
- **Commits**: ea46fb1 (documentation)
- **PR**: #19
- **Files**:
  - `archived/1157-chip-incompatible/analysis.md`
  - `archived/1157-chip-incompatible/summary.md`
- **Impact**: Documented alternative flashing methods for non-ESP devices
- **Note**: Not a software issue - requires different hardware flashing approach

#### #1164: video doorbell telnet access
- **Status**: 📦 Archived (Out of Scope)
- **Date Archived**: 2025-11-06
- **Reason**: User already has telnet access to device and wants to explore it - not a tuya-convert use case
- **Files**: `archived/1164-video-doorbell-telnet/analysis.md`
- **Device**: Tuya video doorbell with open ports (telnet, FTP, IRC)
- **Why Archived**:
  - User already has access (no conversion/flashing needed)
  - Video doorbells typically use ARM SoCs, not ESP8266/ESP32
  - Request is for device exploration, not firmware flashing
  - tuya-convert is specifically for ESP-based firmware flashing via OTA
- **Guidance Provided**:
  - How to explore the device via telnet
  - Alternative resources (HomeAssistant forums, OpenIPC, IoT communities)
  - Warnings about camera device complexity
  - Why video doorbells don't work with tuya-convert
- **Documentation Recommendations**:
  - Add warning to WiFi Cameras section about chip incompatibility
  - Create FAQ entry explaining camera/doorbell limitations
  - Clarify project scope more prominently
- **Related**: #1157 (similar chip incompatibility issue)

---

## Statistics

- **Total Analyzed**: 13 issues
- **Resolved**: 8 (62%)
- **Investigating**: 1 (8%)
- **Archived**: 4 (31%)
- **Resolution Rate**: 89% (8/9 actionable issues, excluding user errors & hardware incompatibilities)

---

## Related Issues Timeline

```
2023-07-16  #1098  Endless flash loop               ✅ Resolved (by #1153)
2024-11-12  #1143  PEP 668 compliance              ✅ Resolved
2024-12-05  #1145  SP25 dead after flash           📦 Archived (User error)
2024-12-07  #1146  SC400W incompatible chip        📦 Archived (Hardware)
2025-01-04  #1153  sslpsk3 migration                ✅ Resolved
2025-03-05  #1157  Chip incompatibility             📦 Archived (Hardware)
2025-04-01  #1159  PEP 668 externally managed       ✅ Resolved (Duplicate)
2025-05-12  #1161  Docker files/ mount              ✅ Resolved
2025-05-26  #1162  SmartConfig loop                 🔍 Investigating
2025-06-13  #1163  Nix flake support                ✅ Resolved
2025-06-19  #1164  Video doorbell telnet            📦 Archived (Out of scope)
2025-09-19  #1165  Gentoo install support           ✅ Resolved
2025-10-15  #1167  Venv PATH sudo screen            ✅ Resolved
```

---

## Common Themes

### Python Environment Management (7 issues)
- **#1098**: Endless flash loop → SSL cipher issues with old sslpsk (resolved by sslpsk3)
- **#1143**: PEP 668 compliance → Virtual environment
- **#1153**: Python 3.12+ compatibility → sslpsk3 migration
- **#1159**: PEP 668 externally managed → Virtual environment (duplicate of #1143)
- **#1162**: SmartConfig loop → Likely sslpsk3 (investigation ongoing)
- **#1165**: Gentoo install → emerge + venv support
- **#1167**: Venv in sudo screen → PATH preservation

**Result**: Comprehensive virtual environment support with Python 3.12+ compatibility across all distributions, modern sslpsk3 resolves SSL/TLS-PSK handshake issues

### Installation Methods (3 issues)
- **#1161**: Docker volume mounting → Fixed
- **#1163**: Nix flake reproducibility → Implemented
- **#1165**: Gentoo distribution support → Native emerge support

**Result**: Multiple installation options (Native on Debian/Arch/Gentoo, Docker, Nix) all fully functional

### Hardware Compatibility / Out of Scope (3 issues)
- **#1146**: SC400W with non-ESP chip (likely Beken BK7231 or RTL8710)
- **#1157**: Non-ESP chip devices (ECR6600 smart plug)
- **#1164**: Video doorbell exploration (ARM SoC, out of scope)

**Result**: Clear documentation that tuya-convert is ESP-only, guidance to alternatives (CloudCutter, ltchiptool)

### User Error / Support (1 issue)
- **#1145**: Device appeared dead after flash (user checking wrong MAC address)

**Result**: Device worked correctly; validates Teckin SP25 compatibility; documents fast power cycle recovery

---

## Quick Links

### By Status
- [Resolved Issues](resolved/) - ✅ Fixed and merged
- [Open Issues](open/) - 🔄 Currently working on
- [Archived Issues](archived/) - 📦 Not actionable

### By Topic
- **Python/Dependencies**: #1098, #1143, #1153, #1159, #1162, #1165, #1167
- **Docker**: #1161
- **Installation**: #1163, #1165
- **Hardware/Out of Scope**: #1146, #1157, #1164
- **User Error/Support**: #1145

### Key Documents
- [README.md](README.md) - Guide to this directory
- [TEMPLATE.md](TEMPLATE.md) - Issue analysis template
- [../project-planning/](../project-planning/) - Project planning docs

---

## Upstream Contribution Status

### Ready for Upstream PR
- ✅ #1163 - Nix flake (complete, documented, ready)
- ✅ #1167 - Venv PATH fix (tested, documented)

### Already in Fork
- ✅ #1143 - Virtual environment support
- ✅ #1153 - sslpsk3 migration
- ✅ #1159 - PEP 668 compliance (duplicate of #1143)
- ✅ #1161 - Docker volume fix
- ✅ #1165 - Gentoo Linux support

### Documented Only (Archived/Out of Scope)
- 📦 #1145 - User error documentation (fast power cycle recovery)
- 📦 #1146 - Non-ESP chip guidance (CloudCutter, ltchiptool alternatives)
- 📦 #1157 - Alternative methods for non-ESP chips
- 📦 #1164 - Video doorbell guidance (out of scope)

---

## Notes

### Next Steps
1. Continue analyzing remaining open issues (check for newer issues > #1167)
2. Request diagnostic information from user for #1162 (log files, environment details)
3. Create PR for #1143 + #1159 (PEP 668 virtual environment support) to upstream
4. Create PR for #1163 (Nix flake) to upstream
5. Create PR for #1165 (Gentoo support) to upstream
6. Create PR for #1167 (venv PATH fix) to upstream
7. Consider adding post-flash verification guide (based on #1145 learnings)
8. Consider adding prominent ESP-only compatibility warning to README (based on #1146, #1157)
9. Consider enhancing non-ESP diagnostic message with alternative tool links
10. Monitor for new upstream issues to analyze

### Lessons Learned
- **Virtual environments are critical** on modern Linux (PEP 668)
- **Python 3.12+ support** required sslpsk3 migration
- **Screen sessions with sudo** need explicit venv activation
- **Hardware limitations** (non-ESP chips) should be clearly documented
- **Multiple installation methods** (Native, Docker, Nix) serve different use cases
- **User verification errors** common after flashing (wrong MAC address, wrong hostname)
- **Fast power cycle recovery** is a valuable firmware feature that should be documented
- **Post-flash verification guide** would reduce false "device dead" reports
- **Non-ESP chip trend accelerating** - most new Tuya devices (2020+) use Beken/RTL, not ESP
- **ESP-only scope needs prominent documentation** - users need to know before attempting
- **Alternative tools exist** for non-ESP (CloudCutter, ltchiptool) - link to them prominently

### Patterns Observed
1. Many issues relate to Python environment management in modern Linux
2. Docker provides alternative but has its own challenges (volume mounting)
3. Nix offers third option for reproducibility
4. Hardware incompatibilities need clear documentation upfront
5. Users often confuse tuya-convert's scope (ESP firmware flashing vs. general Tuya hacking)
6. Post-flash verification confusion is common (MAC addresses, hostnames, device discovery)
7. **Increasing non-ESP device reports** (2-3 out of 12 issues) - reflects chip transition trend
8. tuya-convert's diagnostic correctly detects non-ESP chips but needs better guidance on alternatives

---

**Tracking System Created**: 2025-11-06
**Repository**: https://github.com/sfo2001/tuya-convert
**Upstream**: https://github.com/ct-Open-Source/tuya-convert

For questions or updates, see [README.md](README.md).
