---
title: 0.64.0 - an original Xbox pad
description: The device can now be an original Xbox controller (XID). The protocol comes from ZacharyLeahan's fork, where it was tried on a real Xbox.
tags: input, hardware
date: 2026-10-12 21:00
image: /assets/blog/0-64-0-an-original-xbox-pad/hero.webp
---

Settings -> Input -> Gamepad -> `xbox` makes the device an original Xbox controller. The console sees an XID pad, the same kind of device as the Controller S, and the gamepad panel in the console drives it: a pad on your own computer, or the buttons on the screen.

The original Xbox does not speak plain HID. Its controller is its own USB class, XID, with a fixed report of buttons, analog face buttons and two sticks. [ZacharyLeahan](https://github.com/ZacharyLeahan/espkvm) wrote it in his fork and tried it on a real Xbox. I took it into the main firmware next to the HORI pad for the Switch and the Xbox 360 mode.

A few details:

- White and Black are on LB and RB.
- The console's controller port is not a USB socket, so it needs an adapter cable to USB.
- The pad is alone on the USB port while this mode is on, as with the other console modes, so the keyboard and mouse are off.
- I have not tried this build on an Xbox myself yet.

## Also in 0.64.0

- TC358743 boards: a stuck I2C read no longer leaves "No signal" until a restart. Reads give up after 200 ms.
- A source already above 1080p at power-on is now refused, as it already was later. Also from Zach's fork.
- The Waveshare ESP32-P4-NANO-WIFI6-DB is a tested board.

[Release 0.64.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.64.0)
