---
title: 0.49.0 - microSD at full speed
description: The microSD card now runs at 40 MHz on the Function EV and the P4-ETH, the P4-ETH can write it, and an upload through the console is fifty times faster than before.
tags: storage, media, hardware
date: 2026-09-15
---

Until now the microSD card was the slow part of this KVM. I wrote it off as a
limit of the ESP32-P4 and put it in the README. It was not a limit of the chip.
It was three problems in my firmware, and all three are fixed.

## Before and after

| | Before | After |
|---|---|---|
| Function EV, card bus | 4 MHz | 40 MHz |
| Function EV, card read | ~1.5 MB/s | ~8.5 MB/s |
| Function EV, card write | ~780 KB/s | ~4 MB/s |
| P4-ETH, card bus | 4 MHz | 40 MHz |
| P4-ETH, card read | ~1.5 MB/s | ~9 MB/s |
| P4-ETH, card write | read-only | ~4 MB/s |
| Upload from the console, Function EV | 64 KB/s | ~3.5 MB/s |
| Upload from the console, P4-ETH | not possible | ~1.5 MB/s |
| A 2.7 GB image through the console | about 12 hours | 21 minutes |

Uploads are over Ethernet. Before, the P4-ETH card had to be filled in a card
reader.

## The card had no power on its pins

On both boards the pins of the card slot get their power from one of the
chip's own regulators, LDO 4. My code never turned it on. The card still
answered, so it looked like a slow bus. Reads failed above 4 MHz, and on the
P4-ETH's rev 1.3 chip every write timed out.

With the regulator on, the card runs at 40 MHz on both boards, and the P4-ETH
writes. I checked the writes with CRC: files of 64 MB of random data came back
byte for byte.

## Uploads waited for a timer

An upload came in at 64 KB/s whatever the network. The TCP receive queue held
six packets. When a burst filled it, the network stack dropped the rest until
its next timer, 125 ms later. Six packets every 125 ms is 64 KB/s. The queue now
holds a whole TCP window. The card is also written by a separate task, so the
network does not wait while the card writes.

![An upload from the console on the Function EV, at 3.3 MB/s](/assets/blog/0-49-0-microsd-at-full-speed/upload-chart.webp)

## The SD driver

Now and then a write never finished, and the SD controller then took no
command at all. I found several bugs in the SD driver from ESP-IDF 6.1 and keep a
fixed copy in the project. A failed transfer now resets the controller, stops
the card and is tried again.

## Every card gets its own speed

Boards and cards differ, so the device does not trust one number. It starts at
the fastest clock the board allows and steps down to 20, 10, 4 and 2 MHz when
the card fails. When the card is idle, it tries one step up again. The Media
panel shows the speed it settled at, and Settings can cap it.

## Pause the video while you upload

The video encoder and the Ethernet chip share a bus inside the chip. At full
frame rate the upload drops to a tenth. So during an upload the video goes down
to 2 frames a second, and the Media panel has a link to pause it for the full
speed.

The other boards are not checked yet. They start at 4 MHz, as before. If one
of them has the same regulator wiring, it will get the same speed.

[Release 0.49.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.49.0)
