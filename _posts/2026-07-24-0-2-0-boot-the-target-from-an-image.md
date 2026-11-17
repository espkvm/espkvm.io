---
title: 0.2.0 - boot the target from an image on a card
description: A disk image on the microSD card is handed to the target as a USB drive it can boot from - a rescue system, an installer, a live image.
tags: media, storage
date: 2026-07-24
image:
---

To fix a broken machine you need something to boot from, which until now meant
walking over with a USB stick.

Put disk images on the device's microSD card, pick one in the new Media tab, and
the target sees a USB drive with that image in it. It boots from that the same
way it would from a stick you plugged in yourself.

Two things to know in this version:

- ~~the card is served read-only, because this board cannot write a microSD reliably, so you prepare images in a card reader;~~ since [0.49.0](/blog/0-49-0-microsd-at-full-speed/) the card is writable and images upload from the console;
- ~~the card must be FAT32, and one image can be at most 4 GB, that limit is FAT32's, not ours.~~ exFAT cards work since [0.54.0](/blog/0-54-0-exfat-cards-and-a-picture-sent-once/), and images over 4 GB since [0.55.0](/blog/0-55-0-a-real-dvd-drive-and-images-over-4-gb/).

Reads run at ~~4 MHz, about 1.5 MB/s~~ 40 MHz, about 9 MB/s, since [0.49.0](/blog/0-49-0-microsd-at-full-speed/). A heavy graphical image takes minutes to
boot, a small rescue image about a minute. Higher clock rates fail on this
chip.

[Release v.0.2.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.2.0)
