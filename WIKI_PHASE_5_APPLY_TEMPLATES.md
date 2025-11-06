# Phase 5: Apply Templates to Existing Pages

**Phase Status:** 🔄 IN PROGRESS
**Start Date:** 2025-11-06
**End Date:** -
**Progress:** 1/8 sub-steps (12.5%)
**Note:** Step 5.4 includes 4 sub-steps (5.4a-5.4d) for PSK documentation restructuring

[← Back to Overview](WIKI_RESTRUCTURING_PLAN.md) | [← Previous Phase](WIKI_PHASE_4_NEW_PAGES.md) | [Next Phase →](WIKI_PHASE_6_NEW_HOME.md)

---

## Phase Objectives

Apply standardized templates to existing wiki pages to ensure consistency and professional appearance across all documentation.

Target page groups:
1. Device compatibility pages (3 pages)
2. Raspberry Pi setup guides (2 pages)
3. Advanced topic pages (2 pages)
4. Technical reference pages - PSK documentation (4 sub-steps: extract 2 new pages, clean up 1, standardize 1)
5. Troubleshooting page (1 page)

**Note:** Step 5.4 integrates the PSK extraction work from PSK_EXTRACTION_PLAN.md

---

## Steps Overview

| Step | Pages | Count | Status | Est. Time |
|------|-------|-------|--------|-----------|
| 5.1 | Compatible device pages | 3 | ✅ Complete | 2 hours |
| 5.2 | Setup guides | 2 | ⏳ Pending | 1.5 hours |
| 5.3 | Advanced topic pages | 2 | ⏳ Pending | 1 hour |
| 5.4 | Technical reference pages (PSK) | 4 | ⏳ Pending | 2.5 hours |
| 5.5 | Troubleshooting page | 1 | ⏳ Pending | 1 hour |

---

## Detailed Steps

### Step 5.1: Standardize Compatible-Devices Pages ✅

**Status:** COMPLETE
**Completed:** 2025-11-06

**Pages Updated:**
- `Compatible-devices.md`
- `Compatible-devices-(HTTP-firmware).md`
- `Compatible-devices-(HTTPS-firmware).md`

**Template:** Device-List-Template.md

**Changes Applied:**
- Added standard header with status and last updated date
- Added comprehensive overview sections
- Added "How to Contribute" sections
- Standardized heading structure (H3 for device entries)
- Added cross-references to related pages
- Added external resources sections
- Added footer with help links
- Preserved all original device data

**Validation:**
- [x] All original device entries preserved
- [x] Consistent formatting across all 3 pages
- [x] Templates applied correctly
- [x] Cross-references added

**Commit:**
- Message: "docs(wiki): standardize device compatibility pages"
- SHA: a799b33
- Date: 2025-11-06

---

### Step 5.2: Standardize Setup Guides ⏳

**Pages to Update:**
- `Using-a-Raspberry-Pi.md`
- `Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable.md`

**Template:** Guide-Template.md

**Changes per file:**
- Add standard header
- Add prerequisites section
- Add troubleshooting section
- Add related pages section
- Add code references where applicable
- Add footer

**Validation:**
- [ ] All original content preserved
- [ ] Templates applied correctly
- [ ] Cross-references added
- [ ] Consistent format between both guides

**Commit:** "docs(wiki): standardize Raspberry Pi setup guides"

---

### Step 5.3: Standardize Advanced Topic Pages ⏳

**Pages to Update:**
- `Flash-a-multipart-binary.md`
- `Flashing-of-WiFi-Switch-with-a-Raspberry-Pi.md`

**Template:** Guide-Template.md

**Changes per file:**
- Add standard header
- Add overview section
- Add prerequisites
- Add troubleshooting
- Add related pages
- Add code references

**Validation:**
- [ ] All original content preserved
- [ ] Templates applied correctly
- [ ] Technical accuracy verified

**Commit:** "docs(wiki): standardize advanced topic pages"

---

### Step 5.4: Complete PSK Documentation Restructuring ⏳

**Objective:** Complete the PSK documentation extraction and standardization work.

This step integrates the remaining work from PSK_EXTRACTION_PLAN.md into the wiki restructuring process.

---

#### Step 5.4a: Extract PSK Firmware Database ⏳

**Objective:** Extract firmware data table from Collaboration document into standalone reference page

**Source:** `Collaboration-document-for-PSK-Identity-02.md` (lines 187-254)

**New File:** `docs/PSK-Firmware-Database.md`

**Template:** Reference-Template.md

**Content to Include:**
- Firmware data table (40+ firmware samples)
- Columns: pcap, SDK versions, MAC addresses, prod_idx, auz_key, pskKey
- Color coding legend (🟢🟡🔴)
- String examples and JSON blobs (lines 260-284)
- Technical notes and observations about specific firmware
- Network capture links

**Changes:**
- Add standard header with status and implementation reference
- Add overview section explaining the database purpose
- Preserve complete firmware table with all entries
- Add legend explaining SDK version color codes
- Add notes section at the end
- Add cross-references to related PSK pages

**Validation:**
- [ ] All firmware entries preserved (40 entries)
- [ ] All technical notes preserved
- [ ] Table formatting improved for readability
- [ ] Legend added for color codes
- [ ] Template applied correctly
- [ ] Cross-references added

**Commit:** "docs(wiki): extract PSK firmware database into standalone page"

---

#### Step 5.4b: Extract PSK Research Tools ⏳

**Objective:** Extract tools and resources section into standalone reference page

**Source:** `Collaboration-document-for-PSK-Identity-02.md` (lines 286-309)

**New File:** `docs/PSK-Research-Tools.md`

**Template:** Reference-Template.md

**Content to Include:**
- TuyAPI library links and information
- Tuya API signing tools
- Tuya IoT Platform documentation
- Reverse engineering tools
- mitmproxy setup guide for Android
- Cloud tokens and device authorization info

**Changes:**
- Add standard header
- Add overview section
- Organize tools by category (Development, Analysis, Reverse Engineering)
- Expand each tool entry with description and use cases
- Add setup instructions where applicable
- Add cross-references to related pages

**Validation:**
- [ ] All tools and links preserved
- [ ] Tools organized by category
- [ ] Descriptions added for each tool
- [ ] Template applied correctly
- [ ] Cross-references added

**Commit:** "docs(wiki): extract PSK research tools into standalone page"

---

#### Step 5.4c: Clean Up PSK Identity 02 Main Document ⏳

**Objective:** Remove extracted sections and refocus main document on protocol research

**File:** `Collaboration-document-for-PSK-Identity-02.md`

**Changes:**
- Remove firmware database table (lines 187-254) - replaced with link to new file
- Remove research tools section (lines 286-309) - replaced with link to new file
- Add "Research Resources" section with links to all extracted pages:
  - [PSK Research Procedures](PSK-Research-Procedures.md)
  - [PSK Firmware Database](PSK-Firmware-Database.md)
  - [PSK Research Tools](PSK-Research-Tools.md)
  - [Affected Devices List](PSK-Identity-02-Affected-Devices.md)
- Verify all cross-references are working
- Ensure document flows logically after extraction

**Expected Result:** Main document reduced from 309 lines to ~150 lines, focused on protocol research and findings

**Validation:**
- [ ] All extracted content replaced with links
- [ ] Document flows logically
- [ ] All cross-references working
- [ ] No information loss (all content in extracted files)
- [ ] Professional appearance maintained

**Commit:** "docs(wiki): clean up PSK Identity 02 document after extractions"

---

#### Step 5.4d: Standardize PSK Key Extraction Example Page ⏳

**Objective:** Apply template to existing PSK key extraction example page

**Page to Update:** `PSK-Key-from-Gosund-Wifi-Bulb.md`

**Template:** Reference-Template.md

**Changes:**
- Add standard header with status
- Expand content with more context
- Add implementation details section
- Add code references to firmware extraction
- Add related pages section linking to other PSK docs
- Add troubleshooting section
- Add footer

**Validation:**
- [ ] All original content preserved
- [ ] Template applied correctly
- [ ] Code references added
- [ ] Expanded with additional context
- [ ] Cross-references to PSK documentation

**Commit:** "docs(wiki): standardize PSK key extraction example page"

---

#### Step 5.4 Overall Progress

| Sub-step | Description | Status |
|----------|-------------|--------|
| 5.4a | Extract firmware database | ⏳ Pending |
| 5.4b | Extract research tools | ⏳ Pending |
| 5.4c | Clean up main PSK document | ⏳ Pending |
| 5.4d | Standardize key extraction page | ⏳ Pending |

**Note:** PSK-Research-Procedures.md already extracted in Phase 3

---

### Step 5.5: Standardize Troubleshooting Page ⏳

**Page to Update:**
- `Troubleshooting.md`

**Template:** Reference-Template.md (adapted)

**Changes:**
- Add standard header
- Expand table with more issues
- Add common patterns section
- Add diagnostic procedure
- Add cross-references to related pages
- Add code references for debugging

**Validation:**
- [ ] All original entries preserved
- [ ] New content added from community feedback
- [ ] Template applied
- [ ] Comprehensive coverage

**Commit:** "docs(wiki): expand and standardize troubleshooting page"

---

## Dependencies

- **Phase 2 complete:** Templates must exist
- **Phase 3 complete:** Incomplete pages should be finished first
- **Phase 4 started:** New pages will be cross-referenced

---

## Validation Checklist

For each updated page:
- [ ] All original content preserved
- [ ] Template properly applied
- [ ] Header with metadata added
- [ ] Related pages section added
- [ ] Footer added
- [ ] Cross-references accurate
- [ ] Professional formatting
- [ ] Markdown renders correctly

---

## Phase Progress

### Zero Information Loss Guarantee

Each step must validate that:
- Every paragraph from original is preserved or improved
- Every link from original is preserved or updated
- Every technical detail is maintained
- Content is only added, never removed (unless duplicated elsewhere)

---

## Commit Log

| Step | Commit Message | Date | SHA | Validated |
|------|---------------|------|-----|-----------|
| 5.1 | docs(wiki): standardize device compatibility pages | 2025-11-06 | a799b33 | ✅ |
| 5.2 | [pending] | - | - | ⏳ |
| 5.3 | [pending] | - | - | ⏳ |
| 5.4a | docs(wiki): extract PSK firmware database into standalone page | - | - | ⏳ |
| 5.4b | docs(wiki): extract PSK research tools into standalone page | - | - | ⏳ |
| 5.4c | docs(wiki): clean up PSK Identity 02 document after extractions | - | - | ⏳ |
| 5.4d | docs(wiki): standardize PSK key extraction example page | - | - | ⏳ |
| 5.5 | [pending] | - | - | ⏳ |

---

## Phase Completion Criteria

- [ ] All device compatibility pages standardized
- [ ] All setup guides standardized
- [ ] All advanced topic pages standardized
- [ ] PSK documentation restructuring complete:
  - [ ] PSK firmware database extracted (5.4a)
  - [ ] PSK research tools extracted (5.4b)
  - [ ] PSK main document cleaned up (5.4c)
  - [ ] PSK key extraction page standardized (5.4d)
- [ ] Troubleshooting page expanded and standardized
- [ ] All validations passed
- [ ] All commits made
- [ ] Phase document updated
- [ ] PSK_EXTRACTION_PLAN.md removed (work integrated)

---

## References

- [Main Plan](WIKI_RESTRUCTURING_PLAN.md)
- [Content Inventory](WIKI_CONTENT_INVENTORY.md) - For validation
- [Templates (Phase 2)](WIKI_PHASE_2_TEMPLATES.md)
- [Next Phase](WIKI_PHASE_6_NEW_HOME.md)

---

**Phase 5: Pending** ⏳
**Last Updated:** 2025-11-05
**Estimated Duration:** 8 hours (includes integrated PSK extraction work)
**Total Sub-steps:** 8 (5.1, 5.2, 5.3, 5.4a, 5.4b, 5.4c, 5.4d, 5.5)
