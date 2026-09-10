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
while and they did nothing. They take effect now, with DHCP still the default.
Two ways back if you get it wrong: an address that does not parse falls back to
DHCP at boot, and the board's button reverts to DHCP as well as clearing the
password. A wrong but valid address is a button hold away from fixed.

[Release v.0.4.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.4.0)
