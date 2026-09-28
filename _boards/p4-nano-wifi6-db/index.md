---
title: Waveshare ESP32-P4-NANO-WIFI6-DB
kind: device
status: untested
order: 130
role: Not tested on hardware
summary: The NANO with a dual-band ESP32-C5, so it can join a 5 GHz network.
flasher: p4-nano-wifi6-db
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 3.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet (PoE header), dual-band Wi-Fi 6 (ESP32-C5)
spec.To the target: USB-A
spec.Capture: 15-pin Raspberry Pi camera connector
link.Waveshare product page: https://www.waveshare.com/esp32-p4-nano-wifi6-db.htm
photo: board.webp
photo_style: product
---

The first supported board that can join a 5 GHz network. It carries an
ESP32-P4NRW32**X**, which is rev 3.x silicon, so it has one image and no pre-3.0
twin.

Its right-hand header also brings out the high-speed USB pair, so the target
can be wired there instead of the Type-A socket.

Built from the schematic, not yet run on one.
