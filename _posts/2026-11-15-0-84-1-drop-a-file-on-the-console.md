---
title: 0.84.1 - Drop a file on the console
description: Ethernet boards no longer run out of memory when a phone watches over a slow link. Files can be dropped on the console, and the popups on the left work again.
tags: console, network, media
date: 2026-11-15 12:00
---

A phone over Tailscale on mobile data could run a JetKVM Mini or a P4-ETH out of internal memory, and the console then said it could not reach the device. The network buffers now go to PSRAM on every board, as they already did on the Wi-Fi ones. If memory still gets short, the device drops idle request connections first, and the picture keeps going. A yellow mark next to HDMI and USB says so until it is over.

Drag a file over the console and it splits in two. The left half puts the file on the microSD card. The right half takes a text file and types it on the target, after you check it in the Input panel.

Smaller things:

- The screen of a phone or tablet stays on while the picture plays.
- The console installed as an app shows unread notifications as a number on its icon.
- With the mouse captured in Chrome, your computer no longer adds its own acceleration on top of the target's.

Fixed:

- The temperature, OS and power popups on the left, broken in 0.84.0.
- In Chrome on Android, the keyboard button needed two taps after the keyboard was hidden with Back.
- A session that ended while the console was opening showed "Cannot reach the device" instead of the sign-in form.
- The sign-in cookie ran out 12 hours after the sign-in even while the console was in use.

The full list is in the [changelog](https://github.com/espkvm/espkvm/blob/main/CHANGELOG.md).
