#!/usr/bin/env python3
"""Build the site: _pages/*.html and _posts/*.md into finished HTML.

No dependencies: stdlib Python only, and a small Markdown of its own further
down.

Every page - the front page, the flasher and every post - is assembled from the
same pieces in _partials/ (one stylesheet, one navigation, one footer) around
the shell in _templates/page.html. Nothing is copied between pages, so nothing
can drift between them, and what a reader receives is still a plain static file
that fetches nothing.

    python3 tools/build-site.py [--drafts]

Writes index.html, flash/index.html, blog/index.html, blog/<slug>/index.html,
blog/tags/<tag>/index.html, blog/feed.xml, boards/ and cases/ (from _boards/
and _cases/), and rewrites sitemap.xml. All of those are generated and none of
them are committed.
"""

import argparse
import html
import os
import re
import sys
from urllib.parse import quote
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://espkvm.io"
POSTS_DIR = os.path.join(ROOT, "_posts")
PAGES_DIR = os.path.join(ROOT, "_pages")
PARTIALS_DIR = os.path.join(ROOT, "_partials")
OUT_DIR = os.path.join(ROOT, "blog")
TEMPLATE = os.path.join(ROOT, "_templates", "page.html")
OG_IMAGE = SITE + "/assets/og-image.png"

# Pages that exist by hand rather than being generated, for the sitemap.
# The pages in the sitemap are whatever _pages/ rendered. This used to be a
# hand-written list, and it went stale the first time a page was added: /serial/
# and /tools/ were missing from the sitemap on the day they were written.

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# ---------------------------------------------------------------- front matter

def split_front_matter(text, path):
    """Pull the leading `---` block off a post. Values are plain strings."""
    if not text.startswith("---"):
        sys.exit("%s: no front matter (the file must start with ---)" % path)
    end = text.find("\n---", 3)
    if end == -1:
        sys.exit("%s: front matter is never closed" % path)
    head, body = text[3:end], text[end + 4:]
    meta = {}
    for line in head.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            sys.exit("%s: cannot read front matter line: %s" % (path, line))
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, body.lstrip("\n")


def read_posts(include_drafts):
    posts = []
    # A checkout with no posts has no _posts/ at all - git does not carry an
    # empty directory - and that is a blog with nothing in it, not an error.
    names = sorted(os.listdir(POSTS_DIR)) if os.path.isdir(POSTS_DIR) else []
    for name in names:
        if not name.endswith(".md"):
            continue
        path = os.path.join(POSTS_DIR, name)
        with open(path, encoding="utf-8") as fh:
            meta, body = split_front_matter(fh.read(), path)

        if meta.get("draft", "").lower() in ("true", "yes") and not include_drafts:
            continue

        for required in ("title", "description", "date"):
            if required not in meta:
                sys.exit("%s: front matter needs a %s" % (path, required))

        # Tags are a comma-separated line. They are lower-cased and de-duped
        # here so "Video, video" cannot become two tags with one meaning, and
        # kept in the order they were written - a post's first tag is the one
        # it is mostly about.
        tags = []
        for raw in meta.get("tags", "").split(","):
            tag = raw.strip().lower()
            if tag and tag not in tags:
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", tag):
                    sys.exit("%s: a tag must be lowercase letters, digits and "
                             "dashes: %s" % (path, tag))
                tags.append(tag)

        # The listing wants a picture whether or not the post opens with one, so
        # a post with no hero lends the listing its first inline figure. The
        # hero itself stays exactly what the front matter says.
        # `thumb` names a listing picture that is not the hero (a square crop of
        # a figure that is wide in the post, say).
        thumb = meta.get("thumb") or meta.get("image", "")
        if not thumb:
            first = re.search(r"^!\[([^\]]*)\]\(([^)\s]+)\)$", body, re.M)
            if first:
                thumb = first.group(2)

        slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name[:-3])
        # A time may follow the date - two posts on one day then sit in the
        # order they were published, newest first, rather than by file name.
        try:
            raw = meta["date"].strip()
            fmt = "%Y-%m-%d %H:%M" if " " in raw else "%Y-%m-%d"
            date = datetime.strptime(raw, fmt)
        except ValueError:
            sys.exit("%s: date must be YYYY-MM-DD, with an optional HH:MM" % path)

        posts.append({
            "slug": slug,
            "title": meta["title"],
            "description": meta["description"],
            "date": date,
            "image": meta.get("image", ""),
            "thumb": thumb,
            "tags": tags,
            "body": body,
            "path": path,
            "redirect_from": meta.get("redirect_from", ""),
        })

    slugs = [p["slug"] for p in posts]
    duplicate = next((s for s in slugs if slugs.count(s) > 1), None)
    if duplicate:
        sys.exit("two posts want the same URL: /blog/%s/" % duplicate)

    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


# ---------------------------------------------------------------- catalog
#
# One folder per board in _boards/ and per case in _cases/: an index.md (front
# matter, then prose) and its photos. The build copies the photos next to the
# page it writes, /boards/<id>/ or /cases/<id>/, and draws the tiles on the
# front page and on /boards/ from the same data, so a board is described once.
#
# Front matter a board takes: title, kind (device or capture), status (tested
# or untested), order, role, summary, photo, photo_style (product or photo),
# flasher (its id in the firmware's boards.json), capture (ids of the capture
# boards it takes), and any number of "spec.<Label>: value" rows and
# "link.<Label>: url" links, shown in the order written. A case takes title,
# author, summary, boards (ids it fits), photo, photo_credit and links.

BOARDS_DIR = os.path.join(ROOT, "_boards")
CASES_DIR = os.path.join(ROOT, "_cases")
# The firmware's own list of boards, when the two repos sit side by side. A
# flasher id here that the firmware does not publish is a dead install button.
FIRMWARE_BOARDS = os.path.join(os.path.dirname(ROOT), "espkvm", "boards", "boards.json")


def image_size(path):
    """Width and height of a WebP, JPEG or PNG, read from its header."""
    with open(path, "rb") as fh:
        d = fh.read(256 * 1024)
    if d[:4] == b"RIFF" and d[8:12] == b"WEBP":
        chunk = d[12:16]
        if chunk == b"VP8 ":
            w, h = int.from_bytes(d[26:28], "little"), int.from_bytes(d[28:30], "little")
            return w & 0x3FFF, h & 0x3FFF
        if chunk == b"VP8L":
            v = int.from_bytes(d[21:25], "little")
            return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
        if chunk == b"VP8X":
            return (int.from_bytes(d[24:27], "little") + 1,
                    int.from_bytes(d[27:30], "little") + 1)
    if d[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(d[16:20], "big"), int.from_bytes(d[20:24], "big")
    if d[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(d):
            marker, length = d[i + 1], int.from_bytes(d[i + 2:i + 4], "big")
            if marker in (0xC0, 0xC1, 0xC2):
                return int.from_bytes(d[i + 7:i + 9], "big"), int.from_bytes(d[i + 5:i + 7], "big")
            i += 2 + length
    sys.exit("%s: cannot read the picture's size" % path)


def read_folder_items(base, section):
    items = []
    names = sorted(os.listdir(base)) if os.path.isdir(base) else []
    for name in names:
        folder = os.path.join(base, name)
        index = os.path.join(folder, "index.md")
        if not os.path.isfile(index):
            continue
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            sys.exit("%s: a folder name must be lowercase letters, digits and dashes" % folder)
        with open(index, encoding="utf-8") as fh:
            meta, body = split_front_matter(fh.read(), index)
        for required in ("title", "summary", "photo"):
            if required not in meta:
                sys.exit("%s: front matter needs a %s" % (index, required))
        photo = os.path.join(folder, meta["photo"])
        if not os.path.isfile(photo):
            sys.exit("%s: no such photo: %s" % (index, meta["photo"]))
        w, h = image_size(photo)
        items.append({
            "id": name,
            "section": section,
            "url": "/%s/%s/" % (section, name),
            "folder": folder,
            "path": index,
            "meta": meta,
            "body": body,
            "photo": "/%s/%s/%s" % (section, name, meta["photo"]),
            "photo_w": w,
            "photo_h": h,
            "specs": [(k[5:], v) for k, v in meta.items() if k.startswith("spec.")],
            "links": [(k[5:], v) for k, v in meta.items() if k.startswith("link.")],
            "order": int(meta.get("order", "999")),
        })
    return items


def id_list(value):
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def read_catalog():
    boards = read_folder_items(BOARDS_DIR, "boards")
    cases = read_folder_items(CASES_DIR, "cases")
    ids = {b["id"] for b in boards}
    for b in boards:
        m = b["meta"]
        if m.get("kind") not in ("device", "capture"):
            sys.exit("%s: kind must be device or capture" % b["path"])
        if m.get("status") not in ("tested", "untested"):
            sys.exit("%s: status must be tested or untested" % b["path"])
        for c in id_list(m.get("capture")):
            if c not in ids:
                sys.exit("%s: capture names a board that is not in _boards/: %s" % (b["path"], c))
    for c in cases:
        for b in id_list(c["meta"].get("boards")):
            if b not in ids:
                sys.exit("%s: boards names a board that is not in _boards/: %s" % (c["path"], b))

    if os.path.isfile(FIRMWARE_BOARDS):
        import json
        with open(FIRMWARE_BOARDS, encoding="utf-8") as fh:
            firmware = {b["id"]: b for b in json.load(fh)}
        for b in boards:
            fid = b["meta"].get("flasher")
            if fid and fid not in firmware:
                sys.exit("%s: flasher id %s is not in the firmware's boards.json" % (b["path"], fid))
            if fid and firmware[fid].get("untested", False) != (b["meta"]["status"] == "untested"):
                print("warning: %s is %s here but not in the firmware's boards.json"
                      % (b["id"], b["meta"]["status"]))
        listed = {b["meta"].get("flasher") for b in boards}
        for fid in firmware:
            if fid not in listed:
                print("warning: the firmware publishes %s, which has no folder in _boards/" % fid)

    key = lambda i: (i["order"], i["meta"]["title"])
    return {
        "tested": sorted([b for b in boards if b["meta"]["kind"] == "device"
                          and b["meta"]["status"] == "tested"], key=key),
        "untested": sorted([b for b in boards if b["meta"]["kind"] == "device"
                            and b["meta"]["status"] == "untested"], key=key),
        "capture": sorted([b for b in boards if b["meta"]["kind"] == "capture"], key=key),
        "cases": sorted(cases, key=key),
        "all": boards + cases,
        "by_id": {b["id"]: b for b in boards},
    }


def features(item):
    """Short labels for a card and the catalog's filters, read off the specs so
    nothing is written twice: (filter key, label)."""
    m = item["meta"]
    specs = dict(item["specs"])
    out = []
    if m.get("kind") == "device":
        net = specs.get("Network", "")
        if "Ethernet" in net:
            out.append(("ethernet", "Ethernet"))
        if "Wi-Fi" in net:
            out.append(("wifi", "Wi-Fi"))
        if "PoE" in net:
            out.append(("poe", "PoE"))
        chip = specs.get("Chip", "")
        has1, has3 = "rev 1" in chip, "rev 3" in chip
        if has1 and has3:
            out.append(("rev3", "rev 1.x + 3.x"))
        elif has3:
            out.append(("rev3", "rev 3.x"))
        elif has1:
            out.append(("rev1", "rev 1.x"))
    elif m.get("kind") == "capture":
        if m.get("bridge"):
            out.append(("bridge", m["bridge"]))
    return out


def split_title(item):
    """"Waveshare ESP32-P4-NANO" -> ("Waveshare", "ESP32-P4-NANO"); a case is
    shown under its author."""
    m = item["meta"]
    if item["section"] == "cases":
        return m.get("author", ""), m["title"]
    maker, _, model = m["title"].partition(" ")
    return (maker, model) if model else ("", m["title"])


def tile(item):
    m = item["meta"]
    maker, model = split_title(item)
    feats = features(item)
    untested = m.get("status") == "untested"
    status = ""
    if m.get("kind") == "device":
        status = ('<span class="cat-status untested">Untested</span>' if untested
                  else '<span class="cat-status">Tested</span>')
    chips = "".join('<span class="cat-chip">%s</span>' % html.escape(label)
                    for _, label in feats)
    keys = " ".join([k for k, _ in feats] + ([] if untested else ["tested"]))
    fit = " cat-photo-cover" if m.get("photo_style") == "photo" else ""
    return """          <a class="cat-card" href="{url}" data-f="{keys}">
            <span class="cat-photo{fit}"><img src="{photo}" width="{w}" height="{h}" loading="lazy" alt="" /></span>
            <span class="cat-body">
              <span class="cat-maker">{maker}{status}</span>
              <span class="cat-model">{model}</span>
              <span class="cat-chips">{chips}</span>
            </span>
          </a>""".format(
        url=item["url"], keys=keys, fit=fit, photo=item["photo"],
        w=item["photo_w"], h=item["photo_h"], maker=html.escape(maker),
        status=status, model=html.escape(model), chips=chips)


def tiles(items):
    return "\n".join(tile(i) for i in items)


def fill_catalog(body, catalog):
    """Swap the <!-- catalog:<group> --> markers a page leaves for tiles."""
    def swap(match):
        group = match.group(1)
        if group not in ("tested", "untested", "capture", "cases"):
            sys.exit("unknown catalog group: %s" % group)
        return tiles(catalog[group])
    body = re.sub(r"<!-- catalog:(\w+) -->", swap, body)
    # The flasher's board photos: flasher id -> the photo in _boards/.
    import json
    images = {b["meta"]["flasher"]: b["photo"] for b in catalog["all"]
              if b["meta"].get("flasher")}
    return body.replace("/* catalog:images */ {}", json.dumps(images, sort_keys=True))


def spec_table(item):
    rows = list(item["specs"])
    m = item["meta"]
    if m.get("kind") == "device":
        rows.insert(0, ("Status", "Run on hardware" if m["status"] == "tested"
                        else "Built from the schematic, not run on one yet"))
    if not rows:
        return ""
    return ('<div class="table-scroll"><table class="board-specs"><tbody>\n%s\n'
            "</tbody></table></div>" % "\n".join(
                "<tr><th>%s</th><td>%s</td></tr>" % (html.escape(k), inline(v, item["path"]))
                for k, v in rows))


def rev_note(item):
    """For a board sold with either chip revision: how to tell which one it has
    before choosing an image."""
    chip = dict(item["specs"]).get("Chip", "")
    if "rev 1" not in chip or "rev 3" not in chip:
        return ""
    return ('<p class="board-revnote"><strong>Which revision?</strong> Read the chip: '
            "<strong>ESP32-P4NRW32X</strong>, with an X at the end, is rev 3.x; "
            "<strong>ESP32-P4NRW32</strong> without it is rev 1.x. "
            "The product code does not tell. "
            '<a href="/#faq">More in the FAQ</a>.</p>')


def item_page(shell, item, catalog):
    m = item["meta"]
    kind = m.get("kind")
    actions = []
    if m.get("flasher"):
        actions.append('<a class="btn btn-primary" href="/flash/?board=%s">Install from the browser</a>'
                       % quote(m["flasher"]))
    for label, url in item["links"]:
        actions.append('<a class="btn" href="%s" rel="noopener">%s</a>'
                       % (html.escape(url), html.escape(label)))

    related = []
    if kind == "device":
        caps = [catalog["by_id"][c] for c in id_list(m.get("capture"))]
        if caps:
            related.append(("Capture board" if len(caps) == 1 else "Capture boards", caps))
        cases = [c for c in catalog["cases"] if item["id"] in id_list(c["meta"].get("boards"))]
        if cases:
            related.append(("Cases for it", cases))
    elif kind == "capture":
        users = [b for b in catalog["tested"] + catalog["untested"]
                 if item["id"] in id_list(b["meta"].get("capture"))]
        related.append(("Boards it works with", users))
    else:
        fits = [catalog["by_id"][b] for b in id_list(m.get("boards"))]
        related.append(("Fits", fits))

    extra = "".join(
        '\n      <h2 class="cat-head">%s</h2>\n      <div class="cat-grid">\n%s\n      </div>'
        % (html.escape(title), tiles(items)) for title, items in related)

    back = ('<a href="/boards/#cases">&larr; All cases</a>' if item["section"] == "cases"
            else '<a href="/boards/">&larr; All boards</a>')
    untested = " untested" if m.get("status") == "untested" else ""
    role = m.get("role") or ("A case by " + m["author"] if m.get("author") else "")
    credit = ('<p class="board-credit">%s</p>' % html.escape(m["photo_credit"])
              if m.get("photo_credit") else "")
    is_photo = " is-photo" if m.get("photo_style") == "photo" else ""

    # Someone who lands here from a search for the board has never heard of the
    # project: say in two lines what it is before the specs.
    name = html.escape(m["title"])
    if kind == "device":
        intro = ("<strong>ESP-KVM</strong> is free, open-source firmware that turns the "
                 "%s into an IP-KVM: the screen, keyboard and mouse of another computer "
                 "in your browser, from the BIOS up. Add an HDMI capture board, flash it "
                 "from the browser, and it runs with no Linux, no app and no cloud." % name)
    elif kind == "capture":
        intro = ("<strong>ESP-KVM</strong> is free, open-source firmware that turns an "
                 "ESP32-P4 board into an IP-KVM: another computer's screen, keyboard and "
                 "mouse in your browser, from the BIOS up. The %s is the part that "
                 "brings the computer's HDMI in." % name)
    else:
        intro = ("<strong>ESP-KVM</strong> is free, open-source firmware that turns an "
                 "ESP32-P4 board into an IP-KVM: another computer's screen, keyboard and "
                 "mouse in your browser, from the BIOS up. This is a printed case for one, "
                 "made by someone who built it.")
    intro = ('<p class="board-intro">%s <a href="/">What it does &rarr;</a> '
             '<a href="https://demo.espkvm.io/" rel="noopener">Try the demo &rarr;</a></p>'
             % intro)

    content = """
    <article class="board-page">
      <p class="post-back">{back}</p>
      {intro}
      <div class="board-top">
        <div class="hw-photo board-photo{is_photo}">
          <img src="{photo}" width="{w}" height="{h}" alt="{alt}" />
        </div>
        <div class="board-head">
          <div class="role{untested}">{role}</div>
          <h1>{title}</h1>
          <p class="lead">{summary}</p>
          {specs}
          {revnote}
          <p class="board-actions">{actions}</p>
          {credit}
        </div>
      </div>
      <div class="post-body">
{body}
      </div>{extra}
    </article>
""".format(back=back, intro=intro, is_photo=is_photo, photo=item["photo"], w=item["photo_w"],
           h=item["photo_h"], alt=safe(m["title"]), untested=untested,
           role=html.escape(role), title=html.escape(m["title"]),
           summary=html.escape(m["summary"]), specs=spec_table(item),
           revnote=rev_note(item),
           actions=" ".join(actions), credit=credit,
           body=link_boards(render_markdown(item["body"], item["path"]),
                            set(catalog["by_id"]), skip={item["id"]}),
           extra=extra)

    what = "an IP-KVM" if kind == "device" else ("capture for an IP-KVM" if kind == "capture"
                                                 else "a case for an IP-KVM")
    return render_page(shell, {
        "title": "%s - %s with ESP-KVM" % (m["title"], what),
        "og_title": m["title"],
        "description": m.get("description") or m["summary"],
        "canonical": SITE + item["url"],
        "image": SITE + item["photo"],
        "image_alt": m["title"],
        "og_type": "article",
    }, content)


def catalog_page(shell, catalog):
    devices = catalog["tested"] + catalog["untested"]
    filters = [("all", "All"), ("tested", "Tested"), ("ethernet", "Ethernet"),
               ("wifi", "Wi-Fi"), ("poe", "PoE"), ("rev3", "rev 3.x")]
    buttons = "".join(
        '<button type="button" class="cat-filter" data-filter="%s" aria-pressed="%s">%s</button>'
        % (key, "true" if key == "all" else "false", label) for key, label in filters)

    content = """
    <article class="board-page">
      <h1>Boards</h1>
      <p class="lead">
        The ESP32-P4 boards ESP-KVM runs on, the HDMI capture boards that feed
        them, and printed cases. "Untested" means built from the vendor's
        schematic and not yet run by anyone.
      </p>

      <h2 class="cat-head" id="devices">ESP32-P4 boards <span class="cat-count" id="cat-count">{n}</span></h2>
      <div class="cat-filters" id="cat-filters" hidden>{buttons}</div>
      <div class="cat-grid" id="cat-devices">
{devices}
      </div>

      <h2 class="cat-head" id="capture">HDMI capture <span class="cat-count">{n_capture}</span></h2>
      <div class="cat-grid">
{capture}
      </div>

      <h2 class="cat-head" id="cases">Cases <span class="cat-count">{n_cases}</span></h2>
      <div class="cat-grid">
{cases}
      </div>

      <p class="cat-note">
        Not the board you have? <a href="https://github.com/espkvm/espkvm/issues/new" rel="noopener">Open an issue</a>
        with a link to its schematic. Printed a case? Post it in
        <a href="https://github.com/orgs/espkvm/discussions" rel="noopener">Discussions</a>.
      </p>
    </article>
    <script>
      (function () {{
        var bar = document.getElementById("cat-filters"),
          grid = document.getElementById("cat-devices"),
          count = document.getElementById("cat-count");
        if (!bar || !grid) return;
        bar.hidden = false;
        bar.addEventListener("click", function (e) {{
          var b = e.target.closest("button");
          if (!b) return;
          var f = b.dataset.filter, shown = 0;
          bar.querySelectorAll("button").forEach(function (x) {{
            x.setAttribute("aria-pressed", String(x === b));
          }});
          grid.querySelectorAll(".cat-card").forEach(function (c) {{
            var on = f === "all" || (" " + c.dataset.f + " ").indexOf(" " + f + " ") >= 0;
            c.hidden = !on;
            if (on) shown++;
          }});
          count.textContent = shown;
        }});
      }})();
    </script>
""".format(n=len(devices), buttons=buttons, devices=tiles(devices),
           n_capture=len(catalog["capture"]), capture=tiles(catalog["capture"]),
           n_cases=len(catalog["cases"]), cases=tiles(catalog["cases"]))

    return render_page(shell, {
        "title": "Supported boards and cases - ESP-KVM, an open-source ESP32-P4 IP-KVM",
        "og_title": "ESP-KVM boards and cases",
        "description": "The ESP32-P4 boards ESP-KVM runs on, which ones have been run on "
                       "hardware, the HDMI capture boards and printed cases for them.",
        "canonical": SITE + "/boards/",
        "og_type": "website",
    }, content)


# Board names as they are written in posts and pages, and the page each one
# means. Longest first: "ESP32-P4-NANO-WIFI6-DB" must not become a link to the
# NANO. A name only counts as a whole name - "ESP32-P4-WIFI6" followed by
# "-POE-ETH" is the PoE board, so a trailing hyphen or letter rules a match out.
BOARD_NAMES = [
    (r"(?:Waveshare )?(?:ESP32-P4-)?NANO-WIFI6-DB", "p4-nano-wifi6-db"),
    (r"(?:Espressif )?ESP32-P4X-C5[- ]Function[- ]EV(?:[- ]Board)?", "funcev-c5"),
    (r"(?:Waveshare )?ESP32-P4-WIFI6-DB", "p4-wifi6-db"),
    (r"(?:Waveshare )?(?:ESP32-P4-)?WIFI6-POE-ETH", "p4-poe"),
    (r"(?:Waveshare )?(?:ESP32-P4-)?WIFI6-DEV-KIT", "p4-wifi6-devkit"),
    (r"(?:Waveshare )?(?:ESP32-P4-)?Module-DEV-KIT", "p4-module-devkit"),
    (r"(?:Waveshare )?(?:ESP32-P4-)?WIFI6", "p4-wifi6"),
    (r"(?:Waveshare )?(?:ESP32-P4-)?NANO", "p4-nano"),
    (r"(?:Waveshare )?(?:ESP32-)?P4-ETH", "p4-eth"),
    (r"(?:Espressif )?(?:ESP32-P4X? )?Function EV(?: Board)?", "funcev"),
    (r"Guition (?:ESP32-P4-)?M3-Dev", "p4-guition"),
    (r"(?:DFRobot )?FireBeetle 2(?: ESP32-P4)?", "firebeetle2-p4"),
    (r"(?:VIEWE )?ESP32-P4-Pi", "viewe-p4-pi"),
    (r"(?:M5Stack )?(?:Unit )?PoE-P4X", "m5-poe-p4x"),
    (r"(?:M5Stack )?(?:Unit )?PoE-P4", "m5-poe-p4"),
    (r"(?:Geekworm )?C790", "c790"),
    (r"(?:Waveshare )?HDMI to CSI Adapter", "waveshare-19137"),
    (r"(?:M5Stack )?Add-on Display In", "m5-addon-display-in"),
]
BOARD_NAME_RE = re.compile(
    r"(?<![\w-])(?:%s)(?![\w-])" % "|".join("(%s)" % p for p, _ in BOARD_NAMES))
# Text inside these is never linked: a link inside a link is invalid, and a
# heading, code or a script should read exactly as written.
NO_LINK_TAGS = {"a", "h1", "h2", "h3", "h4", "h5", "h6", "code", "pre", "script",
                "style", "title", "button", "label", "select", "option", "textarea",
                "summary", "th"}


def link_boards(body, known, skip=()):
    """Link the first mention of each board to its page. `known` is the set of
    board ids that have a page; `skip` holds ids not to link (the page's own)."""
    done = set(skip)
    depth = []
    out = []
    for part in re.split(r"(<[^>]+>)", body):
        if part.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)", part)
            if m:
                tag = m.group(2).lower()
                if tag in NO_LINK_TAGS and not part.endswith("/>"):
                    if m.group(1):
                        if tag in depth:
                            depth.reverse()
                            depth.remove(tag)
                            depth.reverse()
                    else:
                        depth.append(tag)
            out.append(part)
            continue
        if depth or not part.strip():
            out.append(part)
            continue

        def swap(match):
            idx = next(i for i, g in enumerate(match.groups()) if g is not None)
            bid = BOARD_NAMES[idx][1]
            if bid in done or bid not in known:
                return match.group(0)
            done.add(bid)
            return '<a href="/boards/%s/">%s</a>' % (bid, match.group(0))
        out.append(BOARD_NAME_RE.sub(swap, part))
    return "".join(out)


def write_catalog(shell, catalog):
    import shutil
    for item in catalog["all"]:
        out = os.path.join(ROOT, item["section"], item["id"])
        os.makedirs(out, exist_ok=True)
        for name in os.listdir(item["folder"]):
            if name != "index.md":
                shutil.copy2(os.path.join(item["folder"], name), os.path.join(out, name))
        write(os.path.join(out, "index.html"), item_page(shell, item, catalog))
    write(os.path.join(ROOT, "boards", "index.html"), catalog_page(shell, catalog))


# ---------------------------------------------------------------- page shell

def read_partial(name):
    path = os.path.join(PARTIALS_DIR, name)
    if not os.path.exists(path):
        sys.exit("missing partial: _partials/%s" % name)
    with open(path, encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def load_shell():
    """The three pieces every page on this site is built from."""
    return {
        "style": read_partial("style.css"),
        "nav": read_partial("nav.html"),
        "footer": read_partial("footer.html"),
    }


def safe(text):
    """Escape for an attribute, but leave HTML entities the author wrote alone."""
    text = re.sub(r"&(?!#?\w+;)", "&amp;", text)
    return text.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_page(shell, meta, content, page_head=""):
    with open(TEMPLATE, encoding="utf-8") as fh:
        page = fh.read()

    fields = {
        "title": safe(meta["title"]),
        "description": safe(meta["description"]),
        "canonical": meta["canonical"],
        "og_title": safe(meta.get("og_title") or meta["title"]),
        "og_description": safe(meta.get("og_description") or meta["description"]),
        "og_type": meta.get("og_type") or "article",
        "image": meta.get("image") or OG_IMAGE,
        "image_alt": safe(meta.get("image_alt")
                          or "The ESP-KVM console showing a target machine's "
                             "desktop in a browser."),
        "style": shell["style"],
        "nav": shell["nav"],
        "footer": shell["footer"],
        "content": content,
        "page_head": page_head,
    }
    for key, value in fields.items():
        page = page.replace("{{%s}}" % key, value)

    left = re.search(r"\{\{(\w+)\}\}", page)
    if left:
        sys.exit("_templates/page.html: nothing fills {{%s}}" % left.group(1))
    return page


# ---------------------------------------------------------------- pages
#
# A page in _pages/ is front matter and then the markup that sits between the
# navigation and the footer. Two things are lifted out of it into <head>: a
# <style> block, because rules belong in the head, and a JSON-LD block, because
# that is where a search engine goes looking for it.

def build_pages(shell, catalog):
    written = []
    for name in sorted(os.listdir(PAGES_DIR)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(PAGES_DIR, name)
        with open(path, encoding="utf-8") as fh:
            meta, body = split_front_matter(fh.read(), path)

        for required in ("title", "description", "canonical", "output"):
            if required not in meta:
                sys.exit("%s: front matter needs a %s" % (path, required))

        head = []
        for pattern in (r"<style>.*?</style>",
                        r'<script type="application/ld\+json">.*?</script>'):
            for block in re.findall(pattern, body, re.S):
                head.append("    " + block.strip())
                body = body.replace(block, "", 1)

        out = meta["output"]
        url = "/" + out[: -len("index.html")] if out.endswith("index.html") else "/" + out
        # A page asks for a share row by leaving this comment where it goes.
        body = body.replace("<!-- share -->", share_links(SITE + url, meta["title"]))
        body = fill_catalog(body, catalog)
        body = link_boards(body, set(catalog["by_id"]))
        body = re.sub(r"\n{3,}", "\n\n", body).strip("\n")
        write(os.path.join(ROOT, meta["output"]),
              render_page(shell, meta, body, "\n".join(head)))
        write_redirects(meta.get("redirect_from", ""), url)
        written.append(out)
    return written


# ---------------------------------------------------------------- markdown
#
# A deliberately small Markdown, written here rather than pulled in, so that
# building the site needs nothing but Python. It covers what these posts
# actually use - headings, paragraphs, fenced code, lists, quotes, rules,
# images, and inline emphasis, code and links - and refuses anything else
# loudly, so a post can never render wrong in silence.

INLINE_CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD = re.compile(r"\*\*(\S(?:[^*]*\S)?)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*(\S(?:[^*]*\S)?)\*(?!\*)")
IMAGE_ONLY = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)$")


def inline(text, where):
    """Escape a line of prose, then put the inline markup back as HTML."""
    spans = []

    def stash(match):
        spans.append(html.escape(match.group(1)))
        return "\x00%d\x00" % (len(spans) - 1)

    text = INLINE_CODE.sub(stash, text)
    if "`" in text:
        sys.exit("%s: an inline code span is never closed" % where)

    text = html.escape(text)
    text = LINK.sub(r'<a href="\2">\1</a>', text)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITALIC.sub(r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00",
                  lambda m: "<code>%s</code>" % spans[int(m.group(1))], text)


def render_markdown(text, where="post"):
    lines = text.split("\n")
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # An HTML comment is a note to myself; keep it, it costs a few bytes
        # and it is how the images still to be taken are marked.
        if stripped.startswith("<!--"):
            block = []
            while i < len(lines):
                block.append(lines[i])
                if "-->" in lines[i]:
                    break
                i += 1
            else:
                sys.exit("%s: an HTML comment is never closed" % where)
            out.append("\n".join(l.strip() for l in block))
            i += 1
            continue

        # An <iframe> is passed through as it was written, in a box that keeps
        # its aspect ratio on a narrow screen. The only markup allowed in raw:
        # a video player is the one thing this page cannot draw itself.
        if stripped.startswith("<iframe"):
            block = []
            while i < len(lines):
                block.append(lines[i].strip())
                if "</iframe>" in lines[i]:
                    break
                i += 1
            else:
                sys.exit("%s: an <iframe> is never closed" % where)
            out.append('<div class="video-embed">%s</div>' % " ".join(block))
            i += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            if i >= len(lines):
                sys.exit("%s: a code fence is never closed" % where)
            attribute = ' class="language-%s"' % language if language else ""
            out.append("<pre><code%s>%s</code></pre>"
                       % (attribute, html.escape("\n".join(body))))
            i += 1
            continue

        if stripped in ("---", "***", "___"):
            out.append("<hr />")
            i += 1
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            if level > 4 or not stripped[level:].startswith(" "):
                sys.exit("%s: cannot read this heading: %s" % (where, stripped))
            if level == 1:
                sys.exit("%s: the page already prints the title as h1 - "
                         "start sections at ##" % where)
            out.append("<h%d>%s</h%d>"
                       % (level, inline(stripped[level:].strip(), where), level))
            i += 1
            continue

        # A table: a header row, a |---| row, then body rows, each on one line.
        # Colons in the rule row set the alignment, as in GitHub's Markdown.
        if stripped.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                if not row.endswith("|"):
                    sys.exit("%s: a table row must end with |: %s" % (where, row))
                rows.append([cell.strip() for cell in row[1:-1].split("|")])
                i += 1
            if len(rows) < 2 or not all(re.match(r"^:?-+:?$", c) for c in rows[1]):
                sys.exit("%s: a table needs a header row and a |---| row under it" % where)
            width = len(rows[0])
            for row in rows:
                if len(row) != width:
                    sys.exit("%s: a table row has %d cells, the header %d: %s"
                             % (where, len(row), width, " | ".join(row)))
            aligns = []
            for rule in rows[1]:
                if rule.startswith(":") and rule.endswith(":"):
                    aligns.append(' style="text-align: center"')
                elif rule.endswith(":"):
                    aligns.append(' style="text-align: right"')
                else:
                    aligns.append("")
            head = "".join("<th%s>%s</th>" % (aligns[k], inline(c, where))
                           for k, c in enumerate(rows[0]))
            body = "\n".join(
                "    <tr>%s</tr>" % "".join("<td%s>%s</td>" % (aligns[k], inline(c, where))
                                          for k, c in enumerate(row))
                for row in rows[2:])
            out.append('<div class="table-scroll">\n<table>\n  <thead><tr>%s</tr></thead>\n'
                       "  <tbody>\n%s\n  </tbody>\n</table>\n</div>" % (head, body))
            continue

        if line.startswith(("  -", "  *", "    -")):
            sys.exit("%s: nested lists are not supported: %s" % (where, stripped))

        # Lists: a run of lines that all start the same way.
        bullet = re.match(r"^([-*])\s+(.*)$", stripped)
        number = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if bullet or number:
            tag = "ul" if bullet else "ol"
            pattern = r"^([-*])\s+(.*)$" if bullet else r"^(\d+)\.\s+(.*)$"
            items = []
            while i < len(lines):
                match = re.match(pattern, lines[i].strip())
                if not match:
                    break
                items.append("  <li>%s</li>" % inline(match.group(2), where))
                i += 1
            out.append("<%s>\n%s\n</%s>" % (tag, "\n".join(items), tag))
            continue

        if stripped.startswith(">"):
            quoted = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quoted.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote><p>%s</p></blockquote>"
                       % inline(" ".join(quoted), where))
            continue

        # A picture on a line of its own becomes a figure, and its alt text
        # doubles as the caption - the two should say the same thing anyway.
        picture = IMAGE_ONLY.match(stripped)
        if picture:
            alt, src = picture.group(1), picture.group(2)
            caption = ("\n  <figcaption>%s</figcaption>" % inline(alt, where)
                       if alt else "")
            out.append('<figure>\n  <img src="%s" alt="%s" loading="lazy" />%s'
                       "\n</figure>" % (html.escape(src), html.escape(alt), caption))
            i += 1
            continue

        # Anything else is a paragraph, running to the next blank line.
        body = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(
                ("#", "```", ">", "<!--", "|")):
            if re.match(r"^([-*]|\d+\.)\s+", lines[i].strip()):
                break
            body.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % inline(" ".join(body), where))

    return "\n".join(out)


def human_date(date):
    return "%d %s %d" % (date.day, MONTHS[date.month - 1], date.year)


def rss_date(date):
    stamped = date.replace(hour=9, tzinfo=timezone.utc)
    return stamped.strftime("%a, %d %b %Y %H:%M:%S +0000")


def tag_links(tags):
    """The tags of one post, as a row of links to their pages."""
    if not tags:
        return ""
    items = "".join('<a class="tag" href="/blog/tags/%s/">%s</a>'
                    % (html.escape(t), html.escape(t)) for t in tags)
    return '<p class="tag-row">%s</p>' % items


def tags_index(posts):
    """Every tag with the posts carrying it, most-used first then alphabetical."""
    index = {}
    for post in posts:
        for tag in post["tags"]:
            index.setdefault(tag, []).append(post)
    return dict(sorted(index.items(), key=lambda kv: (-len(kv[1]), kv[0])))


def share_links(url, text):
    """A row of plain share links. Each is an ordinary link to the network's own
    share form - no script from any of them loads here, so nobody is tracked for
    reading. Mastodon has no one address to send to, which is what Copy link is
    for; the footer's script shows that button and makes it work."""
    text = html.unescape(text)
    u, t = quote(url, safe=""), quote(text, safe="")
    links = [
        ("X", "https://x.com/intent/post?text=%s&url=%s" % (t, u)),
        ("Reddit", "https://www.reddit.com/submit?url=%s&title=%s" % (u, t)),
        ("Hacker News", "https://news.ycombinator.com/submitlink?u=%s&t=%s" % (u, t)),
        ("LinkedIn", "https://www.linkedin.com/sharing/share-offsite/?url=%s" % u),
        ("Telegram", "https://t.me/share/url?url=%s&text=%s" % (u, t)),
        ("Bluesky", "https://bsky.app/intent/compose?text=%s" % quote(text + " " + url, safe="")),
    ]
    items = "".join('<a class="btn btn-sm" href="%s" rel="noopener" target="_blank">%s</a>'
                    % (html.escape(href), name) for name, href in links)
    return ('<p class="share"><span class="share-label">Share</span>%s'
            '<button type="button" class="btn btn-sm share-copy" data-url="%s" hidden>Copy link</button></p>'
            % (items, html.escape(url)))


def post_page(shell, post, known=frozenset()):
    hero = ""
    if post["image"]:
        hero = ('<figure class="post-hero"><img src="%s" alt="" loading="lazy" />'
                "</figure>" % html.escape(post["image"]))

    content = """
    <article class="post">
      <header class="post-head">
        <p class="post-back"><a href="/blog/">&larr; All posts</a></p>
        <h1>{title}</h1>
        <p class="post-meta"><time datetime="{iso}">{human}</time></p>
        {tags}
      </header>
      {hero}
      <div class="post-body">
{body}
      </div>
      <footer class="post-foot">
        <p>
          ESP-KVM is an open-source IP-KVM on the ESP32-P4 &mdash;
          <a href="https://github.com/espkvm/espkvm">the code is on GitHub</a>,
          and you can <a href="/flash/">install it from the browser</a> or
          <a href="https://demo.espkvm.io/">try the console</a> without any hardware.
        </p>
        <p class="post-meta">
          New posts go out on <a href="https://t.me/espkvm" rel="noopener">Telegram</a>,
          <a href="https://x.com/espkvm" rel="noopener">X</a> and
          <a href="/blog/feed.xml">RSS</a>.
        </p>
        {share}
      </footer>
    </article>
""".format(
        title=html.escape(post["title"]),
        iso=post["date"].strftime("%Y-%m-%d"),
        human=human_date(post["date"]),
        hero=hero,
        tags=tag_links(post["tags"]),
        body=link_boards(render_markdown(post["body"], post["path"]), known),
        share=share_links("%s/blog/%s/" % (SITE, post["slug"]), post["title"] + " - ESP-KVM"),
    )

    return render_page(shell, {
        "title": "%s - ESP-KVM" % post["title"],
        "og_title": post["title"],
        "description": post["description"],
        "canonical": "%s/blog/%s/" % (SITE, post["slug"]),
        "image": SITE + post["thumb"] if post["thumb"].startswith("/") else "",
        "og_type": "article",
    }, content)


def index_page(shell, posts, tag=None, all_tags=None):
    """The blog index, or one tag's slice of it when `tag` is given."""
    if posts:
        items = "\n".join(
            """        <li class="post-item{thumb_class}">
{thumb}          <div class="post-item-text">
            <p class="post-meta"><time datetime="{iso}">{human}</time></p>
            <h2><a href="/blog/{slug}/">{title}</a></h2>
            <p>{description}</p>
            {tags}
          </div>
        </li>""".format(
                iso=p["date"].strftime("%Y-%m-%d"),
                human=human_date(p["date"]),
                slug=p["slug"],
                title=html.escape(p["title"]),
                description=html.escape(p["description"]),
                tags=tag_links(p["tags"]),
                # A post with a picture shows it here as well. The alt is empty
                # on purpose: the heading right next to it already says what the
                # post is, and a screen reader repeating that helps nobody.
                thumb_class=" has-thumb" if p["thumb"] else "",
                thumb=('          <a class="post-thumb" href="/blog/%s/" tabindex="-1" '
                       'aria-hidden="true"><img src="%s" alt="" loading="lazy" /></a>\n'
                       % (p["slug"], html.escape(p["thumb"])) if p["thumb"] else ""),
            )
            for p in posts
        )
        listing = '<ul class="post-list">\n%s\n      </ul>' % items
    else:
        listing = "<p>Nothing here yet.</p>"

    # The whole tag list, on every index, so one tag's page is not a dead end.
    cloud = ""
    if all_tags:
        links = "".join(
            '<a class="tag%s" href="/blog/tags/%s/">%s <span>%d</span></a>'
            % (" tag-on" if t == tag else "", html.escape(t), html.escape(t), len(ps))
            for t, ps in all_tags.items()
        )
        cloud = '<p class="tag-row tag-cloud">%s%s</p>' % (
            '<a class="tag%s" href="/blog/">all <span>%d</span></a>'
            % ("" if tag else " tag-on",
               len({p["slug"] for ps in all_tags.values() for p in ps}) if tag else len(posts)),
            links)

    if tag:
        heading = "Tagged %s" % html.escape(tag)
        blurb = ("%d post%s tagged %s. <a href=\"/blog/\">All posts</a>."
                 % (len(posts), "" if len(posts) == 1 else "s", html.escape(tag)))
    else:
        heading = "Blog"
        blurb = ("What broke, what the number was, and what the chip turned out "
                 "to be doing. <a href=\"/blog/feed.xml\">RSS</a>.")

    content = """
    <div class="post">
      <header class="post-head">
        <h1>{heading}</h1>
        <p class="post-meta">{blurb}</p>
        {cloud}
      </header>
      {listing}
    </div>
""".format(heading=heading, blurb=blurb, cloud=cloud, listing=listing)

    if tag:
        meta = {
            "title": "Posts tagged %s - ESP-KVM" % tag,
            "og_title": "ESP-KVM posts tagged %s" % tag,
            "description": "Every ESP-KVM release note and engineering write-up "
                           "tagged %s." % tag,
            "canonical": "%s/blog/tags/%s/" % (SITE, tag),
            "og_type": "website",
        }
    else:
        meta = {
            "title": "Blog - ESP-KVM",
            "og_title": "The ESP-KVM blog",
            "description": "Engineering notes from building an open-source IP-KVM "
                           "on the ESP32-P4: the bugs, the measurements and the fixes.",
            "canonical": SITE + "/blog/",
            "og_type": "website",
        }
    return render_page(shell, meta, content)


def feed(posts):
    built = rss_date(posts[0]["date"]) if posts else rss_date(datetime(2026, 1, 1))
    items = "\n".join(
        """    <item>
      <title>{title}</title>
      <link>{site}/blog/{slug}/</link>
      <guid isPermaLink="true">{site}/blog/{slug}/</guid>
      <pubDate>{date}</pubDate>
      <description>{description}</description>
    </item>""".format(
            title=html.escape(p["title"]),
            site=SITE,
            slug=p["slug"],
            date=rss_date(p["date"]),
            description=html.escape(p["description"]),
        )
        for p in posts
    )
    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>ESP-KVM</title>
    <link>{site}/blog/</link>
    <atom:link href="{site}/blog/feed.xml" rel="self" type="application/rss+xml" />
    <description>Engineering notes from building an open-source IP-KVM on the ESP32-P4.</description>
    <language>en</language>
    <lastBuildDate>{built}</lastBuildDate>
{items}
  </channel>
</rss>
""".format(site=SITE, built=built, items=items)


REDIRECT_HTML = """<!doctype html>
<!-- Written by tools/build-site.py: this address moved, and something out
     there still points at it. -->
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>This page has moved</title>
    <link rel="canonical" href="%(url)s" />
    <meta http-equiv="refresh" content="0; url=%(url)s" />
    <meta name="robots" content="noindex" />
    <link rel="icon" href="/favicon.ico" sizes="any" />
    <style>
      html { color-scheme: dark; }
      body {
        margin: 0; min-height: 100vh; display: flex; align-items: center;
        justify-content: center; background: #0b0d10; color: #c8cdd4;
        font: 16px/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI",
          Roboto, Helvetica, Arial, sans-serif;
        text-align: center; padding: 24px;
      }
      a { color: #7cc4ff; }
    </style>
  </head>
  <body>
    <p>
      This page has moved to <a href="%(url)s">%(pretty)s</a>.
      <br />You are being taken there now.
    </p>
    <script>
      location.replace("%(url)s");
    </script>
  </body>
</html>
"""


def write_redirects(redirect_from, target):
    """
    Old addresses that should still land somewhere.

    GitHub Pages serves files, so there is no 301 to be had: a stub with a
    canonical link, a refresh and a location.replace is what a static host can
    do, and it is what search engines read. Put the old site-root path in the
    front matter as `redirect_from` (several, comma-separated) whenever a page
    or a post is renamed.
    """
    for raw in (redirect_from or "").split(","):
        old = raw.strip().strip("/")
        if not old:
            continue
        if old == target.strip("/"):
            sys.exit("redirect_from points at the page itself: /%s/" % old)
        url = SITE + target
        write(os.path.join(ROOT, old, "index.html"),
              REDIRECT_HTML % {"url": url, "pretty": target})


def page_urls(pages):
    """Rendered output paths as URLs: "flash/index.html" -> "/flash/"."""
    urls = []
    for out in pages or []:
        url = "/" + out[: -len("index.html")] if out.endswith("index.html") else "/" + out
        urls.append((url, "1.0" if url == "/" else "0.8"))
    return urls


def sitemap(posts, tags=None, pages=None, catalog=None):
    entries = "".join(
        "  <url>\n    <loc>%s%s</loc>\n    <priority>%s</priority>\n  </url>\n"
        % (SITE, path, priority)
        for path, priority in page_urls(pages)
    )
    if catalog:
        entries += "  <url>\n    <loc>%s/boards/</loc>\n    <priority>0.8</priority>\n  </url>\n" % SITE
        entries += "".join(
            "  <url>\n    <loc>%s%s</loc>\n    <priority>0.7</priority>\n  </url>\n"
            % (SITE, item["url"]) for item in catalog["all"])
    entries += "".join(
        "  <url>\n    <loc>%s/blog/%s/</loc>\n    <lastmod>%s</lastmod>\n"
        "    <priority>0.6</priority>\n  </url>\n"
        % (SITE, p["slug"], p["date"].strftime("%Y-%m-%d"))
        for p in posts
    )
    # A tag page is a real listing of real posts, so it belongs in the sitemap -
    # below the posts themselves, which are what a reader actually wants.
    entries += "".join(
        "  <url>\n    <loc>%s/blog/tags/%s/</loc>\n    <priority>0.4</priority>\n  </url>\n"
        % (SITE, tag)
        for tag in (tags or {})
    )
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            "%s</urlset>\n" % entries)


# ---------------------------------------------------------------- main

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--drafts", action="store_true",
                        help="build posts marked draft: true as well")
    args = parser.parse_args()

    posts = read_posts(args.drafts)
    shell = load_shell()

    catalog = read_catalog()
    pages = build_pages(shell, catalog)
    write_catalog(shell, catalog)

    for post in posts:
        write(os.path.join(OUT_DIR, post["slug"], "index.html"),
              post_page(shell, post, set(catalog["by_id"])))
        write_redirects(post["redirect_from"], "/blog/%s/" % post["slug"])

    tags = tags_index(posts)
    for tag, tagged in tags.items():
        write(os.path.join(OUT_DIR, "tags", tag, "index.html"),
              index_page(shell, tagged, tag=tag, all_tags=tags))

    write(os.path.join(OUT_DIR, "index.html"),
          index_page(shell, posts, all_tags=tags))
    write(os.path.join(OUT_DIR, "feed.xml"), feed(posts))
    write(os.path.join(ROOT, "sitemap.xml"), sitemap(posts, tags, pages, catalog))

    print("pages:")
    for output in pages:
        print("  /%s" % output)
    print("catalog: %d boards, %d cases" % (
        len(catalog["all"]) - len(catalog["cases"]), len(catalog["cases"])))
    print("blog: %d post%s, %d tag%s"
          % (len(posts), "" if len(posts) == 1 else "s",
             len(tags), "" if len(tags) == 1 else "s"))
    for post in posts:
        print("  /blog/%s/  %s" % (post["slug"], post["title"]))
    for tag, tagged in tags.items():
        print("  /blog/tags/%s/  %d post%s"
              % (tag, len(tagged), "" if len(tagged) == 1 else "s"))


if __name__ == "__main__":
    main()
