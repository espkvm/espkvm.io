---
title: Waveshare ESP32-P4-WIFI6-DEV-KIT
kind: device
status: untested
order: 110
role: Not tested on hardware
summary: Ethernet with PoE and Wi-Fi 6 on one board. Its USB OTG port is set to device by a jumper.
flasher: p4-wifi6-devkit
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each)
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet with PoE, Wi-Fi 6 (ESP32-C6)
spec.Capture: camera connector
spec.microSD: yes
link.Waveshare product page: https://www.waveshare.com/esp32-p4-wifi6-dev-kit.htm
photo: board.webp
photo_style: product
---

A 100M magjack that also takes PoE, plus the ESP32-C6. Same pins as the other
Waveshare boards, so the build is almost the stock one.

Its USB OTG port is switched between host and device by a jumper - the KVM
needs **device**.

Built from the schematic, not yet run on one.
