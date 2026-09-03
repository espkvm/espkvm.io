---
title: 0.42.0 - two things can no longer share a pin
description: A settings write that would put two things on one GPIO is refused, a capture driver announces itself instead of being called by name, and a keyboard the target has forgotten can be re-plugged from the console.
tags: hardware, console, video
date: 2026-09-03
image:
---

The ATX buttons and the round LCD are both wired by hand, and both pick their
GPIOs in the console. Nothing used to notice when they named the same pin - or
when one of them named a pin the board's own hardware holds, like the capture
bus or the Ethernet PHY. Neither shows up as an error. The panel simply stays
dark, or the network stops.

A write that would do that is now refused, naming the pin and what already has
it. The pins are weighed as a set and after the request is imagined applied, so
moving the display off a pin the buttons want still goes through in one go, and
a clash a device already has stored does not block unrelated changes. The
defaults moved too: the buttons used to start unassigned with the wiring page
suggesting the same three pins the LCD starts on, so a device wearing both and
set up by following that page ended up with three pins claimed twice.

The capture path no longer calls the TC358743 by name. A driver registers a
detect function, and the path asks for whatever answers on the bus, getting
back a name to show and a table of operations to drive it with. Adding a bridge
is adding a component. Nothing about the picture changes - there is still one
driver and it is the same one - and the interface is a guess until a second
bridge exists to shape it. The idea comes from Espressif's esp_cam_sensor.

Then two silences. A machine that boots faster than this firmware looks at the
input, finds no monitor, and configures no output; single-board computers in
particular probe once and never look again. The device now watches for that
exact case - the source is powered and attached, but nothing is arriving - and
pretends to be unplugged and plugged back in, at ten seconds, then twenty, then
forty, and then it stops. A target that is simply switched off is left in
peace. The console says which silence it is looking at, instead of offering the
same list of things to check either way.

The other silence is the keyboard. A restart resets this side of the USB cable
while the target's power never drops, so the target goes on holding a
connection this side has forgotten and every keystroke goes nowhere. The
firmware already came back as a new device once at start-up; now it tries again
while nothing has enumerated it, and clicking the USB dot in the status bar
offers "Re-plug USB", which does the same on demand. Off the bus for 100 ms and
back, without restarting either machine.

[Release v.0.42.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.42.0)
