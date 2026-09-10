---
title: 0.3.0 - it knows what the target is running
description: The device guesses the target's operating system from how it plugs in, keeps a rescue image in its own flash, and stops undoing updates that were fine.
tags: input, media, update
date: 2026-07-24
image:
---

A keyboard is not the same on every machine. The Meta key is Win, Cmd or Super
depending on the system, and the useful combinations differ too. The device now
guesses what the target runs from the way it enumerates USB: Windows, macOS,
Linux or Android. You get the guess and the raw fingerprint it read, and a
setting to correct it when it is wrong.

The console then follows that guess. It labels the Meta key properly, and
offers combinations that only make sense on that system. On Linux that is the
magic SysRq sequences REISUB and REISUO, which reboot or power off a hung
machine without losing the disks, and Ctrl+Alt+F1 to F6 for virtual terminals.

Also new: a rescue image inside the device. Something small and bootable - iPXE,
memtest, a DOS floppy - lives in a 4 MB flash partition and is served over the
same USB drive as the card. No microSD needed, and unlike the card you can write
it from the console.

One bug is gone as well. A network update could come up, work, and then be
rolled back at the next reset. The image is now confirmed the moment the device
can be reached and re-flashed, not after every last peripheral has started.

[Release v.0.3.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.3.0)
