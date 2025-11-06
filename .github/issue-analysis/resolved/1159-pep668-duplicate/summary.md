# Issue #1159 Summary: PEP 668 Error (Duplicate of #1143)

## Quick Facts

- **Issue**: #1159 - "error: This environment is externally managed"
- **Reporter**: ricardopretrazy
- **Date**: 2025-04-01
- **Status**: ✅ **RESOLVED** (Duplicate of #1143)
- **Resolution**: Virtual environment support (commit b8a8291, PR #9)

## Problem

`install_prereq.sh` failed on modern Linux (Debian 12+, Ubuntu 23.04+, etc.) with PEP 668 error:
```
error: externally-managed-environment
× This environment is externally managed
```

## Solution

Implemented Python virtual environment support instead of using `--break-system-packages` workaround:

```bash
# Now creates venv automatically
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Key Points

- **Duplicate**: Same issue as #1143, same error, same fix
- **Root Cause**: System-wide pip install violates PEP 668
- **Fix Type**: Proper solution (venv), not workaround
- **Affected Systems**: All modern Linux with PEP 668 (Debian 12+, Ubuntu 23.04+, Arch, Fedora 38+, Gentoo)

## Files Changed

- `install_prereq.sh` - Added `setupPythonVenv()` function
- `start_flash.sh` - Auto-activates venv
- `requirements.txt` - Dependencies (new)
- `activate_venv.sh` - Manual helper (new)
- `TESTING.md` - Test procedures (new)

## Related Issues

- **#1143** - Primary analysis for this issue (same root cause)
- **#1167** - Venv PATH in sudo screen (related fix)
- **#1153** - Python 3.12+ ssl compatibility (uses sslpsk3 in venv)
- **#1165** - Gentoo support (uses same venv approach)

## Testing

✅ Verified on PEP 668-compliant systems
✅ Virtual environment created and activated
✅ All packages install correctly
✅ Works in sudo screen sessions
✅ Python 3.12+ compatible

## Impact

**Before**: Installation failed on all modern Linux distributions
**After**: Installation works correctly using Python best practices

## References

- Full analysis: `analysis.md`
- Primary issue: `.github/issue-analysis/resolved/1143-pep668-compliance/analysis.md`
- PEP 668: https://peps.python.org/pep-0668/
- Upstream: https://github.com/ct-Open-Source/tuya-convert/issues/1159

---

**Status**: ✅ Fully resolved - duplicate of #1143
**Fix Commit**: b8a8291 (PR #9)
**Documentation**: 2025-11-06
