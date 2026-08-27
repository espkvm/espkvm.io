---
title: 0.20.0 - virtual media grows up
description: An ISO is offered as a CD-ROM and everything else as a disk, and the whole microSD card can be handed to the target at once.
tags: media, storage
date: 2026-08-10
image:
---

Virtual media has handed the target an image since 0.2.0. Two things people
kept running into.

**The right kind of drive, chosen for you.** Installers expect an optical drive,
and a lot of them refuse to boot from anything else. So an `.iso` is now
presented as a CD-ROM and anything else as a removable disk, with nothing to
set. You can still force either one if a file is misnamed, and switching between
them re-plugs the USB drive for you.

**The whole card, not one file.** A new item in the Media panel hands the target
the entire microSD card as a USB drive - every file on it, not a single image.
On rev 3.x boards it is read-write, so the target can copy files onto it, which
makes the KVM a way to get data off a machine with no network. While the card is
handed over the console steps off it, so there is only ever one owner, and it
re-reads the card when you take it back. If the target reformatted it, that is
fine.

Uploads now show throughput and an estimate, so a slow multi-gigabyte write
visibly moves instead of looking stuck.

[Release v.0.20.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.20.0)
