Flashing system trobleshooting

# Traced requirements

* The ssl packages is needed to be at least like in Ubuntu 18.04 (bionic).

# Failed attempts

## Ubuntu 12.04 LTS (architecture: i386)

### Problem

No `python3-pip` and `python3-wheel` packages (and it is only tip of the iceberg)

By the way it reached the End Of Life.

### Solution

Use modern distros.

## Ubuntu 14.04 LTS (architecture: i386)

### Problem

No `python3-wheel` package (and it is only tip of the iceberg)

By the way it reached the End Of Life.

### Solution

Use modern distros.

## Ubuntu 16.04 LTS (architecture: i386)

### Specification

* Ubuntu 16.04 LTS (architecture: i386)
* Packages(APT) from `install_prereq.sh`:
```
git=1:1.2.7.4-0ubuntu1.10
iw=3.17-1
dnsmasq=2.75-1ubuntu0.16.04.10
rfkill=0.5-1ubuntu3.1
hostapd=1:2.4-0ubuntu6.8
screen=4.3.1-2ubuntu0.1
curl=7.47.0-1ubuntu2.19
build-essential=12.1ubuntu2
python3-pip=8.1.1-2ubuntu0.6
python3-setuptools=20.7.0-1
python3-wheel=0.29.0-1
python3-dev=3.5.1-3
mosquitto=1.4.8-1ubuntu0.16.04.7
haveged=1.9.1-3
net-tools=1.60-26ubuntu1
libssl-dev=1.0.2g-1ubuntu4.19
```
* Important packages(APT) not mentioned in `install_prereq.sh`:
```
openssl=1.0.2g-1ubuntu4.14
python3=3.5.1-3
```
* PIP packages:
```
paho-mqtt==1.5.1
tornado==6.1
pycryptodomex==3.10.1
```
* Additional details:
    * VirtualBox on the laptop with Windows 10

### Problem

No `smarthack-*.log` files and
```
SmartConfig complete.
Resending SmartConfig Packets
..................
*Many times*
SmartConfig complete.
Resending SmartConfig Packets
........
Timed out while waiting for the device to (re)connect
```

Also in `screen0.log` the following message can be found:
`could not establish sslpsk socket: ('No cipher can be selected.',)`

See the issue [#942](https://github.com/ct-Open-Source/tuya-convert/issues/942) for details

By the way it reaches the End Of Life on April 30, 2021.

### Solution

As for the `smarthack-*.log` files absence see the pull request [#943](https://github.com/ct-Open-Source/tuya-convert/pull/943).

Moving to Ubuntu MATE 18.04 (i386) solved the problem with the ssl cipher.

But also you can add the following lines into the `/etc/apt/source.list` (backup it first!); they adds the repositories (for example witn later `openssl`) from the `security` section of the Ubuntu 18.04:
```
deb http://security.ubuntu.com/ubuntu bionic-security main restricted
# deb-src http://security.ubuntu.com/ubuntu bionic-security main restricted
deb http://security.ubuntu.com/ubuntu bionic-security universe
# deb-src http://security.ubuntu.com/ubuntu bionic-security universe
deb http://security.ubuntu.com/ubuntu bionic-security multiverse
# deb-src http://security.ubuntu.com/ubuntu bionic-security multiverse
```

But it is not enough to update only to the following version; something more needs updating:
```
libssl-dev=1.1.1-1ubuntu2.1~18.04.9
openssl=1.1.1-1ubuntu2.1~18.04.9
```

TODO: Find the exact package(s) needs updating