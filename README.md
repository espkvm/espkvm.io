# espkvm.io

The project page for [ESP-KVM](https://github.com/espkvm/espkvm) - an IP-KVM
built from an ESP32-P4 and a TC358743 HDMI bridge.

Two pages: what the project is, and a flasher that installs the firmware onto a
board over USB straight from the browser.

## How it is built

No framework and no dependencies. Every page is assembled from the same pieces
by `tools/build-site.py`, which needs nothing but Python 3, and what a reader
receives is a plain static file that fetches nothing - no CDN, no fonts, no
analytics. A project whose point is working on a network with no way out should
not describe itself through a CDN. The one exception is a blog post with a video
in it: that post embeds the player from youtube-nocookie.com, and nothing else
on the site does.

```
_partials/style.css    one stylesheet, inlined into every page
_partials/nav.html     one navigation
_partials/footer.html  one footer
_templates/page.html   the shell all of them sit in
_pages/*.html          the front page, the flasher, the tools
_posts/*.md            blog posts
_boards/<id>/          one folder per board: index.md and its photo
_cases/<id>/           one folder per printed case
```

Pages used to carry their own copies of the navigation, the footer and the
styles, and they drifted: the flasher was missing links the front page had
gained. Now nothing is copied between pages, so nothing can come apart. Rules
that genuinely belong to one page live in that page's own `<style>` in
`_pages/`.

A file in `_pages/` is front matter and then the markup that goes between the
navigation and the footer. Its `<style>` and JSON-LD blocks are lifted into
`<head>` for it.

## Renaming a page or a post

Changing a file name in `_posts/` changes the URL, and something out there may
still point at the old one. Put it in the front matter and the build leaves a
stub behind:

```
redirect_from: /blog/the-old-slug/
```

Several are comma-separated, and it works for `_pages/` too. GitHub Pages serves
files and has no 301 to offer, so the stub is what a static host can do: a
canonical link, a meta refresh and a `location.replace`, in the same shape as the
committed `/demo/` redirect. A stub written outside `blog/` needs a line in
`.gitignore`, the way `flash/index.html` has one.

Building writes `index.html`, `flash/index.html`, `blog/` and `sitemap.xml`.
None of those are committed - the published site is assembled by CI, so the
sources are the only copy and cannot go stale. `flash/flash.js` is different:
it is vendored code, committed as it is, and only copied.

```sh
python3 tools/build-site.py     # add --drafts to include unfinished posts
```

The interactive demo is not built here at all. The console repository
publishes it to [demo.espkvm.io](https://demo.espkvm.io/), and `demo/` in
this repo is a small redirect page kept because older articles link to
`espkvm.io/demo/`.

`flash.js` is the one piece of code that came from elsewhere, and it is
vendored rather than linked - see [vendor.md](docs/vendor.md) for what it is and how
to rebuild it.

The firmware images the flasher writes are not stored here. They are published
by the firmware repository's CI to `espkvm.github.io/espkvm/flash/` and fetched
from there, so this site cannot go stale.

## Writing a post

Drop a Markdown file in `_posts/`, named `YYYY-MM-DD-some-slug.md`, starting
with a front matter block:

```
---
title: Five bugs from twelve days of ESP32-P4 firmware
description: One sentence. It is the search result and the link preview.
date: 2026-08-19 14:30
image: /assets/something.webp
---
```

The date may carry a time, and two posts on one day then sit in the order they
were published rather than by file name. `image` is optional (it is the link
preview picture, and the one shown at the top of the post), and `draft: true` keeps a post out of everything until you
remove it. Build, and the post, the blog index, the RSS feed and the sitemap
all follow. Pushing the Markdown is all that publishing takes.

A post that is not for the repository at all lives in `_drafts/`, which git
ignores. Move the file into `_posts/` when it is ready. While `_posts/` is
empty the blog builds as an empty page and nothing links to it - the Blog links
in the nav and the footer come back with the first post.

The builder carries a small Markdown of its own rather than pulling one in,
covering headings, paragraphs, fenced code, lists, quotes, rules, tables, images
and inline emphasis, code and links. Anything outside that makes the build stop
and say so, so a post cannot render wrong quietly. The one piece of raw markup
it passes through is an `<iframe>`, for a video player: it goes into a box that
keeps its aspect ratio on a phone.

## Adding a board or a case

A board is a folder in `_boards/`, named by its id - the same id the firmware
gives it in `boards/boards.json`, so the page's Install button opens the flasher
on that board. In it go `index.md` and the photo:

```
---
title: Waveshare ESP32-P4-NANO
kind: device
status: tested
order: 30
role: The device - community-tested
summary: One sentence. The card text, and the search result.
flasher: p4-nano
capture: c790, waveshare-19137
photo: board.jpg
photo_style: product
spec.Chip: ESP32-P4, rev 1.x or rev 3.x
spec.Memory: 32 MB PSRAM, 16 MB flash
link.Waveshare product page: https://www.waveshare.com/esp32-p4-nano.htm
---

Prose about the board, in the same small Markdown as a post.
```

`kind` is `device` or `capture`, `status` is `tested` or `untested`, `order` is
its place in its group, and `photo_style` is `product` (a shot on white) or
`photo`. A capture board has no `flasher`. `spec.<Label>` rows become the table
on the board's page and `link.<Label>` entries its buttons, both in the order
written.

A case is a folder in `_cases/` with `title`, `author`, `summary`, `boards` (the
ids it fits), `photo`, `photo_credit` and links; it shows up on the pages of the
boards it fits.

The build writes `/boards/<id>/`, `/cases/<id>/` and the `/boards/` catalog,
and draws the cards on the front page where it says `<!-- catalog:tested -->`
(and `untested`, `capture`, `cases`). With the firmware repo checked out next to
this one, it also checks every `flasher` id against the firmware's list.

## Preview

```sh
python3 tools/build-site.py
python3 -m http.server 8000
```

The build has to run at least once, since none of the HTML is committed.

Serial access needs a secure page, so `Install` works over `localhost` or
HTTPS and refuses anything else. That is the browser's rule, not ours.
