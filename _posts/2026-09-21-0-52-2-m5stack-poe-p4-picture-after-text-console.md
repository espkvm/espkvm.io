---
title: 0.52.2 - Fixed: no picture on the M5Stack PoE-P4 after the target switches to a text console
description: The picture vanished when the target switched to a text console, and the firmware had an answer for exactly that - behind a check the board could never pass.
tags: video, diagnostics, console
date: 2026-09-21 06:00
---

Someone switched the machine on the other end to a text console. The picture
went. Switching back to the desktop did not bring it back, and ten minutes
later it was still gone.

## What the chip said

The bridge on that board is an LT6911D, and it was not dead. It answered on
I2C, it gave its chip id, and it still reported a pixel clock. What it would
not give was a mode:

```
W lt6911: no mode from the chip: clk 37 MHz, 00 00 00 00 00 00 00 00
W video: HDMI signal lost (SYS_STATUS=0x00)
```

All zeros where the timings live. The chip had lost its lock on the source and
was not taking it back.

A restart of the device fixed it at once. That narrows it down, because a
restart does one thing to the bridge: it pulls its reset pin.

## The answer was already there

The firmware watches for this. A source that has gone quiet while still being
powered gets a fresh hotplug offered to it, after ten seconds, then twenty,
then forty. It is a good answer and it has been in for months.

On this board it could never run.

Two reasons, each enough on its own. The check is DDC5V - the source's own five
volts on the input - and only the other bridge this project supports reports
it. And even past the check there was nothing to do: a hotplug cycle means
pulling the hotplug line, and on this chip that line belongs to the chip's own
firmware.

So a bridge now says whether its DDC5V means anything at all, and one that
cannot tell is tried anyway, three times and then no more - a machine that has
gone to sleep on purpose should not be poked all night. A bridge with no
hotplug line of its own gets its reset pin pulled instead.

## The wrong turn

My first version answered the DDC5V question with the pixel clock. A number
there, I reasoned, means a source is driving the wire.

A few hours later the picture went again, three resets went by, and none of
them helped. The screen had simply gone to sleep - and the clock register still
read 37 MHz, which is the mode that had been playing. So the firmware had spent
the evening resetting a chip at an empty room, and the reason it looked
plausible is that the number was right for a source that was no longer there.

That is out. The driver reports no DDC5V now, honestly, and takes the bounded
three tries instead of a confident answer.

## What the reset needed

The resets were also failing for a second reason, and this one is ours.

This chip takes about two and a half seconds to lock. Reading its mode takes
its register bus away from its own firmware for thirteen transactions. Poll it
every two seconds while it is trying, and it never finishes - which is exactly
what a reset used as a recovery was doing, while the same reset at start-up
worked every time, because nothing polls yet at start-up.

After a reset the chip now gets that time to itself.

## While I was in there

Two in the console, both from the same night. A browser tab left open for hours
signed back in under "The device is restarting" - a notice from a session that
had ended long before. It is hidden by the sign-in page rather than dropped,
and the timer that would drop it does not run in a tab the browser has frozen.

Worse, the socket that would have replaced it was not coming. It backs off when
the device refuses it, and it is refused every time nobody is signed in, so by
morning it waits thirty seconds between attempts. Signing in now reconnects at
once, which also gives the keyboard and the mouse back half a minute sooner.

## Still open

Nothing the chip reports separates a screen that has gone to sleep from a chip
that has lost its lock. The driver now writes out a block of its registers each
time a mode goes, so the two can be put side by side. One of those bytes should
differ.
