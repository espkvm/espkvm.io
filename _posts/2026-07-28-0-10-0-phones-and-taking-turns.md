---
title: 0.10.0 - phones, and taking turns at the keyboard
description: The screen becomes a trackpad on a phone, and a second person opening the console can see who is driving and ask for the keyboard.
tags: console, mobile, input
date: 2026-07-28
image:
---

Two things: phones, and more than one viewer.

**Touch mode.** A phone has no pointer to map, so pretending it does makes the
console unusable. On a touch screen the picture is now a trackpad: one finger
moves the pointer, a tap is a left click, two fingers tapped is a right click,
two fingers dragged scrolls, and a long press then drag holds the button down.
An on-screen keyboard types through the target's own layout, the way paste
already did. It turns itself on when the browser reports a coarse pointer, and
there is a Touch button if it guesses wrong.

**One driver at a time.** Before this, every new viewer silently took the
keyboard from whoever had it, and the person who lost it had no idea. Now the
first client holds control and keeps it. A second viewer sees a banner saying
somebody else is driving, with a "Take control" button. Taking control demotes
the previous holder to a viewer instead of throwing them out, so they keep
watching and can ask for it back.

[Release v.0.10.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.10.0)
