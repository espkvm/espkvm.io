---
title: 0.1.2 - the first working KVM
description: The first tagged builds. HDMI capture, a keyboard and mouse the target cannot tell from real ones, a web console over HTTPS, and updates over the network.
tags: hardware, video, input
date: 2026-07-23
image: /assets/blog/0-1-2-the-first-working-kvm/diagram.svg
---

Two small boards, about thirty dollars of hardware, and a machine you can see
and drive from a browser when it has no working operating system.

What the first releases already do:

- capture the target's HDMI output, and follow it when the resolution changes;
- send the picture as MJPEG, or as H.264 encoded by the chip itself;
- act as a USB keyboard and mouse, so the target needs no software and no agent;
- serve a web console over HTTPS, with a login and a password reset done by holding the board's button;
- stop the video if the chip gets too hot, rather than getting hotter;
- install new firmware over the network, and roll back on its own if that firmware does not come up;
- mount a microSD card and report what is on it, which is what virtual media is built on a day later.

0.1.1 was the plumbing around all of that: the release pipeline, the update
manifest, and the flasher that writes a board from the browser.

[Release v.0.1.2 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.1.2)
