---
title: M5Stack Unit PoE-P4
family: M5Stack
kind: device
status: tested
order: 70
role: The smallest complete one
summary: A matchbox with PoE and M5Stack's own HDMI capture. Power, network and video on two cables.
flasher: m5-poe-p4
capture: m5-addon-display-in
spec.Chip: ESP32-P4, rev 1.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet, 802.3at PoE
spec.Capture: M5Stack Add-on Display In (LT6911D), 24-pin flat cable
spec.microSD: on the capture module
spec.Measured: 720p: MJPEG 21-23 fps, H.264 17 fps
link.M5Stack documentation: https://docs.m5stack.com/en/unit/Unit_PoE-P4
photo: board.webp
photo_style: product
---

The odd one out: its capture is not a C790 on a camera ribbon but M5Stack's own
[Add-on Display In](/boards/m5-addon-display-in/), which plugs onto a 24-pin flat
cable and brings a microSD slot with it. The same IP101 Ethernet on the same pins
as the P4-ETH, and 802.3at PoE.

## Measured

One viewer, a screen playing video, 2026-09-23:

| Codec | Mode | fps | Bitrate |
|---|---|---|---|
| MJPEG | 1080p | 9 | 17-18 Mbit/s |
| MJPEG | 720p | 21-23 | 21-23 Mbit/s |
| H.264 | 1080p | 6 | 0.5-1.2 Mbit/s |
| H.264 | 720p | 17 | 1-1.8 Mbit/s |

**720p is the mode to give this board.** The byte reordering its bridge needs
costs four times less there, and over a network H.264 at 720p gives 17 fps at a
fifteenth of MJPEG's bandwidth. Pick 720p in the target's own display settings:
the bridge holds its own EDID, so ESP-KVM cannot offer fewer modes. The console
suggests 720p, or MJPEG, when it sees H.264 above 720p on this board.

If it has to be 1080p, give it **30 Hz, not 60**. The bridge writes every frame
it receives into memory, whether or not it gets encoded, and at 60 Hz that alone
takes most of the memory's bandwidth. Measured 2026-10-08: H.264 at 1080p went
from 5-6 fps at 60 Hz to 8 fps at 30 Hz.

## Good to know

- The picture comes out a little flat: the PC sends limited-range RGB to what it thinks is a TV. Setting the graphics driver's HDMI output range to **Full** fixes half of it; the other half is the bridge's own conversion.
- The microSD slot on the add-on writes at 40 MHz, so recording, screenshots and the dashcam all work.
- The bridge cannot tell whether the source is switched on, so after a long "No signal" the console offers a Reconnect HDMI button with a countdown.

The rev 3.x version, the [PoE-P4X](/boards/m5-poe-p4x/), takes the same
firmware from an image of its own.
