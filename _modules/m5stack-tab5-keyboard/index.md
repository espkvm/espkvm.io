---
title: M5Stack Keyboard for Tab5
family: M5Stack
tile_maker: M5Stack
tile_model: Keyboard for Tab5
kind: terminal
status: tested
order: 2
role: Keyboard for the terminal (optional)
chip: I2C keyboard
summary: The keyboard that clips onto the Tab5. The ESP-KVM terminal finds it by itself and types on the target with it.
spec.Connection: the Tab5's expansion connector, I2C at 0x6D
spec.Setting: none, found by itself
link.ESP-KVM terminal: /terminal/
link.M5Stack product page: https://shop.m5stack.com/products/keyboard-for-tab5
photo: module.webp
photo_style: product
---

The [ESP-KVM terminal](/terminal/) finds this keyboard when it starts and
hides its on-screen keyboard while it is there. Keys go to the target as a
normal keyboard, and they type into the terminal's own setup screens too.

Without it the [Tab5](/modules/m5stack-tab5/) still works: an on-screen keyboard appears where one is
needed, and a USB keyboard in the USB-A port does the same job.
