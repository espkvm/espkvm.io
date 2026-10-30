---
title: 0.75.0 - A holiday in Malta and a bug
description: I went to Malta for a rest with a fix for #85 pushed a few hours before the flight. It was only half a fix: the mouse still lagged behind MJPEG video, and one number in the reporter's table showed why. Also updates on trial for a device far away, and Tailscale fixes found while living on it.
tags: video, input, update, vpn
date: 2026-10-30 23:30
image: /assets/blog/0-75-0-a-holiday-in-malta-and-a-bug/hero.webp
---

I went to Malta for a rest. The rest mostly happened in my dreams.

In [#85](https://github.com/espkvm/espkvm/issues/85) a user wrote that the picture froze in Firefox on 0.74.0. Chrome, Edge and Opera were fine. Firefox does not take my WebRTC offer, so it gets the video over the WebSocket, and that path waited too long for a keyframe after a skipped frame. I found it early in the morning, with the flight a few hours away. I wrote in the issue that I was leaving, pushed 0.74.1 and went to the airport. The reporter checked it and said the freeze was gone.

![The plane to Malta at the gate.](/assets/blog/0-75-0-a-holiday-in-malta-and-a-bug/plane.webp)

I left the laptop at home on purpose. Just in case I still packed a Samsung Galaxy Tab and had my phone. One ESP-KVM stayed on the shelf at home, about 2,200 km away, on Ethernet and Tailscale. Remote access turned out to be a great way not to rest at all.

## It came back

The next morning the issue was open again. Better, the reporter wrote, but MJPEG is now much worse than on 0.72, and now and then the picture stops for a moment. Four short videos: Firefox and Opera, 0.72 and 0.74.1.

![Evening on a balcony in Malta, with the console on the tablet.](/assets/blog/0-75-0-a-holiday-in-malta-and-a-bug/balcony.webp)

I measured it on the board at home. At 1080p MJPEG gave about 15 fps on 0.72, on 0.74.1 and on the next build, H.264 about 25. The time from a mouse move to the changed picture was the same on all of them. A real Firefox drew the same frames on both versions. I could not make it happen.

Then the reporter sent a table from the Video popup, every version and browser in a row, and a guess: maybe it is not the picture but the input. Move the mouse a lot and the moves pile up and arrive late.

In the table was the input round trip, a number I had never looked at. It is a ping from the console to the device on the socket that carries the keys and the mouse. Firefox with MJPEG on 0.74.1: 63 ms. On 0.72: 15 ms.

## The cause

In 0.74.0 I made the TLS encryption run one write at a time across the whole device. The cipher runs in software, and three viewers plus a new connection kept both cores busy long enough for a watchdog reset. Taking turns fixed that. But a turn was one whole write, and for the video that is one whole frame. A 1080p MJPEG frame is about 150 KB and takes about 70 ms to encrypt. Everything else the device's web server sent waited behind it: the answer to the ping, a status update, an API reply. While the server waited to send, it did not read the socket with the mouse moves, so they piled up.

My test scripts moved the mouse and watched the frames. They never asked the device anything else, so the server never had to wait. The console asks the device something every few seconds, and each time the input stopped.

## The fix

Now only the video takes turns. A short reply goes out at once. On my board at 1080p MJPEG, with the pointer moving and a ping every 100 ms:

| | Median | 95th percentile |
|---|---|---|
| Before | 78 ms | 288 ms |
| After | 3 ms | 7 ms |

The frame rate did not change, and three viewers at once still run without a reset. The script that measures this number is now part of my bench.

## Updating it from 2,200 km

Every update to the board at home was scary. I felt like a NASA engineer afraid to send one command too many to Curiosity. An update already went back by itself when the new image did not start. But an image can start fine and still lock me out with one mistake in the Wi-Fi or Tailscale code. The device sees itself working and keeps the update, and fixing it takes a USB cable and me in the same room.

Now an update can go on trial. After the restart the device waits for a console to come back and keep it. If nothing comes within 10 minutes, it restarts onto the version it had. By default the console that installed the update keeps it once it gets through. The Firmware popup can also ask you to check first, or skip the trial ("After an update"). Over the API it is `?trial=600` on `/api/v1/system/update`, then `POST /api/v1/system/update/keep`.

## Also in 0.75.0

Living on Tailscale turned up a few bugs in the released versions:

- After the phone restarted its Tailscale app, the connection could stay on the slow relay for good. The device now picks up the phone's new key and tries a direct path again.
- The direct path dropped to the relay every 15 s and came back a moment later. The device checked the path every 30 s but trusted it for only 15. Now it checks every 5 s.
- After WebRTC dropped once, the console stayed on the slower WebSocket until the page was reloaded. Now it tries WebRTC again after 30 s, then less often.
- The log no longer says "DISCO decrypt failed" every 15 s. It was the device's own probe coming back through an old Tailscale node of itself.

And at home:

- The Video popup shows "Shown in this tab", the frames this browser really draws. "Published" is what the device encodes. At 1080p MJPEG over HTTPS that can be 30 against 15.
- The device restarted by itself 10 s after the EDID or gamepad setting was changed by hand. Now the console asks whether to restart.
- Log level "Debug" now shows the Tailscale and HTTPS lines it promised.

[Release 0.75.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.75.0)
