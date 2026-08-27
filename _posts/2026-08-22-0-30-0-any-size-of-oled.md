---
title: 0.30.0 - any size of little OLED
description: Not every status panel is 128x64. Six SSD1306 sizes and four SH1106 ones now work, and a shorter panel drops the lines that matter least.
tags: display
date: 2026-08-22
image:
---

The status display used to assume a 128x64 panel. Plenty of the cheap modules
are not: SSD1306 also comes as 128x32, 96x16, 72x40, 64x48 and 64x32, and SH1106
as 128x32, 96x16 and 64x48.

All of them work now. You pick the panel by controller and size in one list,
because the same chip drives every size and reports none of it - this is the one
thing that genuinely cannot be detected. Devices already set up keep the panel
they had.

A shorter panel simply shows fewer lines, and it drops the least useful first:
the address stays, the uptime goes. A line too long for the glass steps along a
character at a time instead of being cut off, and the screen waits for it to
finish before moving on. A clipped address looks like a real one.

The status pages also got a proper header: the page's name and icon in a
reversed bar, with a dot per page so you can see which one you are on and how
many there are.

[Release v.0.30.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.30.0)
