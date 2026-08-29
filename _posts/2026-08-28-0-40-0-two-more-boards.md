---
title: 0.40.0 - two more boards, one with no wire at all
description: A dev kit that carries both links, and a board whose only way in is WiFi. The second one came from the person who owns it.
tags: hardware, network, input
date: 2026-08-28
image:
---

![The Waveshare ESP32-P4-WIFI6-DEV-KIT. Ethernet on a PoE-capable magjack and an ESP32-C6 for WiFi 6, on one board.](/assets/blog/0-40-0-two-more-boards/board-wifi6-devkit.webp)

The Waveshare ESP32-P4-WIFI6-DEV-KIT became a build target in 0.39.0. It carries
both links - 100M Ethernet on a PoE-capable magjack, and an ESP32-C6 for WiFi 6 -
and its pins are the ones already in use here, so the overlay declares almost
nothing. It is configured from the published schematic; nobody has run this
firmware on one yet. One thing to check before wiring: a jumper switches the USB
OTG port between HOST and DEVICE, and the KVM needs DEVICE.

Two boards in the same family were looked at and left out. The ESP32-P4-Pico and
the ESP32-P4-Core-DEV-KIT have neither Ethernet nor a WiFi co-processor, and a
KVM nobody can reach over the network is not much of a KVM.

![The Waveshare ESP32-P4-WIFI6. The PoE board without its wired half - WiFi is the only way in.](/assets/blog/0-40-0-two-more-boards/board-wifi6.webp)

0.40.0 added the Waveshare ESP32-P4-WIFI6, contributed by
[@nwomn](https://github.com/nwomn), who has one. It is the first supported board
with no wired port at all. Capture through the C790 and the USB keyboard and
mouse are confirmed on hardware, and the pin reservations were checked against
the real thing rather than read off a drawing. Its WiFi did not hold at first;
what was wrong with it is the next post.

His as well: a drag now keeps its path. Pointer reports were merged into the
latest position, which is right while no button is down and wrong while one is -
a drag reached the target as a press and a release with nothing in between, so
drawing and drag-and-drop lost everything in the middle.

[Release v.0.40.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.40.0)
