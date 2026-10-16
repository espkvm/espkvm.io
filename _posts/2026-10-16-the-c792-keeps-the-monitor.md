---
title: The Geekworm C792 - capture that keeps the monitor
description: The C792 is a TC358743 capture board with an HDMI pass-through, so the target keeps its own monitor while ESP-KVM watches the same picture. It is in the catalog now, with the one setting to watch.
tags: hardware
date: 2026-10-16 12:00
image: /boards/c792/board.webp
image_alt: The Geekworm C792 board, with HDMI in and out on one edge and the camera connector on the other.
---

The C790 takes the target's HDMI and keeps it. Fine for a server in a rack, less so for a desktop that someone also sits at. The [Geekworm C792](/boards/c792/) has a second HDMI port: a GSV2001 splitter sends the picture to the TC358743 and to the monitor at the same time.

Behind the splitter it is the same TC358743 as on the C790, so ESP-KVM drives it as it is. It takes both ribbons, the 15-pin and the 22-pin, and wants its own 5 V supply.

One thing works differently. With a monitor on the pass-through, the source reads the monitor's EDID instead of the one ESP-KVM writes, and a modern monitor asks for 1080p60. Two CSI lanes carry about 81 megapixels a second, and 1080p60 needs 124, so the picture stays dark and the console says the mode is too fast. Set the source to 1080p30 or 720p60 and it fits. Without a monitor, the source gets the EDID from ESP-KVM and picks a mode that fits by itself.

A 4K source is scaled down to 1080p by the splitter, at the same refresh rate: 4K30 works, 4K60 is too fast for the same reason.

[The C792 in the catalog](/boards/c792/)
