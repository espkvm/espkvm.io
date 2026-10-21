---
title: The ESP32-P4 boards, rated for an IP-KVM
description: Every ESP32-P4 board ESP-KVM runs on now has a rating out of five for how well it suits an IP-KVM, and the board list is sorted by it, best first.
tags: boards, hardware
date: 2026-10-21 21:00
image: /assets/blog/the-boards-rated/hero.webp
---

The [board list](/boards/) had grown to fifteen ESP32-P4 boards, in the order I added them. To pick one you had to open the pages and work out yourself which of them is a good KVM and which only runs.

Now each board has a rating out of five, drawn as five small screens, and the list is sorted by it, best first.

The rating is ten points, read off the board's specs and rounded to the nearest half screen, so a new board gets one without me choosing a number.

| What | Points |
|---|---|
| Tested on hardware | 3 |
| A rev 3.x chip, for faster H.264 | 1.5 |
| Ethernet | 1.5 |
| PoE, on the board or with an add-on module | 1 |
| A plain USB cable to the target | 1 |
| Wi-Fi | 0.5 |
| microSD | 0.5 |
| A capture ribbon that fits as is | 0.5 |
| A small board: up to 20 cm² / up to 40 cm² | 0.5 / 0.25 |

Tested on hardware counts most: an untested image is built from the schematic alone, and first runs have turned up wrong pins more than once.

Many boards are sold with either chip revision, and the product code does not say which one arrives. Those are rated for the rev 3.x unit, and the board's page says in a coloured box what a rev 1.x unit scores. A board gets the chip point only when someone has seen it with rev 3.x; an image ready for it is not enough.

A plain USB cable means a USB-C port or a lead with nothing to do to it. A USB-A port that always carries 5 V needs an A-to-A cable with the 5 V wire cut, and a 4-pin header needs a lead you make yourself, so those boards lose that point. The capture point goes to the 15-pin Raspberry Pi connector the C790 plugs into; the 22-pin one needs a different cable. Wi-Fi weighs less than Ethernet: a KVM usually sits next to a switch. A small board fits behind a server or inside a case.

Before putting the numbers up I checked every board's page against the vendor's documents and schematics.

Not everyone needs PoE or a small board. Open "What counts in the rating" above the list and untick what does not matter to you: the screens and the order follow, here and on Compare boards, and the browser remembers the choice.

The screens are on the [board list](/boards/), on the front page and in the first row of [Compare boards](/boards/compare/). A board's own page lists every point it got and every one it did not.

The ESP32-P4-ETH, the board this project started on, gets three and a half: it is small and takes PoE with an add-on module, but it has no Wi-Fi, a USB lead on an MX1.25 connector, a 22-pin camera socket, and nobody has seen one with a rev 3.x chip yet. The Function EV gets four and a half: it has all of that, but no PoE, and at 88 by 74 mm it gets nothing for size.

If a rating looks wrong, the cause is usually a spec on the board's page. Leave a comment below and I will fix it.
