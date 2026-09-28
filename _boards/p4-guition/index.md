---
title: Guition ESP32-P4-M3-Dev
kind: device
status: tested
order: 40
role: The device - community-tested
summary: A display board that also carries Ethernet and an ESP32-C6. The capture ribbon goes into J3.
flasher: p4-guition
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each)
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet, Wi-Fi 6 (ESP32-C6)
spec.To the target: USB-C, the OTG-HS one
spec.Capture: camera connector J3
photo: board.webp
photo_style: product
---

A 4.3" MIPI-DSI touch display board; the KVM does not use the display. A
contributor confirmed capture, USB and Ethernet on pre-3.0 silicon.

## Wiring

- The target goes on the **OTG-HS** USB-C port, not the other one.
- The capture board's ribbon goes into **J3**, not J2 ([#61](https://github.com/espkvm/espkvm/issues/61)). With nothing in J3, the only chip the firmware finds on the capture bus is the board's own audio codec, and it says so.
