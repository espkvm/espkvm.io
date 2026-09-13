---
title: A macro that waits
description: 0.47.1 adds runbooks that wait for words on the screen, DuckyScript, a cron scheduler and push notifications with a screenshot - all running on the device.
tags: input, screen-text, home-assistant, console
date: 2026-09-13
thumb: /assets/blog/0-47-1-a-macro-that-waits/ducky-logo.webp
---

0.47.1 is about the device doing things on its own. Until now it could send a
macro and read a text screen. Now it can put the two together and wait.

## Runbooks

A runbook is a macro with two new lines. `wait Press F2` holds until a row of
the screen says so, `gone Loading` until it stops saying so, and `timeout 120`
sets how long to hold. It runs on the device, so it carries on with the browser
closed, and it fails with the line it was on when a phrase never turns up.
Enter the setup, pick the boot device, answer an installer: the sort of thing
that used to need somebody watching.

Waits only see a text screen. On a picture they wait out their timeout and say
so. Each runbook is a button in Home Assistant, with a sensor saying how the
last run went.

## DuckyScript

![DuckyScript is Hak5's payload language for the USB Rubber Ducky. The name and the duck are theirs.](/assets/blog/0-47-1-a-macro-that-waits/ducky-script.webp)

Paste a Hak5 payload into a macro or a runbook and it runs as-is: `REM`,
`STRING`, `DELAY`, `DEFAULT_DELAY`, `REPEAT`, and chords like `GUI r`. It is
recognised by its upper-case verbs, so there is nothing to switch. Keyboard
only.

## A scheduler

Five-field cron lines that fire Wake-on-LAN, an ATX button, a runbook or a
restart. It needs a wall clock, so it sets one over SNTP - a server on the
local network is fine, no internet needed - and does nothing, and says so,
until the clock is set.

## Push notifications

When a watched phrase appears, or the screen goes blank, the device sends a
message to Telegram or a webhook. On the MJPEG codec the screenshot goes with
it, and the tail of the device log can too, so the alert carries what explains
it. Off by default, on its own low-priority task, and it borrows nothing from
the encoder's internal RAM.

The script language is written up in one place: [espkvm.io/scripts](/scripts/).

[Release 0.47.1 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.47.1)
