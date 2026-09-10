---
title: 0.25.0 - the device keeps its own log
description: A log that survives a restart, so the boot that failed is still readable after the device has come back on something that works.
tags: diagnostics, display, update
date: 2026-08-18
image:
---

When a device misbehaves and reboots, the evidence goes with it. Catching it
meant having a serial cable plugged in before it happened, which nobody does.

The device keeps a log now, in a small ring in memory that a restart does not
clear. After a boot that failed you can come back on a working firmware and read
what the failed one said. Diagnostics, then "Download the log".

It holds no passwords or keys. It does name your network, your addresses and the
MAC, and the console says so where you download it. This is a file people paste
into issues.

**The update shows on the little screen** too: the percentage while the image
arrives, then verifying, then restarting, and what went wrong if something did.
The console has just given up its video connection for the duration, so whoever
is standing at the box has somewhere to look.

One more fix, and the second time this one bit. Adding an endpoint pushed the
web server's route table past its end, and the route that fell off was the
keyboard and mouse channel. Registering past the end used to fail silently; it
says so in the log now.

[Release v.0.25.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.25.0)
