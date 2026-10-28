---
title: JetKVM Mini and Mini W
page_title: JetKVM Mini custom firmware - open-source ESP-KVM for the Mini and Mini W
description: Open-source custom firmware for the JetKVM Mini and Mini W, which are built on the ESP32-P4X. An ESP-KVM image for them is in progress.
kind: device
status: planned
order: 900
role: In progress
summary: A small ready-made KVM on the ESP32-P4X, the chip ESP-KVM runs on. The Mini has Ethernet, the Mini W has Wi-Fi 6 instead. An ESP-KVM image for them is in progress.
spec.Chip: ESP32-P4X, rev 3.x
spec.Memory: 32 MB PSRAM, 16 MB flash
spec.Capture: HDMI in, built in (the capture chip is not published)
spec.Network: Mini: 100M Ethernet. Mini W: Wi-Fi 6 on 2.4 and 5 GHz (ESP32-C5)
spec.To the target: USB-C
spec.Screen: 240x240
spec.microSD: yes
link.JetKVM product page: https://jetkvm.com/products/jetkvm-mini
photo: board.webp
photo_style: product
---

The JetKVM Mini is a small ready-made KVM. Inside is the ESP32-P4X, the chip ESP-KVM runs on, with the same 32 MB of PSRAM. The box, the HDMI input and the USB port are already there, so it is a natural device for ESP-KVM as custom firmware.

There is no ESP-KVM image for it yet. This page will say when there is one.

## Mini and Mini W

The two differ in the network. The Mini has 100M Ethernet. The Mini W has an ESP32-C5 for Wi-Fi 6 on 2.4 and 5 GHz in its place. ESP-KVM already runs Wi-Fi through a second chip on the [Function EV Board](/boards/funcev/), and the [C5 version of that board](/boards/funcev-c5/) has an image too.

How ESP-KVM and the JetKVM Mini compare today is on the [comparison page](/compare/).

ESP-KVM is a separate open-source project. It is not made, sold or supported by JetKVM.
