---
title: 0.38.0 - a mouse jiggler
description: A machine left alone locks its screen, and then what you were watching is behind a password. One pixel, there and back, as often as you like.
tags: input, console
date: 2026-08-27
image:
---

You leave a machine running something long, come back, and the screen is locked -
so the thing you wanted to look at is behind a password you now have to type
over a KVM.

Set an interval in Settings and the device nudges the pointer one pixel and puts
it straight back that often. Nothing moves on screen, and the target counts it as
somebody being there.

It runs on the device, not in the browser, and on purpose: the case it exists
for is a machine nobody is sitting in front of, and a jiggler in a browser tab
goes away with the tab. It stands aside whenever you are using the mouse
yourself, and does nothing when no target is attached. Off by default.

The rest of the release is the update popup: it no longer sits lit up behind the
full-screen restart panel with its own progress bar visibly filling through the
frosting, and long version names no longer push it wide enough to scroll
sideways.

[Release v.0.38.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.38.0)
