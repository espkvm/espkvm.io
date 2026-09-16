---
title: 0.49.1 - the rest of the boards, and a faster virtual drive
description: Every board with a card slot now turns on the slot's regulator, the target reads the virtual drive at 9 MB/s instead of 5.6, and swapping the image reaches the target without re-plugging the cable.
tags: storage, media, hardware
date: 2026-09-16
---

The last post ended on an open question. The microSD card turned out to be slow
because the firmware never switched on the regulator that powers the slot's
pins, and I had only proved it on the two boards on my desk. Nine more boards
have a card slot, and I did not know how they were wired.

## They are all wired the same way

I read the schematics. On the NANO, the NANO-WIFI6-DB, the WIFI6, the
WIFI6-DEV-KIT, the Module-DEV-KIT, the WIFI6-POE-ETH, the Guition M3-Dev, the
FireBeetle 2 and the VIEWE P4-Pi, the slot's pins are fed from the chip's LDO 4
- the same as on the Function EV and the P4-ETH. So they all start at 40 MHz
now, and the ones with a rev 1.3 chip can write the card as well.

I have not run this on any of those nine. A schematic is not a measurement. But
the risk is small: when a card cannot keep up, the device steps the clock down
by itself, to 20, 10, 4 and 2 MHz, and the Media panel shows where it settled.
Before this, they all sat at 4 MHz whether they needed to or not.

The M5Stack Unit PoE-P4 is left alone. It has no card slot.

## The target reads the drive faster

USB asks for 4 KB at a time. Sending a fresh command to the card for every 4 KB
cost more than moving the data did. So when a read follows on from the last one,
the device now takes 256 KB off the card at once and answers the next requests
out of that.

| | Before | After |
|---|---|---|
| Whole card, read by the target | 5.6 MB/s | 9 MB/s |
| An image file, read by the target | 5.7 MB/s | 7.5 MB/s |

The same on the Function EV and the P4-ETH. Writes drop the buffer, so the
target never reads a block it has just overwritten.

## Swapping the image reaches the target

Choosing another image, or handing over the whole card, did nothing visible
until the USB cable was pulled and put back: the target went on reading the old
disk at the old size. SCSI has a way to say the medium changed, and the device
never sent it. It does now, and the target picks up the new size and partitions
in a couple of seconds.

## Sign out, where you can find it

It was in Settings, under Security. It is now on the rail on the left, under the
gear, and it asks first.

[Release 0.49.1 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.49.1)
