---
title: 0.22.0 - two firmware slots, and a way back
description: The firmware panel shows both slots and can boot the other one, so going back to a build that worked needs no cable.
tags: update, video
date: 2026-08-12
image:
---

The device has always kept two firmware slots and installed an update into the
one it is not running from. That is what lets a bad update undo itself. Until
now you could not see any of it.

The firmware panel now lists both slots: the version in each, which one is
running, and whether it has been confirmed or is still on trial. Next to the
other one there is a "Boot this" button, which switches to it and restarts. So
dropping back to the previous build is a click, not a cable. A slot with no
valid image refuses, so the button cannot strand the device.

Two fixes in the same release:

- the Function EV board booted slowly and noisily after a library update moved its start-up around, with the WiFi co-processor and the microSD card fighting over a shared bus. It is back to a few seconds.
- a browser's H.264 decoder can quietly stall, filling the picture with rubbish that even a keyframe will not clear. The console now notices no frames are coming out, rebuilds the decoder, and falls back to MJPEG if that does not help, instead of waiting for you to reload.

[Release v.0.22.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.22.0)
