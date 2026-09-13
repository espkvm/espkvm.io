---
title: Twelve minutes of blocks, then twelve minutes of fine
description: The still-screen fault was an int32 overflow in the H.264 rate controller. Why raising the bitrate made it worse, how the arithmetic was checked on hardware, and why the fix is a one-line version bump.
tags: video, diagnostics
date: 2026-09-12
image: /assets/blog/0-46-1-twelve-minutes/keyframes.webp
image_alt: Keyframe size against time on a still screen at 12 Mbit/s. On esp_h264 1.3.6 the line is flat for four minutes and then falls off a cliff; on 1.4.0 it stays flat for seventeen.
---

The picture went blocky on a still screen, stayed that way for a while, and came
back on its own. 0.46.0 shipped a watchdog for it. 0.46.1 has the cause, and the
watchdog was the wrong answer.

## What it actually is

`esp_h264` is Espressif's H.264 component. Its rate controller keeps a running
total of encoded bits minus allowed bits, one addition per frame, in an `int32`
that nothing bounded.

A still screen at 1080p and 4 Mbit/s is allowed about 133,000 bits a frame and
produces about 700. So the total goes down by 132,000 every frame. At 22 frames a
second it reaches `INT32_MIN` in **about twelve minutes**, and wraps.

After the wrap the controller reads an enormous overspend, so it raises the
quantiser by one step per frame until it hits the ceiling. That is the blocks.
Twelve minutes later the counter wraps back and the picture heals itself.

Everything I had measured falls into place at once. Nothing settable moved it,
because nothing settable touches that counter. A new encoder cleared it, because
a new controller starts at zero. And raising the bitrate did not help because a
bigger budget means a bigger gap every frame - it makes the wrap come sooner.

There is a second bug in the same function. The clamp on the other error term is
written `CLIP3((int)err_sum, -5, 5)` while the macro is `CLIP3(min, max, v)`, so
it evaluates `5 > -5` for every input and returns the constant `-5`. That term
never did anything.

## Checking it on hardware

A theory that explains what you already saw is cheap. This one makes a
prediction: the time to the wrap is inversely proportional to the configured
bitrate. Triple the bitrate and the collapse should arrive three times sooner.

So: 12 Mbit/s instead of 4, still screen, watchdog switched off, and watch the
keyframes.

The keyframes sat at 126.6 KB for four minutes, then 85.4, then 27.2. Predicted
244 seconds, measured between 184 and 245. At 4 Mbit/s the same collapse takes
twelve minutes. That is the cause, not a correlation.

The green line is the same seventeen minutes after the fix.

## The fix

Espressif had already fixed it. `esp_h264` 1.4.0 widens the counter to 64 bits,
saturates it at one second of budget, and corrects the argument order in that
clamp. I was on 1.3.6 because the version was pinned in the lock file.

So the fix is one line: the floor moves to `^1.4.0`. No fork and no patch.

## The watchdog was dangerous

0.46.0's guard rebuilds the encoder when keyframes collapse. Twice yesterday that
rebuild failed and took H.264 with it - the device fell back to MJPEG and stayed
there until a restart.

The encoder's reference frame wants one contiguous block of internal RAM, about
135 KB at 1080p, and the component has no PSRAM fallback for it. Releasing a
135 KB block does not reliably leave a 135 KB hole: the log caught it at 314 KB
free with the longest run 132 KB. Three kilobytes short, and the codec is gone.

The guard stays, because a net that never fires costs nothing. But it measures
what the encoder took on the open that worked - 155 KB on this board - and
refuses to rebuild unless that much is free in one piece. A picture in blocks is
better than no picture at all.

## Two more, found while chasing it

**The mouse jiggler had never worked.** It nudges the pointer one pixel and
straight back so the target counts it as activity. The input queue coalesces
motion that is waiting to go out, which is right for a hand on a mouse and wrong
here: the two halves added up to zero and the target received a report with no
movement in it, which its input layer drops. The counter said 1245 nudges while
the screen it was meant to keep awake went dark anyway. Two nights of watching
measured nothing because of it. A nudge is now marked so it cannot be folded into
its neighbours, and the target stayed awake for the first time.

**A console tab left open erased the log.** When its session expires the tab
keeps reconnecting every thirty seconds, which is deliberate. Each refused socket
wrote two warnings, though - 875 of them overnight, enough to flush the 200-line
log ring in under an hour. So the log I was keeping to catch the video fault no
longer had the video fault in it. The refusal is logged once and then at most
once a minute with a count of what it skipped.
