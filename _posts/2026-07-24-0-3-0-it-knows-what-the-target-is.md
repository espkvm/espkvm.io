---
title: 0.3.0 - it knows what the target is running
description: The device guesses the target's operating system from how it plugs in, keeps a rescue image in its own flash, and stops undoing updates that were fine.
tags: input, media, update
date: 2026-07-24
image:
---

A keyboard is not the same on every machine. The Meta key is Win, Cmd or Super
depending on who is asking, and the useful key combinations differ too. So the
device now guesses what the target runs, from the way that machine enumerates
USB: Windows, macOS, Linux or Android. It shows you the guess and the raw
fingerprint it read. If the guess is wrong, there is a
setting to say so.

The console then follows that guess. It labels the Meta key properly, and
offers combinations that only make sense on that system. On Linux that is the
magic SysRq sequences REISUB and REISUO, which reboot or power off a hung
machine without losing the disks, and Ctrl+Alt+F1 to F6 for virtual terminals.

Also new: a rescue image inside the device. Something small and bootable, iPXE
or memtest or a DOS floppy, lives in a 4 MB flash partition and is served over
the same USB drive as the card. No microSD needed, and unlike the card it can be
written from the console.

One bug is gone as well. A network update could come up, work, and then be
rolled back at the next reset. The image is now confirmed the moment the device
can be reached and re-flashed, not after every last peripheral has started.

[Release v.0.3.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.3.0)
