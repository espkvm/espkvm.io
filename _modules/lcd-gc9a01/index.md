---
title: Round LCD - GC9A01
tile_maker: Round SPI LCD
tile_model: GC9A01
kind: display
status: tested
order: 30
role: Status display (optional)
chip: SPI LCD
summary: A 1.28" 240x240 round colour SPI LCD. The same status pages in colour, plus a hotspot QR code a phone camera can join from.
spec.Controller: GC9A01, GC9A01A
spec.Size: 1.28" 240x240; the 1.5" GC9A01A modules work too
spec.Wiring: SPI - SCLK, MOSI, CS, DC and RST to free GPIOs, plus 3V3 and GND
spec.Setting: Settings → Display
photo: module.webp
photo_style: product
---

Any GC9A01 board, such as the common one in the photo or the [Waveshare 1.28inch LCD Module](/modules/waveshare-lcd-128/). Wire its SPI pins to any free GPIOs and pick
them in the console. Each build offers a set of pins known to work on that
board, so you only change them if you wired it differently.

Settings → Pins draws the board's expansion header the way it is printed, with
what holds each pin, so a free GPIO is easy to find.

In hotspot mode it shows the join code, and it draws the recovery button's
ring, which need the room.
