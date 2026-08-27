---
title: 0.33.0 - rev 3.x images for the NANO and the Guition
description: The same board can arrive with either family of chip, and the wrong image simply refuses to flash. Both boards now publish both.
tags: hardware, update
date: 2026-08-24
image:
---

![The Waveshare ESP32-P4-NANO. The same product code ships with either family of ESP32-P4 silicon, and the boot log is the only way to tell.](/assets/blog/0-33-0-rev3-images-for-two-more-boards/board-nano.webp)

A NANO bought in August came up as chip revision v3.1, and the flashing tool
refused every release we had. The board was fine. The image was built for the
other silicon family, and the two fence each other off on purpose.

Both boards now build and publish a `-rev3` image beside the plain one, each with
its own update address, so a device is never offered the other family's build.
The browser flasher offers the choice, and
[docs/FLASHING.md](https://github.com/espkvm/espkvm/blob/main/docs/FLASHING.md)
says how to ask a board which chip it has.

![The Guition ESP32-P4-M3-Dev, the other board that now publishes both images. Its 4.3-inch display is not used by the KVM; what matters here is the Ethernet, the ESP32-C6 and which chip revision is under them.](/assets/blog/0-33-0-rev3-images-for-two-more-boards/board-guition.webp)

Reported by [@levrskn](https://github.com/levrskn) in
[#24](https://github.com/orgs/espkvm/issues/24).

[Release v.0.33.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.33.0)
