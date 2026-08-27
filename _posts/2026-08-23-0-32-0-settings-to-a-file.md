---
title: 0.32.0 - settings to a file, and back
description: Save the configuration before you change it, or bring a second device up like the first.
tags: console
date: 2026-08-23
image:
---

Two buttons at the foot of Settings: save to a file, load from a file. For the
two things people do - keep a copy of a working setup before restoring defaults,
and set a second device up like the first.

The file is plain JSON with the firmware version and the board in its header, so
you can read it and know what it came from.

Two things it deliberately does not carry:

- passwords and keys, because the device never serves them at all - they cannot be in a file it writes;
- the device's own identity. Hostname and static addresses stay as they are, because two devices answering to one name means two certificates and a browser that trusts neither.

Loading a file shows you what it would change before anything is written, and
tells you afterwards what it skipped, not a bare "done".

[Release v.0.32.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.32.0)
