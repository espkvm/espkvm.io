---
title: M5Stack Unit Button
family: M5Stack
tile_maker: M5Stack
tile_model: Unit Button
kind: control
status: untested
order: 20
role: A button on the box (optional)
chip: Button
summary: A push button on a Grove cable. A short press and a 1.5 s hold each run an action - the target's power button, reset, Wake-on-LAN, a runbook, a dashcam clip, a screenshot.
spec.Wiring: the yellow Grove wire to a free GPIO; pressed reads low
spec.Setting: Settings → Power → Button on the box
spec.Firmware: 0.61.0 or newer
link.M5Stack docs: https://docs.m5stack.com/en/unit/button
photo: module.webp
photo_style: product
---

A button on the KVM itself, for the person standing next to it. Set its pin in
Settings → Power → Button on the box, then pick what a short press does and
what holding it for a second and a half does:

- the target's power button, or a hard power off;
- reset;
- Wake-on-LAN;
- a runbook, by name;
- save the dashcam's last seconds as a clip;
- a screenshot to the card;
- on a board with WiFi, the connection: hotspot on and off, the next network
  mode, or Ethernet and WiFi swapped. Each restarts the device.

These are the same actions a schedule can run. The hold fires as soon as it
has been held long enough, so you know it took.

Any push button to ground works the same way; one to 3V3 needs "Button reads
high when pressed" on.

On the M5Stack Unit PoE-P4 the Grove port is GPIO 53 (yellow) and 54, the same
pair the status display uses there, so it is the button or the display.

Not tried with this unit yet.
