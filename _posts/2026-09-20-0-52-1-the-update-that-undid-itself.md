---
title: 0.52.1 - Fixed: after an update the device rolled back to the old version
description: An update would install, reboot, and come back as the old version. The new image was never the problem - it never ran. The firmware on its way out broke the boot behind it.
tags: ota, diagnostics, video
date: 2026-09-20 21:00
---

0.52.0 went out in the evening. Within the hour: "does not start."

That is a bad report on a KVM, because the box is often the only way to reach
the machine it is plugged into. There are two firmware slots for exactly this
reason, and the fallback did work - the board was up on the previous version.
From where the operator stood, the new one simply refused to start.

## The image was fine

I flashed the released image over the cable and watched it boot. Then six more
times, five of those with the slot marked the way an update leaves it. Full boot
every time.

So the image starts. Something else rolled it back.

## The device knew

Serial on this board is the chip's own USB, and a restart makes the port
disappear - which is why nobody had ever captured the log of a failing boot.

The device keeps its own log, and that one survives a reboot. Every boot writes
what ended the run before it:

```
--- boot: v.0.52.0 ---
boot: after another watchdog (rst 0x10); running ota_1 (confirmed)
```

A watchdog, not a crash. The boot after the update hung before it could print a
line, the watchdog reset the board, and the bootloader read that second reset as
"the new image does not run".

Three updates, three rollbacks, the same line every time. It needs a picture
coming in, which is why it had looked random for weeks.

## What was actually wrong

The capture receiver writes every frame straight into memory, and at 1080p30 it
is busy nearly all the time.

An update ends with a software restart, and that is not a power cycle. The
system stops what it can on the way out, and for this transfer it simply aborts
it - but one already running on the bus cannot be stopped in the middle. So the
restart can cut a write in half, and what that leaves behind is enough to stop
the next boot dead.

The fix is to stop the receiver properly first: close the input, let the
transfer end between frames instead of inside one, then reboot. It hangs off the
restart itself, so every deliberate reboot in the firmware gets it.

Before: three updates, three rollbacks. After: eighteen in a row, not one of
them undone.

It also explains the two rollbacks I could never account for, in August and last
week. Both were written off as intermittent. They only looked that way because
they needed a signal on the input.
