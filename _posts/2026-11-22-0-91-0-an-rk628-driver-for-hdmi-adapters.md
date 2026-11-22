---
title: 0.91.0 - An RK628 driver for HDMI adapters
description: A driver for the Rockchip RK628H HDMI bridge on the Waveshare, Radxa and WarpKVM adapters, not yet run on hardware. And the console's first translation, Belarusian.
tags: hardware, console
date: 2026-11-22 22:00
image: /assets/blog/0-91-0-an-rk628-driver-for-hdmi-adapters/hero.webp
---

Someone asked in Discussions for the Rockchip RK628 bridge to be supported. It sits on the [Waveshare HDMI to CSI Adapter (B)](/boards/waveshare-rk628/), on [Radxa's 4K HDMI IN adapter](/boards/radxa-hdmi-in/) and on the open-hardware [WarpKVM boards](/boards/warpkvm-rk628-22p/). This release has a driver for it. I have none of these boards, so it has never run on one, and it may not work.

## Why write it without the board

The C790 does the job for me. But some people already have an RK628 adapter, or find one easier to get than a C790. A driver that has not run yet is still a better start for them than none: one log from a real board shows what is wrong.

## What it does

- **It finds the chip by itself.** Every image carries the driver, and the firmware looks for it after the TC358743 and the LT6911D. Nothing to set.
- **1080p over two lanes.** The chip sends at 1296 Mbit/s on two CSI lanes, which carries 1080p60. A faster source is scaled down to 1080p on the chip. It does not bring 4K: the ESP32-P4 has two lanes, and 4K30 needs four.
- **The same EDID choices** as the TC358743, the monitor name included.
- **Sound over I2S**, wired to the P4 like the C790's.
- **HDMI-CEC** through the chip's own controller, if the board wires the CEC pin to it. Whether these boards do, I do not know.
- ~~**A rev 3.x ESP32-P4 only.** The chip sends only YUV422, and the images for rev 1.x boards capture RGB888. On a rev 1.x board the log says so and the picture stays off.~~ Since [0.91.1](https://github.com/espkvm/espkvm/releases/tag/v.0.91.1) a rev 1.x board takes it too, MJPEG only.

It is written from what Rockchip's own Linux driver does. That driver is GPL, so I took the facts from it and no code.

## If you have one

Flash 0.91.0, plug the adapter in and send me the log lines tagged `rk628`, from start-up to a source plugged in, in [Discussions](https://github.com/orgs/espkvm/discussions/11) or an issue. Whether the picture comes up or not, that log is what gets it to "tested".

## The first translation

The console is now in Belarusian too: Settings, UI, Language.

It is also the first language to arrive without a firmware release. A translation now reaches fw.espkvm.io as soon as it is merged, so the next one will not wait for a new version. To translate the console into your language, see the [translations page](/translations/), and open an issue first so two people do not take the same language.

The release: [v.0.91.0](https://github.com/espkvm/espkvm/releases/tag/v.0.91.0).
