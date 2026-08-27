---
title: 0.4.0 - Wake-on-LAN and a fixed address
description: Power a sleeping machine on without any wiring, and give the KVM a static IP that a typo cannot turn into a brick.
tags: power, network
date: 2026-07-25
image:
---

Two small things.

**Wake-on-LAN.** If the target keeps standby power and has WoL switched on, the
Power panel can now wake it with a magic packet. Put the target's MAC address in
Settings and press Wake. No optocouplers, no wiring, nothing to solder.

**Static addressing that works.** The Network tab has had address fields for a
while; now they actually take effect. DHCP stays the default. Two safety nets
come with it: an address that does not parse falls back to DHCP at boot, and
the board's button now reverts the device to DHCP as well as clearing the
password. So a wrong-but-valid address is recoverable by holding the
button, like a forgotten password.

[Release v.0.4.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.4.0)
