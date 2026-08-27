---
title: 0.21.0 - a little screen on the box itself
description: Solder on a small OLED or a round colour LCD and the device shows its address, its link and its health without a browser at all.
tags: display, hardware
date: 2026-08-11
image: /assets/blog/0-21-0-a-little-screen-on-the-box/round-pages.webp
---

Until now the device only spoke through the browser, so standing next to the box
you could not tell whether it was on the network at all.

Now it can say so itself. Solder on a small mono OLED, an SSD1306 or SH1106.
They are found automatically on the capture chip's own I2C bus, so they cost no
pins. A round GC9A01 colour LCD works too. Turn it on in Settings and the panel
shows a boot logo, then cycles through pages: the IP address, the link, what the
capture sees, and health with temperature and memory bars.

Off by default, and it stays out of the video encoder's way, so switching it on
does not cost frames.

The three pictures above are the round LCD on a real board: the boot logo, the
network page with the address to type, and health with temperature and memory.

![A 128x64 mono OLED soldered to the capture chip's I2C bus, showing the network page: the link it is on, its address, and the name it answers to.](/assets/blog/0-21-0-a-little-screen-on-the-box/oled.webp)

A short silent clip of the round one running:

![A frame from the clip: the round LCD on the bench, cycling its status pages.](/assets/blog/0-21-0-a-little-screen-on-the-box/video.webp)

[Watch it on YouTube](https://www.youtube.com/watch?v=-snDjOOjbSA) - about a
minute, no sound.

**Pins from the console.** Wiring a display means choosing GPIOs, so pin
settings became drop-downs of what is actually free, and a new Pins tab shows
the whole map: what the board reserves, what you have assigned, and what is
left. The ATX pins are on that map too, so two features can no longer quietly
claim the same pin.

[Release v.0.21.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.21.0)
