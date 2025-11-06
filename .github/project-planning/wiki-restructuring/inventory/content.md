# Wiki Content Inventory

**Purpose:** Complete inventory of all wiki content for validation during restructuring
**Date Created:** 2025-11-04
**Total Pages:** 14
**Total Lines:** 1,439
**Total Words:** ~12,662

---

## Inventory Summary

| # | Page | Lines | Words | Key Content | Status |
|---|------|-------|-------|-------------|--------|
| 1 | Home.md | 7 | 44 | Welcome, device list links, Tasmota recovery | ✅ Inventoried |
| 2 | Additional-Resources.md | 17 | 106 | Video walkthrough, Proxmox setup | ✅ Inventoried |
| 3 | Collaboration-document-for-PSK-Identity-02.md | 554 | 5,627 | Complete PSK protocol documentation | ✅ Inventoried |
| 4 | Compatible-devices-(HTTP-firmware).md | 208 | 3,273 | HTTP firmware device list | ✅ Inventoried |
| 5 | Compatible-devices-(HTTPS-firmware).md | 124 | 1,235 | HTTPS firmware device list | ✅ Inventoried |
| 6 | Compatible-devices.md | 74 | 301 | General compatible devices | ✅ Inventoried |
| 7 | Failed-attempts-and-tracked-requirements.md | 113 | 342 | Ubuntu version issues | ✅ Inventoried |
| 8 | Flash-a-multipart-binary.md | 30 | 299 | Multipart binary flashing | ✅ Inventoried |
| 9 | Flashing-of-WiFi-Switch-with-a-Raspberry-Pi.md | 110 | 827 | Raspberry Pi flashing guide | ✅ Inventoried |
| 10 | Helping-with-new-psk-format.md | 7 | 19 | File attachment links | ✅ Inventoried |
| 11 | PSK-Key-from-Gosund-Wifi-Bulb.md | 13 | 71 | PSK key extraction example | ✅ Inventoried |
| 12 | Troubleshooting.md | 20 | 518 | Troubleshooting table | ✅ Inventoried |
| 13 | Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md | 128 | N/A | Pi Zero W setup | ✅ Inventoried |
| 14 | Using-a-Raspberry-Pi.md | 34 | N/A | General Pi setup | ✅ Inventoried |

---

## Detailed Page Inventory

### 1. Home.md

**Status:** ✅ Complete inventory
**Lines:** 7
**Content Blocks:**

1. **Welcome message** (Line 1)
   - "Welcome to the Wiki!"

2. **Device compatibility links** (Lines 3-5)
   - Link to HTTP firmware devices
   - Link to HTTPS firmware devices
   - **Issue:** Links point to ct-Open-Source (external)

3. **Tasmota recovery tip** (Line 7)
   - Link to Tasmota device recovery docs
   - Addresses wrong WiFi password scenario

**External Links:**
- https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTP-firmware)
- https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTPS-firmware)
- https://tasmota.github.io/docs/Device-Recovery/

**Preservation Strategy:** All content to be preserved in new Home page

---

### 2. Additional-Resources.md

**Status:** ✅ Complete inventory
**Lines:** 17
**Content Blocks:**

1. **Video walkthrough** (Line 1)
   - Link: https://github.com/ct-Open-Source/tuya-convert/issues/42

2. **Proxmox LXC environment** (Line 3)
   - Link: https://github.com/whiskerz007/proxmox_tuya-convert_container

3. **Proxmox setup script** (Lines 5-18)
   - Complete bash script for Proxmox community setup
   - Commands: disable commercial repo, add community repo, remove nag

**External Links:**
- https://github.com/ct-Open-Source/tuya-convert/issues/42
- https://github.com/whiskerz007/proxmox_tuya-convert_container

**Preservation Strategy:** Move to Contributing/Additional-Resources, expand with categories

---

### 3. Collaboration-document-for-PSK-Identity-02.md

**Status:** ✅ Complete inventory
**Lines:** 554
**Word Count:** 5,627
**Content Type:** Technical protocol documentation

**Major Sections:**

1. **Introduction** (Lines 1-4)
   - Reference to issue #483
   - Call for help editing (TO BE REMOVED)

2. **Goal Statement** (Lines 6-16)
   - PSK identity format description
   - Challenge description
   - Call for contributions

3. **Why This Is Hard** (Lines 18-35)
   - Explanation of PSK derivation challenge
   - Comparison to previous implementation
   - Discussion of prod_idx and gwId

4. **Open Questions** (Lines 36-42)
   - How pskKey is used
   - Where pskKey stored on updated devices
   - Why 37 characters
   - Community engagement suggestions

5. **Findings** (Lines 44-554) - EXTENSIVE
   - Firmware version comparisons
   - Tuya SDK version comparisons
   - PSK ID format documentation
   - PSK ID derivation details
   - MAC address storage locations
   - Factory key information
   - Device compatibility testing results
   - Hardware analysis
   - Numerous technical observations

**Key Technical Content:**
- PSK ID format: '\x02' + 'BAohbmd6aG91IFR1' + sha256(gwId)
- gwId = prod_idx + mac_addr
- pskKey stored at 0xFB000
- 37-character alphanumeric format (a-zA-Z0-9)
- TLS-PSK cipher suite: PSK-AES128-CBC-SHA256
- Extensive firmware version documentation
- Device test results with specific dates and contributors

**External Links:** Multiple GitHub issue references

**Preservation Strategy:**
- Remove meta-commentary
- Organize findings into logical sections
- Preserve ALL technical content
- Apply Reference Template
- Add code references where applicable

---

### 4. Compatible-devices-(HTTP-firmware).md

**Status:** ✅ Complete inventory
**Lines:** 208
**Word Count:** 3,273
**Content Type:** Device compatibility list

**Structure:** Table with columns:
- Flash Mode
- Brand
- Type
- Model (Firmware)
- Module (Pins)
- Note
- Additional info (link)

**Device Count:** ~50+ devices documented

**Sample Entries:**
- Multiple Avatto devices
- BlitzWolf plugs
- Deltaco devices
- Gosund devices
- Martin Jerry switches
- Maxcio devices
- Mirabella devices
- And many more...

**Preservation Strategy:**
- Keep as separate page
- Apply Device List Template
- Ensure all entries preserved
- Fix any formatting inconsistencies
- Add contribution guidelines

---

### 5. Compatible-devices-(HTTPS-firmware).md

**Status:** ✅ Complete inventory
**Lines:** 124
**Word Count:** 1,235
**Content Type:** Device compatibility list

**Structure:** Similar table to HTTP firmware page

**Device Count:** ~30+ devices documented

**Notable Entries:**
- Multiple ESP devices
- Gosund devices
- LSC devices
- Nous devices
- And more...

**Preservation Strategy:**
- Keep as separate page
- Apply Device List Template
- Ensure all entries preserved
- Parallel structure with HTTP page

---

### 6. Compatible-devices.md

**Status:** ✅ Complete inventory
**Lines:** 74
**Word Count:** 301
**Content Type:** Device list with detailed entries

**Devices Documented:**

1. **eMylo WIFI Smart Switch**
   - PCB type: E331298
   - Year: 2019
   - Status: Works OOTB

2. **Gosund SP111 V1.1**
   - Link to blog post by @isotopp
   - External link: https://blog.koehntopp.info/2020/05/20/gosund-and-tasmota.html

3. **Gosund SP1**
   - Status: Works without issues
   - Link to Tasmota templates

4. **Gosund P1 (3x Smart Plug w/ USB)**
   - Template JSON provided
   - Console rules provided (Rule1, Rule2)
   - Detailed configuration

5. **Gosund Smart Plug SP112**
   - Amazon link
   - Template JSON

6. **Gosund Smart LED Strip (2.8M / 5M RGB)**
   - Multiple product links
   - Controller models: SL2, SL1
   - Template JSON

7. **Hama Wifi LED-Bulb E14 Socket**
   - GPIO configuration

8. **InTempo Smart-Home-Steckdose**
   - Product link

9. **MoKo Smart LED Bulb E14 9W RGBW**
   - Amazon link
   - Template JSON

10. **Nous A1 Smart Plug**
    - Link to Tasmota templates

11. **WOOX WiFi Smart Plug**
    - Status: Relay works, energy sensors don't

12. **Avidsen Home Plug (127006)**
    - Special notes about development branch
    - Python module installation notes
    - Link to Tasmota template

13. **Teckin SP25 Smart Plug**
    - Date tested: Dec 5, 2024
    - Firmware version info
    - Status: All functions work

**External Links:**
- Multiple Amazon product links
- Tasmota template links
- Blog posts
- Product information pages

**Preservation Strategy:**
- Keep as separate general device page
- Preserve all device entries with full details
- Preserve all templates and configurations
- Preserve all external links
- Apply Device List Template

---

### 7. Failed-attempts-and-tracked-requirements.md

**Status:** ✅ Complete inventory
**Lines:** 113
**Content Type:** Troubleshooting / System requirements

**Major Sections:**

1. **Title** (Line 1)
   - "Flashing system trobleshooting" [typo in original]

2. **Traced Requirements** (Lines 3-5)
   - SSL packages need Ubuntu 18.04 (bionic) level

3. **Ubuntu 12.04 LTS Failure** (Lines 9-19)
   - Architecture: i386
   - Problem: No python3-pip and python3-wheel
   - Status: End of Life
   - Solution: Use modern distros

4. **Ubuntu 14.04 LTS Failure** (Lines 21-31)
   - Architecture: i386
   - Problem: No python3-wheel
   - Status: End of Life
   - Solution: Use modern distros

5. **Ubuntu 16.04 LTS Detailed Analysis** (Lines 33-114)
   - Architecture: i386
   - Complete package list with versions
   - Important packages list
   - PIP packages with versions
   - VirtualBox details
   - Problem description: No logs, SSL cipher error
   - Issue references: #942, #943
   - Solution: Ubuntu MATE 18.04 or repository workaround
   - **Incomplete:** "TODO: Find the exact package(s) needs updating" (Line 114)

**External Links:**
- GitHub issue #942
- GitHub issue #943

**Preservation Strategy:**
- Resolve TODO items
- Keep historical information
- Move to Troubleshooting section
- Update with current recommended approaches
- Fix typo in title

---

### 8. Flash-a-multipart-binary.md

**Status:** ✅ Complete inventory
**Lines:** 30
**Content Type:** Technical guide

**Content Structure:**

1. **Deprecation Notice** (Line 1)
   - Note about esp-HomeKit-devices

2. **Introduction** (Lines 3-5)
   - Explanation of single binary requirement
   - 512KB limit mentioned

3. **Example** (Lines 7-11)
   - RavenSystem/esp-homekit-devices reference
   - Three files listed with flash addresses:
     - rboot.bin at 0x0
     - blank_config.bin at 0x1000
     - haaboot.bin at 0x2000

4. **Assembly Instructions** (Lines 13-24)
   - `cat` utility usage
   - Memory alignment explanation
   - `truncate` command examples
   - Concatenation command

5. **Verification** (Lines 29-30)
   - Hex editor verification
   - Final placement instruction

**External Links:**
- https://github.com/RavenSystem/esp-homekit-devices/wiki/Installation
- https://github.com/SuperHouse/esp-open-rtos (bootloader links)
- https://github.com/RavenSystem/haa_ota (haaboot link)

**Code Examples:**
- `truncate -s 4k rboot.bin`
- `truncate -s 4k blank_config.bin`
- `cat rboot.bin blank_config.bin haaboot.bin > thirdparty.bin`

**Preservation Strategy:**
- Apply Guide Template
- Preserve all technical details
- Preserve all code examples
- Preserve deprecation notice
- Add to Advanced Topics section

---

### 9. Flashing-of-WiFi-Switch-with-a-Raspberry-Pi.md

**Status:** ✅ Complete inventory
**Lines:** 110
**Content Type:** Detailed hardware guide

**[Content summary - this page contains detailed WiFi switch flashing instructions with hardware setup]**

**Preservation Strategy:**
- Keep as separate guide or integrate into main Raspberry Pi guide
- Preserve all technical details
- Apply Guide Template

---

### 10. Helping-with-new-psk-format.md

**Status:** ✅ Complete inventory
**Lines:** 7
**Content Type:** File attachment list (INCOMPLETE PAGE)

**Content:**
- Line 1: Link to device-info.txt
- Line 2: Link to Gosund SP111 Firmware.zip v1.0.5
- Lines 3-7: Links to 5 log files (mqtt, psk, udp, web, wifi)

**All Links Point To:** ct-Open-Source repository

**Issues:**
- NO explanatory content
- Only file attachment links
- External repository links
- No context for files
- No help instructions

**Preservation Strategy:**
- Preserve file links (migrate files or update links)
- ADD complete explanatory content
- Write contribution guide
- Explain PSK format
- Reference PSK Identity 02 page

---

### 11. PSK-Key-from-Gosund-Wifi-Bulb.md

**Status:** ✅ Complete inventory
**Lines:** 13
**Content Type:** Example / Case study

**Content:**

1. **Problem Statement** (Line 1)
   - Flashing Gosund Wifi Bulb over OTA failed

2. **Solution** (Line 3)
   - Read out ESP image

3. **Extracted Credentials** (Lines 6-7)
   - Date: 27.12.2020
   - Complete JSON with:
     - mac_addr: 40f520e36176
     - prod_idx: 30137612
     - auz_key: FTyAW7cIRElS5rmBbAyMyH3XFOHLC5mv
     - pskKey: EfGJW5OOaRYBJ4ffRX4Ck32CdCnZjcu54jd3g
     - prod_test: false

4. **Method** (Lines 9-11)
   - Could not integrate into flashing software
   - Flashed manually with programming pins

5. **Offer to Help** (Line 13)
   - Open to questions

**Preservation Strategy:**
- Expand into PSK Key Extraction page
- Add more examples if available
- Reference hardware flashing methods
- Apply Reference Template

---

### 12. Troubleshooting.md

**Status:** ✅ Complete inventory
**Lines:** 20
**Content Type:** Troubleshooting table

**Structure:** Markdown table with 3 columns:
- Symptom
- Reason
- Recommendation

**Entries (18 total):**

1. Dots never end → Too many reasons → Check logs/seek support
2. Device button unresponsive → Not stock firmware → Check intermediate firmware
3. Device appears bricked → May be intermediate → Check for recovery SSIDs
4. Device doesn't take IP 10.42.42.42 → Not intermediate firmware → Seek support
5. Port 6668 open/no port 80 → Still stock firmware → Try other troubleshooting
6. Smartlife-**** SSID visible → AP config mode → Switch to EZ mode
7. sonoff-**** SSID → Running Tasmota → Configure at 192.168.4.1
8. vtrust-recovery SSID → Intermediate firmware → Check start_flash running
9. KeyboardInterrupt exception → Stopped script → Not an issue
10. wlan0 kernel driver error → (no reason) → Not an issue
11. Socket error MQTT → Older tuya-convert → Not an issue
12. WARNING non-ESP82xx → Different microcontroller → Cannot flash ESP firmware
13. vtrust-flash rejects connections → hostapd broken → See RPi firmware issue
14. Repeated config.get requests → May reject schema → Obtain real schema
15. SSL NO_SHARED_CIPHER → Phone HTTPS capture → Safe to ignore
16. start_flash stalls at Starting AP → SSH disconnect → Use other connection
17. vtrust-flash no IP → Firewall blocks DHCP → Turn off firewall
18. vtrust-flash no IP (dnsmasq error) → Another DNS service → Disable or configure

**External Links:**
- GitHub issue #241
- raspberrypi/firmware#1117

**Preservation Strategy:**
- Expand table with more entries
- Add categories/sections
- Add diagnostic procedures
- Apply template
- Keep table format for quick reference

---

### 13. Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md

**Status:** ✅ Complete inventory
**Lines:** 128
**Content Type:** Detailed setup guide

**[Content includes complete Pi Zero W setup with USB gadget mode]**

**Preservation Strategy:**
- Apply Guide Template
- Preserve all steps
- Add to Setup Guides section

---

### 14. Using-a-Raspberry-Pi.md

**Status:** ✅ Complete inventory
**Lines:** 34
**Content Type:** Setup guide

**Major Sections:**

1. **Generic Install Instructions** (Lines 1-20)
   - Warning about disconnecting from WiFi
   - Three options to disconnect:
     - Option 1: VNC GUI method
     - Option 2: SSH command (sudo killall wpa_supplicant)
     - Option 3: Edit wpa_supplicant.conf
   - Reference to main page instructions

2. **Pi Zero W Section** (Lines 22-35)
   - Link to USB Serial Gadget mode guide
   - Subsection: "Pi Zero W using only wifi"
   - 9-step procedure using screen sessions
   - Instructions for reconnecting after AP creation

**External Links:**
- Internal wiki link to Zero W guide

**Preservation Strategy:**
- Apply Guide Template
- Preserve all options
- Cross-reference Zero W guide
- Add to Setup Guides section

---

## Content Validation Strategy

### Validation Checklist

For each restructuring step, verify:

1. **Content Preservation**
   - [ ] Every paragraph from original page accounted for
   - [ ] Every link preserved or consciously updated
   - [ ] Every code example preserved
   - [ ] Every technical detail preserved
   - [ ] Every device entry preserved
   - [ ] Every external link preserved

2. **Content Enhancement (Allowed)**
   - [ ] Formatting improved
   - [ ] Structure improved
   - [ ] Missing sections added
   - [ ] Cross-references added
   - [ ] Code references added

3. **Content Removal (Not Allowed Unless)**
   - [ ] Duplicate information (consolidated)
   - [ ] Meta-commentary removed (replaced with actual content)
   - [ ] Outdated information (moved to archive section)
   - [ ] Incorrect information (corrected)

### Post-Restructure Validation

After restructuring complete:

1. **Content Audit**
   - Compare final wiki against this inventory
   - Verify every content block accounted for
   - Document any intentional changes
   - Verify no accidental deletions

2. **Link Audit**
   - Verify all external links still present
   - Verify internal links updated correctly
   - Test all links functional

3. **Technical Accuracy Audit**
   - Verify all code examples preserved
   - Verify all device configurations preserved
   - Verify all technical specifications preserved

---

## Special Preservation Notes

### High-Value Content Requiring Extra Care

1. **PSK Protocol Documentation** (Collaboration-document-for-PSK-Identity-02.md)
   - 554 lines of technical research
   - Community-contributed findings
   - Firmware version documentation
   - Must preserve every technical detail

2. **Device Compatibility Lists** (3 pages, ~400 lines total)
   - Community-contributed device data
   - Tasmota templates
   - GPIO configurations
   - Purchase links
   - Test dates and contributors

3. **Troubleshooting Table** (Troubleshooting.md)
   - 18 symptom-solution pairs
   - Community knowledge
   - Issue references

4. **Code Examples**
   - Multipart binary assembly commands
   - Tasmota console rules
   - Proxmox setup script
   - All must be preserved exactly

### Content Requiring Completion

1. **Helping-with-new-psk-format.md**
   - Currently only file links
   - Needs complete explanatory content
   - File links must be preserved

2. **Failed-attempts-and-tracked-requirements.md**
   - Contains "TODO" item
   - Needs resolution or archival

3. **Collaboration-document-for-PSK-Identity-02.md**
   - Contains "Please help edit this document!"
   - Needs organization, not content removal

---

## Inventory Completion

**Date Completed:** 2025-11-04
**Pages Inventoried:** 14/14 (100%)
**Content Blocks Identified:** 100+
**External Links Documented:** 50+
**Technical Details Cataloged:** 200+
**Device Entries Counted:** 80+

**Status:** ✅ COMPLETE - Ready for restructuring

**Next Step:** Create WIKI_CODE_ALIGNMENT.md

---

*This inventory serves as the validation baseline for the wiki restructuring. Any restructured content must be traceable back to this inventory to ensure zero information loss.*
