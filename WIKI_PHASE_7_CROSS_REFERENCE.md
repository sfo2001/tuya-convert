# Phase 7: Cross-Reference and Link All Pages

**Phase Status:** ⏳ PENDING
**Start Date:** -
**End Date:** -
**Progress:** 0/2 steps (0%)

[← Back to Overview](WIKI_RESTRUCTURING_PLAN.md) | [← Previous Phase](WIKI_PHASE_6_NEW_HOME.md) | [Next Phase →](WIKI_PHASE_8_VALIDATION.md)

---

## Phase Objectives

Add cross-references and code references to all wiki pages to:
1. Ensure no page is orphaned
2. Enable easy navigation between related topics
3. Link technical documentation to actual code implementation
4. Create bidirectional links where appropriate

---

## Steps

### Step 7.1: Add Cross-References ⏳

**Status:** PENDING

#### Objective
Add "Related Pages" sections to all pages with appropriate links

#### Approach

1. **Review each page** and identify related content
2. **Add "Related Pages" section** if not present
3. **Add bidirectional links** where appropriate
4. **Ensure no orphaned pages** - every page should be reachable

#### Pages to Update
- All 14 existing pages
- All 7+ new pages from Phase 4
- Total: ~21+ pages

#### Cross-Reference Strategy

**Example: Installation.md**
Should link to:
- Quick-Start-Guide.md (next step)
- Troubleshooting.md (if problems occur)
- Using-Docker.md (alternative setup)
- Using-a-Raspberry-Pi.md (platform-specific)

**Example: PSK-Identity-02-Protocol.md**
Should link to:
- Protocol-Overview.md (parent page)
- Helping-with-new-psk-format.md (contribution)
- PSK-Key-from-Gosund-Wifi-Bulb.md (related)
- System-Architecture.md (context)

#### Validation Checklist
- [ ] Every page has "Related Pages" section
- [ ] Bidirectional links where appropriate
- [ ] No orphaned pages
- [ ] Links are relevant
- [ ] No excessive linking (quality over quantity)

#### Planned Commit
- **Message:** "docs(wiki): add cross-references to all pages"
- **References:** WIKI_PHASE_7_CROSS_REFERENCE.md Step 7.1

---

### Step 7.2: Add Code References ⏳

**Status:** PENDING

#### Objective
Add code file references to all technical and guide pages

#### Approach

1. **Review each technical page**
2. **Identify code** that implements documented features
3. **Add code references** with file paths and line numbers
4. **Verify accuracy** against actual codebase

#### Pages Requiring Code References

**High Priority:**
- Installation.md → `install_prereq.sh`
- Quick-Start-Guide.md → `start_flash.sh`, `firmware_picker.sh`
- Using-Docker.md → `docker-compose.yml`, `Dockerfile`, `.env-template`
- System-Architecture.md → All Python scripts, `setup_ap.sh`
- PSK-Identity-02-Protocol.md → `scripts/psk-frontend.py`
- API-Reference.md → `scripts/fake-registration-server.py`, `scripts/mq_pub_15.py`
- Smartconfig-Protocol.md → `scripts/smartconfig/`

**Medium Priority:**
- Flash-a-multipart-binary.md → Related scripts
- Using-a-Raspberry-Pi.md → `setup_ap.sh`
- Troubleshooting.md → Log locations, debug scripts

#### Code Reference Format

```markdown
## Code References

- **Main Implementation:** `scripts/psk-frontend.py`
- **Key Functions:**
  - `generate_psk()` (line 45)
  - `validate_identity()` (line 78)
- **Related Files:**
  - `scripts/smartconfig/tudosmart.py` (line 23)
  - `start_flash.sh` (line 156)
```

#### Validation Using WIKI_CODE_ALIGNMENT.md

- Reference the alignment document from Phase 0
- Verify each code reference against actual files
- Ensure line numbers are accurate (or use ranges if exact lines may change)

#### Validation Checklist
- [ ] All technical pages have code references
- [ ] Code paths accurate
- [ ] Line numbers current (or marked as approximate)
- [ ] Implementation links verified
- [ ] Reference format consistent

#### Planned Commit
- **Message:** "docs(wiki): add code references to technical pages"
- **References:** WIKI_PHASE_7_CROSS_REFERENCE.md Step 7.2

---

## Cross-Reference Map

### Page Relationship Matrix

| From Page | Should Link To |
|-----------|---------------|
| Home | All category hub pages |
| Installation | Quick-Start, Troubleshooting, all Setup Guides |
| Quick-Start-Guide | Installation, Compatible-Devices, Troubleshooting |
| Compatible-Devices pages | Each other, Troubleshooting, Failed-Attempts |
| Setup Guides | Installation, Quick-Start, each other |
| PSK pages | Each other, Protocol-Overview, Contributing |
| Technical Reference | Protocol-Overview, System-Architecture, each other |
| Troubleshooting | Failed-Attempts, all Setup Guides, Installation |
| Contributing pages | Each other, How-to-Contribute hub |

---

## Dependencies

- **All previous phases** should be complete or nearly complete
- **WIKI_CODE_ALIGNMENT.md** from Phase 0 for code references
- **New pages** from Phase 4 must exist

---

## Phase Progress

### Completed Steps: 0/2 (0%)
- ⏳ Step 7.1: Add Cross-References
- ⏳ Step 7.2: Add Code References

### Estimated Time
- Step 7.1: ~3 hours (review all pages, add links)
- Step 7.2: ~2 hours (add code references to technical pages)
- Total: ~5 hours

---

## Validation Strategy

### Pre-Commit Validation
For each modified page:
- [ ] All new links tested
- [ ] All code references verified
- [ ] Related Pages section present
- [ ] Bidirectional links added where needed
- [ ] No broken links introduced

### Post-Phase Validation
- [ ] No orphaned pages
- [ ] All technical pages have code references
- [ ] Cross-reference map fully implemented
- [ ] Navigation experience smooth

---

## Phase Completion Criteria

- [ ] Step 7.1 complete and committed
- [ ] Step 7.2 complete and committed
- [ ] All pages cross-referenced
- [ ] All technical pages have code references
- [ ] No orphaned pages
- [ ] All links validated
- [ ] Phase document updated

---

## Commit Log

| Step | Commit Message | Date | SHA | Validated |
|------|---------------|------|-----|-----------|
| 7.1 | [pending] | - | - | ⏳ |
| 7.2 | [pending] | - | - | ⏳ |

---

## References

- [Main Plan](WIKI_RESTRUCTURING_PLAN.md)
- [Code Alignment](WIKI_CODE_ALIGNMENT.md) - For code references
- [Information Architecture](WIKI_RESTRUCTURING_PLAN.md#information-architecture)
- [Next Phase](WIKI_PHASE_8_VALIDATION.md)

---

**Phase 7: Pending** ⏳
**Last Updated:** 2025-11-05
**Estimated Duration:** 5 hours
