---
title: 0.2.0 - boot the target from an image on a card
description: A disk image on the microSD card is handed to the target as a USB drive it can boot from - a rescue system, an installer, a live image.
tags: media, storage
date: 2026-07-24
image:
---

To fix a broken machine you need something to boot from, and that has meant
walking to it with a USB stick.

Put disk images on the device's microSD card, pick one in the new Media tab, and
the target sees a USB drive with that image in it. It boots from it like it
would from a stick you plugged in yourself.

Two things to know in this version:

- the card is served read-only, because this board cannot write a microSD reliably, so you prepare images in a card reader;
- the card must be FAT32, and one image can be at most 4 GB, that limit is FAT32's, not ours.

Reads run at 4 MHz, about 1.5 MB/s. A heavy graphical image takes minutes to
boot; a small rescue image takes about a minute. Higher clock rates fail on
this chip.

[Release v.0.2.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.2.0)
