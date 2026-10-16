---
title: Is my ESP32-P4 board supported?
description: One page with every ESP32-P4 board I have looked at for ESP-KVM - which run it, which might, and which cannot, with the reason for each.
tags: hardware
date: 2026-10-16 18:00
image: /assets/blog/is-my-board-supported/hero.webp
image_link: /boards/all/
image_alt: Part of the table on /boards/all/ - supported boards, candidates, maybes and two Olimex boards that cannot work, with a column per need.
---

A question I get a lot: "I have this P4 board, will ESP-KVM run on it?" The answer used to be spread over the catalog, a table in the porting guide and old issue threads. Now it is [one page](/boards/all/): 37 boards, each with a verdict.

A board needs four things, and the table has a column for each:

- 32 MB of PSRAM. Capture, the encoder and TLS do not fit in 16.
- A camera connector the capture board's Raspberry Pi ribbon fits. A connector alone is not enough: some boards have their own camera on it, some use a pinout nobody has published.
- The P4's high-speed USB on a connector it can drive as a device. That port is the keyboard and mouse the target sees.
- A network: Ethernet, or an ESP32-C6, C5 or C61 for Wi-Fi.

Green means the board has it, orange means it does not, no colour means nobody knows yet.

Some of the "no" ones look perfect on paper. The Olimex ESP32-P4-PC has the memory, the Ethernet and a Pi camera connector, and then a USB hub on the high-speed port, so it can only ever be a host. The LILYGO T-Halow P4 has 8 MB of PSRAM and brings USB out only on an M.2 edge.

The most promising new one is the Wireless-Tag WT32P4C5-43S, out this month: everything is there on its published schematic, except which pins drive the camera's I2C. If you have one, the page has a button to tell me how it went.

There is a second table at the bottom for [ESP-KVM terminal](/terminal/): boards with a screen that could show a KVM's picture. Today that is the Tab5; the Function EV with its 7" screen is the next candidate.

If your board is not on the page, [open an issue](https://github.com/espkvm/espkvm/issues/new) with a link to its schematic and I will add it.
