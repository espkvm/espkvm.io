---
title: 0.83.1 - Power on over USB, and a menu on the screen
description: ESP-KVM can wake the target the way a keyboard key does, so a box with no ATX wires can still bring a sleeping PC back. The buttons on the box open a menu on the status screen. The JetKVM Mini gets both its buttons, and square screens turn in quarters.
tags: power, display, jetkvm
date: 2026-11-13 23:00
---

A small release, mostly for boxes like the JetKVM Mini that have no wires to the PC's power button.

## Power on over USB

A USB keyboard can wake a sleeping PC with a key press. ESP-KVM now sends the same wake signal. It is in the power menu, on the "No signal" screen, on the buttons on the box, in schedules and in Home Assistant. The API call is `POST /api/v1/power/usb`.

It always wakes a PC that is asleep. A PC that is fully off turns on only if its BIOS has an option like "Power On by USB Keyboard" and keeps the USB port powered when off. In Windows, Fast Startup has to be off for that.

## A menu on the status screen

Set a button's press or hold to "menu on the screen" in Settings, Buttons. A short press then goes to the next item and a hold picks it: power on over USB, Wake-on-LAN, the ATX buttons, a screenshot, a dashcam clip, screen off, the network mode or a restart. Reset, force off, a restart and a network change ask for a second hold. The screen says whether the action worked, and why not if it did not. The menu works on every status screen ESP-KVM drives.

## The JetKVM Mini

Both side buttons on the Mini can now be set up. The top one still flips the status pages and turns the screen off. The bottom one opens the menu. Held at start-up, it still resets the password.

## Square screens turn

The round GC9A01 and the Mini's ST7789 now turn in quarters: Settings, Display, Turned. Upright, 90° either way or upside down, for a box that stands on its side. A screen that was set upside down stays that way.

The full list is in the [changelog](https://github.com/espkvm/espkvm/blob/main/CHANGELOG.md).
