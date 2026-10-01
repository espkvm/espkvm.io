---
title: 0.56.2 - Wi-Fi that holds a stream
description: Over Wi-Fi the P4 ran out of internal RAM as soon as the console loaded. Two buffers moved to PSRAM, and a FireBeetle 2 that stalled now streams without a break.
tags: network, video, update
date: 2026-10-01 12:00
---

## The report

[#63](https://github.com/espkvm/espkvm/issues/63) came from the first person to
run ESP-KVM on a [DFRobot FireBeetle 2](/boards/firebeetle2-p4/). Capture and USB
worked. Wi-Fi did not hold: under a 1080p stream the log filled with
`mempool OOM`, TLS write errors and dropped WebSocket frames.

0.56.1 fixed one part: that board has no pull-ups on the SDIO lines to its
ESP32-C6, so the firmware now turns on the chip's own. The stall stayed.

## Finding it on my own board

My [Function EV](/boards/funcev/) has a C6 too. I read its flash over the
programming header, and it turned out to hold the same esp-hosted image as the
FireBeetle's, byte for byte. So I could reproduce the report at home.

A firmware build that logged internal RAM once a second showed it. Before the
HDMI cable was even in, loading the console took internal RAM from 85 KB to
1 KB, and the TLS server stopped opening connections. Two things were holding
it:

- esp-hosted took a buffer for every packet to the C6 from internal RAM. Its own "prefer PSRAM" setting did not reach that allocator.
- lwIP kept every sent TCP segment in internal RAM until the browser acked it.

Over Ethernet the acks come back almost at once, so neither piles up. Over
Wi-Fi they come later, and a page load with several connections is enough.

Both now go to PSRAM. The lowest point in the same test is about 50 KB. Every
board with a Wi-Fi chip gets this, in Wi-Fi mode and on the setup hotspot.

I also turned off Wi-Fi power saving. By default the C6 woke its radio every
third beacon, about 300 ms.

## The numbers from the FireBeetle

The reporter flashed 0.56.2 and counted the same session:

| Over one session | 0.55.1 | 0.56.2 |
|---|---|---|
| `mempool OOM` | 156 | 0 |
| TLS write errors | 60 | 0 |
| failed WebSocket sends | 50 | 2 |

The picture now runs without a break, at about 9 fps of 1080p MJPEG over Wi-Fi.
So the FireBeetle 2 moves to the boards that have run on real hardware.

## Updating the C6 itself

I also tried the other obvious fix: putting a newer esp-hosted into the C6 from
the P4, over the same SDIO link. That works. The 2024 image accepts it, and its
old bootloader starts the new one. But esp-hosted 3.0.9's faster SDIO mode then
stalled under video, while the factory image ran clean once the RAM was fixed.
So that code is in the firmware, switched off, until I know why.

[Release notes on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.56.2)
