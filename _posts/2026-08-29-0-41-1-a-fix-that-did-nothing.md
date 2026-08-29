---
title: 0.41.1 - a fix that was there and did nothing
description: I shipped a WiFi fix and never called the function. The person who reported the bug found the missing line himself - and while checking that release I found a crash that had been hiding behind three different symptoms.
tags: hardware, network, video
date: 2026-08-29
image:
---

The Waveshare ESP32-P4-WIFI6 pulls its six SDIO lines up through 51k where
Espressif ask for 10k. One of those lines is how the WiFi co-processor says it
has data, and a weak pull-up is enough to lose that. The ESP32-P4 has pull-ups
of its own inside, so 0.40.1 switched them on for that board.

It did nothing. I had written the function and the setting, and never called the
function. The person who reported the stall flashed it, saw no change, went and
read the code, found the missing line, and sent the patch. With the call in
place: resets, reassociations, ten disconnect cycles, a hundred requests in a
row, no errors, at the full bus speed. So 0.41.1 is his line, plus one of mine -
the components I maintain here now fail to build if they contain a function
nothing calls. The warning had been sitting in the build log all along.

Then, while checking that the release changed nothing else, the device rebooted
on me. Closing a tab that was watching the H.264 stream could take the whole
device down: the task pushing video was still writing a frame into a TLS session
the web server had already freed. The crash landed later, in whatever asked for
memory next, which is why the same bug had looked like three different ones over
the past week - a dead web interface, a failed update, a stream that stopped. A
build with heap poisoning on named the freed object at the moment of the bad
write. Sends and session teardown now take the same lock: twenty-four forced
disconnects in a row, no crash, where the same build without the fix died on the
second.

[Release v.0.41.1 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.41.1)
