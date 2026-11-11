---
name: ntfy
title: ESP-KVM alerts through ntfy
page_title: IP-KVM alerts on your phone through ntfy, with a screenshot - ESP-KVM
description: ESP-KVM sends alerts to an ntfy topic, on ntfy.sh or your own server, and the ntfy app shows them on your phone with a screenshot. A phrase on the screen, a blank screen, a dashcam clip, a new release.
tip: Alerts to the ntfy app, with a screenshot
summary: Alerts to an ntfy topic, on ntfy.sh or your own server.
mark: mark.svg
order: 7
link.How notifications work: https://github.com/espkvm/espkvm/blob/main/docs/NOTIFICATIONS.md#ntfy
link.Try the console: https://demo.espkvm.io/
---

ntfy is a small open-source service for push notifications: you post a message to a topic, and every phone subscribed to that topic gets it. There is no bot to make and no account needed on ntfy.sh, and you can run the server yourself. Messages go from the device straight to the ntfy server. Notifications are off by default.

## Setting it up

1. Install the ntfy app on your phone and subscribe to a topic. On ntfy.sh, anyone who knows a topic's name can read it, so make the name long, like `espkvm-7f3k9q2m`.
2. In the console open Settings, Notifications, and turn on Send notifications.
3. Put the topic's full address in ntfy topic: `https://ntfy.sh/espkvm-7f3k9q2m`, or the same on your own server.
4. If the topic needs a login, put an access token (`tk_...`) or `user:password` in ntfy access token.
5. In the table under What goes where, tick what ntfy gets. Everything but the blank screen is ticked to start with.
6. Press Test under the ntfy column of the table. It sends to ntfy only.

The token stays on the device and is never sent back to the console.

## What sends an alert

The same events as every other channel, each a row in the table:

- **A phrase on the screen**, such as `kernel panic` or `Press F1`, from Watch the screen for words.
- **A blank screen**: a stop screen, a display gone dark. Not ticked to start with.
- **A screen area** that fires.
- **A dashcam clip**, named with its file on the card.
- **The Tailscale key** running out soon.
- **The target's log**, a line with a watched word.
- **New firmware**: with Offer firmware updates on, the device looks once a day for a newer release and says so once.

## What comes with it

The screenshot from the moment of the alert goes as an attachment. ntfy.sh takes attachments. A self-hosted server takes them only when attachments are turned on in its settings. Where it does not, the device sends the same message again as text, so nothing is lost but the picture.

## When the network is down

An alert that cannot go out waits and goes out later, oldest first. With a microSD card it waits on the card and survives a restart, and a late message says when it happened.

## Good to know

- The same alerts can also go to [Telegram](/integrations/telegram/), a [webhook](/integrations/webhook/) and [browsers](/integrations/web-push/), in any mix.
- A dashcam clip is not uploaded to ntfy. It stays on the card, and with an [upload folder](/integrations/webdav/) set it can go to your NAS on its own.
