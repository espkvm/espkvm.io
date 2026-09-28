---
title: DFRobot FireBeetle 2 ESP32-P4
kind: device
status: untested
order: 140
role: Not tested on hardware
summary: 60 x 25 mm with an ESP32-C6 and the camera connector. Wi-Fi only.
flasher: firebeetle2-p4
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: Wi-Fi 6 (ESP32-C6) only
spec.To the target: USB-C, the OTG-HS one
spec.Capture: 15-pin Raspberry Pi camera connector
link.DFRobot product page: https://www.dfrobot.com/product-2915.html
photo: board.webp
photo_style: product
---

Everything the KVM needs on a small board, but no wired port: Wi-Fi is the only
link. The AI Kit (DFR1237) is the same board with accessories in the box.

## Wiring

- The USB-C beside the RST button is power, flashing and the log.
- The other USB-C is the OTG-HS that goes to the target.
- Its 5 V ties to the board's rail, so unplugging it at the target's end restarts the KVM.

Built from the schematic, not yet run on one.
