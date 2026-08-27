---
title: 0.29.0 - you can watch an update happen
description: The console takes over the screen during an update, names the step it is on, and afterwards says which version actually came back.
tags: update, console
date: 2026-08-22
image:
---

Installing firmware used to be a progress bar and then a long silence.

The console takes over the screen: the steps, the one it is on now, and a fan of
rays filling as it goes. Writing the image and restarting have nothing to
measure - the device is busy and not talking - so those fill against how long
they usually take and then turn into a sweep, instead of sitting at 100% and
looking stuck. Restarting from Settings and switching the network show the same
screen.

And when it is over, the console says which version came back. A restart ends
the session, so an update that rolled back used to look exactly like one that
worked, and you found out days later. Now it tells you: "came back on 0.28.0,
not 0.29.0". Asked for by [@petrn](https://github.com/petrn) in
[#23](https://github.com/orgs/espkvm/discussions/23).

[Release v.0.29.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.29.0)
