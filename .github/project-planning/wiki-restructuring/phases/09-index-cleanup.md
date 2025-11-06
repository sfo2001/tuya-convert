# Phase 9: Create Wiki Index and Cleanup

**Phase Status:** ⏳ PENDING
**Start Date:** -
**End Date:** -
**Progress:** 0/3 steps (0%)

[← Back to Overview](WIKI_RESTRUCTURING_PLAN.md) | [← Previous Phase](WIKI_PHASE_8_VALIDATION.md)

---

## Phase Objectives

Final touches to complete the wiki restructuring:

1. Create _Sidebar for consistent navigation
2. Create _Footer for consistent footer across all pages
3. Remove template files (no longer needed)

This is the final phase before marking the restructuring complete.

---

## Steps

### Step 9.1: Create _Sidebar ⏳

**Status:** PENDING

#### Objective
Create GitHub wiki sidebar for easy navigation

#### About _Sidebar.md

GitHub wikis support a special `_Sidebar.md` file that appears on every wiki page, providing consistent navigation.

#### Planned Structure

```markdown
**[🏠 Home](Home)**

---

### 🚀 Getting Started
- [Installation](Installation)
- [Quick Start](Quick-Start-Guide)
- [Troubleshooting](Troubleshooting)

### 📱 Devices
- [Compatible Devices](Compatible-devices)
- [HTTP Firmware](Compatible-devices-(HTTP-firmware))
- [HTTPS Firmware](Compatible-devices-(HTTPS-firmware))

### 🔧 Setup Guides
- [Docker](Using-Docker)
- [Raspberry Pi](Using-a-Raspberry-Pi)
- [Pi Zero W](Using-Only-a-Stock-Raspberry-Pi-ZeroW-and-USB-Cable)

### 📚 Advanced
- [Multipart Binary](Flash-a-multipart-binary)
- [Specific Devices](Flashing-of-WiFi-Switch-with-a-Raspberry-Pi)

### 🔬 Technical
- [Protocol Overview](Protocol-Overview)
- [PSK Identity 02](Collaboration-document-for-PSK-Identity-02)
- [System Architecture](System-Architecture)
- [API Reference](API-Reference)

### 🤝 Contributing
- [How to Contribute](How-to-Contribute)
- [PSK Research](Helping-with-new-psk-format)
- [Additional Resources](Additional-Resources)

---

[📖 All Pages](Home)
```

#### Design Considerations
- **Compact** - Fits in sidebar without scrolling
- **Icons** - Visual navigation aids (optional, GitHub supports emoji)
- **Categories** - Matches Home page structure
- **Most Important Links** - Not every page, just key pages
- **Quick Access** - Common pages easily accessible

#### File to Create
- `docs/_Sidebar.md`

#### Validation Checklist
- [ ] Sidebar created
- [ ] Key pages linked
- [ ] Logical grouping
- [ ] Not too long
- [ ] Renders correctly in wiki
- [ ] Links work

#### Planned Commit
- **Message:** "docs(wiki): create navigation sidebar"
- **References:** WIKI_PHASE_9_INDEX_CLEANUP.md Step 9.1

---

### Step 9.2: Create _Footer ⏳

**Status:** PENDING

#### Objective
Create GitHub wiki footer for consistent footer across all pages

#### About _Footer.md

GitHub wikis support a special `_Footer.md` file that appears at the bottom of every wiki page.

#### Planned Content

```markdown
---

**tuya-convert** | [Main Repo](https://github.com/sfo2001/tuya-convert) | [Report Issue](https://github.com/sfo2001/tuya-convert/issues) | [Home](Home) | [All Pages](Home)

*Last Updated: 2025-11-05 | This is a fork of [ct-Open-Source/tuya-convert](https://github.com/ct-Open-Source/tuya-convert)*
```

#### Design Considerations
- **Consistent** - Same on every page
- **Helpful Links** - Back to main repo, issue tracker, home
- **Attribution** - Note this is a fork
- **Not Intrusive** - Small and unobtrusive
- **Professional** - Clean appearance

#### File to Create
- `docs/_Footer.md`

#### Validation Checklist
- [ ] Footer created
- [ ] Links to main repo, issues, home
- [ ] Attribution to original project
- [ ] Professional appearance
- [ ] Renders correctly in wiki

#### Planned Commit
- **Message:** "docs(wiki): create standard footer"
- **References:** WIKI_PHASE_9_INDEX_CLEANUP.md Step 9.2

---

### Step 9.3: Remove Template Files ⏳

**Status:** PENDING

#### Objective
Remove `_templates/` directory after restructuring complete

#### Rationale
Template files were created in Phase 2 for reference during restructuring. Now that restructuring is complete:
- Templates are documented in WIKI_RESTRUCTURING_PLAN.md
- All pages have been standardized
- Template files no longer needed in wiki repository

#### Files to Remove
- `_templates/Guide-Template.md`
- `_templates/Reference-Template.md`
- `_templates/Device-List-Template.md`
- `_templates/Hub-Page-Template.md`
- `_templates/` directory

#### Preservation
Templates are preserved in:
- WIKI_RESTRUCTURING_PLAN.md (documentation)
- Git history (if needed for reference)
- This plan document

#### Validation Checklist
- [ ] Templates documented in main plan
- [ ] No longer needed for wiki
- [ ] Safe to remove

#### Planned Commit
- **Message:** "docs(wiki): remove template files after restructuring complete"
- **References:** WIKI_PHASE_9_INDEX_CLEANUP.md Step 9.3

---

## Phase Progress

### Completed Steps: 0/3 (0%)
- ⏳ Step 9.1: Create _Sidebar
- ⏳ Step 9.2: Create _Footer
- ⏳ Step 9.3: Remove Template Files

### Estimated Time
- Step 9.1: ~30 minutes (create and test sidebar)
- Step 9.2: ~15 minutes (create and test footer)
- Step 9.3: ~15 minutes (remove template files)
- Total: ~1 hour

---

## Validation

### Sidebar Validation
- [ ] Appears on all pages
- [ ] Links work
- [ ] Not too long
- [ ] Logical organization
- [ ] Helpful for navigation

### Footer Validation
- [ ] Appears on all pages
- [ ] Links work
- [ ] Professional appearance
- [ ] Not intrusive
- [ ] Attribution clear

---

## Phase Completion Criteria

- [ ] _Sidebar.md created and validated
- [ ] _Footer.md created and validated
- [ ] Template files removed
- [ ] All commits made
- [ ] Phase document updated
- [ ] Wiki restructuring complete!

---

## Commit Log

| Step | Commit Message | Date | SHA | Validated |
|------|---------------|------|-----|-----------|
| 9.1 | [pending] | - | - | ⏳ |
| 9.2 | [pending] | - | - | ⏳ |
| 9.3 | [pending] | - | - | ⏳ |

---

## Post-Completion

### After This Phase

**Wiki restructuring is COMPLETE!**

The wiki will have:
- ✅ Professional structure with logical information architecture
- ✅ Consistent formatting across all pages
- ✅ Zero information loss (all original content preserved)
- ✅ Comprehensive cross-references and navigation
- ✅ Code references linking docs to implementation
- ✅ New essential pages filling documentation gaps
- ✅ Sidebar and footer for consistent navigation
- ✅ All validation passed

### Final Steps

1. **User testing** - Have someone navigate the wiki
2. **Gather feedback** - Open issue for community feedback
3. **Iterate** - Make minor adjustments based on feedback
4. **Celebrate** - Document completion! 🎉

### Maintenance Going Forward

- Update Last Updated dates when pages are modified
- Keep code references current when code changes
- Add new devices to compatibility pages
- Expand content based on community needs
- Maintain cross-references as new pages are added

---

## References

- [Main Plan](WIKI_RESTRUCTURING_PLAN.md)
- [Previous Phase](WIKI_PHASE_8_VALIDATION.md)
- [GitHub Wiki Sidebar Documentation](https://docs.github.com/en/communities/documenting-your-project-with-wikis/creating-a-footer-or-sidebar-for-your-wiki)

---

**Phase 9: Pending** ⏳
**Last Updated:** 2025-11-05
**Estimated Duration:** 1 hour
**Note:** Final phase before completion! 🎯
