---
title: Waveshare ESP32-P4-WIFI6-DEV-KIT
kind: device
status: tested
order: 65
role: The device - community-tested, PoE
summary: Ethernet with PoE and Wi-Fi 6 on one board. H.264 at about 23 fps on the v1.2 board with a rev 3.1 chip.
flasher: p4-wifi6-devkit
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each); v1.2 boards carry rev 3.1
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet with PoE, Wi-Fi 6 (ESP32-C6)
spec.To the target: USB-A port 1 (A-to-A cable; jumper, see below)
spec.Capture: camera connector
spec.microSD: yes
spec.Measured: H.264 at about 23 fps (rev 3.1)
link.Waveshare product page: https://www.waveshare.com/esp32-p4-wifi6-dev-kit.htm
link.Waveshare FAQ: https://docs.waveshare.com/ESP32-P4-WIFI6-DEV-KIT/FAQ
photo: board.webp
photo_style: product
---

A 100M magjack that also takes PoE, plus the ESP32-C6. Same pins as the other
Waveshare boards, so the build is almost the stock one.

Confirmed by [@brooklyn5w4g](https://github.com/brooklyn5w4g) on a v1.2 board
with a rev 3.1 chip, using the rev 3.x image: H.264 at about 23 fps.

## Wiring

A jumper switches the P4's USB between USB-A **port 1**, wired straight to the
chip, and a hub on ports 2-4. The target goes on port 1, with an A-to-A cable.
Waveshare swapped the jumper's labels between board versions:

| Board version | Jumper for port 1 |
|---|---|
| v1.1 (chip rev 1.3) | DEVICE |
| v1.2 (chip rev 3.1) | HOST |

## Good to know

- Check the chip revision before flashing: a v1.2 board wants the rev 3.x image.
- The one report so far could not connect with the browser flasher. If it fails for you too, hold BOOT while clicking Install, and tell me which USB port you used.
