---
title: Waveshare ESP32-P4-Module-DEV-KIT
kind: device
status: untested
order: 120
role: Not tested on hardware
summary: The P4, an ESP32-C6 and flash in one module, on a carrier with Ethernet and a card slot.
flasher: p4-module-devkit
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each)
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet, Wi-Fi 6 (ESP32-C6)
spec.To the target: USB-A (jumper; A-to-A cable, 5 V wire cut)
spec.Capture: 15-pin Raspberry Pi camera connector
spec.microSD: yes
link.Waveshare product page: https://www.waveshare.com/esp32-p4-module-dev-kit.htm
photo: board.webp
photo_style: product
---

The P4, the ESP32-C6 and 16 MB of flash under one shield, on a carrier with 100M
Ethernet, a card slot, a 2x20 header and four USB-A sockets. Every pin the KVM
touches is one already in use, and a C790 ribbon plugs straight in. The -A, -B
and -C kits are the same board with a different screen in the box.

## Wiring

- A jumper switches the OTG-HS between one Type-A socket and an internal hub. The KVM wants the socket.
- That socket drives its own 5 V, so the lead to the target is an **A-to-A cable with the 5 V wire cut**.

Built from the schematic, not yet run on one.
