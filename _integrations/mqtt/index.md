---
name: MQTT
title: ESP-KVM on your MQTT broker
page_title: IP-KVM over MQTT: telemetry, commands and screen alerts - ESP-KVM
description: ESP-KVM publishes its state to an MQTT broker and takes commands on its own topics: power, reset, Wake-on-LAN, a screenshot, a recording, a runbook. For Node-RED, n8n, openHAB or a script of your own.
tip: MQTT: telemetry, buttons and alerts on your broker
summary: Telemetry, buttons and alerts on any broker.
mark: mark.svg
order: 4
link.Home Assistant over MQTT: https://espkvm.io/integrations/home-assistant/
link.Try the console: https://demo.espkvm.io/
---

ESP-KVM has an MQTT client in its firmware. It sends what it knows about itself and the target to your broker, and listens for commands. Home Assistant finds it there on its own, and that is on [its own page](/integrations/home-assistant/). This page is for everything else that talks MQTT. MQTT is off by default and costs nothing while off.

## Setting it up

1. In the console open Settings, MQTT, and turn on Publish to MQTT.
2. Fill in Broker host and Broker port, and Username and Password if the broker wants them.
3. For TLS, turn on Use TLS and set the port to 8883. Verify broker certificate checks it against the public roots built into the device. Turn that off for a broker with a self-signed certificate.
4. Save. The device connects in a few seconds.

The password stays on the device and is never sent back to the console.

## Topics

The device id is the last three bytes of its MAC address, such as `a1b2c3`. With the default base topic, everything sits under `espkvm/a1b2c3/`:

- `espkvm/a1b2c3/availability` is `online` or `offline`. It is retained, and a last will sets it to `offline` when the device drops off.
- `espkvm/a1b2c3/state` is one JSON message with everything, retained. It goes out every 30 seconds by default, after each command, and soon after a screen alert.
- `espkvm/a1b2c3/areas` has the screen areas, retained.
- `espkvm/a1b2c3/snapshot` is a JPEG of the screen, sent when asked for or with a screen alert.
- `espkvm/a1b2c3/cmd/<command>` is where commands go.

The base topic and the interval can be changed under What it publishes.

## What the state says

Among other things: the version and uptime, the video signal, resolution, codec, frame rate and bitrate, the number of viewers, the target's power LED, the USB link, temperatures and free memory, whether it is recording, the jiggler, the HDMI-CEC state of the source, and the screen alert with the text that set it off. A Node-RED flow or a script can read any of it as JSON.

## Commands

Publish to `espkvm/a1b2c3/cmd/` plus:

- `power`, `reset` and `forceoff` press the target's power and reset buttons, for boards wired to them.
- `wol` sends a Wake-on-LAN packet to the MAC in the settings.
- `cec_wake` and `cec_standby` wake or put to sleep a TV box or console over HDMI-CEC.
- `screenshot` saves one on the card. `snapshot` sends the screen to the snapshot topic.
- `record` with `ON` or `OFF` starts or stops a recording. `clip` saves a dashcam clip. `timelapse` starts a timelapse.
- `runbook` with a runbook's name as the payload runs it.
- `jiggler` with `ON` or `OFF` switches the mouse jiggler.
- `restart` restarts the device. `install` installs a newer release, if one is out.

## Good to know

- Anyone who can publish to the command topics can press the target's power button. Give the device its own user on the broker and keep the broker on your own network.
- The screen alert is the same phrase watch the notifications use. A blank screen has a field of its own in the state. Turn on Send a picture with a screen alert and the snapshot topic gets the screen at that moment.
- When the network drops, the client connects again on its own. Over Wi-Fi as the backup for the cable it came back in about 15 seconds.
