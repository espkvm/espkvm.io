---
title: M5Stack Unit PoE-P4X
family: M5Stack
kind: device
status: untested
order: 160
role: Not tested on hardware - not sold yet
summary: An image for a Unit PoE-P4 with a rev 3.x chip. M5Stack does not list one yet.
flasher: m5-poe-p4x
capture: m5-addon-display-in
spec.Chip: ESP32-P4, rev 3.x
spec.Network: 100M Ethernet, 802.3at PoE
spec.Capture: M5Stack Add-on Display In (LT6911D), 24-pin flat cable
link.M5Stack documentation: https://docs.m5stack.com/en/unit/Unit_PoE-P4
photo: board.webp
photo_style: product
---

M5Stack sells the [Unit PoE-P4](/boards/m5-poe-p4/) with a rev 1.x chip
(ESP32-P4NRW32). This image is for the same board with a rev 3.x chip, should
one appear. M5Stack does not list such a unit today, so the name and the chip
are expected, not announced.

Nobody has run it. One part is known to be unchecked: on rev 3.x the picture
from the LT6911D bridge takes a different path, and its byte order has not
been tried, so the colours may come out wrong.

If your Unit PoE-P4's boot log says `chip revision: v3.x`, this is the image
for it - and please [tell me](https://github.com/espkvm/espkvm/issues) how it went.
