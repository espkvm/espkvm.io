---
title: 0.41.0 - more of the KVM in Home Assistant
description: An update entity, a camera holding a still of the target's screen, the jiggler as a switch, and the numbers worth having when something is wrong.
tags: home-assistant, update, diagnostics
date: 2026-08-28
image:
---

Home Assistant shows which firmware is installed, which one is published, and a
button that installs it. For that the device had to start reading the update
manifest itself, at most once every six hours. Until now only the console did
that, from the browser, which is no use to a dashboard. The entity appears only where
the device is allowed to fetch releases. With that switched off there is none at
all, because one that can never answer is worse than nothing.

There is also a camera holding a still of the target's screen. A button takes
one, and a setting takes one by itself when the screen watch matches a phrase,
so the notification that says `kernel panic` arrives with the screen attached.
It needs the MJPEG codec, because while H.264 runs there is no still to take.
It is off by default too: a 1080p frame is a few hundred kilobytes through your
broker.

The mouse jiggler is a switch now, with its interval beside it, so you can put
it in an automation: quiet during the day, awake overnight. Turning it back on
restores the interval you had.

And the diagnostics: free internal memory and the largest unbroken block in it,
skipped frames, which firmware slot is running, and why the device last booted.
The gap between those first two numbers is what decides whether the H.264
encoder can start at all.

[Release v.0.41.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.41.0)
