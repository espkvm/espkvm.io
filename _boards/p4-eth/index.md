---
title: Waveshare ESP32-P4-ETH
family: Waveshare
kind: device
status: tested
order: 10
role: The device - the one this project is built on
summary: ESP32-P4 with 100M Ethernet, a 22-pin camera connector, USB OTG and a microSD slot.
flasher: p4-eth
capture: c790, waveshare-19137
spec.Chip: ESP32-P4, rev 1.x or rev 3.x (an image for each)
spec.Memory: 32 MB PSRAM, 32 MB flash
spec.Network: 100M Ethernet
spec.To the target: USB 2.0 OTG on an MX1.25 connector
spec.Capture: 22-pin 0.5 mm camera connector (the Pi 5 / Zero kind)
spec.microSD: yes
link.Waveshare product page: https://www.waveshare.com/esp32-p4-eth.htm
spec.Measured: 1080p MJPEG 20 fps; 720p 45 fps
photo: board.webp
photo_style: product
---

The board ESP-KVM was written on, and the default image: the flasher offers it
first. Ethernet only, no Wi-Fi.

## Wiring

- The USB-C port is the flashing and console bridge (CH343), not the target's port.
- The USB 2.0 OTG that goes to the target is on the **MX1.25** connector, so the lead is MX1.25 to USB-A.
- The target's 5 V comes back down that lead: pulling it at the target's end restarts the KVM.
- The camera connector is the narrow **22-pin** one. The C790 has a 22-pin connector on its back and a 22-pin ribbon in the box, so they join directly. A capture board with only the wide 15-pin connector, like Waveshare's adapter, needs a 15-to-22-pin ribbon (sold as a Raspberry Pi 5 camera cable).

## Measured

MJPEG at quality 70, rev 1.3 chip:

| Mode | fps | Bitrate |
|---|---|---|
| 1920x1080 | 20 | 17.5 Mbit/s |
| 1280x720 | 45.5 | 16.8 Mbit/s |
| 1024x768 | 56 | 17.6 Mbit/s |

A still screen costs nothing, since unchanged frames are skipped. H.264 on this
chip runs at 5-7 fps at 1080p and 17 fps at 720p, but an idle desktop costs
170 kbit/s against MJPEG's 8.5 Mbit/s: it is for narrow links, not for
smoothness. A rev 3.x chip does 22-24 fps at 1080p.

## Good to know

- The BOOT button (GPIO 35) is also an Ethernet pin, so the device reads it once, early in start-up. For the password reset: press reset, release, then hold BOOT.
- The microSD writes at 40 MHz because the slot's power comes from the chip's LDO 4.
- Waveshare ships rev 1.3 today, and the product code does not tell the revision. The boot log prints `chip revision:`.

Another ESP32-P4 board with Ethernet and the same camera connector can run it
too. The pins are set in
[menuconfig](https://github.com/espkvm/espkvm/blob/main/docs/PORTING.md), not
in the code.
