# Collaboration Document Refactoring Plan

**Date:** 2025-11-05
**File:** `docs/Collaboration-document-for-PSK-Identity-02.md`
**Status:** Planning Phase

---

## Context

This document has **failed refactoring attempts multiple times**. We need a careful, atomic approach with recovery points.

### Current State

- **Original file:** 554 lines
- **Extracted files created:**
  - `PSK-Research-Procedures.md` (235 lines) - commit `a1bdaaa`
  - `PSK-Identity-02-Affected-Devices.md` (361 lines) - commit `ccc2fec`
- **Problem:** Extracted content still exists in original file (duplicated, not removed)

### Issues to Fix

1. Line 3: "Please help edit this document!" - meta-commentary
2. Lines 132-208: "## Procedures" section - duplicated in PSK-Research-Procedures.md
3. Lines 210-430: "## Known Affected Devices" - duplicated in PSK-Identity-02-Affected-Devices.md

---

## Extraction Verification

### Section 1: Procedures (Lines 132-208)

**In original:**
- Line 132: `## Procedures`
- Line 134: `### Decrypting network captures with known PSK`
- Line 145: `### Creating network captures and firmware backups`
- Content: ~77 lines

**Extracted to:** `PSK-Research-Procedures.md`
- Lines 1-50: Similar content with better structure
- ✅ **VERIFIED:** Content successfully extracted

**Action:** Replace with reference link

---

### Section 2: Known Affected Devices (Lines 210-430)

**In original:**
- Line 210: `## Known Affected Devices`
- Lines 211-430: Alphabetical device list
- Content: ~220 lines

**Extracted to:** `PSK-Identity-02-Affected-Devices.md`
- Lines 35-361: Same device list with better organization
- ✅ **VERIFIED:** Content successfully extracted

**Action:** Replace with reference link

---

## Refactoring Steps (Atomic)

### Step 1: Remove Meta-Commentary ✅ SAFE
**Risk: VERY LOW** - Simple deletion, no dependencies

**Current (lines 1-4):**
```markdown
Here we will share and organize our findings and data from [#483](https://github.com/ct-Open-Source/tuya-convert/issues/483)

### Please help edit this document!
Much of this was bulk copy-pasted and needs to be transformed into a useful form
```

**New:**
```markdown
# PSK Identity 02 Protocol

**Last Updated:** 2025-11-05
**Status:** 🔄 Research In Progress
**Implementation:** `scripts/psk-frontend.py`
**Related:** [Research Procedures](PSK-Research-Procedures.md) | [Affected Devices](PSK-Identity-02-Affected-Devices.md)

## Overview

This document consolidates community research into the PSK Identity 02 protocol used by newer Tuya devices. This protocol prevents OTA flashing via tuya-convert.

**Original research discussion:** [Issue #483](https://github.com/ct-Open-Source/tuya-convert/issues/483)
```

**Validation:**
- [ ] Lines 1-4 replaced with new header
- [ ] File still valid markdown
- [ ] All links work

**Commit:** `docs: add professional header to PSK Identity 02 document`

---

### Step 2: Replace Procedures Section ✅ SAFE
**Risk: LOW** - Content exists in separate file

**Find (lines 132-208):**
```markdown
## Procedures

### Decrypting network captures with known PSK
[... ~77 lines of content ...]
```

**Replace with:**
```markdown
## Research Procedures

Detailed procedures for capturing and analyzing PSK data have been moved to a dedicated page:

**👉 [PSK Research Procedures](PSK-Research-Procedures.md)**

This includes:
- Decrypting network captures with known PSK
- Creating network captures and firmware backups
- Step-by-step experimental procedures
- Required tools and setup instructions
```

**Validation:**
- [ ] Lines 132-208 replaced with reference
- [ ] Link to PSK-Research-Procedures.md works
- [ ] No content lost (verified in extracted file)
- [ ] Line count reduced by ~70 lines

**Commit:** `docs: replace procedures section with reference to extracted file`

---

### Step 3: Replace Known Affected Devices Section ✅ SAFE
**Risk: LOW** - Content exists in separate file

**Find (lines 210-430):**
```markdown
## Known Affected Devices
- AIMASON BSD34 Smart WLAN Plug...
[... ~220 lines of device list ...]
```

**Replace with:**
```markdown
## Known Affected Devices

A comprehensive list of devices confirmed to use PSK Identity 02 has been moved to a dedicated page:

**👉 [PSK Identity 02 Affected Devices](PSK-Identity-02-Affected-Devices.md)**

This page includes:
- Alphabetical device list with purchase dates
- Identification methods
- Device purchase timeline
- Community-contributed test results

**Quick check:** If your `smarthack-psk.log` shows `ID: 02...`, see the [affected devices list](PSK-Identity-02-Affected-Devices.md).
```

**Validation:**
- [ ] Lines 210-430 replaced with reference
- [ ] Link to PSK-Identity-02-Affected-Devices.md works
- [ ] No content lost (verified in extracted file)
- [ ] Line count reduced by ~220 lines

**Commit:** `docs: replace device list section with reference to extracted file`

---

### Step 4: Add Code References ✅ SAFE
**Risk: VERY LOW** - Adding information only

**In "# Findings" section, after line 44, add:**

```markdown
## Implementation Details

The PSK Identity 02 protocol is implemented in tuya-convert:

**Code Reference:** `scripts/psk-frontend.py`
- **Line 12:** Identity prefix constant: `IDENTITY_PREFIX = b"BAohbmd6aG91IFR1"`
- **Lines 26-36:** `gen_psk()` function - PSK generation algorithm
- **Lines 48-49:** Hint value used in PSK calculation
- **Lines 61-66:** TLS-PSK setup with cipher suite `PSK-AES128-CBC-SHA256`

See the code for full implementation details.
```

**Validation:**
- [ ] Code references added
- [ ] Line numbers correct
- [ ] File paths correct
- [ ] Improves technical accuracy

**Commit:** `docs: add code references to PSK Identity 02 document`

---

## Progress Tracking

| Step | Description | Status | Commit | Lines Changed | Recovery Point |
|------|-------------|--------|--------|---------------|----------------|
| 1 | Remove meta-commentary | ⏳ Pending | - | ~10 | Can revert if fails |
| 2 | Replace Procedures section | ⏳ Pending | - | ~70 | Step 1 commit |
| 3 | Replace Devices section | ⏳ Pending | - | ~220 | Step 2 commit |
| 4 | Add code references | ⏳ Pending | - | +15 | Step 3 commit |

---

## Expected Outcome

**Before:**
- 554 lines
- Duplicated content
- Meta-commentary
- Hard to navigate

**After:**
- ~275 lines (50% reduction)
- Clear references to detailed pages
- Professional header
- Code references
- Easy to navigate

**Content Preservation:** ✅ 100% preserved in extracted files

---

## Rollback Plan

If any step fails:
1. `git reset --hard HEAD` (if not committed)
2. `git revert <commit-sha>` (if committed)
3. Review this plan
4. Try alternate approach

---

## Safety Checks

Before each commit:
- [ ] Run `git diff` and review changes
- [ ] Verify markdown syntax: `grep -n "^#" docs/Collaboration-document-for-PSK-Identity-02.md`
- [ ] Check no content lost: Compare line counts with plan
- [ ] Test links: Verify referenced files exist

---

**Next Action:** Execute Step 1 (Remove meta-commentary)
