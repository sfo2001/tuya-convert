# Refactoring Analysis - tuya-convert Python Code

## Current Behavior Documentation

### 1. Encryption/Decryption Functions

**Location**: Duplicated in 4 files
- `scripts/mq_pub_15.py`
- `scripts/fake-registration-server.py`
- `scripts/tuya-discovery.py`
- `scripts/smartconfig/multicast.py`

**Implementation**:
- **Padding**: PKCS#7 padding to 16-byte blocks
- **Encryption**: AES-ECB mode (no IV)
- **Key**: Various keys used (16 bytes)
- **Input**: String (converted to bytes)
- **Output**: Bytes (encrypted) or String (decrypted)

**Critical**: Must maintain exact byte-for-byte compatibility

### 2. CRC Functions

**Location**: `scripts/smartconfig/crc.py`

**Functions**:
- `crc_8_byte(b)`: 8-bit CRC on single byte
- `crc_8(a)`: 8-bit CRC on byte array
- `crc_32(a)`: 32-bit CRC on byte array (with lookup table)

**Critical**: Must produce identical checksums

### 3. Smartconfig Encoding

**Location**: `scripts/smartconfig/`

**broadcast.py**:
- `encode_broadcast_body(password, ssid, token_group)`: Encodes data for UDP broadcast
- Uses CRC-8 checksums
- Specific bit manipulation and sequencing

**multicast.py**:
- `encode_multicast_body(password, ssid, token_group)`: Encodes data for multicast
- Uses CRC-32 checksums
- Password is AES encrypted, SSID and token_group are plaintext
- Encodes to IP addresses in format "226.X.Y.Z"

**Critical**: Must produce identical packet sequences

### 4. Protocol-Specific Functions

**mq_pub_15.py**:
- `iot_enc(message, local_key, protocol)`: Protocol-specific encoding (2.1 vs 2.2)
- `iot_dec(message, local_key)`: Protocol-specific decoding

**fake-registration-server.py**:
- JSON response formatting with optional encryption
- MD5 signatures for protocol 2.2
- HMAC signatures for firmware files

## Test Strategy

### Phase 1: Crypto Tests (Critical Path)
1. Test padding/unpadding with various input lengths
2. Test encryption/decryption round-trip
3. Test with known test vectors
4. Test edge cases (empty strings, unicode, etc.)

### Phase 2: CRC Tests
1. Test CRC-8 with known inputs
2. Test CRC-32 with known inputs
3. Verify against existing smartconfig output

### Phase 3: Integration Tests
1. Test smartconfig encoding produces identical output
2. Test protocol encoding/decoding
3. Test JSON handler responses

### Phase 4: Refactoring
1. Extract crypto functions to `scripts/crypto_utils.py`
2. Update imports in all files
3. Run tests after each file update
4. Apply type hints
5. Fix linting issues

## Development Tools Setup

```bash
# Testing
pip install pytest pytest-cov

# Formatting
pip install black isort

# Linting
pip install flake8 flake8-docstrings mypy

# Code quality
pip install pylint bandit  # security linting
```

## Formatting Configuration

**pyproject.toml**:
```toml
[tool.black]
line-length = 100
target-version = ['py38']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

## Success Criteria

- [ ] All tests pass before refactoring
- [ ] All tests pass after refactoring
- [ ] Byte-for-byte identical output for crypto operations
- [ ] No functional changes to protocol handling
- [ ] All files pass flake8
- [ ] All files pass mypy (with type hints)
- [ ] All files formatted with black
- [ ] 100% test coverage on refactored modules
