# Title:
Feature Request: Remove Unnecessary sudo Usage to Improve Security

# Labels:
enhancement, security, refactoring

# Body:

## Summary
Refactor tuya-convert to minimize or eliminate unnecessary `sudo` usage, particularly for Python scripts that don't require root privileges. This will improve security, simplify virtual environment integration, and follow the principle of least privilege.

## Motivation

Currently, `start_flash.sh` launches Python scripts using `sudo screen`, which creates several issues:

1. **Virtual Environment Problems**: `sudo` resets environment variables, breaking virtual environment activation (requires workarounds like the fix for #1167)
2. **Security Risk**: Running Python interpreters and scripts as root unnecessarily increases attack surface
3. **Permission Issues**: Log files and backups created with root ownership can cause access problems
4. **Complexity**: Requires workarounds like `env` to restore PATH for virtual environments

## Current State

Scripts launched with `sudo screen`:
- `fake-registration-server.py` (port 80)
- `psk-frontend.py` (port 8886)
- `tuya-discovery.py` (UDP broadcast)
- `mosquitto` (port 1883)

**Only the network configuration scripts truly need root** for:
- Creating virtual network interfaces
- Configuring hostapd access point
- Modifying network routes and iptables

## Proposed Solutions

### Option 1: Linux Capabilities (Recommended)
Use capabilities to allow binding privileged ports without full root:

```bash
# One-time setup during install_prereq.sh
sudo setcap CAP_NET_BIND_SERVICE=+ep $(which python3)
sudo setcap CAP_NET_BIND_SERVICE=+ep $(which mosquitto)
```

**Pros:**
- ✅ Fine-grained privilege control
- ✅ No sudo needed at runtime
- ✅ Virtual environments work naturally
- ✅ Better security posture

**Cons:**
- ⚠️ Requires setup during installation
- ⚠️ May need documentation for different distributions

### Option 2: Use High Ports + Port Forwarding
Change Python services to use unprivileged ports (>1024) and forward:

```bash
# Redirect privileged ports to high ports
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
```

**Pros:**
- ✅ No capabilities needed
- ✅ Services run as regular user
- ✅ More portable across systems

**Cons:**
- ⚠️ Requires iptables configuration
- ⚠️ More complex networking setup

### Option 3: systemd Socket Activation
Use systemd to bind privileged ports, pass sockets to userspace processes.

**Pros:**
- ✅ Modern, standard approach
- ✅ Excellent security model

**Cons:**
- ⚠️ Requires systemd (not available on all target platforms)
- ⚠️ Major architectural change

### Option 4: authbind
Use `authbind` to allow specific users to bind privileged ports:

```bash
sudo apt-get install authbind
sudo touch /etc/authbind/byport/80
sudo chmod 500 /etc/authbind/byport/80
sudo chown $USER /etc/authbind/byport/80

# Run scripts with authbind
authbind --deep python3 fake-registration-server.py
```

**Pros:**
- ✅ Simpler than capabilities
- ✅ Well-established tool

**Cons:**
- ⚠️ Additional dependency
- ⚠️ Less common on embedded systems

## Implementation Plan

1. **Phase 1: Investigation**
   - Audit which scripts actually need privileged operations
   - Test each proposed solution on target platforms (Raspberry Pi, Ubuntu, Debian)
   - Document compatibility matrix

2. **Phase 2: Refactoring**
   - Separate privilege-requiring operations into dedicated setup phase
   - Modify Python scripts to use unprivileged approach
   - Update `start_flash.sh` to run scripts without sudo

3. **Phase 3: Migration**
   - Update `install_prereq.sh` with chosen solution setup
   - Add capability checks and clear error messages
   - Update documentation with new security model

4. **Phase 4: Testing**
   - Test on all supported platforms
   - Verify virtual environment integration works seamlessly
   - Ensure no functionality regressions

## Benefits

- 🔒 **Better Security**: Principle of least privilege
- 🐍 **Cleaner Python**: Virtual environments work naturally
- 📝 **Better Logging**: Files owned by correct user
- 🧹 **Simpler Code**: Remove sudo workarounds
- 🎯 **Standards Compliance**: Modern Linux security practices

## References

- [Linux Capabilities Man Page](http://man7.org/linux/man-pages/man7/capabilities.7.html)
- [Python Virtual Environments and Sudo](https://stackoverflow.com/questions/59846065/using-sudo-with-python-virtual-environment)
- [Systemd Socket Activation](https://www.freedesktop.org/software/systemd/man/systemd.socket.html)

## Related Issues

- Upstream ct-Open-Source/tuya-convert#1167: Ubuntu non-docker deps issue (virtual environment broken by sudo)
- Upstream ct-Open-Source/tuya-convert#1159: Python environment error (PEP 668 compliance)

## Priority

**Medium-High**: This is not blocking users, but it improves security, maintainability, and resolves the root cause of virtual environment integration issues.
