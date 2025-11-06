# Issue Analysis Directory

This directory contains analysis and documentation for upstream issues from [ct-Open-Source/tuya-convert](https://github.com/ct-Open-Source/tuya-convert).

## Directory Structure

```
issue-analysis/
├── README.md           # This file
├── TRACKING.md         # Master status tracker
├── TEMPLATE.md         # Template for new issue analysis
│
├── resolved/           # ✅ Fixed and merged issues
│   ├── 1143-pep668-compliance/
│   ├── 1167-venv-sudo-screen/
│   └── ...
│
├── open/               # 🔄 Currently in progress
│   ├── 1163-nix-flake/
│   └── ...
│
└── archived/           # 📦 Not actionable / Won't fix
    ├── 1157-chip-incompatible/
    └── ...
```

## Status Categories

### ✅ Resolved (`resolved/`)
Issues that have been:
- Analyzed and understood
- Fixed with code changes
- Committed and merged (or ready for merge)
- Tested and validated

**Examples**: Bug fixes, feature implementations, documentation improvements

### 🔄 Open (`open/`)
Issues currently being worked on:
- Analysis in progress
- Implementation underway
- Testing/validation pending
- Awaiting approval/review

### 📦 Archived (`archived/`)
Issues that are not actionable:
- Hardware incompatibilities (not fixable in software)
- Duplicate issues (already resolved elsewhere)
- User errors (not actual bugs)
- Won't fix / Out of scope

## File Naming Conventions

### Directory Names
Format: `NNNN-short-description`

Examples:
- `1163-nix-flake/`
- `1167-venv-sudo-screen/`
- `1143-pep668-compliance/`

Rules:
- **NNNN**: 4-digit issue number from upstream
- **short-description**: 2-4 words in kebab-case
- Keep description concise and descriptive

### Standard Files

Each issue directory should contain:

**Required:**
- `analysis.md` - Technical analysis, root cause investigation

**Optional:**
- `summary.md` - Executive summary and quick reference
- `implementation.md` - Implementation details and code changes
- `resolution.md` - How the issue was resolved
- `testing.md` - Testing procedures and validation

## Adding a New Issue Analysis

### Step 1: Create Directory
```bash
mkdir -p .github/issue-analysis/open/NNNN-description/
```

### Step 2: Copy Template
```bash
cp .github/issue-analysis/TEMPLATE.md .github/issue-analysis/open/NNNN-description/analysis.md
```

### Step 3: Fill In Analysis
Edit `analysis.md` with your findings.

### Step 4: Update TRACKING.md
Add entry to `TRACKING.md` with:
- Issue number and title
- Status (🔍 Investigating)
- Location (path to directory)

### Step 5: Commit
```bash
git add .github/issue-analysis/open/NNNN-description/
git commit -m "docs: add analysis for issue #NNNN"
```

## Moving Issues Between States

### Marking as Resolved

When an issue is fixed:

```bash
# Move directory
git mv .github/issue-analysis/open/NNNN-description/ \
       .github/issue-analysis/resolved/NNNN-description/

# Update TRACKING.md
# - Change status to ✅ Resolved
# - Add commit SHA
# - Add PR number (if applicable)

# Commit
git commit -m "docs: mark issue #NNNN as resolved"
```

### Archiving an Issue

When an issue is not actionable:

```bash
# Move directory
git mv .github/issue-analysis/open/NNNN-description/ \
       .github/issue-analysis/archived/NNNN-description/

# Add explanation in summary.md or analysis.md

# Update TRACKING.md
# - Change status to 📦 Archived
# - Add reason

# Commit
git commit -m "docs: archive issue #NNNN - [reason]"
```

## Documentation Standards

### analysis.md Structure

```markdown
# Issue #XXXX: [Title]

**Reporter**: [username]
**Date**: YYYY-MM-DD
**Status**: Open/Resolved/Archived
**Upstream**: [URL to issue]

---

## Summary
[One paragraph executive summary]

## Problem Description
[Detailed description]

## Technical Analysis
[Root cause investigation]

## Proposed Solution
[Your recommended fix]

## Related Issues
[Links to related work]
```

### summary.md Structure

Quick reference document with:
- Key findings
- Resolution approach
- Testing notes
- Links to commits/PRs

### implementation.md Structure

Implementation-specific details:
- Files changed
- Code modifications
- Configuration changes
- Migration steps
- Rollback procedures

## Best Practices

### ✅ Do

- **Be thorough** - Document root causes, not just symptoms
- **Link everything** - Reference commits, PRs, related issues
- **Test before resolving** - Verify fixes work
- **Update TRACKING.md** - Keep status current
- **Use clear language** - Write for future maintainers
- **Include examples** - Show error messages, code snippets
- **Credit contributors** - Acknowledge original reporters

### ❌ Don't

- **Skip analysis** - Don't just implement without understanding
- **Leave incomplete** - Finish documentation before moving on
- **Forget TRACKING.md** - Always keep it updated
- **Mix issues** - One directory per issue
- **Remove history** - Archive rather than delete

## Searching and Navigation

### Find an Issue by Number

```bash
find .github/issue-analysis/ -name "NNNN-*"
```

### Find All Resolved Issues

```bash
ls .github/issue-analysis/resolved/
```

### Search Issue Content

```bash
grep -r "search term" .github/issue-analysis/
```

### View Issue Status

```bash
cat .github/issue-analysis/TRACKING.md
```

## Related Documentation

- [TRACKING.md](TRACKING.md) - Current status of all issues
- [TEMPLATE.md](TEMPLATE.md) - Template for new analyses
- [../project-planning/](../project-planning/) - Project planning documents
- [../../docs/](../../docs/) - User-facing documentation

## Maintenance

### Regular Tasks

**Weekly:**
- Review open issues for status updates
- Update TRACKING.md with progress
- Check for new upstream issues to analyze

**Monthly:**
- Archive resolved issues that are merged upstream
- Clean up duplicate or obsolete entries
- Verify links still work

**As Needed:**
- Add new issue analyses
- Move issues between states
- Update documentation standards

## Questions?

If you have questions about this system:
1. Read [TRACKING.md](TRACKING.md) for current issue status
2. Check [TEMPLATE.md](TEMPLATE.md) for analysis format
3. Review existing issue directories for examples
4. Open a discussion or issue for clarification

---

**Directory Created**: 2025-11-06
**Last Updated**: 2025-11-06
**Maintainer**: sfo2001
