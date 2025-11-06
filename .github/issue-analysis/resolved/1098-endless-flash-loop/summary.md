# Issue #1098: Endless Flash Loop - Quick Summary

**Status**: ✅ Resolved
**Resolution**: sslpsk3 migration (commit 59549b1, issue #1153)
**Reported**: 2023-07-16
**Resolved**: 2025-01-04

---

## TL;DR

**Problem**: Device connects successfully but flashing enters endless loop with `[SSL: NO_SHARED_CIPHER] no shared cipher` error.

**Root Cause**: Deprecated `sslpsk` library had limited SSL cipher support and Python version incompatibilities.

**Solution**: ✅ Migrated to `sslpsk3>=1.0.0` (already implemented in requirements.txt and psk-frontend.py).

**Impact**: Issue is resolved. Users with latest tuya-convert version will not experience this problem.

---

## Key Facts

- **Device**: YTE CZ001 Smart Plug (PSK Identity 02)
- **Error**: `[SSL: NO_SHARED_CIPHER] no shared cipher`
- **Symptom**: SmartConfig succeeds, but SSL/TLS-PSK handshake fails, device loops
- **Fix Commit**: 59549b1 (sslpsk3 migration)
- **Related Issues**: #1153 (Python 3.12+ AttributeError), #1162 (SmartConfig loop)

---

## Technical Details

**Before Fix** (broken):
```python
# requirements.txt
sslpsk  # deprecated, limited cipher support, Python 3.12 incompatible
```

**After Fix** (working):
```python
# requirements.txt
sslpsk3>=1.0.0  # modern, full cipher support, Python 3.12+ compatible
```

**Files Changed**:
- `requirements.txt` → `sslpsk3>=1.0.0`
- `scripts/psk-frontend.py` → `from sslpsk3 import SSLPSKContext`

---

## Verification

**How to confirm fix is applied:**

```bash
# Check requirements.txt
grep sslpsk3 requirements.txt
# Expected: sslpsk3>=1.0.0

# Verify installed package
pip show sslpsk3
# Expected: sslpsk3 version 1.0.0+
```

**Testing result:**
- ✅ No more `NO_SHARED_CIPHER` errors from devices
- ✅ Python 3.12+ compatibility confirmed
- ✅ PSK Identity 02 devices flash successfully

---

## User Action Required

**For users experiencing this issue:**

1. **Update tuya-convert** to latest version (post-January 2025)
2. **Reinstall dependencies**:
   ```bash
   # If using virtual environment (recommended)
   source venv/bin/activate
   pip install -r requirements.txt

   # Or reinstall prerequisites
   ./install_prereq.sh
   ```
3. **Retry flashing** - issue should be resolved

---

## Related Work

- **#1153**: Python 3.12+ AttributeError → Same fix (sslpsk3)
- **#1162**: SmartConfig loop on Kali 2025.1 → Likely same issue
- **#1143**: PEP 668 venv → Ensures sslpsk3 installs correctly
- **#1167**: Venv PATH in sudo → Ensures sslpsk3 is accessible

---

## Links

- **Full Analysis**: [analysis.md](./analysis.md)
- **Upstream Issue**: https://github.com/ct-Open-Source/tuya-convert/issues/1098
- **Fix Commit**: 59549b1
- **Related PR**: #10 (sslpsk3 migration)

---

**Analysis Date**: 2025-11-06
**Last Updated**: 2025-11-06
