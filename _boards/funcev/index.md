---
title: Espressif ESP32-P4 Function EV Board
family: Espressif
kind: device
status: tested
order: 20
role: The device - rev 3.2
summary: Espressif's own ESP32-P4 board, with Ethernet and an ESP32-C6. On a rev 3.x chip, 1080p at a little over 20 fps.
flasher: funcev
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each); the unit here is rev 3.2
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet, Wi-Fi 6 (ESP32-C6)
spec.To the target: USB OTG
spec.Capture: 15-pin Raspberry Pi camera connector
spec.microSD: yes
spec.Measured: 1080p H.264 at 22-24 fps, 720p at 28
link.Espressif user guide: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32p4/esp32-p4x-function-ev-board/user_guide.html
photo: board.webp
photo_style: product
---

Espressif's own board, with rev 3.2 silicon and an ESP32-C6, so it also does
Wi-Fi: station, access point and the rescue hotspot.

The newer chip captures YUV422 straight into the H.264 and JPEG encoders, with
no colour-convert pass. That frees about 4 MB of PSRAM for a deeper capture ring
and lifts 1080p H.264 to 22-24 fps, 28 at 720p.

## Good to know

- Board v1.4 and v1.5.x are board versions, not chip revisions: the same board comes with a rev 1.x or a rev 3.x chip, and Espressif now sells the rev 3.x one as the ESP32-P4X Function EV Board. The image for rev 1.x has not been run on hardware yet.

- Holding BOOT while pressing RST puts this board into download mode: the firmware never starts, and it looks hung. For the password reset: press RST, release, then hold BOOT.
- A "DS3231 for Pi" clock module plugs straight onto pins 1-9 of the Raspberry Pi header: those pins are 3V3, GND and the capture chip's I2C bus. Tested on this board.
- It has a Raspberry Pi header. The C790's audio cable lands on pins 6, 12, 35 and 38 there (audio capture is not in the firmware yet); pin 12 is GPIO 22, which is also the round LCD's default chip select.
