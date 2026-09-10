---
title: 0.9.0 - pressing the power button from a browser
description: Two cheap optocoupler modules let the device press the target's power and reset buttons and read its power LED back.
tags: power, hardware
date: 2026-07-28
image: /assets/blog/0-9-0-the-power-button/817.webp
---

The device can press the target's power and reset buttons now, and read its
power LED back. No custom hardware: a two-channel PC817 optocoupler module does
it, and the two machines stay electrically apart.

The console gets a Power panel with three actions: a click of the power button,
a five second hold for a hard off, and a reset. It asks before the destructive
ones.

The wiring is all settings, not a build: which GPIO pins you used, how long the
pulse should be, which way round the module triggers. The same firmware runs on
a board with nothing wired to it and says the feature is unavailable. If you
guess the polarity wrong, that is a checkbox, not a reflash.


The wiring guide is in [docs/wiring.md](https://github.com/espkvm/espkvm/blob/main/docs/wiring.md).

[Release v.0.9.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.9.0)
