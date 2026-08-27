---
title: 0.9.0 - pressing the power button from a browser
description: Two cheap optocoupler modules let the device press the target's power and reset buttons and read its power LED back.
tags: power, hardware
date: 2026-07-28
image: /assets/blog/0-9-0-the-power-button/817.webp
---

The device can restart the target now, and with no custom hardware: a PC817
two-channel optocoupler module on each side does the whole job.

The device can now press the target's front-panel power and reset buttons, and
read its power LED back the same way. There is no electrical connection between the two machines.

The console gets a Power panel that drives it, and asks before doing anything
destructive. There are three actions: a click of the power button, a five second
hold for a hard off, and a reset.

Everything about the wiring is a setting, not a build: which GPIO pins
you used, how long a pulse should be, and which way round the module triggers.
So the same firmware runs on a board with nothing wired at all - it simply says
the feature is unavailable and why - and guessing a module's polarity wrong is a
checkbox, not a reflash.


The wiring guide is in [docs/wiring.md](https://github.com/espkvm/espkvm/blob/main/docs/wiring.md).

[Release v.0.9.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.9.0)
