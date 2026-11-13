---
title: 0.83.0 - Custom firmware for the JetKVM Mini is ready
description: ESP-KVM, open-source custom firmware for the JetKVM Mini, is tested on a real Mini and ready to install. Its HDMI sound is not wired to the chip, so the device can now be a USB speaker for the target. Plus a page choice and a sleep timer for the status screen, and a new name for the helper program.
tags: hardware, boards, audio
date: 2026-11-12 23:00
image: /assets/blog/0-83-0-custom-firmware-for-the-jetkvm-mini-is-ready/hero.webp
---

Custom firmware for the JetKVM Mini is ready. The Mini has an ESP32-P4X inside, the chip ESP-KVM runs on, and JetKVM opened its firmware, so the pins were known. I had a Mini on the desk, and everything I tried works.

## What I checked on the Mini

- The picture from the HDMI input, at 1080p50.
- Ethernet, and updates over the network.
- Keyboard and mouse on the target.
- The screen and the side button that turns its pages.
- The microSD slot.
- The "Back up the flash" button on the [flasher](/flash/). I also read the flash with esptool, and the two files were the same to the byte.

The [Mini's page](/boards/jetkvm-mini/) has the steps to install it and to go back. The Mini W is the same hardware apart from its Wi-Fi, which has not run on one yet: I do not have a Mini W.

Here the Mini takes an update over the network. The screen wakes from its sleep, shows the progress, restarts and comes back with the pages I left on.

<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/o4fhGyTnafo" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

[Watch it on YouTube](https://www.youtube.com/watch?v=o4fhGyTnafo).

## Sound over USB

Sadly, the Mini's HDMI sound is not wired. The capture chip can take the sound out of HDMI and send it on three wires, but on the Mini those wires go nowhere, so the sound never reaches the P4. JetKVM's own firmware hits the same wall and works around it with a USB speaker. I had to add one too.

Turn on Settings, Audio, Sound over USB, and restart. The target gets a speaker called "ESP-KVM Speaker". Pick it as the sound output there, and what the target plays comes to the console, the recordings and the dashcam, the same way HDMI sound does.

The good part: it is in the firmware for every board, not only the Mini. Sound is now there on boards where HDMI sound is not connected at all: the M5Stack PoE-P4 with the Display In add-on, which has no audio pins, or any board where you never wired the three I2S pins.

It has limits. While the speaker is picked, the target's own speakers are quiet. A BIOS does not play sound to a USB speaker. So on a board where HDMI sound works, HDMI is still the better choice.

Thank you, JetKVM: the idea and the USB descriptor come from your firmware.

## For every board

- The status screen can go dark after a set number of seconds: Settings, Display, Sleep after. The button wakes it on the page it had, and an update or a notice lights it too. 0 keeps it on.
- You pick which pages the status screen shows: network, video, health, and the picture on a colour panel. Untick them all and it shows the ESP-KVM logo.
- When another device on the network or the tailnet has the same name, the console says so and offers to rename this one. Two boxes left at the default "espkvm" used to turn into "espkvm-1" and "espkvm-2" without a word.
- On the target the device is now called just "ESP-KVM". It was "ESP-KVM Keyboard/Mouse", and it has long been more than that.
- espkvm-agent is now ESP-KVM Tools. "Agent" today sounds like an AI agent, and this is a small helper program for the target. It lives at [github.com/espkvm/tools](https://github.com/espkvm/tools), and the [page](/espkvm-tools/) has the new install command. The device still talks to an older espkvm-agent, and the new installer removes it.

## Fixed

- A colour screen (GC9A01 or ST7789) could stop drawing after about ten minutes and then blink every few seconds. Each frame took a copy in the chip's internal memory, and once that memory ran short the frames stopped. They now go to the screen straight from PSRAM.
- A board with a card-detect switch (JetKVM Mini, M5Stack PoE-P4) tried an empty microSD slot ten times at boot and filled the log with errors. It now looks at the switch first.
- The boot log showed an error about the GPIO interrupt service. It was harmless.

[Release 0.83.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.83.0)
