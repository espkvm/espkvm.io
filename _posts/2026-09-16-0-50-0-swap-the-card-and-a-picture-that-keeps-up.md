---
title: 0.50.0 - swap the card while it runs, and a picture that keeps up
description: The microSD card can go in and out without a restart, even in the middle of a copy. And on a still screen the MJPEG picture no longer shows the screen as it was before your last key.
tags: storage, video, console
date: 2026-09-16
---

Two things in this release. One is a feature I had been putting off. The other
is a bug a reader found while working in a BIOS, and it had been there since the
first MJPEG stream.

## The card can come and go

Until now the device looked at the microSD slot once, at boot. Take the card out
and the target kept a drive that no longer answered. Put one in and nothing
happened until a restart.

Now the device checks the slot every five seconds while the card is idle. The
check is one sector read. Pull the card and the drive disappears from the
target. Push it back and it mounts at 40 MHz and is offered to the target again.

A card the target is reading is never idle for five seconds, so that check alone
would miss the worst case. So a read that fails also asks for a check. I pulled a
card in the middle of a copy, and the device noticed 4.6 seconds later.

Testing it turned up three more bugs:

- One pulled card dropped the bus from 40 MHz to 2 MHz in ten milliseconds.
- An empty slot wrote five lines to the log every five seconds.
- With no card in, the whole-card medium logged an error.

A pulled card now costs one speed step, and an empty slot is quiet. One limit
stays: on a board that uses WiFi, the WiFi chip shares the SD controller with the
card, so a card put in after boot is picked up only after a restart. Pulling a
card out is noticed on every board.

## The picture was one step behind

A reader wrote that working in a BIOS through the console was hard: the picture
always showed the screen before the last key. Press down, see the old menu. Press
down again, see the menu after the first press.

A browser shows an MJPEG stream as a row of images. It draws an image when the
marker that ends it arrives. My firmware sent that marker at the start of the
next image. At 30 frames a second nobody sees the delay. But on a still screen
the device sends a new image only when something changes, or every five seconds.
So each image waited for the next key or for five seconds to pass.

Each image now carries its own end marker. Same still screen, measured on the
Function EV:

| | Old firmware | New firmware |
|---|---|---|
| End marker of the first image | 5.0 s after the image | 45 ms after the image |

H.264 never had this bug: it sends every frame, even on a still screen.

[Release 0.50.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.50.0)
