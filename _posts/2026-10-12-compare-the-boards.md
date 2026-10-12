---
title: Compare the boards side by side
description: A new page puts the ESP32-P4 boards ESP-KVM runs on in one table - chip, memory, network, capture, the port to the target and the measured frame rate - with the best of the chosen boards marked.
tags: boards, hardware
date: 2026-10-12 21:30
image: /assets/blog/compare-boards/hero.webp
---

ESP-KVM runs on fifteen ESP32-P4 boards now, ten of them tried on real hardware. Each board has its own page, but to choose between them you had to open several and keep the numbers in your head.

[Compare boards](/boards/compare/) puts them in one table:

- the chip revision, PSRAM, flash and the size of the board;
- Ethernet, PoE and Wi-Fi;
- which HDMI-to-CSI adapter fits and the camera connector it plugs into;
- the port to the target, microSD, HDMI-CEC and HDMI audio;
- the frame rate I measured, where I have one.

Pick the boards you are choosing between; the others are hidden. Green marks the best value in a row among the boards shown. "Only the rows that differ" hides what they all share.

The page address keeps the choice, so a link like [this one](/boards/compare/?b=p4-eth,funcev,p4-poe,m5-poe-p4) opens the same four boards for someone else.

"Untested" means I built the image from the vendor's schematic and nobody has run it yet. On those boards' pages there is now a link that opens a prefilled post in Discussions: if you have one, a few lines about what worked is enough to move it to tested.
