---
title: 0.26.0 - one cable in a rack, and images for the other chip
description: A build for the PoE board, so a KVM in a rack needs one cable, plus images for rev 3.x silicon beside the existing ones.
tags: hardware
date: 2026-08-19
image: /assets/blog/0-26-0-poe-and-the-other-silicon/board-poe.webp
---

**PoE.** The Waveshare ESP32-P4-WIFI6-POE-ETH is the first supported board that
takes power over Ethernet, which means a KVM in a rack needs one cable instead
of two. Its Ethernet, microSD, WiFi co-processor and button turned out to sit on
the same pins as the boards already supported, so most of the description was
inherited. It is configured from the published schematic and has not been run on
one yet - the same footing the NANO and Guition targets started from.

**Two families of chip, two images.** The ESP32-P4 exists as pre-3.0 and rev 3.x
silicon, and neither will start on the other's image, because the header carries
both a minimum and a maximum revision. A product code does not tell you which
chip is in the box. So both are published: `p4-eth` and `p4-eth-rev3`, `p4-poe`
and `p4-poe-rev3`. Check the boot log, which prints `Chip rev:`. On rev 3.x you
also get the faster capture path and a writable microSD card.

The round LCD's pins now default per board, instead of five numbers
that were right for one of them. The NANO's values come from
[@DaveDavenport](https://github.com/DaveDavenport), who worked out what that
board can spare. A device already set up keeps its own values.

[Release v.0.26.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.26.0)
