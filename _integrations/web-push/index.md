---
name: Web Push
title: ESP-KVM alerts on your phone, without an app
page_title: IP-KVM alerts on a phone with Web Push, no app or account - ESP-KVM
description: ESP-KVM sends alerts to your phone or laptop as browser notifications: a phrase on the screen, a blank screen, a dashcam clip, a Tailscale key about to run out. No app, no account, no bot.
tip: Alerts on your phone, as browser notifications
summary: Alerts on a phone or laptop, with no app and no account.
mark: mark.svg
order: 6
foot: none
link.How notifications work: https://github.com/espkvm/espkvm/blob/main/docs/NOTIFICATIONS.md
link.Try the console: https://demo.espkvm.io/
---

The console can sign a browser up for notifications. After that, alerts from the device show up on that phone or laptop like any app's, also with the console closed. A tap on one opens the console. Nothing has to be installed or registered anywhere. Notifications are off by default.

## What it needs

- **HTTPS with a certificate the browser trusts.** Browsers allow notifications only on a trusted page. Either trust the device's own authority once, or turn on the Let's Encrypt certificate over Tailscale. Both are in the [setup guide](https://github.com/espkvm/espkvm/blob/main/docs/SETUP.md#https-and-the-devices-certificate).
- **A way out to the internet** from the device. Each message goes to the browser's push service, which wakes the browser.
- **A browser that does Web Push:** Chrome, Edge, Firefox or Safari.

On an iPhone or iPad, add the console to the Home Screen first and open it from there. Safari offers notifications only to a page opened that way.

## Setting it up

1. Open the console in the browser that should get the alerts.
2. In Settings, Notifications, turn on Send notifications.
3. Press Send them to this browser and allow notifications when the browser asks.
4. In the table under What goes where, tick what browsers get.
5. Save, then press Send a test in the Automation panel.

Do the same on each phone or laptop. Up to 8 browsers can be signed up, and the list under the button has a Remove for each.

## How it works

The device makes its own key the first time and signs each message with it. Each message is encrypted for one browser, so the push service of Google, Mozilla or Apple carries it but cannot read it. A browser that unsubscribed on its own is dropped at the next send.

## Good to know

- A push message carries only text, a few hundred bytes. For the screenshot with the alert, use [Telegram](/integrations/telegram/) or [ntfy](/integrations/ntfy/).
- An alert that cannot go out waits and goes out later, oldest first. With a microSD card it survives a restart.
- The same alerts can also go to Telegram, to a [webhook](/integrations/webhook/) and to [ntfy](/integrations/ntfy/), in any mix.
