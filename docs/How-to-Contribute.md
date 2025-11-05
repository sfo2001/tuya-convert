# How to Contribute

**Last Updated:** 2025-11-05
**Status:** ✅ Complete

## Overview

Thank you for your interest in contributing to tuya-convert! This project thrives on community contributions, whether through device testing, documentation improvements, code contributions, or research assistance. Every contribution helps make this tool better for everyone.

## Prerequisites

Before contributing, please:

- Read the [README](../README.md) for project overview
- Review the [Installation Guide](Installation.md) to set up your development environment
- Check existing [GitHub Issues](https://github.com/ct-Open-Source/tuya-convert/issues) to avoid duplicate work
- Understand the [System Architecture](System-Architecture.md) if contributing code

---

## Table of Contents

1. [Ways to Contribute](#ways-to-contribute)
2. [Reporting Device Compatibility](#reporting-device-compatibility)
3. [Contributing to PSK Research](#contributing-to-psk-research)
4. [Improving Documentation](#improving-documentation)
5. [Code Contributions](#code-contributions)
6. [Testing Procedures](#testing-procedures)
7. [Pull Request Process](#pull-request-process)
8. [Community Support](#community-support)

---

## Ways to Contribute

### 🔧 Device Testing & Reporting

**Most valuable contribution!** Testing devices and reporting compatibility helps the community know what works.

- Test new devices with tuya-convert
- Report successful flashes to device compatibility lists
- Report failed attempts with detailed logs
- Document device hardware variations

**See:** [Reporting Device Compatibility](#reporting-device-compatibility)

---

### 🔬 PSK Protocol Research

**Critical for future compatibility!** Help research the PSK Identity 02 protocol blocking newer devices.

- Capture network traffic from devices
- Extract firmware from working devices
- Analyze PSK generation patterns
- Test hypotheses about PSK derivation

**See:** [Contributing to PSK Research](#contributing-to-psk-research)

---

### 📝 Documentation Improvements

**Always needed!** Help improve guides, fix errors, and expand documentation.

- Fix typos and clarify confusing sections
- Add troubleshooting tips from your experience
- Create tutorials for specific platforms
- Translate documentation to other languages

**See:** [Improving Documentation](#improving-documentation)

---

### 💻 Code Contributions

**Advanced contributions!** Improve scripts, fix bugs, and add new features.

- Bug fixes and stability improvements
- Protocol implementation enhancements
- New platform support
- Testing infrastructure

**See:** [Code Contributions](#code-contributions)

---

### 💬 Community Support

**Help others!** Answer questions and provide support in issues and discussions.

- Answer questions in GitHub Issues
- Help troubleshoot user problems
- Share your experiences and solutions
- Participate in community discussions

---

## Reporting Device Compatibility

### Successful Flashes

If you successfully flash a device, please add it to the appropriate compatibility page:

**Pages:**
- [Compatible Devices (HTTP firmware)](Compatible-devices-(HTTP-firmware).md) - Devices with unencrypted firmware
- [Compatible Devices (HTTPS firmware)](Compatible-devices-(HTTPS-firmware).md) - Devices with encrypted firmware
- [Compatible Devices](Compatible-devices.md) - General compatibility list

**Information to Include:**

1. **Device Information**
   - Brand and model name
   - Purchase date and location
   - Product link (if available)
   - Device type (plug, switch, bulb, etc.)

2. **Flashing Details**
   - Firmware type (HTTP/HTTPS)
   - tuya-convert version used
   - Custom firmware installed (Tasmota, ESPurna, etc.)
   - Any special procedures required

3. **Tasmota Template** (if applicable)
   ```json
   {"NAME":"Device Name","GPIO":[...],"FLAG":...,"BASE":...}
   ```

4. **Console Rules** (if needed)
   ```
   Rule1 ON System#Boot DO Backlog ... ENDON
   ```

**How to Contribute:**
1. Edit the appropriate wiki page on GitHub
2. Add your device in alphabetical order
3. Follow the existing format
4. Create a pull request with clear description

---

### Failed Attempts

If a device fails to flash, please report it:

**Report Location:** [Failed Attempts and Tracked Requirements](Failed-attempts-and-tracked-requirements.md)

**Information to Include:**

1. **Device Information**
   - Brand and model
   - Purchase date (helps identify firmware version)
   - Device type

2. **Error Details**
   - Error message from tuya-convert
   - Contents of `smarthack-psk.log` (check for PSK Identity 02)
   - Screenshots of error output

3. **Logs**
   - Full terminal output from flashing attempt
   - Any error logs from scripts
   - Network capture (if available)

4. **PSK Identity Check**
   ```bash
   cat smarthack-psk.log | grep "ID: 02"
   ```
   If present, this is a PSK Identity 02 device - see [PSK Research](#contributing-to-psk-research)

---

## Contributing to PSK Research

The PSK Identity 02 protocol is the **primary blocker** preventing tuya-convert from working with newer devices (post-September 2019). Your research contributions could help restore functionality!

### Understanding the Problem

**What is PSK Identity 02?**
- New security protocol introduced by Tuya in late 2019
- Uses TLS-PSK (Pre-Shared Key) encryption
- Each device has unique PSK stored only on device and Tuya servers
- PSK cannot be derived from public information (MAC, gwId, etc.)

**Why It Blocks OTA Flashing:**
- tuya-convert cannot complete TLS handshake without PSK
- No TLS connection = no firmware upload
- Makes OTA flashing strategy non-viable for affected devices

**See:** [PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md) for technical details

---

### How to Identify PSK Identity 02 Devices

Check your `smarthack-psk.log` file for this pattern:

```
ID: 0242416f68626d64...  (starts with 02)
PSK: 2a9cf84b7a1b6bf1...
could not establish sslpsk socket: [SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC]
```

If you see `ID: 02`, you have a PSK Identity 02 device.

---

### Research Contributions Needed

#### 1. Network Captures (PCAP)

**What:** Capture network traffic during device pairing and activation

**When Helpful:**
- Capture from devices with **old firmware** before/after update
- Capture from devices that can still be flashed
- Capture showing `tuya.device.uuid.pskkey.get` endpoint

**How to Capture:**
```bash
# Start packet capture
tcpdump -i wlan0 -w capture.pcap port 443 or port 80

# Run tuya-convert while capture is running
# Stop capture when complete
```

**Tools:**
- Wireshark for analysis
- tshark for decryption (if PSK known)

**See:** [PSK Research Procedures](PSK-Research-Procedures.md) for detailed instructions

---

#### 2. Firmware Backups

**What:** Extract firmware from devices for PSK key analysis

**When Helpful:**
- Firmware from devices that **still work** with tuya-convert
- Firmware before/after OTA update to PSK Identity 02
- Firmware with PSK key stored at 0xFB000

**How to Extract:**

Option A: Via tuya-convert (if device is compatible)
```bash
# During flashing, firmware is backed up automatically
# Location: backup/
```

Option B: Serial connection (requires opening device)
```bash
# Use esptool to read flash
esptool.py -p /dev/ttyUSB0 read_flash 0x00000 0x100000 firmware.bin
```

**How to Contribute:**
1. Upload firmware to GitHub (as .zip or .gz)
2. Post link in [PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02.md) discussion
3. Include device information (brand, model, purchase date)

---

#### 3. PSK Key Analysis

**What:** Analyze PSK keys from firmware to find generation patterns

**Data Needed:**
- PSK keys from multiple devices (same model)
- PSK keys from different device models
- MAC addresses, gwId, prod_idx for correlation

**Hypotheses to Test:**
- Is PSK derived from MAC address?
- Is PSK derived from gwId + secret salt?
- Is PSK random but follows predictable pattern?
- Does PSK length (37 chars, base62) indicate specific algorithm?

**See:** [PSK Firmware Database](PSK-Firmware-Database.md) (Phase 5.4) for existing data

---

#### 4. Tool Development

**What:** Create tools to assist with PSK research

**Useful Tools:**
- Automated firmware analyzer (extract keys, versions, strings)
- PCAP analyzer for Tuya protocol patterns
- PSK key bruteforce/dictionary tools
- MAC/gwId to PSK prediction tools

**Languages:** Python preferred (existing codebase)

---

### Research Resources

- [PSK Research Procedures](PSK-Research-Procedures.md) - Detailed research methodology
- [PSK Affected Devices](PSK-Identity-02-Affected-Devices.md) - ~220 known incompatible devices
- [PSK Research Tools](PSK-Research-Tools.md) (Phase 5.4) - Tools for analysis
- [Original Issue #483](https://github.com/ct-Open-Source/tuya-convert/issues/483) - Community discussion

---

## Improving Documentation

### Documentation Structure

Wiki documentation is organized in `/docs/`:

**Core Guides:**
- Installation, Quick Start, Using Docker
- System Architecture, Protocol Overview

**Reference Pages:**
- API Reference, PSK documentation
- Device compatibility lists

**Templates:**
- `/docs/_templates/` - Standardized page templates

---

### Making Documentation Changes

**Small Changes (typos, clarifications):**

1. Edit the file directly on GitHub
2. Click "Edit this file" (pencil icon)
3. Make your changes
4. Submit pull request with description

**Large Changes (new pages, restructuring):**

1. Fork the repository
2. Clone your fork locally
3. Create a new branch: `git checkout -b improve-docs`
4. Make changes following template structure
5. Test markdown rendering locally
6. Commit and push changes
7. Create pull request against `development` branch

---

### Documentation Standards

**Follow Templates:**
- Use appropriate template from `/docs/_templates/`
- Maintain consistent heading hierarchy (H1 → H2 → H3)
- Include "Last Updated" and "Status" metadata

**Writing Style:**
- Clear, concise, beginner-friendly language
- Use code blocks with syntax highlighting
- Include examples for complex concepts
- Cross-reference related pages

**Technical Accuracy:**
- Verify code references (file paths and line numbers)
- Test commands before documenting
- Update documentation when code changes
- Add "Implementation:" field with file reference

**See:** [WIKI_RESTRUCTURING_PLAN.md](../WIKI_RESTRUCTURING_PLAN.md) for documentation architecture

---

## Code Contributions

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/tuya-convert.git
   cd tuya-convert
   ```

2. **Create Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/bug-description
   ```

3. **Install Dependencies**
   ```bash
   sudo ./install_prereq.sh
   ```

4. **Make Changes**
   - Follow existing code style (Python PEP 8)
   - Add comments for complex logic
   - Update documentation if needed

---

### Code Guidelines

**Python Code Style:**
- Follow PEP 8 style guide
- Use type hints for function signatures
- Add docstrings for modules, classes, and functions
- Keep functions focused and modular

**Example:**
```python
def process_device(gwId: str, protocol: str) -> Dict[str, Any]:
    """
    Process device activation request.

    Args:
        gwId: Gateway device ID
        protocol: Protocol version (2.1 or 2.2)

    Returns:
        Dictionary containing device activation response
    """
    # Implementation here
    pass
```

**Shell Scripts:**
- Use `#!/usr/bin/env bash` shebang
- Add script description at top
- Use functions for reusable code
- Validate input parameters

**Error Handling:**
- Catch and handle expected errors gracefully
- Provide helpful error messages
- Log errors for debugging
- Exit with appropriate status codes

---

### Testing Your Changes

**Manual Testing:**

1. **Test Basic Functionality**
   ```bash
   sudo ./start_flash.sh
   ```

2. **Test with Real Device**
   - Use test device if possible
   - Verify no regressions in existing functionality
   - Document test results

3. **Test Edge Cases**
   - Test with different protocol versions (2.1, 2.2)
   - Test with HTTP and HTTPS firmware
   - Test error handling with invalid input

**Code Quality:**
```bash
# Check Python syntax
python3 -m py_compile scripts/*.py

# Check shell scripts
shellcheck scripts/*.sh
```

---

### Commit Messages

**Format:**
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(server): add support for protocol 2.3

fix(smartconfig): correct CRC calculation for multicast mode

docs(wiki): add troubleshooting guide for PSK issues
```

---

## Pull Request Process

### Before Submitting

**Checklist:**
- [ ] Code follows project style guidelines
- [ ] All tests pass (manual testing completed)
- [ ] Documentation updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] Branch is up-to-date with `development` branch
- [ ] No merge conflicts

---

### Creating Pull Request

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**
   - Target: `development` branch (NOT `master`)
   - Title: Clear, concise description
   - Description: Explain what and why

3. **PR Description Template**
   ```markdown
   ## Changes
   - Change 1
   - Change 2

   ## Motivation
   Explain why these changes are needed

   ## Testing
   Describe how you tested these changes

   ## Related Issues
   Fixes #123
   ```

---

### Review Process

**What to Expect:**
- Maintainer will review code and provide feedback
- May request changes or improvements
- Discussion about implementation approach
- Testing by maintainer or community

**Response Time:**
- Reviews typically within 1-2 weeks
- Complex changes may take longer
- Be patient and responsive to feedback

**After Approval:**
- PR will be merged into `development` branch
- Changes will be included in next release
- Your contribution will be acknowledged

---

### Major Code Changes

**Important:** For major code changes, please discuss first!

1. **Open an Issue**
   - Describe proposed changes
   - Explain motivation and use cases
   - Discuss implementation approach

2. **Wait for Feedback**
   - Maintainers will provide guidance
   - Ensure changes align with project goals
   - Coordinate to avoid duplicate work

3. **Proceed with Implementation**
   - Follow agreed-upon approach
   - Keep maintainers updated on progress
   - Submit PR when ready

---

## Testing Procedures

### Device Testing Checklist

When testing a device with tuya-convert:

**Pre-Test:**
- [ ] Record device information (brand, model, purchase date)
- [ ] Take photos of device and packaging
- [ ] Document firmware version if visible in app

**During Test:**
- [ ] Run tuya-convert with logging enabled
- [ ] Save all log files (especially `smarthack-psk.log`)
- [ ] Take screenshots of any errors
- [ ] Note any special procedures required

**Post-Test:**
- [ ] Verify custom firmware works correctly
- [ ] Test all device features (GPIO, switches, etc.)
- [ ] Create Tasmota template if applicable
- [ ] Document any issues or quirks

---

### Regression Testing

If modifying core functionality:

**Test Scenarios:**
1. **Protocol 2.1** (unencrypted devices)
2. **Protocol 2.2** (encrypted devices)
3. **HTTP firmware** devices
4. **HTTPS firmware** devices
5. **Edge cases** (invalid input, network failures)

**Verify:**
- Existing functionality still works
- No new errors introduced
- Performance not degraded
- Documentation still accurate

---

## Community Support

### Supporting Other Users

**Answer Questions:**
- Check [GitHub Issues](https://github.com/ct-Open-Source/tuya-convert/issues) regularly
- Provide helpful, friendly responses
- Share your experiences and solutions
- Link to relevant documentation

**Troubleshooting Help:**
- Ask for logs and error messages
- Help identify PSK Identity 02 issues
- Suggest workarounds for common problems
- Escalate complex issues to maintainers

**Knowledge Sharing:**
- Share successful device flashes
- Document solutions to problems you solved
- Create tutorials for your specific use case
- Help keep compatibility lists updated

---

### Communication Channels

**GitHub Issues:**
- Bug reports and feature requests
- Device compatibility reports
- Technical discussions

**GitHub Discussions:**
- General questions and help
- Ideas and suggestions
- Community showcase

**External Forums:**
- [HomeAssistant Community](https://community.home-assistant.io/)
- [Tasmota Support Chat](https://discord.gg/Ks2Kzd4)

---

## Financial Support

This project is maintained by volunteers who invest significant time and resources.

**Support the Project:**
- [Become a Patron](https://www.patreon.com/kueblc)
- [Buy Me A Coffee](https://www.buymeacoffee.com/kueblc)
- [PayPal](https://paypal.me/kueblc)

Financial contributions help:
- Purchase devices for testing
- Cover hosting and infrastructure costs
- Support developer time
- Enable continued development

---

## Code of Conduct

**Be Respectful:**
- Treat all contributors with respect
- Welcome newcomers and help them learn
- Provide constructive feedback
- Assume good intentions

**Be Professional:**
- Keep discussions on-topic
- Avoid inflammatory language
- Respect differing opinions
- Focus on technical merits

**Be Patient:**
- Maintainers are volunteers
- Reviews take time
- Not all suggestions will be accepted
- Learning takes time

---

## Related Pages

- [Quick Start Guide](Quick-Start-Guide.md) - Get started with tuya-convert
- [Installation](Installation.md) - Set up development environment
- [System Architecture](System-Architecture.md) - Understand the codebase
- [Troubleshooting](Troubleshooting.md) - Common issues and solutions

---

## Contact

**Project Maintainer:** Colin Kuebler (@kueblc)

**Repository:** https://github.com/ct-Open-Source/tuya-convert

**Issues:** https://github.com/ct-Open-Source/tuya-convert/issues

---

*Thank you for contributing to tuya-convert! Every contribution, no matter how small, makes a difference.*
