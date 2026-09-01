---
title: 0.28.0 - reading the screen as text, and watching it while you are away
description: Select and copy the words off a BIOS screen instead of typing them out, and let the device raise an alert when a phrase you care about appears.
tags: screen-text, diagnostics, video
date: 2026-08-21
image: /assets/blog/0-28-0-reading-the-screen-as-text/clip.webp
---

Until now, getting a serial number or an error code off a BIOS screen meant
reading it and typing it out somewhere else. Press Select and sweep the mouse
over the picture as if it were a page, or press Copy and take the whole screen.
A UEFI boot menu, memtest, a Linux console: all of them come back as text.

There is a short silent clip of it happening: a NixOS boot menu, its lines being
selected with the mouse while the menu is walked up and down at the same time -
which is the part that proves this is the live screen and not a screenshot
somebody pasted.

[Watch it on YouTube](https://youtu.be/QGABqgAR5H0) - no sound, nothing installed
on the target, and the machine has not booted yet.

**It is not OCR.** A text screen is drawn by a character
generator: a fixed grid, one fixed bitmap per character. So each cell is simply
looked up in a table of the shapes the font has. Either a cell matches and the
character is certain, or it comes back as a question mark and you can see
exactly which cells were not read. There is no "recognised, probably" to catch
you out three days later.

Three fonts are known: the one a legacy BIOS draws with, the one a Linux console
draws with (a different font - five printable characters differ, including f and
v) and the one a UEFI console draws with.

**The device can watch the screen when nobody is.** Give it a phrase or two -
`no boot device`, `kernel panic` - and with the console closed it reads the
screen once a second and raises an alert the moment one appears, clearing it
when it goes. Both edges go in the log, and Home Assistant gets a sensor with
the matched text. It is off by default, and while it is off it costs nothing.

Also here: EDID profiles that cap the target at 720p or 1024x768, which on older
silicon is the difference between 7 frames a second and something you can work
in; the Pins tab now draws the board's expansion header the way it is printed
instead of a list of GPIO numbers; and paste learned Czech, Ukrainian and
Lithuanian.

[Release v.0.28.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.28.0)
