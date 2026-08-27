---
title: 0.36.0 - a panel that can stay open, and arrows on a phone
description: Pin a panel beside the picture instead of over it, and drive a boot menu from a phone that has no arrow keys.
tags: console, mobile
date: 2026-08-25
image:
---

Panels float over the picture on purpose: a picture that resizes every time
something opens makes you find everything again. On a wide screen there is room
for both.

The pin in a panel's header now hands it a strip of the stage. The picture
shrinks to what is left, and everything drawn on the picture stays lined up with
it. Off by default, remembered per browser - it depends on your window, not on
the device - and not offered on a phone, where a panel is the whole width
anyway.

**Arrows on a phone.** A soft keyboard has no arrow keys, which makes a BIOS
menu or a boot list impossible to drive from a phone. Touch mode now has a pad:
the four arrows in the shape they have on a keyboard, with Esc, Tab and Enter
around them. Hold a key and it repeats.

Two more rearrangements. The ten numbers about the capture no longer have a
panel that slides over the very picture they describe - click the ones in the
status bar and the rest open just below. And power is a menu at the foot of the
rail with the target's power state on it, instead of a panel covering the
machine you want to watch restart.

[Release v.0.36.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.36.0)
