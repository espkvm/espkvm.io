---
title: The card and the radio
description: 0.48.0 lets the microSD card and WiFi run together, keeps the video alive when the HDMI signal comes back, lets H.264 be switched on after boot, and adds a Sign out button.
tags: storage, video, hardware, community
date: 2026-09-14
---

0.48.0 is mostly fixes. One of them came from a contributor, and it turned out
to cover every board with WiFi, not only the NANO.

## microSD and WiFi at the same time

On boards with WiFi, the radio is a separate ESP32-C6 chip on an SDIO bus. The
microSD card is on SDIO too. Both were set up on the same SDMMC slot, slot 1.
So in WiFi mode the card stayed unmounted, and the README said you could have
one or the other.

@Crisspii hit this on the NANO and sent a fix in
[#46](https://github.com/espkvm/espkvm/pull/46). While reviewing it I checked
the pins on the other boards. On every board with WiFi the card sits on the
pins of slot 0, so the card can simply use slot 0. The two slots share one
controller, and the driver handles that.

So the card now takes slot 0 when it is wired to the slot 0 pins, and uses
slot 1 otherwise. On a Function EV board in WiFi mode the log shows the card
mounted and the C6 coming up on the same controller a moment later.

## Video after the target's screen sleeps

A P4-ETH lost its picture for good after the target's screen went to sleep and
woke up again. The log said `CSI: no mem for backup buffer`.

Each time capture restarts, the camera driver frees its spare 6 MB frame buffer
and asks for it again. After some hours PSRAM is in pieces, and the largest
free block was 2.3 MB. The request failed and capture stayed off until a
reboot. The spare buffer is now one more slot in the frame ring, allocated once
at boot. I forced twelve capture restarts under an H.264 viewer to check, and
the stream did not stop.

## H.264 after boot

A board that booted on MJPEG could not switch to H.264 a minute later. The
encoder needs one 135 KB block of internal RAM at 1080p. The block is there at
boot, but browser TLS sessions soon cut it into smaller pieces. The encoder is
now built at 1.8 seconds, before the network starts, and kept whichever codec
runs.

On pre-3.0 chips the same failure also never reached the capture loop. So
nothing fell back to MJPEG, and the build was retried ten times a second. That
is fixed too.

## Smaller things

- Settings > Security shows who is signed in and has a Sign out button.
- After a watchdog or a panic, the boot line says how far the previous run got.

[Release 0.48.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.48.0)
