# Phase 6: Create New Home Page

**Phase Status:** ⏳ PENDING
**Start Date:** -
**End Date:** -
**Progress:** 0/1 steps (0%)

[← Back to Overview](WIKI_RESTRUCTURING_PLAN.md) | [← Previous Phase](WIKI_PHASE_5_APPLY_TEMPLATES.md) | [Next Phase →](WIKI_PHASE_7_CROSS_REFERENCE.md)

---

## Phase Objectives

Complete rewrite of Home.md to create a professional wiki landing page with full navigation structure.

Current Home.md is minimal (7 lines) with no structure. New Home.md will be the central navigation hub for the entire wiki.

---

## Steps

### Step 6.1: Design New Home Page ⏳

**Status:** PENDING

#### Objective
Create comprehensive new home page with full navigation

#### Current State
```markdown
# TuyaConvert
## Collect things here

Devices:
* [Old devices](Compatible-devices)
* [HTTP (old) firmware](Compatible-devices-(HTTP-firmware))
* [HTTPS (new) firmware](Compatible-devices-(HTTPS-firmware))
```

#### Planned Structure

```markdown
# Welcome to tuya-convert Wiki

## Overview
[2-3 paragraphs about what tuya-convert is and does]

## Quick Start
- [Installation](Installation) - Set up tuya-convert
- [Quick Start Guide](Quick-Start-Guide) - Flash your first device
- [Troubleshooting](Troubleshooting) - Common issues and solutions

## Getting Started
- [Overview](Overview) - What is tuya-convert and how it works
- [Installation](Installation) - Detailed installation guide
- [Quick Start Guide](Quick-Start-Guide) - First device flash walkthrough
- [Supported Hardware](Supported-Hardware) - Hardware requirements

## Device Information
- [Compatible Devices](Compatible-devices) - Overview
- [HTTP Firmware Devices](Compatible-devices-(HTTP-firmware)) - Old firmware
- [HTTPS Firmware Devices](Compatible-devices-(HTTPS-firmware)) - New firmware
- [Failed Devices](Failed-attempts-and-tracked-requirements) - Known limitations

## Setup Guides
- [Using Docker](Using-Docker) - Docker setup
- [Using Raspberry Pi](Using-a-Raspberry-Pi) - Standard Pi setup
- [Using Pi Zero W](Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable) - Minimal setup
- [Using VirtualBox/VM](Using-VirtualBox-or-VM) - Virtual machine setup

## Advanced Topics
- [Flashing Multipart Binaries](Flash-a-multipart-binary) - Advanced flashing
- [Flashing Specific Devices](Flashing-of-WiFi-Switch-with-a-Raspberry-Pi) - Device-specific guides
- [Manual Flashing via Serial](Manual-Flashing-via-Serial) - Direct serial access

## Technical Reference
- [Protocol Overview](Protocol-Overview) - Protocol documentation hub
- [PSK Identity 02 Protocol](Collaboration-document-for-PSK-Identity-02) - PSK details
- [PSK Key Extraction](PSK-Key-from-Gosund-Wifi-Bulb) - Key extraction guide
- [Smartconfig Protocol](Smartconfig-Protocol) - Smartconfig details
- [System Architecture](System-Architecture) - How it all works together
- [API Reference](API-Reference) - HTTP endpoints and MQTT topics

## Troubleshooting
- [Troubleshooting Guide](Troubleshooting) - Common issues
- [Failed Attempts](Failed-attempts-and-tracked-requirements) - Known issues
- [Common FAQ](Common-Issues-FAQ) - Frequently asked questions

## Contributing
- [How to Contribute](How-to-Contribute) - Contribution guide
- [Contributing Device Data](Contributing-Device-Data) - Report compatibility
- [Contributing to PSK Research](Helping-with-new-psk-format) - Help with research
- [Additional Resources](Additional-Resources) - External resources

## Support
- [GitHub Issues](https://github.com/sfo2001/tuya-convert/issues) - Report bugs
- [Main Repository](https://github.com/sfo2001/tuya-convert) - Source code

---

**Last Updated:** [Date]
```

#### File Modified
- `docs/Home.md`

#### Template Used
- Hub-Page-Template.md (adapted for main landing page)

#### Validation Checklist
- [ ] All wiki pages linked
- [ ] Logical hierarchy
- [ ] Relative links only (no absolute URLs)
- [ ] Professional appearance
- [ ] Clear organization by category
- [ ] Quick start section at top
- [ ] No broken links
- [ ] Renders correctly in wiki

#### Planned Commit
- **Message:** "docs(wiki): create comprehensive new home page"
- **References:** WIKI_PHASE_6_NEW_HOME.md Step 6.1

---

## Dependencies

- **All previous phases** should be substantially complete
- **New pages** from Phase 4 should exist (or be marked as coming soon)
- **Cross-references** will be validated in Phase 7

---

## Design Considerations

### Navigation Priority
1. **Quick Start** - Most common user path
2. **Getting Started** - New users
3. **Device Information** - Primary user concern
4. **Setup Guides** - Platform-specific help
5. **Advanced Topics** - Power users
6. **Technical Reference** - Developers/researchers
7. **Troubleshooting** - Problem solving
8. **Contributing** - Community engagement

### User Experience Goals
- First-time visitor can find installation in < 10 seconds
- Device compatibility check is immediately visible
- Troubleshooting is easy to find
- Advanced users can quickly jump to technical docs
- Contributors can find how to help

---

## Validation

### Link Validation
Every link on the home page must:
- [ ] Exist (page is created or planned)
- [ ] Be relative (no absolute URLs to external repos)
- [ ] Work in wiki navigation
- [ ] Have accurate description

### Completeness Validation
- [ ] Every existing wiki page is linked
- [ ] Every new page from Phase 4 is linked
- [ ] No orphaned pages (all pages reachable from Home)

### Professional Appearance
- [ ] Clear headings and hierarchy
- [ ] Consistent formatting
- [ ] Brief descriptions for each link
- [ ] Organized by logical categories
- [ ] Not too long (scrollable in one page)

---

## Phase Completion Criteria

- [ ] New Home.md created
- [ ] All pages linked
- [ ] Navigation hierarchy clear
- [ ] Professional appearance
- [ ] Validation complete
- [ ] Commit made
- [ ] Phase document updated

---

## Commit Log

| Step | Commit Message | Date | SHA | Validated |
|------|---------------|------|-----|-----------|
| 6.1 | [pending] | - | - | ⏳ |

---

## References

- [Main Plan](WIKI_RESTRUCTURING_PLAN.md)
- [Information Architecture](WIKI_RESTRUCTURING_PLAN.md#information-architecture)
- [Hub Template (Phase 2)](WIKI_PHASE_2_TEMPLATES.md)
- [Next Phase](WIKI_PHASE_7_CROSS_REFERENCE.md)

---

**Phase 6: Pending** ⏳
**Last Updated:** 2025-11-05
**Estimated Duration:** 2 hours
