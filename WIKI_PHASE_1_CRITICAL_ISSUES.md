# Phase 1: Fix Critical Issues

**Phase Status:** 🔄 IN PROGRESS
**Start Date:** 2025-11-04
**End Date:** -
**Progress:** 2/3 steps (67%)

[← Back to Overview](WIKI_RESTRUCTURING_PLAN.md) | [← Previous Phase](WIKI_PHASE_0_PREPARATION.md) | [Next Phase →](WIKI_PHASE_2_TEMPLATES.md)

---

## Phase Objectives

Fix critical broken links and external references that prevent proper wiki navigation:

1. Fix Home page links to compatible devices pages
2. Standardize Additional-Resources page with external link documentation
3. Fix file attachment links in PSK format help page

This phase addresses immediate usability issues before proceeding with content restructuring.

---

## Steps

### Step 1.1: Fix Home Page Links ✅

**Status:** COMPLETE
**Completed:** 2025-11-04

#### Objective
Replace ct-Open-Source external links with relative internal links

#### Problem Identified
Home.md contained hardcoded links to the original ct-Open-Source repository:
- Line 4: `https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTP-firmware)`
- Line 5: `https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTPS-firmware)`

These links redirected users away from the fork to the original project.

#### Actions Taken
- Replaced absolute URLs with relative wiki links
- Changed `https://github.com/ct-Open-Source/...` to relative page names
- Verified links work in wiki navigation

#### Changes Made
```diff
- * [HTTP (old) firmware](https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTP-firmware))
+ * [HTTP (old) firmware](Compatible-devices-(HTTP-firmware))
- * [HTTPS (new) firmware](https://github.com/ct-Open-Source/tuya-convert/wiki/Compatible-devices-(HTTPS-firmware))
+ * [HTTPS (new) firmware](Compatible-devices-(HTTPS-firmware))
```

#### File Modified
- `docs/Home.md`

#### Validation
- [x] Links work in GitHub wiki preview
- [x] No external ct-Open-Source links remain in Home.md
- [x] Relative links navigate correctly
- [x] No information lost

#### Commit
- **Message:** Part of "docs: migrate wiki to main repository /docs directory"
- **SHA:** 256a89b
- **Date:** 2025-11-04
- **Note:** This fix was included in the wiki migration commit

---

### Step 1.2: Fix Additional-Resources Links ✅

**Status:** COMPLETE
**Completed:** 2025-11-05

#### Objective
Standardize Additional-Resources page with proper external link documentation

#### Problem Identified
Additional-Resources.md contained links to:
- Original project's GitHub issue (line 5)
- Third-party tools

These links were not clearly marked as external references, potentially confusing users about whether they belong to this fork or the original project.

#### Actions Taken
- Added standard header with Last Updated and Status
- Added clear note explaining page contains external links
- Clearly labeled external links to original project
- Kept external links (appropriate as external references)
- Verified all links work

#### Changes Made
1. **Added Header:**
   ```markdown
   **Last Updated:** 2025-11-05
   **Status:** ✅ Complete
   ```

2. **Added External Link Note:**
   ```markdown
   > **Note:** This page contains external links to resources from the original tuya-convert project and third-party tools.
   ```

3. **Restructured video tutorial link** for clarity

#### File Modified
- `docs/Additional-Resources.md`

#### Validation
- [x] Links work correctly
- [x] External links clearly marked as external
- [x] Standard header applied
- [x] Professional appearance
- [x] No information lost

#### Commit
- **Message:** "docs(wiki): standardize Additional-Resources with external link documentation"
- **SHA:** de9178e
- **Date:** 2025-11-05

#### Follow-up Update
- **Message:** "docs: update WIKI_RESTRUCTURING_PLAN.md with Step 1.2 completion"
- **SHA:** 74fa883
- **Date:** 2025-11-05

---

### Step 1.3: Fix Helping-with-new-psk-format File Links ⏳

**Status:** PENDING
**Assigned To:** Next work item

#### Objective
Fix file attachment links that point to original ct-Open-Source repository

#### Problem Identified
Helping-with-new-psk-format.md contains file links that point to the original repository:
```markdown
[20191213_122529.csv](https://github.com/ct-Open-Source/tuya-convert/files/3973599/...)
[all-packets.tar.gz](https://github.com/ct-Open-Source/tuya-convert/files/3973601/...)
[flash-packets.tar.gz](https://github.com/ct-Open-Source/tuya-convert/files/3973602/...)
...
```

These files are attachments to the original wiki and need to be addressed.

#### Options to Consider
1. **Download and re-upload** files to this fork's GitHub (if repository supports attachments)
2. **Keep external links** with clear documentation they reference original project
3. **Host files elsewhere** (e.g., in repository as binary files)
4. **Create clear external reference** section noting dependency on original project files

#### Recommended Approach
Based on GitHub's wiki attachment limitations, recommend **Option 2**:
- Keep links as external references
- Add clear note that files are hosted on original project
- Add context explaining what files contain
- Ensure content explaining PSK format is complete (already done in Step 3.1)

#### Files Affected
- `docs/Helping-with-new-psk-format.md`

#### Validation Checklist
- [ ] File links accessible
- [ ] Clear note about external hosting
- [ ] Content explains what files contain
- [ ] Alternative access methods documented (if any)
- [ ] No information lost

#### Planned Commit
- **Message:** "docs(wiki): document external file attachments in PSK format page"
- **References:** WIKI_PHASE_1_CRITICAL_ISSUES.md Step 1.3

---

## Phase Progress

### Completed Steps: 2/3 (67%)
- ✅ Step 1.1: Fix Home Page Links
- ✅ Step 1.2: Fix Additional-Resources Links
- ⏳ Step 1.3: Fix Helping-with-new-psk-format File Links

### Remaining Work
- 1 step pending in this phase

### Blockers
- None

### Estimated Time to Completion
- ~30 minutes (1 step remaining)

---

## Commit Log

| Step | Commit Message | Date | SHA | Validated |
|------|---------------|------|-----|-----------|
| 1.1 | docs: migrate wiki to main repository /docs directory | 2025-11-04 | 256a89b | ✅ |
| 1.2 | docs(wiki): standardize Additional-Resources with external link documentation | 2025-11-05 | de9178e | ✅ |
| 1.2 (update) | docs: update WIKI_RESTRUCTURING_PLAN.md with Step 1.2 completion | 2025-11-05 | 74fa883 | ✅ |
| 1.3 | [pending] | - | - | ⏳ |

---

## Validation Summary

### Pre-Commit Validations Performed

#### Step 1.1 Validation
- ✅ Content preserved (all original links converted, not removed)
- ✅ Links tested (relative links work in wiki)
- ✅ Format compliant (proper markdown syntax)
- ✅ No regressions (wiki navigation improved)

#### Step 1.2 Validation
- ✅ Content preserved (all original links kept)
- ✅ Links tested (external links verified working)
- ✅ Format compliant (standard header applied)
- ✅ Professional appearance (clear documentation)
- ✅ No regressions (external references clearly marked)

---

## Issues and Resolutions

### Issue 1: Home Page Link Format
**Problem:** Hard-coded absolute URLs to original repository
**Solution:** Converted to relative wiki links
**Status:** ✅ Resolved

### Issue 2: External Link Clarity
**Problem:** External links not clearly marked as external
**Solution:** Added clear documentation note and context
**Status:** ✅ Resolved

### Issue 3: File Attachments
**Problem:** File attachments hosted on original repository
**Solution:** [Pending - Step 1.3]
**Status:** ⏳ In Progress

---

## Lessons Learned

### What Worked Well
1. **Atomic commits** - Each step committed separately for easy tracking
2. **Validation checklists** - Prevented missed requirements
3. **Clear documentation** - External references now well-documented

### Challenges
1. **File attachments** - GitHub wiki attachment limitations require creative solution
2. **Link verification** - Manual testing needed for each link

### Improvements for Next Phase
1. Continue atomic commit approach
2. Document external dependencies clearly
3. Consider hosting strategy for binary files

---

## Phase Completion Criteria

Before marking this phase complete:

- [x] Step 1.1 complete and committed
- [x] Step 1.2 complete and committed
- [ ] Step 1.3 complete and committed
- [ ] All links validated
- [ ] All external references documented
- [ ] No broken links remain
- [ ] Phase document updated with all commits

---

## Next Phase

**Phase 2: Create Standard Templates** - [WIKI_PHASE_2_TEMPLATES.md](WIKI_PHASE_2_TEMPLATES.md)

After critical link issues are fixed, Phase 2 will create standardized templates for:
- Guide/Tutorial pages
- Reference pages
- Device list pages
- Hub/Landing pages

---

## Related Phases

- **Phase 0: Preparation** - [WIKI_PHASE_0_PREPARATION.md](WIKI_PHASE_0_PREPARATION.md)
- **Phase 3: Complete Incomplete Pages** - [WIKI_PHASE_3_INCOMPLETE_PAGES.md](WIKI_PHASE_3_INCOMPLETE_PAGES.md) (also in progress)

---

## References

- [Main Plan](WIKI_RESTRUCTURING_PLAN.md)
- [Content Inventory](WIKI_CONTENT_INVENTORY.md)
- [Previous Phase](WIKI_PHASE_0_PREPARATION.md)
- [Next Phase](WIKI_PHASE_2_TEMPLATES.md)

---

**Phase 1: In Progress** 🔄
**Last Updated:** 2025-11-05
**Next Step:** Step 1.3 - Fix Helping-with-new-psk-format File Links
