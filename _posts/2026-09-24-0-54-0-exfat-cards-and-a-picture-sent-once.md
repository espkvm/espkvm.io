---
title: 0.54.0 - exFAT cards, all keys in full screen, and a picture that left the device twice
description: A microSD card straight out of the packet works now, even above 32 GB. The console can send Alt+Tab and the Windows key to the target. And every frame had been leaving the device twice.
tags: storage, console, video
date: 2026-09-24 12:00
---

## A card as it comes out of the packet

A microSD card above 32 GB comes from the factory as exFAT, often on a GPT
partition table. ESP-KVM could read neither: the card had to be reformatted
to FAT32 on a computer first. Now both work, and the format is read off the
card when it mounts, so FAT32 and MBR cards behave as before. One file still
stays under 4 GB, on exFAT too. It costs 12 KB of flash.

## All keys in full screen

A browser keeps some keys for itself. Alt+Tab, Ctrl+W and the Windows key
never reached the target, and Ctrl+W closed the console. In full screen, with
control taken, there is now an "All keys" button. It asks Chromium for those
keys, and Esc gives them back. Firefox and Safari have nothing like it, so
they do not show the button. And closing the tab while you have control now
asks first.

## Every frame, twice

The console has two ways to get the picture: a WebSocket, and an MJPEG
stream in an image element for older paths. While the WebSocket had the
picture, the image element was hidden - but hidden is not gone. Its address
was still set, so the browser kept downloading the stream next to the
WebSocket, and every frame left the device twice. At 1080p MJPEG that was
36 Mbit/s where 17 was enough.

## Switching codecs, for good

Switching between MJPEG and H.264 could end with no picture until a restart:
each codec wants several megabytes in a few large pieces, and after hours of
work the memory was not always the shape it had been. Now both codecs share
one region taken at boot, and it is never given back. On the M5Stack at
1080p, 8 switches out of 8. On the P4-ETH a switch to H.264 at 1080p used to
be refused until a restart; now it just works.

Also: updates stick with H.264 and the dashcam running, and signing in from a
phone no longer throws out the console you are working in.

[Release notes on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.54.0)
