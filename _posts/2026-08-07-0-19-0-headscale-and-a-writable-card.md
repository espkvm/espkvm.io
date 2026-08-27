---
title: 0.19.0 - your own control server, and a card you can write
description: Point the device's Tailscale client at your own Headscale, and on rev 3.x boards upload images to the microSD card from the console.
tags: vpn, storage
date: 2026-08-07
image:
---

Tailscale is convenient and it is somebody else's control server. If you run
your own - Headscale, or Ionscale - the device can now be pointed at it instead.
It is one field in the VPN settings: the control server URL, and a port if it
needs one. Everything else works the same.

Two smaller things in the same few days:

- on rev 3.x boards the microSD card is writable, so images can be uploaded and deleted from the console. The code was always there but switched off, because the older chip revision times out on SD writes. Rev 3.x handles it, verified on hardware. Pre-3.0 boards stay read-only.
- the target now sees the monitor as ESP-KVM, rather than under the capture chip's Toshiba name.

The NANO and Guition builds were also switched to pre-3.0 silicon by default,
because the units a contributor actually tested turned out to be pre-3.0 and the
previous images would not boot on them.

[Release v.0.19.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.19.0)
