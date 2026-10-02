---
title: 0.57.0 - a clock, 2FA, and alerts that wait
description: An optional DS3231 clock module keeps the time across a restart with no network, sign-in can ask for a code from an authenticator app, and alerts wait for the network instead of being lost.
tags: security, hardware, notifications
date: 2026-10-02 23:00
image: /assets/blog/0-57-0-a-clock-2fa-and-alerts-that-wait/hero.webp
---

## A clock that survives a power cut

The ESP32-P4 forgets the time when it loses power. Until it reached an NTP
server or a browser signed in, it did not know the date, and file names on the
card and two-factor codes need it. Now you can fit
a DS3231 module on the capture board's I2C bus. On the [Function EV](/boards/funcev/)
and the Waveshare boards that is pins 1, 3, 5 and 9 of the 40-pin header, so a
"DS3231 for Pi" module plugs straight on. The device finds it at start-up and
sets its clock from it. When it learns the time from NTP or from a browser, it
writes it back to the chip.

I pulled the cable on my Function EV several times. Each time the clock came
back within a second of the real time. Diagnostics also shows the temperature
from the chip's thermometer.

The clock chips it knows:

| Chip | Common modules | Found by itself | Tried on hardware |
|---|---|---|---|
| DS3231, DS3231M | ZS-042, "DS3231 for Pi", ChronoDot v2, Adafruit DS3231 | yes | yes |
| PCF8563, BM8563, RTC8563 | M5Stack Unit RTC | yes | not yet |
| PCF85063 | | no, name it in Settings | not yet |
| PCF8523 | Adafruit PCF8523 | no, name it in Settings | not yet |

The chip is picked in Settings -> System -> Clock, and there it can also go on
pins of its own instead of the capture board's bus. A DS1307 is not supported.

## Two-factor sign-in

Settings -> Security can now ask for a six-digit code from an authenticator
app after the password. You scan a QR code the device draws, and you get eight
one-time recovery codes for a lost phone. The board's reset button turns it
off together with the password.

## Alerts that wait

A notification that could not go out used to be lost. Now it waits, up to 50
of them, and goes out when the server can be reached again, with the time it
really happened. With a microSD card they survive a restart too.

## Smaller things

- Updates now come from fw.espkvm.io. The old address redirects, so older firmware keeps updating.
- The console asks once whether to turn on update checks, which are off by default.
- A console left open through a restart now shows the sign-in form. Before, its buttons just did nothing.
- The DFRobot FireBeetle 2 is confirmed on hardware.
- Tailscale links are steadier, with fixes from the microlink contributors.

[Release notes on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.57.0)
