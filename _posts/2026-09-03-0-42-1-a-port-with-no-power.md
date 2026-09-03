---
title: 0.42.1 - the keyboard that died while the machine slept
description: A target woke from sleep with no power on its USB port, and the device could only say "USB is not active". It tells the two silences apart now.
tags: diagnostics, input, hardware
date: 2026-09-03
image:
---

The machine went to sleep. When it woke, the keyboard and the mouse were dead.

The console has a button for exactly this - it presents the keyboard to the
target again, as if the cable had been pulled and put back - and it did nothing.
Nor did pressing it twice more. Nor did restarting the device, which starts by
doing the same thing and then tries three more times on its own: four
presentations, and the target never answered one of them. Nor did pulling the
cable at the target's end, which turned out to reboot the device, because on
this board the target's five volts come back down that same lead. What worked in
the end was pulling every cable and giving the board a cold start.

By then the obvious conclusion was that something on this side gets stuck by a
sleeping host and only a power cycle clears it. That was wrong, and one number
said so. TinyUSB tracks whether there is a live bus at all, separately from
whether the target has enumerated us, and that flag was false. There was no bus.
Every re-plug had been toggling a pull-up on a wire with nobody on the other
end. The machine had suspended the bus on its way down and its port came back
from sleep without power.

Nothing on the device's end can reach that, and it should never have pretended
otherwise. So the status pill now separates the two silences: a target that has
stopped listening, which re-plugging does fix, and a port with no power, which
wants the cable re-seated at the machine or the machine restarted. The popup
offers the repair only when the repair can work. Both states are on the API too,
in `GET /api/v1/system/usbprobe`, next to the enumeration trace.

Three smaller things came out of the same afternoon. The log now writes the bus
going quiet and coming back, because a keyboard that dies over a lunch break used
to leave nothing at all behind. A re-plug asked for by hand takes a second rather
than 100 ms, since a hub is allowed to ignore a change shorter than its debounce,
and a button press has no deadline to meet. And the automatic retry no longer
spends its three attempts on a port that has no power - it waits, keeps them, and
writes one line saying why.

[Release v.0.42.1 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.42.1)
