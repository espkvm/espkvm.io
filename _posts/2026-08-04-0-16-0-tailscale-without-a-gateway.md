---
title: 0.16.0 - Tailscale, right on the device
description: The KVM joins your tailnet by itself - no gateway, no VPS, no port forwarding - and the console installs to a phone's home screen.
tags: vpn, network, console, mobile
date: 2026-08-04
image:
---

WireGuard wants somewhere to connect to: a peer with a fixed address, or a port
opened on your router. The device now speaks Tailscale natively instead.

Set a Tailscale auth key in Settings and the device joins your tailnet. It is
then reachable at its 100.x address, or its MagicDNS name, from anywhere you are
signed in - NAT traversal handled for it, nothing forwarded, no gateway machine
in the middle. It is built on a native client ported to ESP-IDF 6, and it runs on
its own task, so joining never holds up boot.

The certificate follows: it is re-issued to name the tailnet address and the
MagicDNS name, so the console is trusted over Tailscale the same way it is on
the local network.

**The console is installable.** It ships a manifest, a service worker and icons,
so a phone can add it to the home screen and run it full screen. That also gets rid of the browser's own bars. Touch control became a
proper trackpad with acceleration at the same time.

The device's own certificate authority is now named after the device, so it is
recognisable in a phone's list of trusted credentials, instead of one more
identical entry.

[Release v.0.16.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.16.0)
