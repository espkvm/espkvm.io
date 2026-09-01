---
title: Two pages that answer the questions I keep asking
description: A serial monitor that needs no terminal, and three readers: a firmware image, a panic dump, an EDID. All in the browser, nothing uploaded.
tags: diagnostics, console, update
date: 2026-09-01
image:
---

Every hard bug in this project has cost the same three messages. *What does the
serial log say?* *Which image is actually on the board?* *What did the panic
say, exactly?* Each one is a day of waiting, and each answer is something the
person already has. They just have no easy way to read it.

So the site now has two pages that read it for them, and neither uploads
anything: the files you drop are opened in the browser and go no further.

**[The serial monitor](/serial/)** talks to the board over USB and prints its
log: no terminal to install, no driver hunt, and a Save button that produces a
file worth attaching to an issue. It only ever listens. It clears DTR and RTS
the moment the port opens, because asserting those is what holds a board in
reset or drops it into the ROM loader, and a monitor that did that would change
the thing it is watching.

**[The tools page](/tools/)** has three readers.

Drop a firmware image on the first and it says what version it really is and,
more usefully, **which silicon it will boot on**. The two ESP32-P4 families
refuse each other's images, and "the board just sits there" is almost always
that. It reads a merged image too, finding the application wherever the
partition table put it.

The second decodes a panic. Give it the dump and the `-symbols.zip` from the
release that was running, and every address that lands in a function is named -
a reboot becomes a stack. It was tested against a real report: the dump in
issue #22 comes back as `mbedtls_ssl_write_record +0xb6`, which is exactly the
crash that 0.41.1 fixed.

The third reads an EDID and marks every mode the capture path cannot carry: two
MIPI lanes at 972 Mbit/s carrying RGB888 stop at about 81 Mpixel/s, and a mode
above that gives a black screen rather than a slower one.
