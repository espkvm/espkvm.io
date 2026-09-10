---
title: 0.10.0 - phones, and taking turns at the keyboard
description: The screen becomes a trackpad on a phone, and a second person opening the console can see who is driving and ask for the keyboard.
tags: console, mobile, input
date: 2026-07-28
image:
---

Two things: phones, and more than one viewer.

**Touch mode.** A phone has no pointer to map, and pretending it does made the
console unusable. On a touch screen the picture is a trackpad now: one finger
moves the pointer, a tap is a left click, two fingers tapped is a right click,
two fingers dragged scrolls, a long press then drag holds the button down. The
on-screen keyboard types through the target's own layout, the way paste already
did. It switches itself on when the browser reports a coarse pointer, and there
is a Touch button when it gets that wrong.

**One driver at a time.** Until now every new viewer quietly took the keyboard
from whoever had it, and the one who lost it was not told. The first client
holds control now and keeps it. A second viewer gets a banner saying somebody
else is driving, with a "Take control" button. Taking control drops the previous
holder to a viewer instead of throwing them out, so they keep watching and can
ask for it back.

[Release v.0.10.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.10.0)
