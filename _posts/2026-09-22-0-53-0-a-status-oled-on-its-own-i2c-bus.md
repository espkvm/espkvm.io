---
title: 0.53.0 - The status OLED can sit on its own I2C bus, for the M5Stack Mini OLED
description: The status OLED always shared the capture chip's I2C bus. On the M5Stack Unit PoE-P4 the socket for one is the Grove port, which is a bus of its own, so now it can have one. Plus two fixes found with a unit on the desk.
tags: display, hardware, console
date: 2026-09-22 20:00
image: /assets/blog/0-53-0-a-status-oled-on-its-own-i2c-bus/m5-mini-oled.webp
image_alt: The M5Stack Mini OLED Unit, a 0.42-inch 72x40 panel with a Grove connector.
---

ESP-KVM can drive a small OLED that shows the device's address, the link, the
capture and its health. Until now that OLED had one place to live: the I2C bus
the capture chip is on. That was not a shortcut - it means the panel needs no
pins, no soldering and no setting, on every board.

The M5Stack Unit PoE-P4 does not work that way. Its capture bus goes to the
add-on through a level shifter, and the socket you would actually plug a panel
into is the Grove port, which is a second I2C bus: SDA on GPIO 53, SCL on 54.
M5Stack sell a 0.42&Prime; 72&times;40 OLED that fits it with a cable and nothing
else.

So an OLED can now have a bus of its own. Two new settings under Display, OLED
SDA and OLED SCL, and on the M5Stack firmware they are already set to the Grove
pins. Leave them at None and nothing changes: the panel is looked for on the
capture bus, as before. The panel itself is in the list as "SSD1315 72x40".

I have not had that panel in front of me yet. The size was already supported -
it is the same 28-column offset as the SSD1306 version - so what is new here is
the bus, not the glass.

## Two things a unit on the desk found

**The USB icon was grey until you took control.** The device tells the console
whether the target sees the keyboard, and it sent that to the console holding
control and to no other. A second browser tab, or a tab you had only opened to
look, showed the icon grey with "no power on the target's port" - which is the
worst of the three things that icon can mean, and it was not true. It goes to
every open console now.

**A refresh rate that was never real.** On the Unit PoE-P4 the console said the
input was `1920x1080p15` for a 60 Hz source. The rate is worked out from what
the capture chip calls its pixel clock, and on this chip that register is not
one: it reads the same four bytes whatever is on the wire, with a mode, without
one, with the cable out. They look like a firmware date. So the rate is reported
as unknown now, which is the honest answer, and the hunt for the register that
really says what the input is doing goes on.
