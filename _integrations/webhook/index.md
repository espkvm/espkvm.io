---
name: Webhook
title: ESP-KVM alerts to a webhook
page_title: IP-KVM alerts to a webhook, for n8n, Node-RED or a script - ESP-KVM
description: ESP-KVM posts a small JSON message to a URL of yours when something happens on the target. A phrase on the screen, a blank screen, a dashcam clip, a Tailscale key about to run out. Good for n8n, Node-RED or a script of your own.
tip: Alerts as JSON to a URL of yours
summary: Alerts as a small JSON message to a URL of yours.
mark: mark.svg
order: 8
foot: none
link.How notifications work: https://github.com/espkvm/espkvm/blob/main/docs/NOTIFICATIONS.md
link.Try the console: https://demo.espkvm.io/
---

A webhook is the channel for everything that is not Telegram or a browser. The device sends a `POST` with a short JSON body to the URL you give it, and whatever answers there decides what to do next. Notifications are off by default.

## What it sends

```json
{
  "title": "Screen text",
  "message": "The phrase \"Press F1 to continue\" is on the screen.",
  "device": "espkvm",
  "at": 1790857313,
  "log": "the last few kilobytes of the device log"
}
```

- `title` is the kind of event, in a few words.
- `message` is the sentence a person reads.
- `device` is the device's hostname, so several devices can share one URL.
- `at` is when it happened, in Unix seconds. It is there once the device's clock is set.
- `log` is the tail of the device log, only while Attach recent log is on.

The header is `Content-Type: application/json`. Any 2xx answer counts as delivered.

No screenshot or file goes this way. A dashcam clip is named in `message` with its path on the card.

## Setting up the device

1. In the console open Settings, Notifications, and turn on Send notifications.
2. Paste the address into Webhook URL.
3. In the table under What goes where, tick what the webhook gets. Everything but the blank screen is ticked to start with.
4. Save, then press Send a test in the Automation panel.

## Where to point it

- **n8n or Node-RED.** A webhook node takes the body as it is. From there it can go to Slack, Discord, email or anything else they can reach.
- **Home Assistant.** An automation with a webhook trigger reads `trigger.json.message`. ESP-KVM also talks to Home Assistant over [MQTT](/integrations/home-assistant/), which gives buttons and sensors too.
- **A script of your own.** Any small HTTP server works. Discord and Slack webhooks expect their own format, so they need something like this in between.

## When the network is down

An alert that cannot go out waits and goes out later, oldest first. With a microSD card it waits on the card and survives a restart. In a late one, `at` still says when it happened. A 4xx answer is taken as a refusal and is not retried.

## Good to know

- There is no signature or shared secret. Keep the URL on your own network, or give it a long path nobody can guess.
- An HTTPS URL needs a certificate from a public authority.
- The same alerts can also go to [Telegram](/integrations/telegram/), to [browsers](/integrations/web-push/) and to [ntfy](/integrations/ntfy/), in any mix.
