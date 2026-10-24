---
title: 0.69.0 - Faster memory, faster H.264
description: On boards with a rev 3.x chip the memory now runs at 250 MHz instead of 200, and 1080p H.264 goes from 22 to 27 frames a second.
tags: video, hardware
date: 2026-10-24 12:00
image: /assets/blog/0-69-0-faster-memory-faster-h264/hero.webp
---

On a rev 3.x chip, 1080p H.264 ran at 22-24 frames a second. I wanted to know what holds it there.

The encoder was busy 96-99 % of the time, so it is the limit. A 1080p frame took 43 ms. For each frame the encoder reads the picture and a reference frame from PSRAM and writes the result back, so I looked at the memory first.

## 250 MHz instead of 200

The PSRAM sits inside the ESP32-P4 package. On rev 3.x chips it can run at 250 MHz; on rev 1.x the limit is 200, and the build system does not offer more. With 250 MHz a frame takes 36 ms instead of 43.

I measured both builds on the same Function EV, one after the other, with "Measure the delay" in the console: the pointer moved on the target until the browser shows it. The H.264 went over WebRTC.

| 1080p H.264 | 200 MHz | 250 MHz |
|---|---|---|
| Encode a frame | 43 ms | 36 ms |
| Frames a second | 22.5 | 26.5-27 |
| Delay, same network | 150 ms | 118 ms |
| Delay, phone network over Tailscale | 190 ms | 174 ms |

The delay drops by more than the 7 ms the encoder saves: with frames closer together, the pointer's move gets into a frame sooner too. Over the phone network the two measurements did not get the same connection: the round trip was 23 ms while I measured the 200 MHz build and 43 ms while I measured the 250 MHz one. The 250 MHz build was faster all the same.

At 720p the encoder was not the limit before, so the frame rate stays at about 26. A frame encodes in 16 ms instead of 18.5, and the delay goes from 79 to 67 ms.

It is one line in the build settings of every rev 3.x board. Builds for rev 1.x chips are the same as before.

I ran it for ten minutes of 1080p video and then a night: 37 &deg;C under load, no errors, no restarts. I tested it on the Function EV. The other rev 3.x boards have the same chip and memory inside it, so they should get the same.

## Where 30 is

Espressif gives 30 frames a second at 1080p for this encoder, but with YUV420 input, 12 bits a pixel. The HDMI bridge sends YUV422, 16 bits. I tried giving the encoder YUV420: it was 13 % faster, not the 25 % the smaller frame suggests.

The rev 3.x chip has a block in the camera input that should turn YUV422 into YUV420 on the way in, for free. I could not get it to write anything in that mode. The other way is a second pass through the memory, and memory is what is short here. So it stays at 27 for now.

[Release 0.69.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.69.0)
