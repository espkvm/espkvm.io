---
title: JetKVM Mini W
h1: JetKVM Mini W custom firmware
page_title: JetKVM Mini W custom firmware - open-source ESP-KVM for the Wi-Fi Mini
description: Open-source custom firmware for the JetKVM Mini W, the Wi-Fi model on the ESP32-P4X. Everything but the Wi-Fi is the same hardware as the Mini, where ESP-KVM is tested.
kind: device
status: untested
order: 901
role: Same as the Mini, Wi-Fi not run on one yet
summary: The Wi-Fi model of the JetKVM Mini, with an ESP32-C5 for Wi-Fi 6 in place of the Ethernet. The rest is the Mini, where ESP-KVM is tested.
spec.Chip: ESP32-P4X, rev 3.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Capture: HDMI in, built in (TC358743)
spec.Network: Wi-Fi 6 on 2.4 and 5 GHz (ESP32-C5)
spec.To the target: USB-C
spec.Screen: 240x240 colour (ST7789)
spec.microSD: yes
spec.Power: 5 V, 500 mA, from either USB-C port
spec.HDMI audio: no, the capture chip's audio lines are not wired to the P4
spec.Size: 42 x 42 x 23 mm
link.JetKVM product page: https://jetkvm.com/products/jetkvm-mini
flasher: jetkvm-mini-w
photo: board.webp
photo_style: product
---

The Mini W is the [JetKVM Mini](/boards/jetkvm-mini/) with an ESP32-C5 for Wi-Fi 6 on 2.4 and 5 GHz instead of the Ethernet port. Everything else is the same box, and the steps before flashing are on the Mini's page.

The firmware is the same ESP-KVM as on the other boards, and the capture, the USB to the target, the screen, the buttons and the microSD slot are the same hardware as on the Mini, where I tested it. Only the Wi-Fi part, the ESP32-C5 with the firmware it ships with, has not run on a Mini W yet: I do not have one. Make the backup from the steps on the [Mini's page](/boards/jetkvm-mini/) first, as with any flashing. At worst the image does not start, and you flash it again over USB.

On the first boot ESP-KVM opens its own setup hotspot, and the screen shows a code to join it. The C5 keeps the firmware it ships with. If the Wi-Fi does not come up, tell me.

ESP-KVM is a separate open-source project. It is not made, sold or supported by JetKVM.
