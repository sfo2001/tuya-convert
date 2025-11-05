# PSK Collaboration Document - Extraction Plan

**Source File:** `docs/Collaboration-document-for-PSK-Identity-02.md` (554 lines)
**Status:** One extraction completed, three more planned

---

## Already Extracted ✅

### 1. PSK-Identity-02-Affected-Devices.md (361 lines)
- **Lines extracted:** 208-430
- **Content:** Complete list of ~220 devices known to have PSK Identity 02
- **Status:** ✅ Completed (commit: ccc2fec)

---

## Sections to Extract

### 2. PSK-Research-Procedures.md
**Lines:** 132-207 (76 lines)
**Content:**
- Decrypting network captures with known PSK (tshark commands)
- Creating network captures and firmware backups (step-by-step)
- Experiment design for understanding PSK generation
- Requirements and steps for testing
- Known issues with the experiment

**Why extract:**
- Self-contained technical procedures
- Useful for researchers working on PSK analysis
- Clearer as standalone reference document
- Can be updated independently

**References needed:**
- Link to firmware database
- Link to affected devices list

---

### 3. PSK-Firmware-Database.md
**Lines:** 431-500 (70 lines)
**Content:**
- Complete firmware data table (40 firmware samples)
- Columns: pcap, SDK versions, MAC addresses, prod_idx, auz_key, pskKey
- Color coding for firmware compatibility (🟢🟡🔴)
- Technical notes and observations about specific firmware
- String examples from firmware analysis

**Why extract:**
- Large technical data table
- Reference material for firmware analysis
- Separate concerns (data vs. analysis)
- Easier to update/maintain as table

**Additional content to include:**
- Lines 505-530 (String examples, JSON blobs)

---

### 4. PSK-Research-Tools.md
**Lines:** 531-554 (24 lines)
**Content:**
- TuyAPI library links and info
- Tuya API signing tools
- Tuya IoT Platform documentation links
- Reverse engineering tools
- mitmproxy setup guide for Android

**Why extract:**
- Resource collection for researchers
- Tools and external references
- Can be expanded without cluttering main doc
- Easier discoverability

---

## Restructured Main Document

**New file:** `docs/PSK-Identity-02-Protocol.md` (rename from Collaboration-document)
**Estimated size:** ~150 lines (down from 554)

**Structure:**
```markdown
# PSK Identity 02 Protocol Research

## Overview
- Brief description of PSK Identity 02 issue
- Link to GitHub issue #483

## Current Status
- What we know
- What we don't know
- Why this is hard

## The Challenge
- Technical explanation of PSK vs. previous identity
- Why OTA may no longer be viable

## Open Questions
- List of unanswered research questions

## Key Findings
- Firmware changes
- SDK versions
- PSK derivation formula
- Security mechanisms
- Important observations

## Research Resources
- [PSK Research Procedures](PSK-Research-Procedures.md) - How to capture and analyze
- [PSK Firmware Database](PSK-Firmware-Database.md) - Analyzed firmware samples
- [Affected Devices List](PSK-Identity-02-Affected-Devices.md) - Known incompatible devices
- [Research Tools](PSK-Research-Tools.md) - Tools and resources

## How You Can Help
- Steps for contributing to research
- What data to collect
- How to report findings

## Contributing
- Link to main repo CONTRIBUTING.md
- How to edit this research
```

---

## Implementation Steps

1. ✅ **Step 1:** Extract affected devices list (DONE)

2. **Step 2:** Extract PSK Research Procedures
   - Create `docs/PSK-Research-Procedures.md`
   - Copy lines 132-207 from main doc
   - Add frontmatter and navigation
   - Add code references where applicable
   - Commit: "docs: extract PSK research procedures"

3. **Step 3:** Extract PSK Firmware Database
   - Create `docs/PSK-Firmware-Database.md`
   - Copy lines 431-500 from main doc
   - Include string examples (505-530)
   - Improve table formatting if needed
   - Add legend and notes
   - Commit: "docs: extract PSK firmware database"

4. **Step 4:** Extract PSK Research Tools
   - Create `docs/PSK-Research-Tools.md`
   - Copy lines 531-554 from main doc
   - Organize by tool category
   - Add descriptions and use cases
   - Commit: "docs: extract PSK research tools"

5. **Step 5:** Restructure main document
   - Rename to `PSK-Identity-02-Protocol.md`
   - Remove extracted sections (keep lines 1-131)
   - Add cross-references to extracted files
   - Improve organization and clarity
   - Remove "Please help edit this document!" message
   - Commit: "docs: restructure PSK Identity 02 main document"

6. **Step 6:** Update README.md
   - Update docs/README.md to reflect new structure
   - Add PSK research section with all 5 files
   - Commit: "docs: update README with restructured PSK documentation"

---

## Benefits of This Extraction

### Organization
- Main doc becomes ~70% shorter and more focused
- Each document has single clear purpose
- Easier to find specific information

### Maintainability
- Firmware database can be updated independently
- Procedures can be improved without affecting findings
- Tools list can grow without cluttering research

### Discoverability
- Researchers can find procedures quickly
- Developers can access firmware data directly
- Tool recommendations are easy to locate

### Collaboration
- Clearer where to contribute specific types of info
- Easier to review and approve changes
- Less merge conflicts

---

## Validation Checklist

After all extractions:
- [ ] All 554 lines accounted for (no information loss)
- [ ] All cross-references working
- [ ] Main document reads clearly
- [ ] Each extracted file has proper frontmatter
- [ ] docs/README.md updated
- [ ] All commits pushed to branch

---

**Next Action:** Proceed with Step 2 (Extract PSK Research Procedures)
