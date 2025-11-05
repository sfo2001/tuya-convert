# Wiki Restructuring Plan

**Project:** tuya-convert
**Repository:** https://github.com/sfo2001/tuya-convert
**Wiki Repository:** https://github.com/sfo2001/tuya-convert.wiki
**Working Directory:** `docs/` (wiki migrated to main repository)
**Date Created:** 2025-11-04
**Last Updated:** 2025-11-05
**Status:** EXECUTION PHASE - Phase 1 In Progress

---

## ⚠️ Important: Working Directory

**All wiki restructuring work is performed in the `docs/` directory of the main repository.**

- **Migration Date:** 2025-11-04 (commit `256a89b`)
- **Reason:** Better version control and documentation-code alignment
- **Source:** GitHub Wiki (https://github.com/sfo2001/tuya-convert/wiki)
- **Backup:** `wiki-backup-20251105/` (preserved for reference)
- **Current Status:** Wiki files migrated to `docs/`, restructuring in progress

All file paths in this plan refer to files in the `docs/` directory unless otherwise specified.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Current State Analysis](#current-state-analysis)
3. [Restructuring Principles](#restructuring-principles)
4. [Standardized Page Templates](#standardized-page-templates)
5. [Information Architecture](#information-architecture)
6. [Detailed Step-by-Step Plan](#detailed-step-by-step-plan)
7. [Validation Checkpoints](#validation-checkpoints)
8. [Codebase Alignment Strategy](#codebase-alignment-strategy)
9. [Progress Tracking](#progress-tracking)

---

## Executive Summary

### Objectives
1. **Restructure** the wiki with a professional, logical information architecture
2. **Standardize** all pages using consistent templates and formatting
3. **Preserve** 100% of existing information (zero information loss)
4. **Align** wiki documentation with actual codebase implementation
5. **Fix** broken links and references to original repository
6. **Complete** incomplete pages and remove "call for help" messages
7. **Validate** each step with checkpoints before committing

### Scope
- **14 existing wiki pages** to be restructured
- **New pages** to be created for missing documentation
- **All commits** to be atomic and validated
- **Cross-references** between code and wiki to be established

---

## Current State Analysis

### Wiki Inventory (14 Pages)

| # | Page Name | Lines | Status | Issues |
|---|-----------|-------|--------|--------|
| 1 | Home.md | 7 | ⚠️ Poor | No structure, broken links to ct-Open-Source |
| 2 | Additional-Resources.md | 17 | ✅ OK | Minimal but complete |
| 3 | Collaboration-document-for-PSK-Identity-02.md | 554 | ⚠️ Draft | Call for help, bulk copy-paste, needs organization |
| 4 | Compatible-devices-(HTTP-firmware).md | 208 | ✅ Good | Complete device list |
| 5 | Compatible-devices-(HTTPS-firmware).md | 124 | ✅ Good | Complete device list |
| 6 | Compatible-devices.md | 74 | ✅ Good | Complete device list |
| 7 | Failed-attempts-and-tracked-requirements.md | 113 | ⚠️ Incomplete | Contains TODO items, unresolved |
| 8 | Flash-a-multipart-binary.md | 30 | ✅ Good | Complete technical guide |
| 9 | Flashing-of-WiFi-Switch-with-a-Raspberry-Pi.md | 110 | ✅ Good | Complete guide |
| 10 | Helping-with-new-psk-format.md | 7 | ❌ Incomplete | Only file links, no content |
| 11 | PSK-Key-from-Gosund-Wifi-Bulb.md | 13 | ✅ OK | Short but complete |
| 12 | Troubleshooting.md | 20 | ✅ Good | Well-structured table |
| 13 | Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md | 128 | ✅ Good | Complete guide |
| 14 | Using-a-Raspberry-Pi.md | 34 | ✅ Good | Complete guide |

### Critical Issues Identified

#### 1. Broken/External Links
- Home.md line 4: `https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTP-firmware)`
- Home.md line 5: `https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTPS-firmware)`
- Additional-Resources.md line 1: `https://github.com/ct-Open-Source/tuya-convert/issues/42`
- Helping-with-new-psk-format.md lines 1-7: All file links point to ct-Open-Source
- Multiple pages: Various references to original repository

#### 2. Incomplete Content
- **Helping-with-new-psk-format.md**: Only contains file attachment links, no explanatory content
- **Collaboration-document-for-PSK-Identity-02.md**: Contains "Please help edit this document!" and unorganized bulk copy-paste
- **Failed-attempts-and-tracked-requirements.md**: Contains "TODO: Find the exact package(s) needs updating"

#### 3. No Information Architecture
- No clear categorization (Getting Started, Advanced, Reference, Contributing)
- No navigation hierarchy
- Home page provides no overview or structure
- Related pages not cross-referenced

#### 4. Missing Essential Pages
- No Installation guide (separate from README)
- No Quick Start guide
- No Docker Setup guide (separate from README)
- No Contributing guide
- No Protocol Reference overview page
- No Architecture/System Design documentation

---

## Restructuring Principles

### Core Principles

1. **Zero Information Loss**
   - Every piece of information from existing pages MUST be preserved
   - Before deleting/moving content, validate it exists elsewhere
   - Archive old content if restructuring significantly

2. **Atomic Commits**
   - Each step = one commit
   - Commit message must describe exactly what changed
   - Include validation status in commit message

3. **Validation Before Commit**
   - Content validation (all info preserved)
   - Link validation (all links work)
   - Format validation (follows template)
   - Cross-reference validation (related pages linked)

4. **Professional Consistency**
   - All pages follow standardized template
   - Consistent heading hierarchy (H1 = title, H2 = major sections, etc.)
   - Consistent terminology throughout
   - Consistent code block formatting

5. **Codebase Alignment**
   - Wiki technical documentation must reference actual code
   - Code file paths and line numbers included where relevant
   - Protocol documentation aligned with implementation
   - No documentation-code drift

---

## Standardized Page Templates

### Template 1: Guide/Tutorial Page

```markdown
# [Page Title]

**Last Updated:** [Date]
**Status:** ✅ Complete | ⚠️ Draft | 🔄 In Progress

## Overview

[1-3 sentences describing what this guide covers and who it's for]

## Prerequisites

- Prerequisite 1
- Prerequisite 2
- Prerequisite 3

## [Main Content Section 1]

[Content...]

### [Subsection if needed]

[Content...]

## [Main Content Section 2]

[Content...]

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| ... | ... | ... |

## Related Pages

- [Link to related page 1]
- [Link to related page 2]

## References

- [External link 1]
- [Internal code reference: `path/to/file.py:123`]

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
```

### Template 2: Reference Page

```markdown
# [Reference Title]

**Last Updated:** [Date]
**Status:** ✅ Complete | ⚠️ Draft | 🔄 In Progress
**Implementation:** `path/to/implementation.py`

## Overview

[1-3 sentences describing what this reference covers]

## [Topic 1]

### Description
[Detailed explanation]

### Implementation Details
[Technical details]

### Code Reference
- File: `path/to/file.py`
- Function: `function_name()` (line 123)
- Related: `other_file.sh` (line 45)

## [Topic 2]

[Same structure...]

## Examples

```bash
# Example 1
code here
```

## Related Pages

- [Link to related page 1]
- [Link to related page 2]

## External References

- [External link 1]
- [External link 2]

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues) or check the [Troubleshooting](Troubleshooting) page.*
```

### Template 3: Device List Page

```markdown
# [Device Category]

**Last Updated:** [Date]
**Status:** ✅ Maintained | 🔄 Community Updated

## Overview

[Description of device category and compatibility criteria]

## How to Contribute

To add a device to this list:
1. Successfully flash the device using tuya-convert
2. Document the device details below
3. [Edit this page](link) or [open an issue](link)

## Device List

### [Device Name 1]

**Status:** ✅ Works | ⚠️ Partial | ❌ Failed
**Date Tested:** YYYY-MM-DD
**Firmware Type:** HTTP | HTTPS
**Purchase Link:** [Link if available]

**Details:**
- Model: [Model number]
- Tested by: @username
- Notes: [Any special notes]

**Tasmota Template:**
```json
{"NAME":"...","GPIO":[...],"FLAG":...,"BASE":...}
```

**Console Rules (if applicable):**
```
Rule1 ...
```

### [Device Name 2]

[Same structure...]

## Related Pages

- [Compatible Devices Overview](Compatible-devices)
- [Troubleshooting](Troubleshooting)
- [How to Contribute](Contributing)

---

*Need help? [Open an issue](https://github.com/sfo2001/tuya-convert/issues).*
```

### Template 4: Landing/Hub Page

```markdown
# [Section Title]

[Brief introduction to this section]

## Quick Navigation

### [Category 1]
- [Page 1](link) - Brief description
- [Page 2](link) - Brief description

### [Category 2]
- [Page 3](link) - Brief description
- [Page 4](link) - Brief description

## Overview

[More detailed overview if needed]

---

*Back to [Home](Home)*
```

---

## Information Architecture

### Proposed Wiki Structure

```
Home (Landing page with full navigation)
│
├── Getting Started/
│   ├── Overview (What is tuya-convert)
│   ├── Installation
│   ├── Quick-Start-Guide
│   └── Supported-Hardware
│
├── Device Information/
│   ├── Compatible-Devices (Hub page)
│   ├── Compatible-Devices-(HTTP-firmware)
│   ├── Compatible-Devices-(HTTPS-firmware)
│   └── Failed-Devices-and-Limitations
│
├── Setup Guides/
│   ├── Using-Docker
│   ├── Using-Raspberry-Pi
│   ├── Using-Raspberry-Pi-Zero-W
│   └── Using-VirtualBox-or-VM
│
├── Advanced Topics/
│   ├── Flashing-Multipart-Binaries
│   ├── Flashing-Specific-Devices (detailed guides)
│   └── Manual-Flashing-via-Serial
│
├── Technical Reference/
│   ├── Protocol-Overview (New hub page)
│   ├── PSK-Identity-02-Protocol
│   ├── PSK-Key-Extraction
│   ├── Smartconfig-Protocol
│   ├── System-Architecture (New)
│   └── API-Reference (New)
│
├── Troubleshooting/
│   ├── Troubleshooting (Main page)
│   ├── Failed-Attempts-and-Requirements
│   └── Common-Issues-FAQ (New)
│
└── Contributing/
    ├── How-to-Contribute (New)
    ├── Contributing-Device-Data
    ├── Contributing-to-PSK-Research
    └── Additional-Resources
```

### Page Mapping (Old → New)

| Current Page | New Location | Changes Required |
|--------------|--------------|------------------|
| Home.md | Home.md | Complete rewrite with navigation |
| Additional-Resources.md | Contributing/Additional-Resources.md | Expand and categorize |
| Collaboration-document-for-PSK-Identity-02.md | Technical-Reference/PSK-Identity-02-Protocol.md | Clean up, organize, remove meta-commentary |
| Compatible-devices.md | Device-Information/Compatible-Devices.md | Add hub navigation |
| Compatible-devices-(HTTP-firmware).md | Device-Information/Compatible-Devices-(HTTP-firmware).md | Apply template, fix links |
| Compatible-devices-(HTTPS-firmware).md | Device-Information/Compatible-Devices-(HTTPS-firmware).md | Apply template, fix links |
| Failed-attempts-and-tracked-requirements.md | Troubleshooting/Failed-Attempts-and-Requirements.md | Complete TODOs, organize |
| Flash-a-multipart-binary.md | Advanced-Topics/Flashing-Multipart-Binaries.md | Apply template |
| Flashing-of-WiFi-Switch-with-a-Raspberry-Pi.md | Advanced-Topics/Flashing-Specific-Devices.md | Integrate or keep separate |
| Helping-with-new-psk-format.md | Contributing/Contributing-to-PSK-Research.md | Write complete content |
| PSK-Key-from-Gosund-Wifi-Bulb.md | Technical-Reference/PSK-Key-Extraction.md | Expand with more examples |
| Troubleshooting.md | Troubleshooting/Troubleshooting.md | Expand, apply template |
| Using-a-Raspberry-Pi.md | Setup-Guides/Using-Raspberry-Pi.md | Apply template |
| Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md | Setup-Guides/Using-Raspberry-Pi-Zero-W.md | Apply template |

### New Pages to Create

1. **Getting-Started/Overview.md** - What is tuya-convert, how it works
2. **Getting-Started/Installation.md** - Detailed installation guide
3. **Getting-Started/Quick-Start-Guide.md** - First device flash walkthrough
4. **Getting-Started/Supported-Hardware.md** - Hardware requirements
5. **Setup-Guides/Using-Docker.md** - Docker setup guide
6. **Technical-Reference/Protocol-Overview.md** - Hub for protocol docs
7. **Technical-Reference/System-Architecture.md** - How components work together
8. **Technical-Reference/Smartconfig-Protocol.md** - Smartconfig explanation
9. **Technical-Reference/API-Reference.md** - HTTP endpoints, MQTT topics
10. **Contributing/How-to-Contribute.md** - General contribution guide

---

## Detailed Step-by-Step Plan

### Phase 0: Preparation (CURRENT PHASE)

#### Step 0.1: Create Restructuring Plan ✅
- **Status:** COMPLETE
- **File:** `WIKI_RESTRUCTURING_PLAN.md`
- **Commit:** "docs: create comprehensive wiki restructuring plan"

#### Step 0.2: Create Backup ✅
- **Status:** COMPLETE
- **Action:** Create full backup of current wiki state
- **Command:** `git clone https://github.com/sfo2001/tuya-convert.wiki.git wiki-backup-$(date +%Y%m%d)`
- **Validation:** ✅ Backup directory `wiki-backup-20251105` exists with all 14 .md files
- **Commit:** N/A (backup only)
- **Completed:** 2025-11-05

#### Step 0.3: Content Inventory ✅
- **Status:** COMPLETE
- **Action:** Create detailed inventory of all content
- **File:** `WIKI_CONTENT_INVENTORY.md`
- **Validation:** ✅ Every paragraph of every page documented (19K file, all 14 pages inventoried)
- **Commit:** "docs: create wiki content inventory for validation"
- **Completed:** 2025-11-04

#### Step 0.4: Analyze Codebase ✅
- **Status:** COMPLETE
- **Action:** Map wiki technical docs to code implementation
- **File:** `WIKI_CODE_ALIGNMENT.md`
- **Validation:** ✅ All technical claims verified against code (24K file with comprehensive mapping)
- **Commit:** "docs: create wiki-code alignment mapping"
- **Completed:** 2025-11-04

---

### Phase 1: Fix Critical Issues

#### Step 1.1: Fix Home Page Links ✅
- **Status:** COMPLETE (completed in commit 256a89b during wiki migration)
- **Action:** Replace ct-Open-Source links with relative links
- **File:** `docs/Home.md`
- **Changes:**
  ```diff
  - * [HTTP (old) firmware](https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTP-firmware))
  + * [HTTP (old) firmware](Compatible-devices-(HTTP-firmware))
  - * [HTTPS (new) firmware](https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTPS-firmware))
  + * [HTTPS (new) firmware](Compatible-devices-(HTTPS-firmware))
  ```
- **Validation:**
  - [x] Links work in GitHub wiki preview
  - [x] No external ct-Open-Source links remain
- **Commit:** Part of "docs: migrate wiki to main repository /docs directory" (256a89b)
- **Completed:** 2025-11-04

#### Step 1.2: Fix Additional-Resources Links ✅
- **Status:** COMPLETE
- **Action:** Update issue link to be relative or keep as external reference
- **File:** `docs/Additional-Resources.md`
- **Changes:**
  - Added standard header with Last Updated and Status
  - Added clear note about external links at top of page
  - Kept external links to original project (appropriate as external references)
  - All links verified as working and properly labeled
- **Validation:**
  - [x] Links work correctly
  - [x] External links clearly marked as external
- **Commit:** "docs(wiki): standardize Additional-Resources with external link documentation"
- **Completed:** 2025-11-05

#### Step 1.3: Fix Helping-with-new-psk-format File Links
- **Action:** Either migrate files to your fork or update links
- **File:** `Helping-with-new-psk-format.md`
- **Validation:**
  - [ ] All file links accessible
  - [ ] Files downloaded and re-uploaded if necessary
- **Commit:** "docs(wiki): fix file attachment links in PSK format page"

---

### Phase 2: Create Standard Templates

#### Step 2.1: Create Template Files
- **Action:** Create template files in wiki repo
- **Files:**
  - `_templates/Guide-Template.md`
  - `_templates/Reference-Template.md`
  - `_templates/Device-List-Template.md`
  - `_templates/Hub-Page-Template.md`
- **Validation:**
  - [ ] All templates complete
  - [ ] Templates follow GitHub markdown standards
- **Commit:** "docs(wiki): add standardized page templates"

---

### Phase 3: Complete Incomplete Pages

#### Step 3.1: Complete "Helping-with-new-psk-format"
- **Action:** Write complete content explaining new PSK format
- **File:** `Helping-with-new-psk-format.md`
- **Content to add:**
  - What is the new PSK format
  - Why it matters
  - How to help with research
  - What the attached files demonstrate
  - Step-by-step contribution guide
- **Validation:**
  - [ ] All original file links preserved
  - [ ] Complete explanatory content added
  - [ ] Cross-references to PSK Identity 02 page
- **Commit:** "docs(wiki): complete PSK format help page with full content"

#### Step 3.2: Clean Up "Collaboration-document-for-PSK-Identity-02" ✅
- **Status:** COMPLETE (4 atomic steps with recovery points)
- **Action:** Organize bulk copy-paste into proper sections
- **File:** `docs/Collaboration-document-for-PSK-Identity-02.md`
- **Changes:**
  - Removed "Please help edit this document!" meta-commentary
  - Added professional header with status and metadata
  - Replaced Procedures section with reference to extracted file
  - Replaced Device List section with reference to extracted file
  - Added Implementation Details section with code references
  - File reduced from 562 to 309 lines (45% reduction)
- **Validation:**
  - [x] All original content preserved (100% in extracted files)
  - [x] No information lost
  - [x] Professional appearance
  - [x] Code references added
- **Commits:**
  - 4eb1db9: "docs: add professional header to PSK Identity 02 document"
  - a5e2bd1: "docs: replace procedures section with reference to extracted file"
  - 8a0c649: "docs: replace device list section with reference to extracted file"
  - 3ffadcb: "docs: add code references to PSK Identity 02 document"
- **Plan:** `COLLAB_DOC_REFACTORING_PLAN.md` (detailed 4-step approach)
- **Completed:** 2025-11-05

#### Step 3.3: Complete "Failed-attempts-and-tracked-requirements"
- **Action:** Resolve TODO items and complete content
- **File:** `Failed-attempts-and-tracked-requirements.md`
- **Changes:**
  - Complete "TODO: Find the exact package(s) needs updating"
  - Add current recommended solutions
  - Organize by relevance (archive old Ubuntu versions)
- **Validation:**
  - [ ] No TODO items remain
  - [ ] All issues resolved or marked as historical
  - [ ] Current solutions documented
- **Commit:** "docs(wiki): complete failed attempts page and resolve TODOs"

---

### Phase 4: Create New Essential Pages

#### Step 4.1: Create Installation Guide
- **Action:** Extract and expand installation content from README
- **File:** `Installation.md`
- **Content:**
  - Detailed prerequisites
  - Platform-specific instructions
  - Installation verification
  - Common installation issues
- **Source:** `README.md` lines 25-52, `install_prereq.sh`
- **Validation:**
  - [ ] All README installation content covered
  - [ ] Links to code files included
  - [ ] Cross-referenced with Troubleshooting
- **Commit:** "docs(wiki): create detailed Installation guide"

#### Step 4.2: Create Quick Start Guide
- **Action:** Create beginner-friendly walkthrough
- **File:** `Quick-Start-Guide.md`
- **Content:**
  - Prerequisites checklist
  - Step-by-step first flash
  - Expected output at each step
  - What to do after successful flash
- **Source:** `README.md` PROCEDURE section, `start_flash.sh`
- **Validation:**
  - [ ] Complete user journey documented
  - [ ] Screenshots/examples included
  - [ ] Links to detailed guides
- **Commit:** "docs(wiki): create Quick Start Guide"

#### Step 4.3: Create Docker Setup Guide
- **Action:** Extract and expand Docker content from README
- **File:** `Using-Docker.md`
- **Content:**
  - Why use Docker
  - Requirements
  - Setup instructions
  - Environment variables
  - Docker-specific troubleshooting
- **Source:** `README.md` lines 79-105, `.env-template`, `docker-compose.yml`
- **Validation:**
  - [ ] All README Docker content covered
  - [ ] .env-template explained
  - [ ] Common Docker issues documented
- **Commit:** "docs(wiki): create Docker setup guide"

#### Step 4.4: Create System Architecture Page
- **Action:** Document how all components work together
- **File:** `System-Architecture.md`
- **Content:**
  - Component overview (AP, web server, MQTT, PSK, discovery)
  - Data flow diagram
  - Network topology
  - Security model
- **Source:** Analyze `start_flash.sh`, Python scripts, `setup_ap.sh`
- **Validation:**
  - [ ] All components documented
  - [ ] Diagram included (ASCII or link to image)
  - [ ] Code references for each component
- **Commit:** "docs(wiki): add system architecture documentation"

#### Step 4.5: Create Protocol Overview Hub
- **Action:** Create hub page linking to all protocol documentation
- **File:** `Protocol-Overview.md`
- **Content:**
  - Brief overview of each protocol
  - Links to detailed pages
  - Implementation status
  - Known limitations
- **Validation:**
  - [ ] Links to all protocol pages
  - [ ] Accurate status information
- **Commit:** "docs(wiki): create protocol overview hub page"

#### Step 4.6: Create API Reference
- **Action:** Document HTTP endpoints and MQTT topics
- **File:** `API-Reference.md`
- **Content:**
  - HTTP endpoints from fake-registration-server
  - MQTT topics and messages
  - Request/response formats
  - Examples
- **Source:** `scripts/fake-registration-server.py`, `scripts/mq_pub_15.py`
- **Validation:**
  - [ ] All endpoints documented
  - [ ] Code line references included
  - [ ] Examples provided
- **Commit:** "docs(wiki): create API reference documentation"

#### Step 4.7: Create Contributing Guide
- **Action:** Create comprehensive contribution guide
- **File:** `How-to-Contribute.md`
- **Content:**
  - How to report device compatibility
  - How to help with PSK research
  - How to improve documentation
  - Code contribution guidelines
- **Source:** README CONTRIBUTING section
- **Validation:**
  - [ ] Clear contribution paths
  - [ ] Links to relevant pages
- **Commit:** "docs(wiki): create contributing guide"

---

### Phase 5: Apply Templates to Existing Pages

#### Step 5.1: Standardize Compatible-Devices Pages
- **Files:**
  - `Compatible-devices.md`
  - `Compatible-devices-(HTTP-firmware).md`
  - `Compatible-devices-(HTTPS-firmware).md`
- **Action:** Apply Device List Template
- **Changes per file:**
  - Add header with status and last updated
  - Add "How to Contribute" section
  - Ensure consistent device entry format
  - Add cross-references
- **Validation:**
  - [ ] All original device entries preserved
  - [ ] Consistent formatting
  - [ ] Templates applied correctly
- **Commit:** "docs(wiki): standardize device compatibility pages"

#### Step 5.2: Standardize Setup Guides
- **Files:**
  - `Using-a-Raspberry-Pi.md`
  - `Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md`
- **Action:** Apply Guide Template
- **Changes per file:**
  - Add header
  - Add prerequisites section
  - Add troubleshooting section
  - Add related pages section
- **Validation:**
  - [ ] All original content preserved
  - [ ] Templates applied correctly
  - [ ] Cross-references added
- **Commit:** "docs(wiki): standardize Raspberry Pi setup guides"

#### Step 5.3: Standardize Advanced Topic Pages
- **Files:**
  - `Flash-a-multipart-binary.md`
  - `Flashing-of-WiFi-Switch-with-a-Raspberry-Pi.md`
- **Action:** Apply Guide Template
- **Validation:**
  - [ ] All original content preserved
  - [ ] Templates applied correctly
- **Commit:** "docs(wiki): standardize advanced topic pages"

#### Step 5.4: Standardize Technical Reference Pages
- **Files:**
  - `Collaboration-document-for-PSK-Identity-02.md` (already done in Phase 3)
  - `PSK-Key-from-Gosund-Wifi-Bulb.md`
- **Action:** Apply Reference Template to PSK-Key page
- **Validation:**
  - [ ] All original content preserved
  - [ ] Template applied correctly
  - [ ] Code references added
- **Commit:** "docs(wiki): standardize PSK key extraction page"

#### Step 5.5: Standardize Troubleshooting Page
- **File:** `Troubleshooting.md`
- **Action:** Expand and apply template
- **Changes:**
  - Add header
  - Expand table with more issues
  - Add common patterns section
  - Add diagnostic procedure
- **Validation:**
  - [ ] All original entries preserved
  - [ ] New content added
  - [ ] Template applied
- **Commit:** "docs(wiki): expand and standardize troubleshooting page"

---

### Phase 6: Create New Home Page

#### Step 6.1: Design New Home Page
- **Action:** Complete rewrite of Home.md
- **File:** `Home.md`
- **Content:** (See Information Architecture section)
  - Welcome section
  - What is tuya-convert
  - Quick Start links
  - Full navigation structure
  - Support section
- **Validation:**
  - [ ] All wiki pages linked
  - [ ] Logical hierarchy
  - [ ] Relative links only
  - [ ] Professional appearance
- **Commit:** "docs(wiki): create comprehensive new home page"

---

### Phase 7: Cross-Reference and Link All Pages

#### Step 7.1: Add Cross-References
- **Action:** Add "Related Pages" sections to all pages
- **Files:** All wiki pages
- **Validation:**
  - [ ] Every page has related links
  - [ ] Bidirectional links where appropriate
  - [ ] No orphaned pages
- **Commit:** "docs(wiki): add cross-references to all pages"

#### Step 7.2: Add Code References
- **Action:** Add code file references to technical pages
- **Files:** All technical/protocol pages
- **Validation:**
  - [ ] Code paths accurate
  - [ ] Line numbers current
  - [ ] Implementation links work
- **Commit:** "docs(wiki): add code references to technical pages"

---

### Phase 8: Final Validation

#### Step 8.1: Content Validation
- **Action:** Verify all original content preserved
- **Tool:** Compare against `WIKI_CONTENT_INVENTORY.md`
- **Validation:**
  - [ ] Every paragraph accounted for
  - [ ] No information lost
  - [ ] Everything either kept, moved, or improved
- **Commit:** N/A (validation only)

#### Step 8.2: Link Validation
- **Action:** Test all internal links
- **Tool:** Manual click-through or link checker
- **Validation:**
  - [ ] All internal links work
  - [ ] No broken links
  - [ ] External links valid
- **Commit:** N/A (validation only)

#### Step 8.3: Template Compliance
- **Action:** Verify all pages follow templates
- **Validation:**
  - [ ] Consistent headers
  - [ ] Consistent sections
  - [ ] Consistent formatting
- **Commit:** N/A (validation only)

#### Step 8.4: Codebase Alignment
- **Action:** Verify technical docs match code
- **Tool:** Compare against `WIKI_CODE_ALIGNMENT.md`
- **Validation:**
  - [ ] All code references accurate
  - [ ] No documentation-code drift
  - [ ] Implementation details correct
- **Commit:** N/A (validation only)

---

### Phase 9: Create Wiki Index and Cleanup

#### Step 9.1: Create _Sidebar
- **Action:** Create GitHub wiki sidebar
- **File:** `_Sidebar.md`
- **Content:** Navigation tree for all pages
- **Validation:**
  - [ ] All pages listed
  - [ ] Logical grouping
  - [ ] Easy navigation
- **Commit:** "docs(wiki): create navigation sidebar"

#### Step 9.2: Create _Footer
- **Action:** Create GitHub wiki footer
- **File:** `_Footer.md`
- **Content:** Standard footer for all pages
- **Validation:**
  - [ ] Consistent footer
  - [ ] Links to home, issues, repo
- **Commit:** "docs(wiki): create standard footer"

#### Step 9.3: Remove Template Files
- **Action:** Delete `_templates/` directory (templates documented in this plan)
- **Validation:**
  - [ ] Templates documented in restructuring plan
  - [ ] No longer needed in wiki
- **Commit:** "docs(wiki): remove template files after restructuring complete"

---

## Validation Checkpoints

### Pre-Commit Validation Checklist

Before each commit, verify:

- [ ] **Content Preservation:** All original information preserved or intentionally moved
- [ ] **Link Validation:** All links tested and working
- [ ] **Format Compliance:** Page follows appropriate template
- [ ] **Cross-References:** Related pages linked
- [ ] **Code Alignment:** Technical claims verified against code
- [ ] **Spelling/Grammar:** No obvious errors
- [ ] **Markdown Syntax:** Renders correctly in preview

### Phase Completion Validation

At the end of each phase:

- [ ] **All steps completed:** Every step in phase marked done
- [ ] **All commits made:** Every planned commit executed
- [ ] **All validations passed:** Every validation checkbox checked
- [ ] **No regressions:** Wiki still functions correctly
- [ ] **Documentation updated:** This plan updated with actual progress

### Final Validation Checklist

Before marking restructuring complete:

- [ ] **100% Content Preserved:** Every piece of original content accounted for
- [ ] **Zero Broken Links:** All internal links work
- [ ] **Full Template Compliance:** All pages follow templates
- [ ] **Complete Navigation:** Every page reachable from Home
- [ ] **Full Cross-References:** Related pages linked
- [ ] **Code Alignment Verified:** All technical docs match code
- [ ] **Professional Appearance:** Consistent, polished presentation
- [ ] **User Testing:** At least one external user can navigate successfully

---

## Codebase Alignment Strategy

### Alignment Principles

1. **Technical Documentation Must Reference Code**
   - Every technical claim backed by code reference
   - File paths and line numbers included
   - Links to GitHub code view where helpful

2. **Protocol Documentation Matches Implementation**
   - Documented behavior verified in code
   - Documented formats match actual formats
   - Documented flow matches actual execution

3. **Examples Use Actual Code**
   - Configuration examples from actual config files
   - Command examples from actual scripts
   - Output examples from actual log files

### Code-to-Wiki Mapping

| Wiki Page | Primary Code Files | Validation Method |
|-----------|-------------------|-------------------|
| Installation.md | `install_prereq.sh` | Script command verification |
| Quick-Start-Guide.md | `start_flash.sh`, `firmware_picker.sh` | Flow verification |
| Using-Docker.md | `docker-compose.yml`, `.env-template`, `Dockerfile` | Configuration verification |
| System-Architecture.md | `start_flash.sh`, all Python scripts, `setup_ap.sh` | Component verification |
| PSK-Identity-02-Protocol.md | `scripts/psk-frontend.py` | Algorithm verification |
| API-Reference.md | `scripts/fake-registration-server.py` | Endpoint verification |
| Smartconfig-Protocol.md | `scripts/smartconfig/` | Protocol verification |

### Verification Process

For each technical page:

1. **Read Code:** Understand implementation
2. **Document Behavior:** Describe what code does
3. **Add References:** Link to specific code sections
4. **Test Claims:** Verify documented behavior matches code
5. **Update on Code Changes:** Mark pages needing updates when code changes

---

## Progress Tracking

### Phase Status

| Phase | Status | Start Date | End Date | Notes |
|-------|--------|------------|----------|-------|
| Phase 0: Preparation | ✅ Complete | 2025-11-04 | 2025-11-05 | All steps complete (0.1-0.4) |
| Phase 1: Fix Critical Issues | 🔄 Partial | 2025-11-04 | - | Step 1.1 complete (1.2-1.3 pending) |
| Phase 2: Create Standard Templates | ⏳ Pending | - | - | - |
| Phase 3: Complete Incomplete Pages | 🔄 Partial | 2025-11-05 | - | Steps 3.1-3.2 complete (3.3 pending) |
| Phase 4: Create New Essential Pages | ⏳ Pending | - | - | - |
| Phase 5: Apply Templates to Existing Pages | ⏳ Pending | - | - | - |
| Phase 6: Create New Home Page | ⏳ Pending | - | - | - |
| Phase 7: Cross-Reference and Link All Pages | ⏳ Pending | - | - | - |
| Phase 8: Final Validation | ⏳ Pending | - | - | - |
| Phase 9: Create Wiki Index and Cleanup | ⏳ Pending | - | - | - |

### Step Tracking

- ✅ Completed
- 🔄 In Progress
- ⏳ Pending
- ⚠️ Blocked
- ❌ Failed (requires retry)

### Commit Log

| Step | Commit Message | Date | SHA | Validated |
|------|---------------|------|-----|-----------|
| 0.1 | docs: create comprehensive wiki restructuring plan | 2025-11-04 | [merged] | ✅ |
| 0.2 | N/A (backup only) | 2025-11-05 | N/A | ✅ |
| 0.3 | docs: create wiki content inventory for validation | 2025-11-04 | [merged] | ✅ |
| 0.4 | docs: create wiki-code alignment mapping | 2025-11-04 | [merged] | ✅ |
| 1.1 | docs: migrate wiki to main repository /docs directory | 2025-11-04 | 256a89b | ✅ |
| 3.1 | docs: complete PSK format contribution guide | 2025-11-04 | 15df5b6 | ✅ |
| 3.2a | docs: add professional header to PSK Identity 02 document | 2025-11-05 | 4eb1db9 | ✅ |
| 3.2b | docs: replace procedures section with reference to extracted file | 2025-11-05 | a5e2bd1 | ✅ |
| 3.2c | docs: replace device list section with reference to extracted file | 2025-11-05 | 8a0c649 | ✅ |
| 3.2d | docs: add code references to PSK Identity 02 document | 2025-11-05 | 3ffadcb | ✅ |
| plan | docs: create detailed refactoring plan for PSK collaboration document | 2025-11-05 | e760824 | ✅ |
| meta | docs: document wiki working directory location | 2025-11-05 | 4807756 | ✅ |
| meta | docs: update refactoring plan with completion status | 2025-11-05 | a446feb | ✅ |
| 1.2 | docs(wiki): standardize Additional-Resources with external link documentation | 2025-11-05 | de9178e | ✅ |

---

## Notes and Decisions

### Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-11-04 | Use atomic commits per step | Easier to track, rollback if needed |
| 2025-11-04 | Keep device list pages separate | Too large to combine, better user experience |
| 2025-11-04 | Create new hub pages instead of mega-pages | Better navigation, easier maintenance |

### Open Questions

1. **Should we rename pages for better URL structure?**
   - e.g., `Compatible-devices-(HTTP-firmware).md` → `Devices-HTTP.md`
   - Decision: TBD - discuss after testing restructure

2. **Should we create a separate wiki repo or continue with GitHub wiki?**
   - Decision: Continue with GitHub wiki for now, evaluate later

3. **Should we add images/diagrams?**
   - Decision: Yes, but as separate phase after text restructuring

---

## Contact and Feedback

**Project Maintainer:** sfo2001
**Restructuring Led By:** Claude (AI Assistant)
**Date:** 2025-11-04

For questions or suggestions about this restructuring plan:
- Open an issue: https://github.com/sfo2001/tuya-convert/issues
- Reference: `WIKI_RESTRUCTURING_PLAN.md`

---

**End of Restructuring Plan**
