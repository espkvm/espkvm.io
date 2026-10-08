---
title: Espressif ESP32-P4X-C5-Function-EV-Board
family: Espressif
kind: device
status: untested
order: 125
role: Not tested on hardware
summary: The Function EV with a dual-band ESP32-C5, so it can join a 5 GHz network. Ethernet, microSD, rev 3.x.
flasher: funcev-c5
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 3.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet, dual-band Wi-Fi 6 (ESP32-C5)
spec.To the target: USB-C, the HS OTG one
spec.Capture: 15-pin 1.0 mm camera connector
spec.microSD: yes
link.Espressif user guide: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-c5-function-ev-board/user_guide.html
photo: board.webp
photo_style: product
---

The Function EV with an ESP32-C5-MINI-1 where the C6 was. Espressif's own
esp-hosted preset for this board puts the C5 on the same pins the C6 used, so
the image is the Function EV's with the co-processor swapped.

## Wiring

- The HS OTG goes to a Type-C and a Type-A, and they cannot be used at once. The target goes on the **Type-C**.
- Flashing and the log go through the chip's own USB Serial/JTAG Type-C.

Built from the user guide, not yet run on one.
