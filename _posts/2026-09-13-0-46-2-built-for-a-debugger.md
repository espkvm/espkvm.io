---
title: Compiled for a debugger all along
description: 0.46.2 is the first build at -O2. Also why a device with 314 KB of free RAM could not find 155 KB of it, and a watchdog that now reboots instead of writing a warning.
tags: video, diagnostics, update
date: 2026-09-13
---

0.46.2 has no new feature. It has three things I should have done a long time
ago, found in one evening of reading the build configuration instead of the
code.

## -Og

ESP-IDF compiles at `-Og` by default. That is the setting for a debugger: it
keeps variables where a debugger can watch them and skips most of what an
optimiser would do. Every release so far was built that way - the capture path,
the frame conversions, TLS, all of it.

0.46.2 is built at `-O2`. The frame rate at 1080p is the same 22 fps, because
the encoder is hardware and was never the bottleneck. What changes is everything
that runs on the CPU beside it: the pixel-format conversion, the text-screen
scanner, the TLS handshake, the web server.

The compiler also found a bug the moment it had a reason to look. The Home
Assistant state message was built in a buffer sized for a short screen alert.
Since 0.41 the alert names every matched phrase at once, and with a long list
the JSON would have ended mid-field and been thrown away by the broker's
consumer. The buffer fits the worst case now, and a payload that still does not
fit is not sent at all.

## 314 KB free, 132 KB usable

The H.264 encoder wants about 155 KB of internal RAM in one piece for its
reference frame, and the component has no PSRAM fallback for it. Twice in
0.46.0 a rebuild of the encoder failed with the log showing 314 KB free and the
longest run 132 KB.

The holes came from the network. The allocator sends anything up to 16 KB to
internal RAM first, and 16 KB is exactly a TLS record buffer. Every connection
the browser opened carved 20 KB out of internal RAM and handed it back later,
and after enough of them there was plenty free and none of it contiguous.

The threshold is 4 KB now, so TLS buffers live in PSRAM. Anything that needs
DMA-capable memory asks for it explicitly and is not affected. After seven hours
of streaming the longest free run is 160 KB and has not moved.

The diagnostics report both numbers now, `internalFree` and `internalLargest`,
because the second one is the one that mattered and nothing showed it.

## A hung task is a reboot now

The task watchdog was enabled, but it watched only the idle tasks, and when it
fired it wrote a warning and carried on. A capture loop or a USB worker stuck in
a call would have been a black screen until somebody pulled the plug.

The capture loop, the encoder and the USB worker are under the watchdog now, and
a hang is a restart with a core dump in flash rather than a black screen. Ten
seconds, because a codec switch may legitimately wait five for a slow viewer to
let go.

One more fix. A failed H.264 start at boot fell back to MJPEG and saved that as
the preference, so H.264 was never tried again. It falls back for that boot only.

[Release 0.46.2 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.46.2)
