# Wiki Restructuring Plan - Overview

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
6. [Overall Progress Tracking](#overall-progress-tracking)
7. [Phase Documents](#phase-documents)
8. [Validation Checkpoints](#validation-checkpoints)
9. [Codebase Alignment Strategy](#codebase-alignment-strategy)

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
| 2 | Additional-Resources.md | 17 | ✅ Complete | Standardized with external link documentation |
| 3 | Collaboration-document-for-PSK-Identity-02.md | 309 | ✅ Complete | Professional format with code references |
| 4 | Compatible-devices-(HTTP-firmware).md | 208 | ✅ Good | Complete device list |
| 5 | Compatible-devices-(HTTPS-firmware).md | 124 | ✅ Good | Complete device list |
| 6 | Compatible-devices.md | 74 | ✅ Good | Complete device list |
| 7 | Failed-attempts-and-tracked-requirements.md | 113 | ⚠️ Incomplete | Contains TODO items, unresolved |
| 8 | Flash-a-multipart-binary.md | 30 | ✅ Good | Complete technical guide |
| 9 | Flashing-of-WiFi-Switch-with-a-Raspberry-Pi.md | 110 | ✅ Good | Complete guide |
| 10 | Helping-with-new-psk-format.md | 7 | ✅ Complete | Full contribution guide |
| 11 | PSK-Key-from-Gosund-Wifi-Bulb.md | 13 | ✅ OK | Short but complete |
| 12 | Troubleshooting.md | 20 | ✅ Good | Well-structured table |
| 13 | Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md | 128 | ✅ Good | Complete guide |
| 14 | Using-a-Raspberry-Pi.md | 34 | ✅ Good | Complete guide |

### Critical Issues Summary

1. **Broken/External Links** - Fixed in Phase 1
2. **Incomplete Content** - Being addressed in Phase 3
3. **No Information Architecture** - Being addressed through phases
4. **Missing Essential Pages** - Phase 4 will create new pages

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
| Additional-Resources.md | Contributing/Additional-Resources.md | ✅ Standardized |
| Collaboration-document-for-PSK-Identity-02.md | Technical-Reference/PSK-Identity-02-Protocol.md | ✅ Cleaned and organized |
| Compatible-devices.md | Device-Information/Compatible-Devices.md | Add hub navigation |
| Compatible-devices-(HTTP-firmware).md | Device-Information/Compatible-Devices-(HTTP-firmware).md | Apply template, fix links |
| Compatible-devices-(HTTPS-firmware).md | Device-Information/Compatible-Devices-(HTTPS-firmware).md | Apply template, fix links |
| Failed-attempts-and-tracked-requirements.md | Troubleshooting/Failed-Attempts-and-Requirements.md | Complete TODOs, organize |
| Flash-a-multipart-binary.md | Advanced-Topics/Flashing-Multipart-Binaries.md | Apply template |
| Flashing-of-WiFi-Switch-with-a-Raspberry-Pi.md | Advanced-Topics/Flashing-Specific-Devices.md | Integrate or keep separate |
| Helping-with-new-psk-format.md | Contributing/Contributing-to-PSK-Research.md | ✅ Complete content added |
| PSK-Key-from-Gosund-Wifi-Bulb.md | Technical-Reference/PSK-Key-Extraction.md | Expand with more examples |
| Troubleshooting.md | Troubleshooting/Troubleshooting.md | Expand, apply template |
| Using-a-Raspberry-Pi.md | Setup-Guides/Using-Raspberry-Pi.md | Apply template |
| Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md | Setup-Guides/Using-Raspberry-Pi-Zero-W.md | Apply template |

---

## Overall Progress Tracking

### Phase Overview

| Phase | Status | Progress | Start Date | End Date | Document |
|-------|--------|----------|------------|----------|----------|
| Phase 0: Preparation | ✅ Complete | 4/4 (100%) | 2025-11-04 | 2025-11-05 | [WIKI_PHASE_0_PREPARATION.md](WIKI_PHASE_0_PREPARATION.md) |
| Phase 1: Fix Critical Issues | 🔄 In Progress | 2/3 (67%) | 2025-11-04 | - | [WIKI_PHASE_1_CRITICAL_ISSUES.md](WIKI_PHASE_1_CRITICAL_ISSUES.md) |
| Phase 2: Create Standard Templates | ⏳ Pending | 0/1 (0%) | - | - | [WIKI_PHASE_2_TEMPLATES.md](WIKI_PHASE_2_TEMPLATES.md) |
| Phase 3: Complete Incomplete Pages | 🔄 In Progress | 2/3 (67%) | 2025-11-05 | - | [WIKI_PHASE_3_INCOMPLETE_PAGES.md](WIKI_PHASE_3_INCOMPLETE_PAGES.md) |
| Phase 4: Create New Essential Pages | ⏳ Pending | 0/7 (0%) | - | - | [WIKI_PHASE_4_NEW_PAGES.md](WIKI_PHASE_4_NEW_PAGES.md) |
| Phase 5: Apply Templates to Existing Pages | ⏳ Pending | 0/5 (0%) | - | - | [WIKI_PHASE_5_APPLY_TEMPLATES.md](WIKI_PHASE_5_APPLY_TEMPLATES.md) |
| Phase 6: Create New Home Page | ⏳ Pending | 0/1 (0%) | - | - | [WIKI_PHASE_6_NEW_HOME.md](WIKI_PHASE_6_NEW_HOME.md) |
| Phase 7: Cross-Reference and Link All Pages | ⏳ Pending | 0/2 (0%) | - | - | [WIKI_PHASE_7_CROSS_REFERENCE.md](WIKI_PHASE_7_CROSS_REFERENCE.md) |
| Phase 8: Final Validation | ⏳ Pending | 0/4 (0%) | - | - | [WIKI_PHASE_8_VALIDATION.md](WIKI_PHASE_8_VALIDATION.md) |
| Phase 9: Create Wiki Index and Cleanup | ⏳ Pending | 0/3 (0%) | - | - | [WIKI_PHASE_9_INDEX_CLEANUP.md](WIKI_PHASE_9_INDEX_CLEANUP.md) |

### Overall Statistics

- **Total Phases:** 10
- **Completed Phases:** 1 (10%)
- **In Progress Phases:** 2 (20%)
- **Pending Phases:** 7 (70%)
- **Total Steps:** 34
- **Completed Steps:** 8 (24%)
- **In Progress Steps:** 0 (0%)
- **Pending Steps:** 26 (76%)

### Recent Activity

| Date | Phase | Step | Description | Status |
|------|-------|------|-------------|--------|
| 2025-11-05 | 1 | 1.2 | Fix Additional-Resources Links | ✅ Complete |
| 2025-11-05 | 3 | 3.2 | Clean Up PSK Identity 02 Document | ✅ Complete |
| 2025-11-04 | 3 | 3.1 | Complete PSK Format Help Page | ✅ Complete |
| 2025-11-04 | 1 | 1.1 | Fix Home Page Links | ✅ Complete |
| 2025-11-04 | 0 | 0.4 | Analyze Codebase | ✅ Complete |
| 2025-11-04 | 0 | 0.3 | Content Inventory | ✅ Complete |
| 2025-11-05 | 0 | 0.2 | Create Backup | ✅ Complete |
| 2025-11-04 | 0 | 0.1 | Create Restructuring Plan | ✅ Complete |

---

## Phase Documents

Each phase has a dedicated document with detailed steps, tracking, and commit logs:

1. **[Phase 0: Preparation](WIKI_PHASE_0_PREPARATION.md)** ✅ Complete
   - Create restructuring plan
   - Create backup
   - Content inventory
   - Codebase analysis

2. **[Phase 1: Fix Critical Issues](WIKI_PHASE_1_CRITICAL_ISSUES.md)** 🔄 In Progress (67% complete)
   - Fix Home page links ✅
   - Fix Additional-Resources links ✅
   - Fix Helping-with-new-psk-format file links ⏳

3. **[Phase 2: Create Standard Templates](WIKI_PHASE_2_TEMPLATES.md)** ⏳ Pending
   - Create template files

4. **[Phase 3: Complete Incomplete Pages](WIKI_PHASE_3_INCOMPLETE_PAGES.md)** 🔄 In Progress (67% complete)
   - Complete "Helping-with-new-psk-format" ✅
   - Clean up "Collaboration-document-for-PSK-Identity-02" ✅
   - Complete "Failed-attempts-and-tracked-requirements" ⏳

5. **[Phase 4: Create New Essential Pages](WIKI_PHASE_4_NEW_PAGES.md)** ⏳ Pending
   - Installation guide
   - Quick start guide
   - Docker setup guide
   - System architecture
   - Protocol overview
   - API reference
   - Contributing guide

6. **[Phase 5: Apply Templates to Existing Pages](WIKI_PHASE_5_APPLY_TEMPLATES.md)** ⏳ Pending
   - Standardize device compatibility pages
   - Standardize setup guides
   - Standardize advanced topic pages
   - Standardize technical reference pages
   - Standardize troubleshooting page

7. **[Phase 6: Create New Home Page](WIKI_PHASE_6_NEW_HOME.md)** ⏳ Pending
   - Design new home page

8. **[Phase 7: Cross-Reference and Link All Pages](WIKI_PHASE_7_CROSS_REFERENCE.md)** ⏳ Pending
   - Add cross-references
   - Add code references

9. **[Phase 8: Final Validation](WIKI_PHASE_8_VALIDATION.md)** ⏳ Pending
   - Content validation
   - Link validation
   - Template compliance
   - Codebase alignment

10. **[Phase 9: Create Wiki Index and Cleanup](WIKI_PHASE_9_INDEX_CLEANUP.md)** ⏳ Pending
    - Create sidebar
    - Create footer
    - Remove template files

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
- [ ] **Documentation updated:** Phase document updated with actual progress

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

## Way of Working

### Step Execution Process

For each step:

1. **Read Phase Document:** Understand the step requirements
2. **Plan Changes:** Identify files to modify and changes needed
3. **Make Changes:** Edit files following templates and principles
4. **Validate:** Run through validation checklist
5. **Commit:** Create atomic commit with descriptive message
6. **Update Phase Document:** Mark step complete with commit SHA
7. **Update Overview:** Update phase progress in this document

### Commit Message Format

```
<type>(<scope>): <subject>

[optional body with details]

Validation:
✅ Item 1
✅ Item 2

References: <Phase Document> <Step Number>
```

Types: `docs`, `feat`, `fix`, `refactor`, `test`, `chore`

### Progress Tracking

- Update phase documents after each step completion
- Update overview document after each phase completion
- Keep commit logs current in phase documents
- Maintain phase status indicators (✅ 🔄 ⏳ ⚠️ ❌)

---

## Notes and Decisions

### Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2025-11-04 | Use atomic commits per step | Easier to track, rollback if needed |
| 2025-11-04 | Keep device list pages separate | Too large to combine, better user experience |
| 2025-11-04 | Create new hub pages instead of mega-pages | Better navigation, easier maintenance |
| 2025-11-05 | Split plan into phase documents | Better organization, easier tracking |

### Open Questions

1. **Should we rename pages for better URL structure?**
   - e.g., `Compatible-devices-(HTTP-firmware).md` → `Devices-HTTP.md`
   - Decision: TBD - discuss after testing restructure

2. **Should we create a separate wiki repo or continue with GitHub wiki?**
   - Decision: Continue with GitHub wiki for now, evaluate later

3. **Should we add images/diagrams?**
   - Decision: Yes, but as separate phase after text restructuring

---

## Supporting Documents

- **[WIKI_CONTENT_INVENTORY.md](WIKI_CONTENT_INVENTORY.md)** - Complete content inventory for validation
- **[WIKI_CODE_ALIGNMENT.md](WIKI_CODE_ALIGNMENT.md)** - Code-to-wiki mapping for technical accuracy
- **[COLLAB_DOC_REFACTORING_PLAN.md](COLLAB_DOC_REFACTORING_PLAN.md)** - Detailed plan for PSK document cleanup
- **[PSK_EXTRACTION_PLAN.md](PSK_EXTRACTION_PLAN.md)** - PSK-specific technical documentation

---

## Contact and Feedback

**Project Maintainer:** sfo2001
**Restructuring Led By:** Claude (AI Assistant)
**Date:** 2025-11-04

For questions or suggestions about this restructuring plan:
- Open an issue: https://github.com/sfo2001/tuya-convert/issues
- Reference: `WIKI_RESTRUCTURING_PLAN.md`

---

**Last Updated:** 2025-11-05
