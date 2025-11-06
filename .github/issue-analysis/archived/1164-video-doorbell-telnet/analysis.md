# Issue #1164: video doorbell telnet access

**Reporter**: gralfj
**Date Posted**: 2025-06-19
**Status**: Out of Scope (Archived)
**Upstream**: https://github.com/ct-Open-Source/tuya-convert/issues/1164
**Related Issues**: #1157 (chip incompatibility - archived)

---

## Executive Summary

User reports gaining telnet and FTP access to a Tuya video doorbell from AliExpress and asks whether useful information can be extracted from the device. **This issue is out of scope for tuya-convert**, as the project is designed to flash alternative firmware on ESP8266/ESP32-based devices, not to explore or reverse engineer already-accessible devices. Video doorbells typically use non-ESP chips (ARM, proprietary SoCs) which are incompatible with tuya-convert's flashing process. The issue should be archived with guidance to appropriate resources for device exploration.

---

## Problem Description

### Context

The user purchased a Tuya-branded video doorbell from AliExpress and discovered open network services through port scanning. They self-identify as a beginner-level user but express willingness to follow detailed instructions.

### What the User Has

**Device Information**:
- **Type**: Tuya video doorbell
- **Source**: AliExpress
- **Network Address**: 192.168.0.46
- **Hostname**: 6c60ebc916cc

**Open Ports** (discovered via Nmap 7.94SVN):
- `21/tcp` - FTP (File Transfer Protocol)
- `23/tcp` - Telnet (remote terminal access)
- `6668/tcp` - IRC port (possibly repurposed for device communication)

### The User's Question

The user asks:
> "Is it feasible to extract useful information from the device given their skill level?"

They already have **root-level telnet access** and want to:
1. Explore the filesystem
2. Fix poor translations
3. Customize settings
4. Understand the device better

### What This Is NOT

- ❌ This is **not** a tuya-convert compatibility question
- ❌ The user is **not** trying to flash alternative firmware
- ❌ The device does **not** need to be "converted" or "hacked" for access
- ❌ This is **not** an ESP8266/ESP32 flashing issue

---

## Technical Analysis

### Why This Is Out of Scope for tuya-convert

#### 1. tuya-convert's Purpose

**From README.md:lines 1-8**:

> "tuya-convert provides the means to **backup the original and flash an alternative firmware**. Since reflashing devices using the ESP8266/85 is widespread among DIY smart home enthusiasts, we wanted to provide an easy way for everyone to **free their devices from the cloud** without the need for a soldering iron."

**tuya-convert is designed for**:
- ✅ **Flashing alternative firmware** (Tasmota, ESPurna, etc.) via OTA
- ✅ **ESP8266/ESP8285/ESP32** based devices
- ✅ Devices that **lack access** and need to be "converted"
- ✅ **Intercepting OTA updates** to install custom firmware

**tuya-convert is NOT designed for**:
- ❌ Exploring already-accessible devices
- ❌ Reverse engineering device internals
- ❌ Customizing existing firmware
- ❌ Non-ESP chip devices (ARM, proprietary SoCs)

#### 2. Video Doorbells Use Different Chips

**Camera/Video Doorbell Reality**:

**From `docs/Compatible-devices-(HTTP-firmware).md:228-232`**:
```
## Wifi Cameras

|Vendor|Area|Device Name|Vendors device ID|GPIOs|Notes|2nd MCU|Flash size/mode
|---------|:--------------:|:-----------:|:---------:|:------------:|:-------------------:|:-----------:|:------------:
|Akaso|EU|CS300|?|?|?|?|?|
```

**Observations**:
- Only **ONE** camera device listed in entire compatibility database
- All fields marked as "?" (unknown)
- No GPIO assignments (no ESP chip)
- No video doorbells listed at all

**Why Video Doorbells Are Different**:

Video doorbells typically use:
- **ARM-based SoCs** (System on Chip) - for video processing
- **Proprietary chips** - Custom silicon from camera module manufacturers
- **High-powered processors** - H.264/H.265 video encoding requires significant compute
- **Dedicated video hardware** - Hardware video encoders, ISPs (Image Signal Processors)
- **Large memory** - Video buffering needs far more RAM than ESP8266's 80KB

**Likely chip types in video doorbells**:
- **ARM Cortex processors** (ARM9, ARM11, Cortex-A series)
- **HiSilicon** chips (Chinese camera SoC vendor)
- **Ingenic** processors (T10, T20, T30 series)
- **MStar/Sigmastar** SoCs
- **Grain Media** GM chips
- **Anyka** AK37xx/AK39xx series

**None of these run ESP firmware** - they run Linux-based operating systems with proprietary camera stacks.

#### 3. The User Already Has Access

**Key Point**: The user **already gained telnet access** to the device.

This means:
- Device is **not locked down** (unusual for modern Tuya devices)
- No firmware flashing needed
- No "conversion" necessary
- Device is already "hacked" in terms of access

**tuya-convert's value proposition** is to **gain access** to locked-down devices. If you already have access, tuya-convert offers no benefit.

#### 4. Different Skill Set Required

**tuya-convert skills**:
- Running bash scripts
- Basic networking (connecting to WiFi AP)
- Following step-by-step instructions
- Understanding OTA flashing concepts

**Device exploration skills** (what user needs):
- Linux command line proficiency
- Filesystem navigation (`ls`, `cd`, `cat`, `find`)
- Understanding embedded Linux systems
- Reading configuration files
- Reverse engineering (optional, for deeper work)
- Hex editing, binary analysis (advanced)
- Understanding ARM assembly (advanced)
- Firmware unpacking/repacking (advanced)

These are **very different skill sets**.

---

## Why This Issue Exists

### User Confusion About Project Scope

**What users think tuya-convert does**:
- "Tuya device hacking tool"
- "General Tuya device exploration"
- "Community for all Tuya modifications"

**What tuya-convert actually does**:
- ESP8266/ESP32 firmware flashing via OTA
- Intercepting Tuya cloud OTA updates
- Installing Tasmota/ESPurna/etc.

### Limited Camera/Video Doorbell Documentation

**From device compatibility page**:
- Only 1 camera listed (out of hundreds of devices)
- No video doorbells at all
- No warning that cameras are generally incompatible
- Users may assume if it's Tuya, it works with tuya-convert

**Documentation gap**: No prominent notice that video/camera devices are generally out of scope.

### Success of Other Tuya Projects

Other projects in the Tuya ecosystem handle different use cases:
- **ltchiptool** - Flashing BK7231, RTL8710B, etc.
- **CloudCutter** - Exploiting newer Tuya cloud vulnerabilities
- **Various reverse engineering efforts** - Exploring Tuya protocols

Users may conflate these projects with tuya-convert.

---

## Proposed Resolution

### Archive as Out of Scope

**Recommendation**: **Archive this issue** with status **"Out of Scope - Not a tuya-convert Use Case"**

**Reasoning**:
1. ✅ User already has access (no conversion needed)
2. ✅ Video doorbell likely uses non-ESP chip
3. ✅ Request is for device exploration, not firmware flashing
4. ✅ tuya-convert cannot help with this use case
5. ✅ Different tools and skills required

### Provide Helpful Guidance

While archiving, provide the user with **constructive guidance** on where to get help:

---

## Response to User (Recommended)

Hi @gralfj,

Thanks for reaching out! I understand you have telnet access to your video doorbell and want to explore it. However, **this is out of scope for tuya-convert**.

### Why tuya-convert can't help

**tuya-convert is specifically designed** to:
- Flash alternative firmware (Tasmota, ESPurna) on **ESP8266/ESP32 devices**
- Intercept Tuya OTA updates to install custom firmware
- Help users who **don't have access** to their devices

Your situation is different:
- ✅ You **already have telnet access** (no conversion needed)
- ✅ Video doorbells typically use **ARM-based SoCs**, not ESP8266/ESP32
- ✅ You want to **explore existing firmware**, not flash new firmware

### What you can do

Since you have telnet access, here's what I recommend:

#### 1. Identify the Chip

```bash
# Connect via telnet
telnet 192.168.0.46

# Check CPU info
cat /proc/cpuinfo

# Check kernel version
uname -a

# Check mounted filesystems
cat /proc/mounts
```

This will tell you what processor you're dealing with (likely ARM, not ESP).

#### 2. Explore the Filesystem

```bash
# List root filesystem
ls -la /

# Check for interesting directories
ls /etc/
ls /opt/
ls /mnt/
ls /root/

# Look for configuration files
find / -name "*.conf" 2>/dev/null
find / -name "*.cfg" 2>/dev/null
find / -name "*.ini" 2>/dev/null
```

#### 3. Understand the System

```bash
# Check running processes
ps aux

# Check network connections
netstat -tulpn

# Look for startup scripts
ls /etc/init.d/
cat /etc/rc.local
```

#### 4. Backup Before Making Changes

```bash
# Create backup of important files before editing
cp /etc/some_config.conf /tmp/some_config.conf.backup
```

### Better Resources for Your Use Case

For exploring Tuya devices with existing access, check out:

1. **HomeAssistant Community Forums**
   - [https://community.home-assistant.io/](https://community.home-assistant.io/)
   - Many users discuss Tuya camera/doorbell modifications

2. **HACS Tuya Local Integration**
   - Alternative to cloud control
   - [https://github.com/rospogrigio/localtuya](https://github.com/rospogrigio/localtuya)

3. **IoT Device Hacking Communities**
   - [/r/homeautomation](https://www.reddit.com/r/homeautomation/)
   - [/r/homeassistant](https://www.reddit.com/r/homeassistant/)
   - [EEVblog Electronics Forums](https://www.eevblog.com/forum/)

4. **General Embedded Linux Resources**
   - [OpenWrt Forums](https://forum.openwrt.org/) (for embedded Linux expertise)
   - [Exploitee.rs](https://exploitee.rs/) (IoT security research)

### Warnings

⚠️ **Be Careful**:
- Modifying system files can **brick your device**
- Always make backups before changes
- Video doorbells often have **second MCUs** for camera processing
- Some partitions may be **read-only** (`mount -o remount,rw /`)

⚠️ **Legal Considerations**:
- Ensure you own the device (obviously, you do)
- Modifying firmware **may void warranty**
- Respect privacy laws when working with camera devices

### Why Video Doorbells Are Challenging

Video doorbells are more complex than simple switches/plugs:
- **Multiple processors** (main SoC + camera processor)
- **Proprietary video codecs**
- **Complex firmware** (often full Linux distributions)
- **Large flash storage** (50-100MB+, not 1MB like ESP devices)
- **Hardware dependencies** (camera modules, PIR sensors, speakers)

### If You Want ESP Firmware Flashing

If you have **other Tuya devices** (plugs, switches, bulbs) that you want to flash with Tasmota/ESPurna, then tuya-convert can help! But video doorbells are generally not compatible.

### Summary

- ✅ Your telnet access is great! You can explore the device.
- ❌ tuya-convert won't help with this particular use case.
- 🔍 Check out the resources above for device exploration guidance.
- 💡 Come back if you have **ESP8266/ESP32 devices** to flash!

Good luck with your exploration! 🚀

---

## Documentation Improvements

### Add Warning to Compatible Devices Page

**Proposed addition to `docs/Compatible-devices-(HTTP-firmware).md:228`**:

```markdown
## Wifi Cameras

⚠️ **IMPORTANT**: Most WiFi cameras and video doorbells use **ARM-based SoCs** (HiSilicon, Ingenic, MStar, etc.) rather than ESP8266/ESP32 chips. These devices are **not compatible with tuya-convert** and cannot run Tasmota or other ESP firmware.

**tuya-convert only works with ESP8266/ESP8285/ESP32-based devices.**

If you want to modify a camera/doorbell device:
- Check the chip type first (telnet/serial access may reveal this)
- Look for alternative tools specific to your chip (e.g., OpenIPC for HiSilicon)
- Consider local network control instead of firmware flashing

|Vendor|Area|Device Name|Vendors device ID|GPIOs|Notes|2nd MCU|Flash size/mode
|---------|:--------------:|:-----------:|:---------:|:------------:|:-------------------:|:-----------:|:------------:
|Akaso|EU|CS300|?|?|Compatibility unknown - cameras rarely use ESP chips|?|?|
```

### Add FAQ Entry

**Proposed addition to FAQ or Troubleshooting**:

```markdown
### Q: Can I use tuya-convert on my Tuya camera/video doorbell?

**A: Probably not.** Video cameras and doorbells almost always use ARM-based processors (HiSilicon, Ingenic, MStar, etc.) rather than ESP8266/ESP32 chips. These devices:

- ❌ **Cannot run ESP firmware** (Tasmota, ESPurna)
- ❌ **Will not work with tuya-convert**
- ❌ **Require different flashing tools** (if flashable at all)

**Why?** Video encoding requires much more processing power than ESP8266 can provide. Manufacturers use dedicated video SoCs with hardware encoding.

**Alternatives:**
- **Local network control**: Many cameras can be controlled via local API without firmware flashing
- **OpenIPC**: Firmware for HiSilicon/Ingenic camera chips ([https://openipc.org/](https://openipc.org/))
- **RTSP streams**: Access camera feed directly without cloud
- **Serial flashing**: If you're comfortable with hardware hacking (requires soldering)

**How to check your device:**
1. Look for FCC ID and search for teardown photos
2. Check if telnet/SSH is accessible and run `cat /proc/cpuinfo`
3. Open device and photograph the main chip (post to community forums for identification)
```

---

## Related Work

### Related Issues

- **#1157** - new tuya smart plug 20A convert failed attempt
  - **Status**: 📦 Archived (Hardware incompatibility)
  - **Similarity**: Also discovered device uses non-ESP chip (ECR6600)
  - **Resolution**: Documented alternative flashing methods
  - **Relevance**: Establishes precedent for archiving incompatible chip issues

### Related Documentation

- `docs/Compatible-devices-(HTTP-firmware).md:228-232` - WiFi Cameras section (mostly empty)
- `docs/Alternative-Chips-And-Flashing.md` - Alternative chips and flashing methods
- `README.md` - Project scope and purpose

---

## Timeline

- **2025-06-19**: Issue reported by gralfj
- **2025-11-06**: Analysis completed by Claude
- **2025-11-06**: Issue archived as "Out of Scope"

---

## Notes

### Why This User Had Telnet Access

**Interesting observation**: The device has **open telnet** (port 23) accessible on the local network.

This is **unusual** for modern Tuya devices because:
- Newer devices lock down telnet/SSH
- Security patches typically close these ports
- PSK Identity 02 devices are more locked down

**Possible explanations**:
1. **Older firmware version** - Device hasn't received security updates
2. **Development/Debug build** - Device shipped with debug firmware enabled
3. **OEM customization** - Reseller left debug access enabled
4. **Different manufacturer** - "Tuya-compatible" but not official Tuya firmware

**For the user**: This is actually **good news**! Having telnet access gives you significant control over the device. You can explore freely.

### Educational Value

While this issue is out of scope, it highlights an **important community education opportunity**:

**Many users think**:
- "Tuya = tuya-convert compatible"
- "All WiFi devices use ESP chips"
- "Cloud devices need firmware flashing to control locally"

**Reality**:
- Only ESP-based Tuya devices work with tuya-convert
- Many WiFi devices use ARM, MIPS, or proprietary chips
- Local control often possible without firmware flashing (APIs, MQTT, etc.)

**Documentation should make this clearer.**

### Positive Aspects of This Issue

Despite being out of scope, this issue shows:
1. ✅ Active, curious community
2. ✅ Users willing to explore and tinker
3. ✅ Opportunity to guide users to appropriate resources
4. ✅ Chance to improve documentation about scope

### Other Projects for Camera/Doorbell Devices

If the user is interested in camera/doorbell firmware modification:

**OpenIPC** - [https://openipc.org/](https://openipc.org/)
- Open-source IP camera firmware
- Supports HiSilicon, Goke, XM, etc.
- Active community
- Not as simple as tuya-convert, but very capable

**Wyze Hacks** - [https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks](https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks)
- Custom firmware for Wyze/Xiaomi cameras
- Many use similar chips to Tuya cameras
- May have applicable techniques

---

## Conclusion

**Issue Status**: **📦 Archived - Out of Scope**

**Reason**: This issue requests help with exploring an already-accessible video doorbell device, which is outside the scope of tuya-convert. The project is designed specifically for flashing alternative firmware on ESP8266/ESP32-based devices via OTA, not for device exploration or modification of ARM-based camera systems.

**Action Taken**:
1. ✅ Analyzed issue and determined out of scope
2. ✅ Provided comprehensive guidance to user
3. ✅ Recommended appropriate resources and communities
4. ✅ Documented issue for future reference
5. ✅ Proposed documentation improvements

**Resolution**: Archived with helpful guidance. User directed to appropriate resources for embedded Linux device exploration and camera-specific communities.

**Documentation Improvements Recommended**:
- Add warning to WiFi Cameras section about chip compatibility
- Add FAQ entry explaining why cameras/doorbells aren't supported
- Clarify project scope more prominently in documentation

---

**Analysis By**: Claude
**Analysis Date**: 2025-11-06
**Last Updated**: 2025-11-06
