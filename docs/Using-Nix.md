# Using Nix with tuya-convert

This guide explains how to use the Nix package manager to set up a reproducible development environment for tuya-convert.

## Table of Contents

- [What is Nix?](#what-is-nix)
- [Why Use Nix?](#why-use-nix)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [What Happens Under the Hood](#what-happens-under-the-hood)
- [Flashing a Device](#flashing-a-device)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)
- [Updating Dependencies](#updating-dependencies)
- [Comparison with Other Methods](#comparison-with-other-methods)

---

## What is Nix?

**Nix** is a powerful package manager that enables:
- **Reproducible builds**: Exact same environment on every machine
- **Declarative configuration**: Define your environment in code
- **Isolated environments**: No pollution of system packages
- **Atomic upgrades**: Changes are safe and reversible

A **Nix flake** is a standardized way to package software with locked dependencies, ensuring everyone gets identical package versions.

---

## Why Use Nix?

### Benefits for tuya-convert Users

✅ **One-Command Setup**: `nix develop` installs everything
✅ **Cross-Distribution**: Works on any Linux distribution (even macOS)
✅ **No System Pollution**: Packages installed in isolated Nix store
✅ **Guaranteed Reproducibility**: Exact dependency versions locked
✅ **Easy Cleanup**: Exit the shell, environment is gone
✅ **Version Pinning**: Prevent "works on my machine" issues

### Comparison with Other Methods

| Feature | Nix Flake | Native Install | Docker |
|---------|-----------|----------------|--------|
| Setup Speed | ⚡ Fast (first time: moderate) | ⚡ Fast | 🐢 Slow (image build) |
| Reproducibility | ✅ Perfect | ⚠️ Version drift possible | ✅ Good |
| System Impact | ✅ None (isolated) | ⚠️ Modifies system | ✅ None (containerized) |
| Disk Usage | 📊 Moderate (~500MB) | 📊 Small (~100MB) | 📊 Large (~1GB+) |
| Iteration Speed | ⚡ Instant | ⚡ Instant | 🐢 Rebuild required |
| Learning Curve | 📚 Moderate | 📚 Low | 📚 Moderate |
| Cross-Distribution | ✅ Yes | ⚠️ Script-dependent | ✅ Yes |

---

## Prerequisites

### 1. Install Nix

**On Linux** (multi-user installation with systemd):
```bash
sh <(curl -L https://nixos.org/nix/install) --daemon
```

**On macOS**:
```bash
sh <(curl -L https://nixos.org/nix/install)
```

**On NixOS**: Already installed! ✅

### 2. Enable Flakes

Edit `~/.config/nix/nix.conf` (create if doesn't exist):
```
experimental-features = nix-command flakes
```

Or add to `/etc/nix/nix.conf` (system-wide):
```
experimental-features = nix-command flakes
```

**Restart Nix daemon** (Linux):
```bash
sudo systemctl restart nix-daemon
```

### 3. Verify Installation

```bash
nix --version
# Should show: nix (Nix) 2.18.0 or newer
```

---

## Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/ct-Open-Source/tuya-convert
cd tuya-convert
```

### Step 2: Enter the Development Environment

```bash
nix develop
```

**First time**: This will download and build all dependencies (~500MB). Subsequent runs are instant.

**You'll see**:
```
╔════════════════════════════════════════════════════════════════╗
║                    🔧 tuya-convert (Nix)                       ║
╚════════════════════════════════════════════════════════════════╝

✅ Development environment loaded successfully

📦 Installed dependencies:
   • Python 3.11.x with packages:
     - paho-mqtt
     - tornado
     - pycryptodomex
     - sslpsk3
   • System tools: git, iw, dnsmasq, hostapd, mosquitto, screen
   ...
```

### Step 3: Verify Installation

```bash
# Check Python version
python3 --version

# Verify sslpsk3 is available
python3 -c "import sslpsk3; print(f'sslpsk3 {sslpsk3.__version__}')"

# Check networking tools
which dnsmasq
which hostapd
```

### Step 4: Flash Your Device

```bash
./start_flash.sh
```

Follow the prompts to flash your device. See [Quick Start Guide](Quick-Start-Guide.md) for detailed flashing instructions.

### Step 5: Exit the Environment

```bash
exit
# Or press Ctrl+D
```

---

## What Happens Under the Hood

### Nix Development Shell

When you run `nix develop`, Nix:

1. **Reads `flake.nix`**: Parses the configuration file
2. **Resolves Dependencies**: Checks what needs to be installed
3. **Downloads Packages**: Fetches from Nix binary cache or builds from source
4. **Creates Shell**: Sets up environment with all dependencies in `$PATH`
5. **Runs Shell Hook**: Displays welcome message

### Dependency Isolation

Nix stores packages in `/nix/store/` with unique hashes:
```
/nix/store/abc123-python3-3.11.8/
/nix/store/def456-dnsmasq-2.89/
/nix/store/ghi789-hostapd-2.10/
```

Your system Python and packages are **not affected**. The Nix environment is completely isolated.

### Reproducibility

The `flake.lock` file (auto-generated) pins exact versions:
```json
{
  "nodes": {
    "nixpkgs": {
      "locked": {
        "lastModified": 1710889954,
        "narHash": "sha256-abc123...",
        "rev": "e8f5f3a..."
      }
    }
  }
}
```

This ensures **everyone gets identical package versions**, regardless of when they run `nix develop`.

---

## Flashing a Device

### Standard Process

```bash
# 1. Enter Nix environment
nix develop

# 2. Run the flash script
./start_flash.sh

# 3. Follow prompts:
#    - Press ENTER to start
#    - Connect phone to vtrust-flash WiFi
#    - Put device in pairing mode (LED blinking rapidly)
#    - Select firmware to flash

# 4. Wait for completion
#    Device will reboot with new firmware

# 5. Exit Nix environment
exit
```

### Important Notes

⚠️ **Root Access Required**: `start_flash.sh` uses `sudo` to:
- Stop NetworkManager
- Configure network interfaces
- Start access point
- Manage firewall

⚠️ **Network Disruption**: Your network will be temporarily unavailable during flashing.

⚠️ **Service Management**: `start_flash.sh` automatically:
- Stops NetworkManager and firewall
- Restarts them after flashing completes

---

## Troubleshooting

### Issue: "experimental-features" Error

**Error**:
```
error: experimental Nix feature 'nix-command' is disabled
```

**Solution**: Enable flakes in Nix configuration:
```bash
mkdir -p ~/.config/nix
echo "experimental-features = nix-command flakes" >> ~/.config/nix/nix.conf
```

### Issue: Hash Mismatch for sslpsk3

**Error**:
```
error: hash mismatch in fixed-output derivation '/nix/store/...-sslpsk3-1.0.0.tar.gz':
  specified: sha256-...
  got:       sha256-BFScu9wtJy6eILMDzsGgLBlao3iQslGH1nEgQXZsBV4=
```

**Solution**: The hash in `flake.nix` needs updating. Copy the "got:" hash and update line 44 in `flake.nix`:
```nix
hash = "sha256-BFScu9wtJy6eILMDzsGgLBlao3iQslGH1nEgQXZsBV4=";
```

### Issue: "permission denied" During Flashing

**Error**:
```
sudo: a password is required
```

**Solution**: Run `start_flash.sh` and enter your password when prompted. The script requires root access.

### Issue: Build Failures with Old nixpkgs

**Error**:
```
error: attribute 'pycryptodomex' missing
```

**Solution**: Update nixpkgs to a newer version:
```bash
nix flake update
nix develop
```

Or explicitly use a newer nixpkgs:
```bash
nix develop --override-input nixpkgs github:NixOS/nixpkgs/nixos-unstable
```

### Issue: Slow Downloads

**Problem**: First-time setup is slow.

**Solution**: Nix is downloading and building packages. This is normal for the first run. Subsequent `nix develop` commands are instant because packages are cached.

**Tip**: Use Nix binary caches to speed up downloads:
```bash
# Add to /etc/nix/nix.conf or ~/.config/nix/nix.conf
substituters = https://cache.nixos.org https://nix-community.cachix.org
trusted-public-keys = cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY= nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs=
```

### Issue: ModuleNotFoundError for sslpsk3

**Error**:
```python
ModuleNotFoundError: No module named 'sslpsk3'
```

**Solution**: Ensure you're inside the Nix shell:
```bash
# Check if in Nix environment
echo $TUYA_CONVERT_NIX
# Should output: 1

# If not, enter the environment:
nix develop
```

### Issue: Device Not Detected

**Problem**: Device doesn't connect during flashing.

**Solution**: This is not a Nix issue. See [Troubleshooting](Troubleshooting.md) for device-specific problems.

---

## Advanced Usage

### Running Without Entering Shell

Use `nix run` to execute directly:
```bash
nix run . # Runs ./start_flash.sh
```

### Using Specific nixpkgs Version

For stability, pin to a specific nixpkgs release:
```bash
# Use NixOS 24.05 (stable)
nix develop --override-input nixpkgs github:NixOS/nixpkgs/nixos-24.05

# Use NixOS 23.11
nix develop --override-input nixpkgs github:NixOS/nixpkgs/nixos-23.11
```

### Direnv Integration

For automatic environment activation when entering the directory:

1. Install direnv:
```bash
nix-env -iA nixpkgs.direnv
```

2. Create `.envrc`:
```bash
echo "use flake" > .envrc
direnv allow
```

3. Now `cd tuya-convert` automatically activates the environment! ✨

### Garbage Collection

Remove unused Nix packages to free disk space:
```bash
# Remove old generations
nix-collect-garbage

# Remove everything not currently in use (aggressive)
nix-collect-garbage -d

# Check what would be deleted (dry run)
nix-store --gc --print-dead
```

### Offline Usage

After first setup, Nix works offline:
```bash
# All packages are cached locally
nix develop --offline
```

---

## Updating Dependencies

### Update to Latest Packages

```bash
# Update flake.lock to latest nixpkgs
nix flake update

# Re-enter environment
nix develop
```

### Update Specific Input

```bash
# Update only nixpkgs
nix flake lock --update-input nixpkgs

# Update to specific commit
nix flake lock --override-input nixpkgs github:NixOS/nixpkgs/abc123def
```

### Check for Outdated Packages

```bash
# Show current package versions
nix develop --command python3 --version
nix develop --command dnsmasq --version

# Compare with latest in nixpkgs:
nix search nixpkgs python3
nix search nixpkgs dnsmasq
```

---

## Comparison with Other Methods

### When to Use Nix

✅ **Use Nix when**:
- You want guaranteed reproducibility
- You're developing/contributing to tuya-convert
- You use NixOS or already have Nix
- You need multiple isolated environments
- You want to avoid modifying system packages

### When to Use Native Install

✅ **Use `install_prereq.sh` when**:
- You're comfortable with system package management
- You only need to flash once or twice
- You prefer distribution-native packages
- You don't have Nix installed

### When to Use Docker

✅ **Use Docker when**:
- You need the highest level of isolation
- You're running in CI/CD
- You want a completely disposable environment
- Network complexity is not a concern

---

## Additional Resources

### Official Nix Documentation
- [Nix Manual](https://nixos.org/manual/nix/stable/)
- [Nix Flakes](https://nixos.wiki/wiki/Flakes)
- [NixOS Packages Search](https://search.nixos.org/)

### tuya-convert Documentation
- [Installation Guide](Installation.md)
- [Quick Start Guide](Quick-Start-Guide.md)
- [Troubleshooting](Troubleshooting.md)
- [Compatible Devices](Compatible-devices.md)

### Community Support
- [tuya-convert GitHub Issues](https://github.com/ct-Open-Source/tuya-convert/issues)
- [Nix Community](https://discourse.nixos.org/)

---

## Credits

This Nix flake was contributed by **SHU-red** in [issue #1163](https://github.com/ct-Open-Source/tuya-convert/issues/1163) with improvements by **seanaye** and **mberndt123**.

The flake has been adapted to use `sslpsk3` (Python 3.12+ compatible) instead of the original `sslpsk` package, aligning with the project's migration in [issue #1153](https://github.com/ct-Open-Source/tuya-convert/issues/1153).

---

## Contributing

Found an issue with the Nix flake? Want to improve it?

1. Check existing [issues](https://github.com/ct-Open-Source/tuya-convert/issues)
2. Open a new issue with:
   - Your Nix version (`nix --version`)
   - Your system (`uname -a`)
   - Error messages
   - Steps to reproduce
3. Submit a pull request with improvements

---

**Happy flashing! 🚀**
