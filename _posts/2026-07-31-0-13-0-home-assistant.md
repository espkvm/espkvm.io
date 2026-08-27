---
title: 0.13.0 - the KVM shows up in Home Assistant
description: Turn on MQTT and the device is discovered as one Home Assistant device, with sensors for what it sees and buttons for what it can press.
tags: home-assistant, security
date: 2026-07-31
image: /assets/blog/0-13-0-home-assistant/ha.webp
---

If you run Home Assistant, the KVM can now live there as an ordinary device. Turn
MQTT on in Settings, point it at your broker, and it is discovered
automatically - no YAML to write.

What you get:

- sensors for chip temperature, viewers, video mode, frame rate, codec, bitrate, uptime and free memory;
- sensors for whether HDMI has a signal, whether a USB target is attached, and whether the target has power;
- buttons for power, reset, force off, Wake-on-LAN and restarting the KVM itself;
- an availability topic, so the device shows as offline when it really is.

TLS is supported, either verified against the built-in certificate bundle or
skipped for a self-signed broker.

Off by default.


There is a security fix in the same release: while the default password is still
in force, a session can now reach nothing but the login endpoints. That rule
used to be enforced by the console alone, which is the wrong place for it.

[Release v.0.13.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.13.0)
