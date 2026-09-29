---
title: 0.56.0 - two dual-band boards, and the right image for every chip
description: The Function EV and the WIFI6 now come with an ESP32-C5 for 5 GHz Wi-Fi. Older Function EV units and newer ESP32-P4-Modules get the image their chip needs, and the flasher tells you how to read the chip.
tags: hardware, update
date: 2026-09-29 12:00
---

## Two boards with a C5

Espressif and Waveshare both made a version of a board ESP-KVM already runs on,
with a dual-band ESP32-C5 in place of the C6, so it can join a 5 GHz network:
the ESP32-P4X-C5-Function-EV-Board and the ESP32-P4-WIFI6-DB. In both the C5
sits on the pins the C6 used, so each image is the old board's with the
co-processor swapped. Neither has been run on hardware yet.

## The right image for the chip

The ESP32-P4 comes in two revisions, and an image for one does not start on the
other. Two boards had only one image, and the other chip was turning up:

- Function EV boards with a rev 1.x chip now have their own image. The one I brought up is rev 3.2, but board v1.4 and v1.5 are board versions, not chip revisions.
- Waveshare's shop lists the ESP32-P4-Module with the rev 3.x chip now, so the Module-DEV-KIT gets a rev 3.x image.

To tell which chip you have, read it. The part number ends in X on rev 3.x
(ESP32-P4NRW32X). To be exact, the second character of the manufacturing code on
the chip is the revision: E is 1.3, F, G and H are 3.0, 3.1 and 3.2. The flasher
says this above the revision buttons now.

## Also

- The WIFI6-DEV-KIT is confirmed on hardware by @brooklyn5w4g: a v1.2 board, rev 3.1, H.264 at about 23 fps. Its USB jumper labels changed between board versions; on v1.2 the target's port is HOST.
- The flasher installs any version from a file: pick a release's -merged.bin, and it checks the file before writing it.
- "Install any release" on the NANO-WIFI6-DB asked for a file the releases do not have. Fixed.

[Release notes on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.56.0)
