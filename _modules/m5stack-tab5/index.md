---
title: M5Stack Tab5
family: M5Stack
tile_maker: M5Stack
tile_model: Tab5
kind: terminal
status: tested
order: 1
role: Handheld terminal (optional, experimental)
chip: ESP32-P4 + ESP32-C6
summary: A 5" touch screen with an ESP32-P4 inside. With the experimental ESP-KVM terminal firmware it shows an ESP-KVM device's screen and controls the target, with no browser.
spec.Chip: ESP32-P4 (rev 1.x), ESP32-C6 for Wi-Fi
spec.Screen: 5", 1280x720, touch
spec.Ports: USB-A (keyboard and mouse), USB-C
spec.Firmware: ESP-KVM terminal, separate from the KVM's own
link.ESP-KVM terminal: /terminal/
link.M5Stack docs: https://docs.m5stack.com/en/core/Tab5
photo: module.webp
photo_style: product
---

Not a part of the KVM itself: a second device that talks to it over the
network. With the [ESP-KVM terminal](/terminal/) firmware the Tab5 finds
ESP-KVM devices on the network, signs in, and shows the target's screen. A
finger is the pointer; the [Keyboard for Tab5](/modules/m5stack-tab5-keyboard/) or a USB keyboard types.

The picture is MJPEG only: the Tab5's chip has no H.264 decoder, so set the
KVM's codec to MJPEG. Over Wi-Fi it shows 10 to 20 fps at 1280x720.

It is an experiment; more on [its page](/terminal/).
