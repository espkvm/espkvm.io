---
title: 0.37.0 - the screen as two kilobytes
description: Work a machine over a phone tether by sending the characters instead of the video, hand a dashboard a view-only token, and go back to any published release.
tags: screen-text, video, security, update
date: 2026-08-26
image:
---

A text screen is about two kilobytes. The video of that same screen is megabits
a second. On a phone tether that decides whether you get anything at all.

Tick "text when the screen is text" in the video readout and the console shows
the characters and stops the stream. The keyboard still reaches the target,
which is most of what a BIOS asks for. It is a standing preference, not a place you go. With it on, the view follows
the machine by itself. Characters at the boot menu, the picture the moment a
desktop paints, characters again at the next restart. Both directions need two readings to agree, so a screen near the edge of
being readable does not flicker between the two. The readings arrive along the
same socket the picture used, carrying only what changed, so walking a boot menu
moves the highlight about as fast as the machine repaints it.

The selected row comes through too. A menu says which line you are on by drawing
it inverted, and plain text loses exactly that; inverted cells are now reported
and drawn inverted.

**A screen gone to one flat colour is noticed.** Reading characters cannot cover
a modern Windows stop screen. That is a graphical page in a proportional font,
with no grid to cut. What it does have is a shape a few hundred samples can see:
nearly all one colour, and it stays. The device reports how long the picture has
been flat, and publishes it to Home Assistant. What it means is your call.

![The console on a phone with the on-screen keyboard up: the target's screen stays fully visible above it, with the touch controls and the status bar in place.](/assets/blog/0-37-0-the-screen-as-two-kilobytes/phone.webp)

**The phone's keyboard stops pushing the picture off the screen.** A virtual
keyboard covers the window rather than shrinking it, so the console was laid out
as if it were not there, and the browser did the only thing left to it: it
scrolled the page to reach the field, taking the status bar and the top of the
picture with it. The keyboard is measured now and the console is sized to what
is left, so the whole screen stays visible above it and nothing scrolls.

**A viewing token.** Home Assistant's camera integrations can be handed a URL and
little else, so putting a target's screen on a dashboard used to mean turning the
login off. A token lives in Settings, Security, and stays off until you make one.
It opens the MJPEG stream, a single frame and the capture figures. It cannot
press a key or cut the power. Only its hash is kept, so it is shown once.

**Go back to any published release.** The two slots let you step back one
version, which helps only while the one you want is still in the other slot.
Settings now lists what the project has published and installs the one you pick.
The device fetches the image itself, because the browser is not allowed to, and
that means the device talking to GitHub - so it is off until you turn it on. A
KVM often sits where nothing is meant to reach the internet, and ordinary
updates do not need it.

Underneath all that: security headers on every answer, a stricter idea of who is
asking, a hotspot that no longer comes up open by default, and a long list of
fixes found by re-reading the new code rather than by running it.

[Release v.0.37.0 on GitHub](https://github.com/espkvm/espkvm/releases/tag/v.0.37.0)
