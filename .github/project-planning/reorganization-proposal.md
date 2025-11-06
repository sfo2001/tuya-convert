# Proposal: Issue Tracking and Analysis Reorganization

**Date**: 2025-11-06
**Status**: Proposal
**Purpose**: Organize issue analysis files and improve project tidiness

---

## Current Problems

### Root Directory Clutter

Currently, the project root contains **27+ markdown files**, including:

**Issue Analysis Files (10+)**:
- `ANALYSIS_ISSUE_1143.md`
- `ANALYSIS_ISSUE_1157.md`
- `ANALYSIS_ISSUE_1163.md`
- `ANALYSIS_ISSUE_1167.md`
- `IMPLEMENTATION_ISSUE_1167.md`
- `SUMMARY_ISSUE_1143.md`
- `SUMMARY_ISSUE_1157.md`
- `SUMMARY_ISSUE_1163.md`
- `SUMMARY_ISSUE_1167.md`
- `GITHUB_ISSUE_CONTENT.md`
- `ISSUE_DRAFT_REMOVE_SUDO.md`

**Wiki Planning Files (10+)**:
- `WIKI_RESTRUCTURING_PLAN.md`
- `WIKI_PHASE_0_PREPARATION.md` through `WIKI_PHASE_9_INDEX_CLEANUP.md`
- `WIKI_CODE_ALIGNMENT.md`
- `WIKI_CONTENT_INVENTORY.md`

**Documentation Files**:
- `DOCUMENTATION_AUDIT_STATUS.md`
- `COLLAB_DOC_REFACTORING_PLAN.md`

**Problems**:
1. ❌ **Hard to find specific information** - Need to search through many files
2. ❌ **No clear status tracking** - Which issues are resolved? Pending? Abandoned?
3. ❌ **Difficult to navigate** - No index or hierarchy
4. ❌ **Naming inconsistency** - Different patterns (ANALYSIS_, SUMMARY_, IMPLEMENTATION_)
5. ❌ **Doesn't scale** - Will get worse with more issues
6. ❌ **Cluttered root** - Makes project look disorganized
7. ❌ **No historical record** - Hard to see progression of work

---

## Proposed Solution

### Option A: GitHub-Centric Structure (Recommended)

```
.github/
├── issue-analysis/
│   ├── README.md                    # Index and guide
│   ├── TRACKING.md                  # Status of all issues
│   ├── upstream/                    # Upstream (ct-Open-Source) issues
│   │   ├── 1143/
│   │   │   ├── analysis.md
│   │   │   ├── summary.md
│   │   │   └── resolution.md
│   │   ├── 1157/
│   │   │   ├── analysis.md
│   │   │   └── summary.md
│   │   ├── 1163/
│   │   │   ├── analysis.md
│   │   │   ├── implementation.md
│   │   │   └── summary.md
│   │   └── 1167/
│   │       ├── analysis.md
│   │       ├── implementation.md
│   │       └── summary.md
│   └── fork/                        # Your fork's issues (if any)
│       └── 1/
│           └── analysis.md
├── wiki-planning/
│   ├── README.md
│   ├── restructuring-plan.md
│   ├── phases/
│   │   ├── phase-0-preparation.md
│   │   ├── phase-1-critical-issues.md
│   │   ├── ...
│   │   └── phase-9-index-cleanup.md
│   └── inventory/
│       ├── content-inventory.md
│       └── code-alignment.md
└── project-planning/
    ├── documentation-audit.md
    └── collab-doc-refactoring.md
```

**Pros**:
- ✅ `.github/` is standard location for GitHub-related content
- ✅ Clear hierarchical structure
- ✅ Easy to find issues by number
- ✅ Separates upstream vs fork issues
- ✅ Can add CI workflows in `.github/workflows/`

**Cons**:
- ⚠️ `.github/` typically for GitHub Actions, issues templates, etc.

---

### Option B: Documentation-Centric Structure

```
docs/
├── analysis/                        # Issue analysis
│   ├── README.md
│   ├── TRACKING.md
│   ├── issues/
│   │   ├── 1143-install-prereq-pep668/
│   │   ├── 1157-new-chip-incompatible/
│   │   ├── 1163-nix-flake-support/
│   │   └── 1167-venv-path-sudo-screen/
│   └── resolved/                    # Archive resolved issues
│       └── 1153-sslpsk3-migration/
├── planning/
│   ├── wiki-restructuring/
│   └── documentation-audit/
└── [existing docs structure]
```

**Pros**:
- ✅ Part of documentation hierarchy
- ✅ Easy to link from user-facing docs
- ✅ Clear separation of active vs resolved

**Cons**:
- ⚠️ May mix development notes with user docs

---

### Option C: Dedicated Research Directory

```
research/                            # Or "analysis/" or "notes/"
├── README.md
├── issues/
│   ├── TRACKING.md
│   ├── upstream/
│   │   └── [by issue number]
│   └── fork/
│       └── [by issue number]
├── wiki-planning/
├── documentation/
└── archive/                         # Completed/resolved work
```

**Pros**:
- ✅ Clearly separates research from code/docs
- ✅ Flexible structure
- ✅ Can include non-issue research

**Cons**:
- ⚠️ Adds new top-level directory

---

## Recommended Structure (Hybrid Approach)

I recommend **Option A with enhancements**:

```
.github/
├── issue-analysis/
│   ├── README.md                    # How to use this directory
│   ├── TRACKING.md                  # Master status tracker
│   ├── TEMPLATE.md                  # Template for new issue analysis
│   │
│   ├── resolved/                    # ✅ Completed issues
│   │   ├── 1143-pep668-compliance/
│   │   │   ├── analysis.md
│   │   │   └── resolution.md
│   │   ├── 1153-sslpsk3-migration/
│   │   ├── 1161-docker-files-mount/
│   │   └── 1167-venv-sudo-screen/
│   │       ├── analysis.md
│   │       ├── implementation.md
│   │       └── summary.md
│   │
│   ├── open/                        # 🔄 Under investigation
│   │   └── 1163-nix-flake/
│   │       ├── analysis.md
│   │       ├── implementation.md
│   │       └── summary.md
│   │
│   └── archived/                    # 📦 Not actionable/won't fix
│       └── 1157-chip-incompatible/
│           ├── analysis.md
│           └── summary.md
│
├── project-planning/
│   ├── wiki-restructuring/
│   │   ├── plan.md
│   │   ├── phases/
│   │   │   ├── 00-preparation.md
│   │   │   ├── 01-critical-issues.md
│   │   │   └── ...
│   │   └── inventory/
│   │       ├── content.md
│   │       └── code-alignment.md
│   │
│   └── documentation/
│       ├── audit-status.md
│       └── refactoring-plan.md
│
└── templates/
    ├── ISSUE_TEMPLATE/
    └── PULL_REQUEST_TEMPLATE.md
```

---

## TRACKING.md Structure

The master tracking file provides an at-a-glance view:

```markdown
# Issue Analysis Tracking

**Last Updated**: 2025-11-06

## Legend

- ✅ **Resolved** - Fixed and merged
- 🔄 **In Progress** - Currently working on
- 📦 **Archived** - Not actionable / Won't fix
- 🔍 **Investigating** - Analysis phase
- ⏸️ **Paused** - Blocked or deprioritized

---

## Upstream Issues (ct-Open-Source/tuya-convert)

| Issue | Title | Status | Location | Commits | PR |
|-------|-------|--------|----------|---------|-----|
| #1143 | PEP 668 compliance | ✅ Resolved | `resolved/1143-pep668-compliance/` | 1663d29 | #17 |
| #1153 | sslpsk3 migration | ✅ Resolved | `resolved/1153-sslpsk3-migration/` | 59549b1 | #10 |
| #1157 | Chip incompatibility | 📦 Archived | `archived/1157-chip-incompatible/` | - | #19 |
| #1161 | Docker files/ mount | ✅ Resolved | `resolved/1161-docker-files-mount/` | bb8f12e | #14 |
| #1163 | Nix flake support | 🔄 In Progress | `open/1163-nix-flake/` | f78bd4a | - |
| #1167 | Venv PATH sudo | ✅ Resolved | `resolved/1167-venv-sudo-screen/` | d071bdc | - |

---

## Quick Links

- **Resolved Issues**: [resolved/](resolved/)
- **In Progress**: [open/](open/)
- **Archived**: [archived/](archived/)

---

## Statistics

- Total Analyzed: 6
- Resolved: 4 (67%)
- In Progress: 1 (17%)
- Archived: 1 (17%)
```

---

## Migration Plan

### Phase 1: Create Directory Structure (5 minutes)

```bash
# Create directories
mkdir -p .github/issue-analysis/{resolved,open,archived}
mkdir -p .github/project-planning/{wiki-restructuring,documentation}

# Create index files
touch .github/issue-analysis/README.md
touch .github/issue-analysis/TRACKING.md
touch .github/issue-analysis/TEMPLATE.md
```

### Phase 2: Migrate Issue Files (10 minutes)

```bash
# Example migration commands
# Issue 1143 (resolved)
mkdir -p .github/issue-analysis/resolved/1143-pep668-compliance
mv ANALYSIS_ISSUE_1143.md .github/issue-analysis/resolved/1143-pep668-compliance/analysis.md
mv SUMMARY_ISSUE_1143.md .github/issue-analysis/resolved/1143-pep668-compliance/summary.md

# Issue 1157 (archived - not actionable)
mkdir -p .github/issue-analysis/archived/1157-chip-incompatible
mv ANALYSIS_ISSUE_1157.md .github/issue-analysis/archived/1157-chip-incompatible/analysis.md
mv SUMMARY_ISSUE_1157.md .github/issue-analysis/archived/1157-chip-incompatible/summary.md

# Issue 1163 (in progress)
mkdir -p .github/issue-analysis/open/1163-nix-flake
mv ANALYSIS_ISSUE_1163.md .github/issue-analysis/open/1163-nix-flake/analysis.md
mv SUMMARY_ISSUE_1163.md .github/issue-analysis/open/1163-nix-flake/summary.md

# Issue 1167 (resolved)
mkdir -p .github/issue-analysis/resolved/1167-venv-sudo-screen
mv ANALYSIS_ISSUE_1167.md .github/issue-analysis/resolved/1167-venv-sudo-screen/analysis.md
mv IMPLEMENTATION_ISSUE_1167.md .github/issue-analysis/resolved/1167-venv-sudo-screen/implementation.md
mv SUMMARY_ISSUE_1167.md .github/issue-analysis/resolved/1167-venv-sudo-screen/summary.md

# Misc issue files
mv GITHUB_ISSUE_CONTENT.md .github/issue-analysis/archived/
mv ISSUE_DRAFT_REMOVE_SUDO.md .github/issue-analysis/archived/
```

### Phase 3: Migrate Wiki Planning (5 minutes)

```bash
# Create wiki planning structure
mkdir -p .github/project-planning/wiki-restructuring/{phases,inventory}

# Move main plan
mv WIKI_RESTRUCTURING_PLAN.md .github/project-planning/wiki-restructuring/plan.md

# Move phase files
mv WIKI_PHASE_0_PREPARATION.md .github/project-planning/wiki-restructuring/phases/00-preparation.md
mv WIKI_PHASE_1_CRITICAL_ISSUES.md .github/project-planning/wiki-restructuring/phases/01-critical-issues.md
# ... continue for all phases

# Move inventory files
mv WIKI_CONTENT_INVENTORY.md .github/project-planning/wiki-restructuring/inventory/content.md
mv WIKI_CODE_ALIGNMENT.md .github/project-planning/wiki-restructuring/inventory/code-alignment.md
```

### Phase 4: Migrate Documentation Planning (2 minutes)

```bash
mv DOCUMENTATION_AUDIT_STATUS.md .github/project-planning/documentation/audit-status.md
mv COLLAB_DOC_REFACTORING_PLAN.md .github/project-planning/documentation/refactoring-plan.md
```

### Phase 5: Create Documentation (10 minutes)

Create the README and TRACKING files with proper content.

### Phase 6: Commit Changes (2 minutes)

```bash
git add .github/
git commit -m "refactor: reorganize issue analysis and planning documents

- Create structured .github/ directory for project organization
- Move issue analysis files to .github/issue-analysis/{resolved,open,archived}
- Move wiki planning to .github/project-planning/wiki-restructuring/
- Move documentation planning to .github/project-planning/documentation/
- Add TRACKING.md for master issue status
- Add README.md for directory usage guide

This improves project organization and makes it easier to:
- Track issue resolution status
- Find relevant analysis documents
- Navigate project history
- Maintain a clean root directory"
```

---

## Benefits

### For Issue Tracking
✅ **Clear status** - At-a-glance view of resolved/open/archived
✅ **Easy navigation** - Issues organized by number
✅ **Consistent structure** - Every issue has analysis, summary, implementation
✅ **Historical record** - Can see evolution of solutions
✅ **Searchability** - Easier to grep/search

### For Project Maintenance
✅ **Clean root directory** - Only essential files (README, LICENSE, etc.)
✅ **Professional appearance** - Organized structure
✅ **Scalability** - Can handle hundreds of issues
✅ **Documentation** - Clear guide on how to use the system
✅ **Automation-ready** - Can add scripts to generate TRACKING.md

### For Collaboration
✅ **Onboarding** - New contributors can understand project history
✅ **Transparency** - Clear record of what's been addressed
✅ **Discoverability** - Easy to find relevant analysis
✅ **Consistency** - Template ensures quality

---

## TEMPLATE.md Structure

Provide a template for consistent issue analysis:

```markdown
# Issue #XXXX: [Title]

**Reporter**: [username]
**Date**: YYYY-MM-DD
**Status**: Open/Resolved/Archived
**Upstream**: [URL]
**Related Issues**: #XXX, #YYY

---

## Summary

[One paragraph executive summary]

## Problem Description

[Detailed description of the issue]

## Technical Analysis

[Root cause analysis, code investigation]

## Proposed Solution

[Your proposed fix/resolution]

## Implementation

[What was actually implemented, if resolved]

## Testing

[How to test/verify the fix]

## Related Work

[Links to commits, PRs, related issues]

---

**Analysis Date**: YYYY-MM-DD
**Analyst**: [Your name or "Claude"]
**Resolution Date**: YYYY-MM-DD (if resolved)
```

---

## Automation Opportunities

### 1. Generate TRACKING.md

Create a script to auto-generate TRACKING.md from directory structure:

```bash
#!/usr/bin/env bash
# .github/scripts/generate-tracking.sh

# Scan directories and generate TRACKING.md
# Parse metadata from analysis.md files
# Output formatted table
```

### 2. Issue Analysis Workflow

Create a GitHub Action to:
- Detect new issue analysis files
- Validate structure (has analysis.md, summary.md)
- Update TRACKING.md automatically
- Create PR summary

### 3. Link Checker

Validate that:
- All issue numbers in TRACKING.md have directories
- All directories have required files
- Links between documents are valid

---

## Naming Conventions

### Directory Names
- Format: `NNNN-short-slug` (e.g., `1163-nix-flake`)
- Use issue number as prefix
- Use kebab-case for slug
- Keep slug short (2-4 words)

### File Names
- Standard files: `analysis.md`, `summary.md`, `implementation.md`, `resolution.md`
- Lowercase, no prefixes
- Consistent across all issues

### Status Categories
- `resolved/` - Fixed and merged (✅)
- `open/` - Currently working on (🔄)
- `archived/` - Won't fix / not actionable (📦)

---

## Maintenance Guidelines

### Adding New Issue Analysis
1. Create directory in `open/`: `.github/issue-analysis/open/NNNN-slug/`
2. Copy TEMPLATE.md to `analysis.md`
3. Fill in analysis
4. Update TRACKING.md
5. Commit with message: `docs: add analysis for issue #NNNN`

### Resolving an Issue
1. Move from `open/` to `resolved/`
2. Add `resolution.md` or update `summary.md` with resolution
3. Update TRACKING.md status to ✅
4. Add commit SHA and PR number
5. Commit with message: `docs: mark issue #NNNN as resolved`

### Archiving an Issue
1. Move from `open/` to `archived/`
2. Update `summary.md` with reason for archiving
3. Update TRACKING.md status to 📦
4. Commit with message: `docs: archive issue #NNNN - [reason]`

---

## Alternative: Keep Analysis in PR Descriptions

**Consideration**: Some projects keep issue analysis in PR descriptions rather than separate files.

**Pros**:
- ✅ Analysis tied directly to PR
- ✅ No separate files to maintain
- ✅ GitHub issue/PR is source of truth

**Cons**:
- ❌ Analysis lost if PR closed/deleted
- ❌ Hard to find without PR number
- ❌ No place for analysis if not implementing
- ❌ Can't track "investigated but not fixed" issues

**Verdict**: Keep analysis files, but **link them in PR descriptions**.

---

## Rollout Plan

### Immediate (This Session)
1. ✅ Create proposal document (this file)
2. 🔄 Get approval from user
3. ⏳ Execute migration if approved

### Short Term (Next Session)
1. Create automation scripts
2. Add to documentation
3. Update contributing guidelines

### Long Term
1. GitHub Action for validation
2. Auto-generated TRACKING.md
3. Issue template integration

---

## Questions to Consider

1. **Should wiki planning be separate or integrated with issue analysis?**
   - Current proposal: Separate in `project-planning/`
   - Alternative: Wiki planning in `docs/wiki-planning/`

2. **How to handle multi-issue work?**
   - Example: Wiki restructuring addresses multiple issues
   - Proposal: Create a "project" directory with cross-references

3. **Should resolved issues stay forever or be archived?**
   - Proposal: Keep in `resolved/` indefinitely
   - Alternative: Archive to separate repo after 1 year

4. **Version control for TRACKING.md?**
   - Manual updates
   - Script-generated
   - Both (script + manual edits)

---

## Recommendation

**Proceed with migration** using the recommended hybrid structure:
- ✅ Clean root directory (only README, LICENSE, core files)
- ✅ Organized `.github/` structure
- ✅ Clear status tracking
- ✅ Consistent naming
- ✅ Scalable approach

**Estimated Time**: 30-40 minutes for complete migration

**Immediate Benefit**: Clean project structure, easier navigation

**Long Term Benefit**: Sustainable issue tracking, easier collaboration

---

## Next Steps

1. **Review this proposal** - Does this structure work for you?
2. **Approve or modify** - Any changes to the structure?
3. **Execute migration** - Move files to new structure
4. **Create documentation** - README.md and TRACKING.md
5. **Commit changes** - Clean commit with clear message

---

**What would you like to do?**
- A) Proceed with this structure as-is
- B) Modify the structure (specify changes)
- C) Consider alternative approaches
- D) Discuss further before deciding
