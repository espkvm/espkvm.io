---
name: Telegram
title: ESP-KVM alerts in Telegram
page_title: Telegram alerts from an IP-KVM, with a screenshot - ESP-KVM
description: ESP-KVM sends alerts to a Telegram chat through your own bot: a phrase on the screen, a blank screen, a dashcam clip, a Tailscale key about to run out. The screenshot comes with the message.
tip: Alerts with a screenshot to Telegram
summary: Alerts through your own bot, with a screenshot.
mark: mark.svg
order: 5
link.How notifications work: https://github.com/espkvm/espkvm/blob/main/docs/NOTIFICATIONS.md
link.Try the console: https://demo.espkvm.io/
---

ESP-KVM writes to Telegram through a bot you make yourself. Messages go from the device straight to Telegram, with no server of mine in between. It needs only a way out to the internet. Notifications are off by default.

## Making the bot

1. In Telegram open a chat with [@BotFather](https://t.me/BotFather) and send `/newbot`.
2. Give the bot a name, then a username that ends in `bot`, such as `my_espkvm_bot`.
3. BotFather answers with a token like `123456789:AAH...`. Copy it. Anyone with the token can write as the bot, so keep it to yourself.
4. Open the chat with your new bot and press Start, or send it any message. A bot cannot write to someone who has never written to it.

For alerts in a group, add the bot to the group and send a message there.

## Setting up the device

1. In the console open Settings, Notifications, and turn on Send notifications.
2. Paste the token into Telegram bot token.
3. Press Find chats. It lists the chats that wrote to the bot lately: pick yours. A group or channel id can also be typed in by hand.
4. In the table under What goes where, tick what Telegram gets. Everything but the blank screen is ticked to start with.
5. Save, then press Send a test in the Automation panel. A message should come in a few seconds.

The token stays on the device and is never sent back to the console.

## What sends an alert

Each of these is a row in the table, so Telegram can get some and a webhook or a browser others.

- **A phrase on the screen.** Turn on Watch the screen for words under Settings, Video, and list the phrases, such as `kernel panic` or `Press F1`. The device reads a text screen even with nobody watching.
- **A blank screen.** The output stays one colour: a stop screen, a display that went dark. Not ticked to start with.
- **A screen area.** An area set up in Screen areas, with its alert on, sends one each time it fires.
- **A dashcam clip.** A clip under 50 MB comes as a video that plays in the chat. A bigger one is named, and the file stays on the card.
- **The Tailscale key.** A reminder 14 days before the node key runs out, or as many days as you set.
- **The target's log.** With Receive the target's log on, a line with a watched word sends an alert.
- **New firmware.** With Offer firmware updates on, the device looks once a day for a newer release and says so once, with a link to what changed.

## What comes with it

- A screenshot of the screen at the moment of the alert, on either codec. It can be turned off.
- The tail of the device log, if Attach recent log is on.

## When the network is down

An alert that cannot go out waits and goes out later, oldest first. With a microSD card it waits on the card and survives a restart. A late message says when it happened, and the screenshot shows the screen as it was then.

## Good to know

- The same alerts can also go to a [webhook](/integrations/webhook/), to [browsers](/integrations/web-push/) and to [ntfy](/integrations/ntfy/), in any mix.
