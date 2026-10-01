---
title: DFRobot FireBeetle 2 ESP32-P4
kind: device
status: tested
order: 68
role: The device - community-tested, the smallest
summary: 60 x 25 mm with an ESP32-C6 and the camera connector. Wi-Fi only; about 9 fps of 1080p MJPEG over it.
flasher: firebeetle2-p4
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: Wi-Fi 6 (ESP32-C6) only
spec.To the target: USB-C, the OTG-HS one
spec.Capture: 15-pin Raspberry Pi camera connector
spec.Measured: about 9 fps of 1080p MJPEG over Wi-Fi (0.56.2)
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

## Confirmed by a user

[@Diego-fe](https://github.com/Diego-fe) ran it in
[#63](https://github.com/espkvm/espkvm/issues/63): capture, USB and Wi-Fi work.
At first Wi-Fi stalled under a 1080p stream, and two fixes came out of that:

- 0.56.1: the board has no pull-ups on the SDIO lines to the C6, so the firmware turns on the chip's own.
- 0.56.2: over Wi-Fi the P4 ran out of internal RAM under load.

On 0.56.2 the picture runs without a break, at about 9 fps of 1080p MJPEG.
