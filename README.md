# espkvm.io

The project page for [ESP-KVM](https://github.com/espkvm/espkvm) - an IP-KVM
built from an ESP32-P4 and a TC358743 HDMI bridge.

Two pages: what the project is, and a flasher that installs the firmware onto a
board over USB straight from the browser.

## How it is built

No framework and no dependencies. Every page is assembled from the same pieces
by `tools/build-site.py`, which needs nothing but Python 3, and what a reader
receives is a plain static file that fetches nothing. A project whose point is
working on a network with no way out should not describe itself through a CDN.

```
_partials/style.css    one stylesheet, inlined into every page
_partials/nav.html     one navigation
_partials/footer.html  one footer
_templates/page.html   the shell all of them sit in
_pages/*.html          the front page and the flasher
_posts/*.md            blog posts
```

Pages used to carry their own copies of the navigation, the footer and the
styles, and they drifted: the flasher was missing links the front page had
gained. Now nothing is copied between pages, so nothing can come apart. Rules
that genuinely belong to one page live in that page's own `<style>` in
`_pages/`.

A file in `_pages/` is front matter and then the markup that goes between the
navigation and the footer. Its `<style>` and JSON-LD blocks are lifted into
`<head>` for it.

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
date: 2026-08-19
image: /assets/something.webp
---
```

`image` is optional (it is the link preview picture, and the one shown at the
top of the post), and `draft: true` keeps a post out of everything until you
remove it. Build, and the post, the blog index, the RSS feed and the sitemap
all follow. Pushing the Markdown is all that publishing takes.

A post that is not for the repository at all lives in `_drafts/`, which git
ignores. Move the file into `_posts/` when it is ready. While `_posts/` is
empty the blog builds as an empty page and nothing links to it - the Blog links
in the nav and the footer come back with the first post.

The builder carries a small Markdown of its own rather than pulling one in,
covering headings, paragraphs, fenced code, lists, quotes, rules, images and
inline emphasis, code and links. Anything outside that makes the build stop and
say so, so a post cannot render wrong quietly.

## Preview

```sh
python3 tools/build-site.py
python3 -m http.server 8000
```

The build has to run at least once, since none of the HTML is committed.

Serial access needs a secure page, so `Install` works over `localhost` or
HTTPS and refuses anything else. That is the browser's rule, not ours.
