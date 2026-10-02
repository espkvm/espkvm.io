---
title: VIEWE ESP32-P4-Pi
kind: device
status: untested
order: 150
role: Not tested on hardware
summary: A Raspberry-Pi-shaped carrier for VIEWE's P4 module, with Ethernet, an ESP32-C6 and microSD.
flasher: viewe-p4-pi
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Network: 100M Ethernet, Wi-Fi 6 (ESP32-C6)
spec.To the target: USB-C, the OTG-HS one
spec.Capture: 15-pin Raspberry Pi camera connector
spec.microSD: yes
link.VIEWE documentation: https://github.com/VIEWESMART/ESP32-P4-Pi
photo: board.webp
photo_style: product
---

Both schematics are published, carrier and module, so every pin - even the
C6's SDIO lines - was read rather than guessed, and all of them land on the
firmware's defaults.

## Wiring

- The Type-C marked UART is power, flashing and the log.
- The other Type-C is the OTG-HS that goes to the target, so that lead is C to A.
- The Type-A socket is a host port the KVM does not use.
- PoE is only half wired: the magjack's centre taps reach a 4-pin header, but the module's 5 V has to go back in through the expansion header.

Built from the schematic, not yet run on one.

Its 40-pin header has the Raspberry Pi layout, with the capture chip's I2C bus on pins 3 and 5, so a "DS3231 for Pi" clock module should plug straight onto pins 1-9 (read from the vendor pinout, not tried on this board).
