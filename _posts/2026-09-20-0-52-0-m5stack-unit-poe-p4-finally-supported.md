---
title: 0.52.0 - Support for the M5Stack Unit PoE-P4 with the Display In module
description: A whole IP-KVM the size of a matchbox. Its capture module uses a chip this firmware had never driven, and getting a picture out of it took a week - in which I was wrong three times and the chip was innocent every time.
tags: hardware, boards, m5stack, video, screen-text, display
date: 2026-09-20 18:00
redirect_from: /blog/0-52-0-the-smallest-one-yet/
image: /assets/blog/0-52-0-m5stack-unit-poe-p4-finally-supported/unit.webp
image_alt: The M5Stack Unit PoE-P4: a dark grey plastic block the size of a matchbox, its pin map printed on the top, an Ethernet socket and a USB-C at one end.
---

Every board supported here so far has been the same shape of thing: a P4 board,
a capture board, and a ribbon between them - two boards in a box somebody has to
print.

The M5Stack Unit PoE-P4 is one object the size of a matchbox. Power and network
arrive on one cable, the target's HDMI on the other, and that is the whole KVM.

It works now: 23 frames a second at 1280x720, H.264 as well, and the microSD on
the module reads and writes at full speed, so recording, screenshots, the
timelapse and the dashcam are all there.

Getting there took a week, and I was wrong three times.

## The module

![The Add-on Display In: a narrow blue board with an HDMI socket at one end, the LT6911D under it, a USB-A socket, and a 24-pin flat cable coming off the back.](/assets/blog/0-52-0-m5stack-unit-poe-p4-finally-supported/add-on.webp)

M5Stack's Add-on Display In carries a Lontium LT6911D. Every other board here
uses a Toshiba TC358743, and the two are not alike - different registers, a
different way of being asked what they see, and a different idea of what a reset
line is for.

Worth knowing before buying: that module plugs onto M5Stack's own units and onto
nothing else. It is not a Raspberry Pi camera ribbon.

## Three wrong answers

**The bus is dead.** Nothing answered on the capture bus at all. I checked the
obvious things - a chip that boots slowly, swapped wires, missing pull-ups, a
missing clock - and it was none of them. Reset on this module is wired the other
way round from every board before it, so releasing it the way the old chip wants
is holding the new one down.

**Their firmware never sends anything.** Now the chip answered and reported
itself, a PC on the other end saw a monitor, and not one frame arrived. I got as
far as drafting a letter to M5Stack asking for their firmware image. Both
reasons were mine: I had left a register window open that locks the chip out of
its own settings and takes its HDMI side down with it, and I was looking for the
wrong pixel format on the wire.

**The picture is scrambled.** The bytes arrive in one order and the encoder
reads them in another, and I spent a long time deciding which order by looking
at the result and arguing about it. Looking was the mistake. Asking for a
screenshot from the machine at the other end and measuring the difference
settled it in an hour.

H.264 looked impossible here at first - this silicon's encoder takes one layout
and nothing on the chip makes it from what the module sends. But the conversion
is a plain rearrangement of bytes, so the processor does it, in place of work it
was already doing. 15 frames a second at 720p, 6 at 1080p.

One thing to set on the machine at the other end: the module's EDID makes a PC
treat it as a television, so the picture comes out flat. Set the output range to
Full.

## A console that reads as nothing

The other story here is the same shape - something that worked on my bench and
returned nothing on a real machine.

Reading a text screen is not OCR here. The firmware knows the grid the
characters sit on and the shapes drawn on it, so a serial number comes back
exactly or not at all. A real Ubuntu console came back not at all, for two
reasons at once.

The first was four pixels. 1080 does not divide by 16, and the leftover rows are
not where I assumed - a Linux console leaves them all at the bottom, not split
top and bottom. Four pixels of offset cut every letter in half.

The second was the font. Two were built in, the one a BIOS uses and the one the
kernel carries. A distribution loads neither: it renders its own at boot, thinner
than both. Every letter was a shape the firmware had never seen.

Both are fixed, and the cells read off that screen are kept as a test, so real
pixels off a real machine prove it.

## The rest

The status display can be turned upside down, contributed by Crisspii, who
designed an enclosure where the panel had to be mounted that way.

There is a keyboard on the page now, for when the real one cannot be used - a
phone, a combination the browser swallows, a key the local layout does not have.

Settings open in a window instead of the side panel; there are over a hundred of
them, and a panel was the wrong shape for that. And every answer the device
gives now carries `X-Frame-Options`, so an old browser is told what the content
policy already said: this console does not go in somebody else's frame.
