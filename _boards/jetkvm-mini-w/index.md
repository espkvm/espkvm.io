---
title: JetKVM Mini W
page_title: JetKVM Mini W custom firmware - open-source ESP-KVM for the Wi-Fi Mini
description: Open-source custom firmware for the JetKVM Mini W, the Wi-Fi model on the ESP32-P4X. ESP-KVM has a first version for it.
kind: device
status: untested
order: 901
role: First version, testing in progress
summary: The Wi-Fi model of the JetKVM Mini, with an ESP32-C5 for Wi-Fi 6 in place of the Ethernet. ESP-KVM has a first version for it, still being tested.
spec.Chip: ESP32-P4X, rev 3.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Capture: HDMI in, built in (TC358743)
spec.Network: Wi-Fi 6 on 2.4 and 5 GHz (ESP32-C5)
spec.To the target: USB-C
spec.Screen: 240x240 colour (ST7789)
spec.microSD: yes
spec.HDMI audio: no, the capture chip's audio lines are not wired to the P4
spec.Size: 42 x 42 x 23 mm
link.JetKVM product page: https://jetkvm.com/products/jetkvm-mini
flasher: jetkvm-mini-w
photo: board.webp
photo_style: product
---

The Mini W is the [JetKVM Mini](/boards/jetkvm-mini/) with an ESP32-C5 for Wi-Fi 6 on 2.4 and 5 GHz instead of the Ethernet port. Everything else is the same box, and the steps before flashing are on the Mini's page.

> **The first version for this device.** ESP-KVM on the Mini W is new and has not been through enough testing yet. In theory nothing can break: at worst the image does not start, and you flash it again over USB. Still, a first version is at your own risk, so make the backup from the steps on the [Mini's page](/boards/jetkvm-mini/) first: it is the only way back to the stock firmware. Once it has been tested properly, I will say so here, and from then on it can be installed without any worry.

On the first boot ESP-KVM opens its own setup hotspot, and the screen shows a code to join it. The C5 keeps the firmware it ships with. If the Wi-Fi does not come up, tell me.

ESP-KVM is a separate open-source project. It is not made, sold or supported by JetKVM.
