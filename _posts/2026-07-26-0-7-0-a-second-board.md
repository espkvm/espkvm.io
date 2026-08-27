---
title: 0.7.0 - a second board, and a release for each
description: The Espressif ESP32-P4 Function EV board joins the Waveshare one, and CI now builds and publishes every board separately.
tags: hardware
date: 2026-07-26
image: /assets/blog/0-7-0-a-second-board/board-funcev.webp
---

Until now there was one board and one firmware image. Now there are two.

The ESP32-P4 comes in two silicon families, and an image built for one will not
start on the other - the header carries both a minimum and a maximum revision.
The Waveshare ESP32-P4-ETH is an older revision; the Function EV board is
rev 3.2. So they cannot share an image, and both have to be built.

What that means in practice:

- every board is built by CI and gets its own release files, with the board name in the file name;
- every board gets its own update manifest, so a device only ever checks for images that will run on it;
- the plain files stay where they were, so devices flashed before this release keep updating exactly as they did.

A board is a settings overlay, not code, so the next one is cheap to
add.


[Release v.0.7.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.7.0)
