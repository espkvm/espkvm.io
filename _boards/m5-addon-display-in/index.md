---
title: M5Stack Add-on Display In
kind: capture
status: tested
order: 30
role: The capture - M5Stack units only
summary: A Lontium LT6911D and a microSD slot, on a 24-pin flat cable. Fits the Unit PoE-P4 and nothing else.
bridge: LT6911D
spec.Bridge: Lontium LT6911D
spec.Input: HDMI
spec.Connector: 24-pin flat cable (M5Stack's own)
spec.microSD: yes
spec.Measured: 720p MJPEG at 23 fps
link.M5Stack shop page: https://shop.m5stack.com/products/add-on-display-in-for-poe-p4-lt6911d
photo: board.webp
photo_style: product
---

Not a TC358743. It plugs onto the 24-pin flat cable on M5Stack's Unit PoE-P4
and PoE-P4X - not the 15-pin camera cable every other board here uses, so it
fits none of them and none of them drives it.

The LT6911D cannot tell whether the source is switched on, so after a long "No
signal" the console offers a Reconnect HDMI button with a countdown.
