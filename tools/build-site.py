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
import json
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
            "image_link": meta.get("image_link", ""),
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
# Front matter a board takes: title, kind (device or capture), status (tested,
# untested, or planned: a device with no image yet, listed apart), order, role, summary, photo, photo_style (product or photo),
# flasher (its id in the firmware's boards.json), rev3 ("image only" when a rev
# 3.x image exists but no rev 3.x board has been seen), capture (ids of the capture
# boards it takes), and any number of "spec.<Label>: value" rows and
# "link.<Label>: url" links, shown in the order written. A case takes title,
# author, summary, boards (ids it fits), photo, photo_credit and links.
# A module in _modules/ (a status display, a clock or a serial adapter) takes
# title, kind (display, clock, serial, control or terminal), status, order, role, summary, photo, chip (the label on
# its tile), boards (ids it plugs straight into), specs and links, and
# tile_maker / tile_model when the title does not split at its first space.

BOARDS_DIR = os.path.join(ROOT, "_boards")
CASES_DIR = os.path.join(ROOT, "_cases")
MODULES_DIR = os.path.join(ROOT, "_modules")
MODULE_KINDS = {"display": ("Status displays", "displays", "a status display for an IP-KVM"),
                "clock": ("Clocks", "clocks", "a clock for an IP-KVM"),
                "serial": ("Serial adapters", "serial", "a serial adapter for an IP-KVM"),
                "control": ("Power control and buttons", "control", "power control for an IP-KVM"),
                "terminal": ("Terminal parts", "terminal", "a handheld terminal for an IP-KVM")}
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
    modules = read_folder_items(MODULES_DIR, "modules")
    ids = {b["id"] for b in boards}
    for mod in modules:
        m = mod["meta"]
        if m.get("kind") not in MODULE_KINDS:
            sys.exit("%s: kind must be one of %s" % (mod["path"], ", ".join(MODULE_KINDS)))
        if m.get("status") not in ("tested", "untested"):
            sys.exit("%s: status must be tested or untested" % mod["path"])
        for b in id_list(m.get("boards")):
            if b not in ids:
                sys.exit("%s: boards names a board that is not in _boards/: %s" % (mod["path"], b))
    for b in boards:
        m = b["meta"]
        if m.get("kind") not in ("device", "capture"):
            sys.exit("%s: kind must be device or capture" % b["path"])
        if m.get("status") not in ("tested", "untested", "planned"):
            sys.exit("%s: status must be tested, untested or planned" % b["path"])
        if m.get("status") == "planned" and (m.get("kind") != "device" or m.get("flasher")):
            sys.exit("%s: a planned board is a device with no flasher id" % b["path"])
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
        "planned": sorted([b for b in boards if b["meta"]["status"] == "planned"], key=key),
        "capture": sorted([b for b in boards if b["meta"]["kind"] == "capture"], key=key),
        "cases": sorted(cases, key=key),
        "displays": sorted([m for m in modules if m["meta"]["kind"] == "display"], key=key),
        "clocks": sorted([m for m in modules if m["meta"]["kind"] == "clock"], key=key),
        "serial": sorted([m for m in modules if m["meta"]["kind"] == "serial"], key=key),
        "control": sorted([m for m in modules if m["meta"]["kind"] == "control"], key=key),
        "terminal": sorted([m for m in modules if m["meta"]["kind"] == "terminal"], key=key),
        "all": boards + cases + modules,
        "by_id": {b["id"]: b for b in boards},
    }


def family_slug(name):
    """A maker's family as a URL part: "M5Stack" -> "m5stack"."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def families(catalog):
    """Everything that names a family, by family: {slug: (name, [items])}."""
    out = {}
    for item in catalog["all"]:
        name = item["meta"].get("family")
        if name:
            out.setdefault(family_slug(name), (name, []))[1].append(item)
    return out


def family_page(shell, slug, name, items):
    """One family's parts on one page, in the catalog's own order of sections."""
    key = lambda i: (i["order"], i["meta"]["title"])
    groups = [
        ("ESP32-P4 boards", [i for i in items if i["meta"].get("kind") == "device"]),
        ("HDMI capture", [i for i in items if i["meta"].get("kind") == "capture"]),
    ]
    for kind, (title, _, _) in MODULE_KINDS.items():
        groups.append((title, [i for i in items if i["section"] == "modules"
                               and i["meta"].get("kind") == kind]))
    groups.append(("Cases", [i for i in items if i["section"] == "cases"]))
    sections = "".join(
        '\n      <h2 class="cat-head">%s <span class="cat-count">%d</span></h2>'
        '\n      <div class="cat-grid">\n%s\n      </div>'
        % (html.escape(title), len(group), tiles(sorted(group, key=key)))
        for title, group in groups if group)
    # Optional text for a family's page: _families/<slug>.md
    extra = ""
    intro = os.path.join(ROOT, "_families", slug + ".md")
    if os.path.exists(intro):
        with open(intro, encoding="utf-8") as f:
            extra = "\n" + render_markdown(f.read(), intro)
    content = """
    <article class="board-page">
      <p class="post-back"><a href="/boards/">&larr; All boards</a></p>
      <h1>{name} and ESP-KVM</h1>
      <p class="lead">
        Every {name} part on this site: the boards ESP-KVM runs on, the capture
        that feeds them and the modules that plug in. "Untested" means built from
        the maker's documentation and not yet run by anyone.
      </p>{extra}{sections}
    </article>
""".format(name=html.escape(name), extra=extra, sections=sections)
    url = SITE + "/boards/family/%s/" % slug
    return render_page(shell, {
        "title": "%s parts for ESP-KVM, an open-source ESP32-P4 IP-KVM" % name,
        "og_title": "%s and ESP-KVM" % name,
        "description": "The %s boards, HDMI capture and modules ESP-KVM works with, "
                       "and which of them have been run on hardware." % name,
        "canonical": url,
        "og_type": "website",
    }, content, json_ld(breadcrumbs(("ESP-KVM", SITE + "/"), ("Boards", SITE + "/boards/"),
                                    (name, url))))


# The rows of the comparison, in this order; a spec not listed here comes after.
# Memory and Network are split into one row per part.
COMPARE_ROWS = ["Status", "Fit for a KVM", "Chip", "PSRAM", "Flash", "Ethernet", "PoE", "Wi-Fi", "HDMI capture",
                "Capture connector",
                "To the target", "microSD", "HDMI-CEC", "HDMI audio", "Measured"]


# The capture boards' comparison: the same table, rows of their own.
COMPARE_CAPTURE_ROWS = ["Status", "Bridge", "Input", "HDMI out", "15-pin ribbon", "22-pin ribbon",
                        "24-pin ribbon (M5Stack)", "Works with",
                        "HDMI-CEC", "HDMI audio", "Power", "Measured"]


def capture_cells(d, catalog):
    """A capture board's cells: row -> (text, score), as compare_cells."""
    specs = dict(d["specs"])
    cells = {k: (v, None) for k, v in specs.items()}
    tested = d["meta"]["status"] == "tested"
    cells["Status"] = ('<span class="cat-status">Tested</span>' if tested
                       else '<span class="cat-status untested">Untested</span>', int(tested))
    out = specs.get("HDMI out", "")
    cells["HDMI out"] = (out, int(out.startswith("pass")))
    for row in ("15-pin ribbon", "22-pin ribbon"):
        v = specs.get(row, "")
        cells[row] = (v, int(v.startswith("yes")))
    # M5Stack's own cable fits only M5Stack's own boards: a warning, not a plus.
    v = specs.get("24-pin ribbon (M5Stack)", "")
    cells["24-pin ribbon (M5Stack)"] = (v, "warn" if v.startswith("yes") else None)
    cec = specs.get("HDMI-CEC", "")
    cells["HDMI-CEC"] = (cec, int(cec.startswith("yes")))
    users = [b for b in catalog["tested"] + catalog["untested"]
             if d["id"] in id_list(b["meta"].get("capture"))]
    fams = {b["meta"].get("family") for b in users}
    if users and len(fams) == 1 and None not in fams and len(users) <= 3:
        # One maker's boards only: name them, and mark it as the limit it is.
        fam = fams.pop()
        cells["Works with"] = ("only %s: %s" % (fam, ", ".join(
            "[%s](%s)" % (b["meta"]["title"].replace(fam + " ", "", 1), b["url"])
            for b in users)), "warn")
    else:
        cells["Works with"] = ("%d ESP32-P4 board%s" % (len(users), "" if len(users) == 1 else "s")
                               if users else "", len(users))
    return cells


SIZE_PX_PER_MM = 1.2  # one scale for every board, so the drawings compare


def size_px(text):
    """"78 x 21 mm" -> the outline in pixels, long side across. Only the first
    two numbers count (a case's depth, an antenna are in the text)."""
    nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)[:2]]
    if len(nums) < 2:
        return (0, 0)
    return (round(max(nums) * SIZE_PX_PER_MM), round(min(nums) * SIZE_PX_PER_MM))


def size_label(text):
    """"30 x 45 mm, 12 mm tall" -> "45 x 30 mm": long side first, as drawn."""
    nums = re.findall(r"\d+(?:\.\d+)?", text)[:2]
    if len(nums) < 2:
        return text.split(",")[0]
    a, b = sorted(nums, key=float, reverse=True)
    return "%s x %s mm" % (a, b)


def size_drawing(text):
    """The board's outline to scale, as a rectangle."""
    w, h = size_px(text)
    if not w:
        return ""
    return ('<svg class="cmp-size" width="%d" height="%d" viewBox="0 0 %d %d" aria-hidden="true">'
            '<rect x="1" y="1" width="%d" height="%d" rx="3"/></svg>') % (
        w + 2, h + 2, w + 2, h + 2, w, h)


def compare_cells(d, catalog):
    """A board's cells for the comparison: row -> (text, score). The score
    marks the best of the boards shown; None where a row has no better."""
    specs = dict(d["specs"])
    cells = {}
    for k, v in specs.items():
        if k not in ("Memory", "Network"):
            cells[k] = (v, None)
    tested = d["meta"]["status"] == "tested"
    cells["Status"] = ('<span class="cat-status">Tested</span>' if tested
                       else '<span class="cat-status untested">Untested</span>', int(tested))
    halves, parts = fit(d)
    earned = ",".join("%g" % (p * g) for (p, _), (_, g) in zip(FIT, parts))
    cells["Fit for a KVM"] = ('<span class="cat-fit" data-fit="%s">%s</span> <span class="fit-t">%s</span>'
                              % (earned, fit_icons(halves), fit_text(halves)), halves)
    chip = specs.get("Chip", "")
    cells["Chip"] = (chip, int("rev 3" in chip))

    mem = specs.get("Memory", "")
    m = re.search(r"(\d+) MB PSRAM", mem)
    cells["PSRAM"] = (m.group(1) + " MB" if m else "", int(m.group(1)) if m else 0)
    m = re.search(r"(\d+) MB flash", mem)
    cells["Flash"] = (m.group(1) + " MB" if m else "", int(m.group(1)) if m else 0)

    net = specs.get("Network", "")
    m = re.search(r"(\d+M) Ethernet", net)
    cells["Ethernet"] = (m.group(1) if m else "", int(bool(m)))
    if "802.3at" in net:
        poe = ("802.3at", 2)
    elif "add-on" in net:
        poe = ("with an add-on module", 1)
    elif "PoE" in net:
        poe = ("yes", 2)
    else:
        poe = ("", 0)
    cells["PoE"] = poe
    m = re.search(r"((?:dual-band )?Wi-Fi \d+) \((ESP32-\w+)\)", net)
    cells["Wi-Fi"] = (("%s, %s" % (m.group(1), m.group(2))) if m else "",
                      (2 if "dual-band" in m.group(1) else 1) if m else 0)

    caps = [catalog["by_id"][c] for c in id_list(d["meta"].get("capture"))
            if c in catalog["by_id"]]
    cells["HDMI capture"] = (" or ".join(
        "[%s](%s)" % (c["meta"]["title"], c["url"]) for c in caps), None)

    sd = specs.get("microSD", "")
    cells["microSD"] = (sd, int(bool(sd)))
    # fps at 1080p; a figure with no resolution next to it is 1080p too
    meas = specs.get("Measured", "")
    best = 0
    for part in meas.split(";"):
        if "fps" in part and ("1080p" in part or "720p" not in part):
            best = max([best] + [int(n) for n in re.findall(r"(\d+) fps", part)])
    cells["Measured"] = (meas, best)
    return cells


def compare_page(shell, catalog, capture=False):
    """Every ESP32-P4 board, or every capture board, side by side. The table
    holds all of them, so it reads without JavaScript; the script shows only
    the ones picked."""
    if capture:
        devices = catalog["capture"]
        cells = {d["id"]: capture_cells(d, catalog) for d in devices}
        keys = list(COMPARE_CAPTURE_ROWS)
    else:
        devices = catalog["tested"] + catalog["untested"]
        cells = {d["id"]: compare_cells(d, catalog) for d in devices}
        keys = list(COMPARE_ROWS)
    for d in devices:
        for k in cells[d["id"]]:
            if k not in keys and k != "Size":  # drawn under the photo instead
                keys.append(k)

    def cell(d, key):
        text, score = cells[d["id"]].get(key, ("", None))
        if key in ("Status", "Fit for a KVM"):
            body = text
        else:
            body = inline(text, d["path"]) if text else '<span class="cmp-none">-</span>'
        if score == "warn":  # a drawback, marked whatever else is shown
            return '<td class="cmp-col cmp-warn" data-id="%s">%s</td>' % (html.escape(d["id"]), body)
        return '<td class="cmp-col" data-id="%s"%s>%s</td>' % (
            html.escape(d["id"]), "" if score is None else ' data-score="%d"' % score, body)

    used = [k for k in keys if any(cells[d["id"]].get(k, ("",))[0] for d in devices)]
    def head_size(d):
        """The board's outline to scale and its size, under the photo. The
        box is as tall as the tallest outline, so the names stay level."""
        text = cells[d["id"]].get("Size", ("", None))[0]
        return '<span class="cmp-head-size" style="height:%dpx">%s<small>%s</small></span>' % (
            size_box_h, size_drawing(text) if text else "",
            html.escape(size_label(text)) if text else "&nbsp;")  # the notes stay on the board's page

    size_box_h = max([size_px(cells[d["id"]].get("Size", ("",))[0])[1] for d in devices] + [0]) + 22
    head = "".join(
        '<th class="cmp-col" data-id="{id}" scope="col"><div class="cmp-head">'
        '<a href="{url}" tabindex="-1" aria-hidden="true">'
        '<img src="{photo}" width="{w}" height="{h}" loading="lazy" alt="" /></a>'
        '{size}<a href="{url}"><span>{title}</span></a></div></th>'.format(
            id=html.escape(d["id"]), url=d["url"], photo=d["photo"], w=d["photo_w"],
            h=d["photo_h"], size=head_size(d), title=html.escape(d["meta"]["title"]))
        for d in devices)
    rows = "\n".join(
        '<tr><th scope="row">%s</th>%s</tr>' % (html.escape(k), "".join(cell(d, k) for d in devices))
        for k in used)
    picks = "".join(
        '<button type="button" class="cat-filter" data-id="%s" aria-pressed="false">%s</button>'
        % (html.escape(d["id"]), html.escape(d["meta"]["title"])) for d in devices)
    # a first view that fits: three tested boards, or every capture board
    tested = ",".join(d["id"] for d in (devices if capture else catalog["tested"][:3]))
    store = "espkvm-compare-capture" if capture else "espkvm-compare"
    if capture:
        h1, url = "Compare capture boards", SITE + "/boards/compare/capture/"
        lead = ("The HDMI capture boards ESP-KVM reads, side by side: the bridge chip, "
                "the connector, whether a monitor can stay on the target, and which "
                "ESP32-P4 boards each one fits. Pick the ones you are choosing between. "
                "\"Untested\" means nobody has run ESP-KVM with it yet.")
        other = '<a href="/boards/compare/">Compare the ESP32-P4 boards &rarr;</a> &middot; <a href="/boards/all/">Every ESP32-P4 board, supported or not &rarr;</a>'
    else:
        h1, url = "Compare boards", SITE + "/boards/compare/"
        lead = ("The ESP32-P4 boards ESP-KVM runs on, side by side. Pick the ones you are "
                "choosing between; the address of this page keeps the choice, so it can "
                "be sent to someone. \"Untested\" means built from the vendor's schematic "
                "and not yet run by anyone. Green marks the best of the boards shown. "
                "The first row is the board's rating for a KVM, out of five.")
        other = '<a href="/boards/compare/capture/">Compare the capture boards &rarr;</a> &middot; <a href="/boards/all/">Every ESP32-P4 board, supported or not &rarr;</a>'

    content = """
    <article class="board-page">
      <p class="post-back"><a href="/boards/">&larr; All boards</a></p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <p class="cat-note">{other}</p>
      <div class="cat-filters" id="cmp-picks" hidden>{picks}</div>
      <label class="cmp-diff" id="cmp-diff-wrap" hidden><input type="checkbox" id="cmp-diff" /> Only the rows that differ</label>
      {fit_tune}
      <div class="table-scroll">
        <table class="cmp-table" id="cmp-table">
          <thead><tr><th scope="col"></th>{head}</tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </article>
    <script>
      (function () {{
        var picks = document.getElementById("cmp-picks"),
          table = document.getElementById("cmp-table");
        if (!picks || !table) return;
        var q = new URLSearchParams(location.search).get("b"),
          kept = null;
        try {{ kept = (JSON.parse(localStorage.getItem("{store}")) || []).join(","); }} catch (e) {{}}
        var chosen = (q || kept || "{tested}").split(",").filter(Boolean);
        var diff = document.getElementById("cmp-diff");
        function show() {{
          picks.querySelectorAll("button").forEach(function (b) {{
            b.setAttribute("aria-pressed", String(chosen.indexOf(b.dataset.id) >= 0));
          }});
          table.querySelectorAll(".cmp-col").forEach(function (c) {{
            c.hidden = chosen.indexOf(c.dataset.id) < 0;
          }});
          table.querySelectorAll("tbody tr").forEach(function (r) {{
            var seen = {{}}, n = 0;
            r.querySelectorAll("td:not([hidden])").forEach(function (c) {{
              var t = c.textContent.trim();
              if (!seen[t]) {{ seen[t] = 1; n++; }}
            }});
            r.hidden = diff.checked && n < 2;
            var cells = r.querySelectorAll("td[data-score]:not([hidden])"),
              hi = -1, lo = Infinity;
            cells.forEach(function (c) {{
              var v = +c.dataset.score;
              hi = Math.max(hi, v); lo = Math.min(lo, v);
            }});
            r.querySelectorAll("td[data-score]").forEach(function (c) {{
              c.classList.toggle("cmp-best", !c.hidden && hi > lo && +c.dataset.score === hi);
            }});
          }});
        }}
        picks.hidden = false;
        document.getElementById("cmp-diff-wrap").hidden = false;
        diff.addEventListener("change", show);
        document.addEventListener("fit-change", show);
        picks.addEventListener("click", function (e) {{
          var b = e.target.closest("button");
          if (!b) return;
          var i = chosen.indexOf(b.dataset.id);
          if (i >= 0) chosen.splice(i, 1);
          else chosen.push(b.dataset.id);
          history.replaceState(null, "", chosen.length ? "?b=" + chosen.join(",") : location.pathname);
          try {{ localStorage.setItem("{store}", JSON.stringify(chosen)); }} catch (e) {{}}
          show();
        }});
        show();
      }})();
{fit_tune_js}
    </script>
""".format(picks=picks, head=head, rows=rows, tested=tested, store=store,
           fit_tune="" if capture else fit_tune_html(
               "Untick what does not matter to you; the rating row follows, and this browser "
               "remembers it, here and on the board list."),
           fit_tune_js="" if capture else fit_tune_js("""function (els) {
          els.forEach(function (el) { el.closest("td").dataset.score = el.dataset.halves; });
          document.dispatchEvent(new Event("fit-change"));
        }"""),
           h1=h1, lead=html.escape(lead).replace("&amp;rarr;", "&rarr;"), other=other)

    if capture:
        meta = {"title": "Compare HDMI capture boards for ESP-KVM, an open-source IP-KVM",
                "og_title": "Compare ESP-KVM capture boards",
                "description": "The HDMI to CSI capture boards ESP-KVM works with side by "
                               "side: TC358743 or LT6911D, connector, HDMI pass-through, "
                               "CEC, audio and the ESP32-P4 boards each one fits."}
    else:
        meta = {"title": "Compare ESP32-P4 boards for ESP-KVM, an open-source IP-KVM",
                "og_title": "Compare ESP-KVM boards",
                "description": "The ESP32-P4 boards ESP-KVM runs on side by side, with their rating "
                               "for an IP-KVM: chip revision, memory, network, HDMI capture, USB to the target, microSD and "
                               "measured frame rates."}
    meta.update({"canonical": url, "og_type": "website"})
    return render_page(shell, meta, content, json_ld(breadcrumbs(
        ("ESP-KVM", SITE + "/"), ("Boards", SITE + "/boards/"), ("Compare capture boards" if capture else "Compare", url))))


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
    elif m.get("chip"):
        out.append(("chip", m["chip"]))
    if m.get("family"):
        out.append(("family-" + family_slug(m["family"]), m["family"]))
    return out


# How well a board suits a KVM, read off its specs: (points, what it means).
# Ten points in all, shown as five screens with halves, rounded to the nearest half.
FIT = [(3, "tested on hardware"),
       (1.5, "rev 3.x chip (faster H.264)"),
       (1.5, "Ethernet"),
       (0.5, "Wi-Fi"),
       (1, "PoE"),
       (0.5, "microSD"),
       (1, "plain USB cable to the target"),
       (0.5, "capture ribbon fits as is"),
       (0.5, "small board")]


# The same criteria, short, for the buttons that leave one out of the rating.
FIT_SHORT = ["Tested", "rev 3.x", "Ethernet", "Wi-Fi", "PoE", "microSD", "Plain USB cable",
             "Ribbon fits", "Small board"]


def board_area(size):
    """Square centimetres from a "78 x 21 mm" spec, or None."""
    m = re.match(r"\s*([\d.]+)\s*x\s*([\d.]+)", size)
    return float(m.group(1)) * float(m.group(2)) / 100 if m else None


def has_rev3(item):
    """A rev 3.x chip someone has seen on this board. "rev3: image only" in the
    front matter marks a board with a rev 3.x image ready and no such chip
    seen yet."""
    return "rev 3" in dict(item["specs"]).get("Chip", "") and item["meta"].get("rev3") != "image only"


def sold_both(item):
    """Sold with either chip revision, so a buyer cannot choose."""
    return has_rev3(item) and "rev 1" in dict(item["specs"]).get("Chip", "")


def fit(item):
    """(halves of a screen out of 10, [(label, share of its points)]) for a device board."""
    m = item["meta"]
    specs = dict(item["specs"])
    net = specs.get("Network", "")
    usb = specs.get("To the target", "")
    sd = specs.get("microSD", "")
    area = board_area(specs.get("Size", ""))
    got = [m.get("status") == "tested",
           has_rev3(item),
           "Ethernet" in net,
           "Wi-Fi" in net,
           "PoE" in net,
           sd.startswith("yes") and "not confirmed" not in sd,
           bool(usb) and not re.search(r"wire cut|jumper|header|MX1\.25", usb),
           "22-pin" not in specs.get("Capture connector", ""),
           0 if area is None else 1 if area <= 20 else 0.5 if area <= 40 else 0]
    labels = [label for _, label in FIT]
    labels[-1] = ("board size not known" if area is None else "%s board (%d cm\u00b2)" % (
        "small" if area <= 20 else "medium" if area <= 40 else "large", round(area)))
    points = sum(p * float(g) for (p, _), g in zip(FIT, got))
    item["fit_points"] = points
    return int(points + 0.5 + 1e-9), [(l, float(g)) for l, g in zip(labels, got)]


def logo_pixels():
    """The pixel letters of the site's logo (assets/icon.svg) as two paths,
    one unit a pixel: ESP (rows 0-4) and KVM (rows 6-10), 17 wide."""
    with open(os.path.join(ROOT, "assets", "icon.svg"), encoding="utf-8") as fh:
        svg = fh.read()
    cells = sorted({((int(x) - 6) // 3, (int(y) - 15) // 3) for x, y in
                    re.findall(r'<rect x="(\d+)" y="(\d+)" width="3" height="3"', svg)})
    path = lambda rows: "".join("M%d %dh1v1h-1z" % c for c in cells if c[1] in rows)
    return path(range(0, 6)), path(range(6, 11))


LOGO_ESP, LOGO_KVM = logo_pixels()


def fit_icon(state):
    """One small screen showing the logo: blue letters for a point (state 2),
    grey for none (0); half a point (1) lights ESP and leaves KVM grey."""
    esp, kvm = ("on", "on") if state == 2 else ("on", "off") if state == 1 else ("off", "off")
    frame = "f-on" if state else "f-off"
    return ('<svg class="fit-i" viewBox="0 0 23 20" width="27" height="23" aria-hidden="true">'
            '<rect x="0.6" y="0.6" width="21.8" height="15.8" rx="2" class="scr %s"/>'
            '<g transform="translate(3 3)"><path d="%s" class="%s"/><path d="%s" class="%s"/></g>'
            '<path d="M9 17h5v1.2h-5zM7 18.2h9v1.6h-9z" class="%s"/></svg>'
            % (frame, LOGO_ESP, esp, LOGO_KVM, kvm, frame))


def fit_icons(halves):
    """Five screens for a score in halves."""
    return "".join(fit_icon(min(2, max(0, halves - 2 * i))) for i in range(5))


def fit_text(halves):
    return "%s of 5" % ("%d" % (halves // 2) if halves % 2 == 0 else "%.1f" % (halves / 2))


class RawHTML(str):
    """A spec cell that is already HTML, not prose to escape."""


def fit_breakdown(item):
    """The score and every point behind it, for a board's own page."""
    halves, parts = fit(item)
    def row(p, label, g):
        state = "has" if g == 1 else "part" if g else "lacks"
        mark = {"has": "&#10003;", "part": "&#9680;", "lacks": "&#10007;"}[state]
        pts = ("+%g" % (p * g)) if g == 1 else ("+%g of %g" % (p * g, p)) if g else "0 of %g" % p
        return ('<li class="%s"><span class="fit-mark">%s</span>%s<span class="fit-pts">%s</span></li>'
                % (state, mark, html.escape(label), pts))
    rows = "".join(row(p, label, g) for (p, _), (label, g) in zip(FIT, parts))
    warn = ""
    if sold_both(item):
        warn = ('<p class="fit-warn"><strong>Rated for a unit with the rev 3.x chip.</strong> '
                "This board is also sold with rev 1.x, and the product code does not say "
                "which one arrives. With rev 1.x it scores %s. "
                '<a href="/tools/#board-check">Read the chip in the browser</a>.</p>'
                % fit_text(int(item["fit_points"] - FIT[1][0] + 0.5 + 1e-9)))
    return ('<span class="cat-fit">%s</span> <strong>%s</strong> <span class="fit-sum">%g of 10 points</span>'
            '<ul class="fit-list">%s</ul>%s' % (fit_icons(halves), fit_text(halves), item["fit_points"], rows, warn))


def fit_title(item):
    """The same, as plain lines for a card's tooltip."""
    halves, parts = fit(item)
    note = ("\nRated for a rev 3.x unit; with rev 1.x it scores %s"
            % fit_text(int(item["fit_points"] - FIT[1][0] + 0.5 + 1e-9))
            if sold_both(item) else "")
    return "Fit for a KVM: %s%s\n%s" % (fit_text(halves), note, "\n".join(
        ("\u2713 " if g == 1 else "\u25d0 " if g else "\u2717 ") + label for label, g in parts))


def fit_tune_html(note):
    """The rating's criteria as ticks, folded away; a script fills it in."""
    picks = "".join('<li><label><input type="checkbox" data-i="%d" data-name="%s" checked /> %s'
                    '<span class="fit-pts">%g</span></label></li>'
                    % (i, html.escape(n), html.escape(n), FIT[i][0]) for i, n in enumerate(FIT_SHORT))
    return ('<details class="fit-tune" id="fit-picks" hidden>\n'
            '        <summary>What counts in the rating <span id="fit-off"></span></summary>\n'
            '        <p>%s</p>\n        <ul>%s</ul>\n      </details>' % (note, picks))


def fit_tune_js(after):
    """The rating with only what matters to the reader: every .cat-fit with a
    data-fit list is scored again without the unticked criteria, then
    after(elements) runs. The choice is kept in this browser, for both pages."""
    return """      (function () {
        var bar = document.getElementById("fit-picks");
        if (!bar) return;
        var W = %s, ICONS = %s, KEY = "espkvm-fit-off", off = [];
        try { off = JSON.parse(localStorage.getItem(KEY)) || []; } catch (e) {}
        var els = Array.prototype.slice.call(document.querySelectorAll(".cat-fit[data-fit]"));
        function apply() {
          var max = 0, names = [];
          W.forEach(function (w, i) { if (off.indexOf(i) < 0) max += w; });
          bar.querySelectorAll("input").forEach(function (b) {
            b.checked = off.indexOf(+b.dataset.i) < 0;
            if (!b.checked) names.push(b.dataset.name);
          });
          document.getElementById("fit-off").textContent = names.length ? "(without " + names.join(", ") + ")" : "";
          els.forEach(function (el) {
            var got = 0;
            el.dataset.fit.split(",").forEach(function (v, i) { if (off.indexOf(i) < 0) got += +v; });
            var h = max ? Math.floor(got / max * 10 + 0.5 + 1e-9) : 0, out = "";
            for (var i = 0; i < 5; i++) out += ICONS[Math.min(2, Math.max(0, h - 2 * i))];
            el.innerHTML = out;
            el.setAttribute("aria-label", "Fit for a KVM: " + h / 2 + " of 5");
            var t = el.nextElementSibling;
            if (t && t.classList.contains("fit-t")) t.textContent = h / 2 + " of 5";
            el.dataset.score = max ? got / max : 0;
            el.dataset.halves = h;
          });
          (%s)(els);
        }
        bar.hidden = false;
        bar.addEventListener("change", function (e) {
          var i = +e.target.dataset.i, k = off.indexOf(i);
          if (k >= 0) off.splice(k, 1); else off.push(i);
          try { localStorage.setItem(KEY, JSON.stringify(off)); } catch (e) {}
          apply();
        });
        if (off.length) apply();
      })();""" % (json.dumps([p for p, _ in FIT]), json.dumps([fit_icon(st) for st in range(3)]), after)


def by_fit(devices):
    """Best suited first; the catalog's own order among equals."""
    for d in devices:
        fit(d)
    return sorted(devices, key=lambda i: (-i["fit_points"], i["order"], i["meta"]["title"]))


def split_title(item):
    """"Waveshare ESP32-P4-NANO" -> ("Waveshare", "ESP32-P4-NANO"); a case is
    shown under its author."""
    m = item["meta"]
    if item["section"] == "cases":
        return m.get("author", ""), m["title"]
    if m.get("tile_model"):
        return m.get("tile_maker", ""), m["tile_model"]
    maker, _, model = m["title"].partition(" ")
    return (maker, model) if model else ("", m["title"])


def item_category(item):
    """The GA4 item category: board, capture, module or case."""
    if item["section"] == "boards":
        return "board" if item["meta"].get("kind") == "device" else "capture"
    return "module" if item["section"] == "modules" else "case"


def tile(item):
    m = item["meta"]
    maker, model = split_title(item)
    feats = features(item)
    untested = m.get("status") == "untested"
    planned = m.get("status") == "planned"
    status = ""
    if planned:
        status = '<span class="cat-status planned">In progress</span>'
    elif m.get("kind") == "device" or item["section"] == "modules":
        status = ('<span class="cat-status untested">Untested</span>' if untested
                  else '<span class="cat-status">Tested</span>')
    chips = "".join('<span class="cat-chip">%s</span>' % html.escape(label)
                    for _, label in feats)
    keys = " ".join([k for k, _ in feats] + ([] if untested or planned else ["tested"]))
    cover = " cat-photo-cover" if m.get("photo_style") == "photo" else ""
    rating = ""
    if m.get("kind") == "device" and item["section"] == "boards" and not planned:
        halves, parts = fit(item)
        earned = ",".join("%g" % (p * g) for (p, _), (_, g) in zip(FIT, parts))
        rating = ('\n              <span class="cat-fit" data-fit="{e}" title="{tip}" aria-label="Fit for a KVM: {t}">{i}</span>'
                  .format(e=earned, tip=html.escape(fit_title(item)), t=fit_text(halves), i=fit_icons(halves)))
    return """          <a class="cat-card" href="{url}" data-f="{keys}" data-item-id="{iid}" data-item-name="{iname}" data-item-category="{icat}">
            <span class="cat-photo{fit}"><img src="{photo}" width="{w}" height="{h}" loading="lazy" alt="" /></span>
            <span class="cat-body">
              <span class="cat-maker">{maker}{status}</span>
              <span class="cat-model">{model}</span>{rating}
              <span class="cat-chips">{chips}</span>
            </span>
          </a>""".format(
        url=item["url"], keys=keys, fit=cover, photo=item["photo"], rating=rating,
        iid=html.escape(item["id"]), iname=html.escape(html.unescape(m["title"])), icat=item_category(item),
        w=item["photo_w"], h=item["photo_h"], maker=html.escape(maker),
        status=status, model=html.escape(model), chips=chips)


def tiles(items):
    return "\n".join(tile(i) for i in items)


EVERY_DATA = os.path.join(ROOT, "_data", "p4-boards.json")
MARKS = {"y": ('<span class="mk mk-y" title="yes">&#10003;</span>'),
         "n": ('<span class="mk mk-n" title="no">&#10007;</span>'),
         "?": ('<span class="mk mk-q" title="not known">?</span>')}
VERDICTS = [("supported", "Supported"), ("candidate", "Candidate"), ("maybe", "Maybe"),
            ("no", "No"), ("terminal", "As a terminal")]


def every_data():
    import json
    with open(EVERY_DATA, encoding="utf-8") as fh:
        return json.load(fh)


def try_url(name):
    body = "Board: %s\nFirmware version: \nCapture board: \nWhat works:\n\nWhat does not:\n" % name
    return ("https://github.com/espkvm/espkvm/discussions/new?category=general&title=%s&body=%s"
            % (quote("Tried it: " + name), quote(body)))


def source_note(e):
    bits = []
    if e.get("src"):
        bits.append('<a href="%s" rel="noopener">source</a>' % html.escape(e["src"]))
    if e.get("checked"):
        bits.append("checked " + html.escape(e["checked"]))
    return (' <span class="tnote">(%s)</span>' % ", ".join(bits)) if bits else ""


def every_rows(catalog):
    """The KVM table: catalog boards first (all four marks by definition),
    then the hand-checked ones from _data/p4-boards.json."""
    rows = []
    for d in catalog["tested"] + catalog["untested"]:
        specs = dict(d["specs"])
        chip = specs.get("Chip", "")
        revs = ", ".join(x for x, k in (("1.x", "rev 1"), ("3.x", "rev 3")) if k in chip) or "?"
        tested = d["meta"]["status"] == "tested"
        status = '<span class="st st-ok">Supported</span>' + (
            "" if tested else ' <span class="tnote">not run on one yet</span>')
        conn = specs.get("Capture connector", "")
        ribbon = ("15-pin, Pi order" if "15-pin" in conn else "22-pin, Pi 5 kind" if "22-pin" in conn
                  else "24-pin, M5Stack add-on only" if "24-pin" in conn
                  else "works with the C790" if "c790" in id_list(d["meta"].get("capture")) else conn or "?")
        rows.append(("supported", d["id"], '<a href="%s">%s</a>' % (d["url"], html.escape(d["meta"]["title"])),
                     status, ["y"] * 4, revs, html.escape(specs.get("Network", "")), ribbon))
    for e in every_data()["kvm"]:
        name = html.escape(e["name"])
        name = '<a href="%s">%s</a>' % (e["url"], name) if e.get("url") else name
        v = e["verdict"]
        if v == "terminal":
            status = '<a class="st st-alt" href="#terminal">As a terminal</a>'
        else:
            status = '<span class="st %s">%s</span>' % (
                {"candidate": "st-new", "maybe": "st-new", "no": "st-no"}[v], dict(VERDICTS)[v])
        note = html.escape(e["note"]) + source_note(e)
        if v == "candidate":
            note += (' <a class="every-try" href="%s" rel="noopener" target="_blank" data-try>'
                     'Have one? Post your result &rarr;</a>' % html.escape(try_url(e["name"])))
        rows.append((v, e["id"], name, status, [e["psram"], e["camera"], e["usb"], e["network"]],
                     html.escape(e.get("chip", "?")), note, e.get("ribbon", "")))
    return rows


def every_kvm_table(catalog):
    rows = every_rows(catalog)
    def cells(marks, ribbon):
        out = []
        for i, m in enumerate(marks):
            cls = {"?": "q"}.get(m, m)
            # the camera column says what the connector is, not just yes or no
            body = ('<span class="rib">%s</span>' % html.escape(ribbon)) if i == 1 and ribbon else MARKS[m]
            out.append('<td class="c-%s">%s</td>' % (cls, body))
        return "".join(out)
    body = "\n".join(
        '        <tr id="b-%s" data-v="%s"><td>%s</td><td>%s</td>%s<td>%s</td><td>%s</td></tr>'
        % (rid, v, name, status, cells(marks, ribbon), chip, note)
        for v, rid, name, status, marks, chip, note, ribbon in rows)
    return body


def every_filters(catalog):
    rows = every_rows(catalog)
    counts = {k: sum(1 for r in rows if r[0] == k) for k, _ in VERDICTS}
    btns = ['<button type="button" class="cat-filter" data-f="" aria-pressed="true">All <span>%d</span></button>' % len(rows)]
    btns += ['<button type="button" class="cat-filter" data-f="%s" aria-pressed="false">%s <span>%d</span></button>'
             % (k, label, counts[k]) for k, label in VERDICTS if counts[k]]
    return '<div class="cat-filters" id="every-filters" hidden>%s</div>' % "".join(btns)


def every_terminal_table():
    out = []
    for e in every_data()["terminal"]:
        name = html.escape(e["name"])
        name = '<a href="%s">%s</a>' % (e["url"], name) if e.get("url") else name
        status = {"supported": '<span class="st st-ok">Supported</span>',
                  "candidate": '<span class="st st-new">Candidate</span>',
                  "not-ported": '<span class="st st-no">Not ported</span>'}[e["status"]]
        note = html.escape(e.get("note", "")) + source_note(e)
        bat = e["battery"]
        out.append('        <tr id="%s"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class="c-%s">%s</td><td>%s</td></tr>'
                   % (e["id"], name, status, html.escape(e["screen"]), html.escape(e["network"]),
                      {"?": "q"}.get(bat, bat), MARKS[bat], note))
    return "\n".join(out)


def fill_catalog(body, catalog):
    """Swap the <!-- catalog:<group> --> markers a page leaves for tiles."""
    def swap(match):
        group = match.group(1)
        devices = by_fit(catalog["tested"] + catalog["untested"])
        if group == "teaser":  # the start of the catalog, fading out on the home page
            return tiles(devices[:8])
        if group == "count":
            return str(len(devices))
        if group == "all_kvm":  # /boards/all/: every P4 board, catalog + _data
            return every_kvm_table(catalog)
        if group == "all_filters":
            return every_filters(catalog)
        if group == "all_terminal":
            return every_terminal_table()
        if group not in ("tested", "untested", "capture", "cases", "displays", "clocks", "serial", "control", "terminal"):
            sys.exit("unknown catalog group: %s" % group)
        return tiles(catalog[group])
    body = re.sub(r"<!-- catalog:(\w+) -->", swap, body)
    # A module the page imports carries a hash of its content, so a browser that
    # cached the old one takes the new one after a change.
    import hashlib
    for js in ("board-check.js",):
        with open(os.path.join(ROOT, "assets", "js", js), "rb") as fh:
            tag = hashlib.sha256(fh.read()).hexdigest()[:10]
        body = body.replace('"/assets/js/%s"' % js, '"/assets/js/%s?v=%s"' % (js, tag))
    # The flasher's board photos: flasher id -> the photo in _boards/.
    import json
    images = {b["meta"]["flasher"]: b["photo"] for b in catalog["all"]
              if b["meta"].get("flasher")}
    body = body.replace("/* catalog:images */ {}", json.dumps(images, sort_keys=True))
    # What a board's chip and memory are, for the "check my board" hints on the
    # flasher and the tools page: flasher id -> flash and PSRAM in MB.
    memory = {}
    for b in catalog["all"]:
        fid = b["meta"].get("flasher")
        mem = dict(b["specs"]).get("Memory", "")
        if not fid:
            continue
        fl = re.search(r"(\d+)\s*MB flash", mem)
        ps = re.search(r"(\d+)\s*MB PSRAM", mem)
        chip = dict(b["specs"]).get("Chip", "")
        memory[fid] = {"label": b["meta"].get("title", fid), "url": b["url"], "photo": b["photo"],
                       "rev1": "rev 1" in chip, "rev3": "rev 3" in chip,
                       "tested": b["meta"].get("status") == "tested",
                       "flash": int(fl.group(1)) if fl else None,
                       "psram": int(ps.group(1)) if ps else None}
    return body.replace("/* catalog:memory */ {}", json.dumps(memory, sort_keys=True))


def spec_table(item):
    rows = list(item["specs"])
    m = item["meta"]
    if m.get("status") == "planned":
        rows.insert(0, ("Status", "In progress: no ESP-KVM image for it yet"))
    elif m.get("kind") == "device":
        rows.insert(0, ("Status", "Run on hardware" if m["status"] == "tested"
                        else "Built from the schematic, not run on one yet"))
        rows.insert(1, ("Fit for a KVM", RawHTML(fit_breakdown(item))))
    elif item["section"] == "modules":
        rows.insert(0, ("Status", "Run on hardware" if m["status"] == "tested"
                        else "Written from the datasheet, not run on one yet"))
    fam = m.get("family")
    if fam:
        rows.insert(1 if rows and rows[0][0] == "Status" else 0,
                    ("Family", "[All %s parts](/boards/family/%s/)" % (fam, family_slug(fam))))
    if not rows:
        return ""
    return ('<div class="table-scroll"><table class="board-specs"><tbody>\n%s\n'
            "</tbody></table></div>" % "\n".join(
                "<tr><th>%s</th><td>%s</td></tr>" % (html.escape(k), v if isinstance(v, RawHTML)
                                                    else inline(v, item["path"]))
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
            "The product code does not tell. Or plug the board in and "
            '<a href="/tools/#board-check">read it in the browser</a>: it shows the '
            "revision, the flash and the PSRAM.</p>")


def try_note(item):
    """For an untested board or module: ask whoever has one to say how it went,
    with a post in Discussions already started."""
    m = item["meta"]
    if m.get("status") != "untested" or item["section"] == "cases":
        return ""
    name = html.unescape(m["title"])
    body = "Part: %s\nFirmware version: \n%s\nWhat works:\n\nWhat does not:\n" % (
        name, "Capture board: \n" if m.get("kind") == "device" else "")
    url = ("https://github.com/espkvm/espkvm/discussions/new?category=general&title=%s&body=%s"
           % (quote("Tried it: " + name), quote(body)))
    return ('<div class="board-try"><strong>Have one?</strong> Nobody has run ESP-KVM on this '
            "yet. If you try it, tell me how it went, whether it worked or not: "
            "one report moves it to tested or gets the bug fixed. "
            '<a href="%s" rel="noopener" target="_blank" data-try>Post your result &rarr;</a></div>'
            % html.escape(url))


def item_page(shell, item, catalog):
    m = item["meta"]
    kind = m.get("kind")
    actions = []
    if m.get("flasher"):
        actions.append('<a class="btn btn-primary" href="/flash/?board=%s" data-install>Install from the browser</a>'
                       % quote(m["flasher"]))
    for label, url in item["links"]:
        actions.append('<a class="btn" href="%s" rel="noopener">%s</a>'
                       % (html.escape(url), html.escape(label)))
    planned = m.get("status") == "planned"
    if kind == "device" and not planned:
        # This board next to the first two tested others.
        others = [b["id"] for b in catalog["tested"] if b["id"] != item["id"]][:2]
        actions.append('<a class="btn" href="/boards/compare/?b=%s">Compare</a>'
                       % ",".join([item["id"]] + others))
    elif kind == "capture":
        actions.append('<a class="btn" href="/boards/compare/capture/">Compare</a>')

    related = []
    if kind == "device":
        caps = [catalog["by_id"][c] for c in id_list(m.get("capture"))]
        if caps:
            related.append(("Capture board" if len(caps) == 1 else "Capture boards", caps))
        cases = [c for c in catalog["cases"] if item["id"] in id_list(c["meta"].get("boards"))]
        if cases:
            related.append(("Cases for it", cases))
        mods = [x for x in catalog["displays"] + catalog["clocks"] + catalog["serial"] + catalog["control"]
                if item["id"] in id_list(x["meta"].get("boards"))]
        if mods:
            related.append(("Modules that fit it", mods))
    elif kind == "capture":
        users = [b for b in catalog["tested"] + catalog["untested"]
                 if item["id"] in id_list(b["meta"].get("capture"))]
        related.append(("Boards it works with", users))
    elif item["section"] == "modules":
        fits = [catalog["by_id"][b] for b in id_list(m.get("boards"))]
        if fits:
            related.append(("Fits these boards", fits))
        if kind == "terminal":
            pair = [x for x in catalog["terminal"] if x is not item]
            if pair:
                related.append(("Goes with it", pair))
    else:
        fits = [catalog["by_id"][b] for b in id_list(m.get("boards"))]
        related.append(("Fits", fits))

    extra = "".join(
        '\n      <h2 class="cat-head">%s</h2>\n      <div class="cat-grid">\n%s\n      </div>'
        % (html.escape(title), tiles(items)) for title, items in related)

    if item["section"] == "cases":
        back = '<a href="/boards/#cases">&larr; All cases</a>'
    elif item["section"] == "modules":
        back = '<a href="/boards/#%s">&larr; All %s</a>' % (
            MODULE_KINDS[kind][1], MODULE_KINDS[kind][0].lower())
    else:
        back = '<a href="/boards/">&larr; All boards</a>'

    untested = " untested" if m.get("status") in ("untested", "planned") else ""
    role = m.get("role") or ("A case by " + m["author"] if m.get("author") else "")
    credit = ('<p class="board-credit">%s</p>' % html.escape(m["photo_credit"])
              if m.get("photo_credit") else "")
    is_photo = " is-photo" if m.get("photo_style") == "photo" else ""

    # Someone who lands here from a search for the board has never heard of the
    # project: say in two lines what it is before the specs.
    name = html.escape(m["title"])
    if planned:
        intro = ("<strong>ESP-KVM</strong> is free, open-source firmware that turns an "
                 "ESP32-P4 board into an IP-KVM: another computer's screen, keyboard and "
                 "mouse in your browser, from the BIOS up, with no Linux and no cloud. "
                 "An ESP-KVM image for the %s is in progress: the chip inside is "
                 "the same." % name)
    elif kind == "device":
        intro = ("<strong>ESP-KVM</strong> is free, open-source firmware that turns the "
                 "%s into an IP-KVM: the screen, keyboard and mouse of another computer "
                 "in your browser, from the BIOS up. Add an HDMI capture board, flash it "
                 "from the browser, and it runs with no Linux, no app and no cloud." % name)
    elif kind == "capture":
        intro = ("<strong>ESP-KVM</strong> is free, open-source firmware that turns an "
                 "ESP32-P4 board into an IP-KVM: another computer's screen, keyboard and "
                 "mouse in your browser, from the BIOS up. The %s is the part that "
                 "brings the computer's HDMI in." % name)
    elif item["section"] == "modules":
        part = {"display": "a small screen on the box that shows its address and health",
                "clock": "a battery-backed clock that keeps the time across a power cut",
                "serial": "it puts a computer's RS-232 serial port on the device's pins, "
                          "for the serial console in the browser",
                "control": "it presses the target's buttons, or gives the box a button "
                           "of its own",
                "terminal": "with the experimental ESP-KVM terminal firmware it shows "
                            "the target's screen in your hand, with no browser"}[kind]
        intro = ("<strong>ESP-KVM</strong> is free, open-source firmware that turns an "
                 "ESP32-P4 board into an IP-KVM: another computer's screen, keyboard and "
                 "mouse in your browser, from the BIOS up. The %s is an optional extra: "
                 "%s." % (name, part))
    else:
        intro = ("<strong>ESP-KVM</strong> is free, open-source firmware that turns an "
                 "ESP32-P4 board into an IP-KVM: another computer's screen, keyboard and "
                 "mouse in your browser, from the BIOS up. This is a printed case for one, "
                 "made by someone who built it.")
    intro = ('<p class="board-intro">%s <a href="/">What it does &rarr;</a> '
             '<a href="https://demo.espkvm.io/" rel="noopener">Try the demo &rarr;</a></p>'
             % intro)

    content = """
    <article class="board-page" data-item-page data-item-id="{iid}" data-item-name="{iname}" data-item-category="{icat}">
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
          {trynote}
          {credit}
        </div>
      </div>
      <div class="post-body">
{body}
      </div>{extra}
    </article>
""".format(iid=html.escape(item["id"]), iname=html.escape(html.unescape(m["title"])),
           icat=item_category(item),
           back=back, intro=intro, is_photo=is_photo, photo=item["photo"], w=item["photo_w"],
           h=item["photo_h"], alt=safe(m["title"]), untested=untested,
           role=html.escape(role), title=html.escape(m["title"]),
           summary=html.escape(m["summary"]), specs=spec_table(item),
           revnote=rev_note(item), trynote=try_note(item),
           actions=" ".join(actions), credit=credit,
           body=link_boards(render_markdown(item["body"], item["path"]),
                            set(catalog["by_id"]), skip={item["id"]}),
           extra=extra)

    if item["section"] == "modules":
        what = MODULE_KINDS[kind][2]
        section = (MODULE_KINDS[kind][0], SITE + "/boards/#" + MODULE_KINDS[kind][1])
    else:
        what = "an IP-KVM" if kind == "device" else ("capture for an IP-KVM" if kind == "capture"
                                                     else "a case for an IP-KVM")
        section = (("Cases", SITE + "/boards/#cases") if item["section"] == "cases"
                   else ("Boards", SITE + "/boards/"))
    ld = json_ld(breadcrumbs(("ESP-KVM", SITE + "/"), section,
                             (html.unescape(m["title"]), SITE + item["url"])))
    return render_page(shell, {
        "title": m.get("page_title") or "%s - %s with ESP-KVM" % (m["title"], what),
        "og_title": m["title"],
        "description": (m.get("description") or m["summary"]) + (
            " Rated %s for an IP-KVM." % fit_text(fit(item)[0])
            if kind == "device" and item["section"] == "boards" and not planned else ""),
        "canonical": SITE + item["url"],
        "image": SITE + item["photo"],
        "image_alt": m["title"],
        "og_type": "article",
    }, content, ld)


def catalog_page(shell, catalog):
    devices = by_fit(catalog["tested"] + catalog["untested"])
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
        them, the optional status displays, clocks and serial adapters, and printed cases.
        Have a board already? <a href="/tools/#board-check">Read it in the browser</a>
        to see its chip revision, flash and PSRAM, and which of these it matches.
        "Untested" means built from the vendor's schematic or the chip's
        datasheet and not yet run by anyone.
      </p>{by_maker}

      <h2 class="cat-head" id="devices">ESP32-P4 boards <span class="cat-count" id="cat-count">{n}</span></h2>
      <div class="cat-filters" id="cat-filters" hidden>{buttons}</div>
      <p class="cat-note">Sorted by how well a board suits a KVM, out of five screens. Tested on hardware counts most, then a rev 3.x chip, Ethernet, PoE, a plain USB cable to the target, Wi-Fi, microSD, a capture ribbon that fits as is and a small board (up to 20 cm² for the whole half point, up to 40 for half of it). Each board's page says what it has and what it lacks.</p>
      {fit_tune}
      <div class="cmp-cta">
        <p><strong>Choosing between a few?</strong> Put them side by side: the rating, chip, memory, Ethernet, PoE, Wi-Fi, microSD and the measured frame rate, with the best marked.</p>
        <div class="cmp-cta-btns"><a class="btn btn-primary" href="/boards/compare/">Compare boards</a> <a class="btn" href="/boards/all/">Is my board supported?</a></div>
      </div>
      <div class="cat-grid" id="cat-devices">
{devices}
          <a class="cat-card cat-card-add" href="https://github.com/espkvm/espkvm/issues/new" rel="noopener">
            <span class="cat-photo"><img src="/assets/board-add.svg" width="680" height="340" loading="lazy" alt="" /></span>
            <span class="cat-body">
              <span class="cat-maker">Yours, maybe</span>
              <span class="cat-model">Not on the list?</span>
              <span class="cat-chips"><span class="cat-chip">open an issue with its schematic</span></span>
            </span>
          </a>
      </div>
{planned}
      <h2 class="cat-head" id="capture">HDMI capture <span class="cat-count">{n_capture}</span></h2>
      <p class="cat-note"><a href="/boards/compare/capture/">Compare the capture boards &rarr;</a></p>
      <div class="cat-grid">
{capture}
      </div>

      <h2 class="cat-head" id="displays">Status displays <span class="cat-count">{n_displays}</span></h2>
      <div class="cat-grid">
{displays}
      </div>

      <h2 class="cat-head" id="clocks">Clocks <span class="cat-count">{n_clocks}</span></h2>
      <div class="cat-grid">
{clocks}
      </div>

      <h2 class="cat-head" id="serial">Serial adapters <span class="cat-count">{n_serial}</span></h2>
      <div class="cat-grid">
{serial}
      </div>

      <h2 class="cat-head" id="control">Power control and buttons <span class="cat-count">{n_control}</span></h2>
      <div class="cat-grid">
{control}
      </div>

      <h2 class="cat-head" id="terminal">Terminal (optional, experimental) <span class="cat-count">{n_terminal}</span></h2>
      <p class="cat-note">For the <a href="/terminal/">ESP-KVM terminal</a>: the target's screen on an M5Stack Tab5, no browser.</p>
      <div class="cat-grid">
{terminal}
      </div>

      <h2 class="cat-head" id="cases">Cases <span class="cat-count">{n_cases}</span></h2>
      <div class="cat-grid">
{cases}
      </div>

      <p class="cat-note">
        Not the board you have? See <a href="/boards/all/">every ESP32-P4 board I have looked at</a>, and why some cannot work, or <a href="https://github.com/espkvm/espkvm/issues/new" rel="noopener">open an issue</a>
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
          grid.querySelectorAll(".cat-card:not(.cat-card-add)").forEach(function (c) {{
            var on = f === "all" || (" " + c.dataset.f + " ").indexOf(" " + f + " ") >= 0;
            (c.parentNode.classList.contains("cat-item") ? c.parentNode : c).hidden = !on;
            if (on) shown++;
          }});
          count.textContent = shown;
        }});
      }})();
{fit_tune_js}
      // A scales button on each board adds it to the comparison; the choice
      // is kept in this browser and the compare page starts from it.
      (function () {{
        var grid = document.getElementById("cat-devices");
        if (!grid) return;
        var KEY = "espkvm-compare", chosen = [];
        try {{ chosen = JSON.parse(localStorage.getItem(KEY)) || []; }} catch (e) {{}}
        var icon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v18M7 21h10M5 7h14M12 5l-7 2M12 5l7 2M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/></svg>';
        var bar = document.createElement("div");
        bar.className = "cmp-float";
        bar.hidden = true;
        bar.innerHTML = '<a class="btn btn-primary" id="cmp-go">' + icon + '<span></span></a>' +
          '<button type="button" class="cmp-clear" aria-label="Clear the comparison">&times;</button>';
        document.body.appendChild(bar);
        function save() {{
          try {{ localStorage.setItem(KEY, JSON.stringify(chosen)); }} catch (e) {{}}
          grid.querySelectorAll(".cmp-add").forEach(function (b) {{
            var on = chosen.indexOf(b.dataset.id) >= 0;
            b.setAttribute("aria-pressed", String(on));
            b.title = on ? "Remove from the comparison" : "Add to the comparison";
          }});
          bar.hidden = !chosen.length;
          var go = bar.querySelector("#cmp-go");
          go.href = "/boards/compare/?b=" + chosen.join(",");
          go.querySelector("span").textContent = "Compare " + chosen.length +
            (chosen.length === 1 ? " board" : " boards");
        }}
        grid.querySelectorAll(".cat-card:not(.cat-card-add)").forEach(function (c) {{
          var wrap = document.createElement("div");
          wrap.className = "cat-item";
          c.parentNode.insertBefore(wrap, c);
          wrap.appendChild(c);
          var b = document.createElement("button");
          b.type = "button";
          b.className = "cmp-add";
          b.dataset.id = c.dataset.itemId;
          b.setAttribute("aria-label", "Compare " + c.dataset.itemName);
          b.innerHTML = icon;
          wrap.appendChild(b);
        }});
        grid.addEventListener("click", function (e) {{
          var b = e.target.closest(".cmp-add");
          if (!b) return;
          var i = chosen.indexOf(b.dataset.id);
          if (i >= 0) chosen.splice(i, 1);
          else chosen.push(b.dataset.id);
          save();
        }});
        bar.querySelector(".cmp-clear").addEventListener("click", function () {{
          chosen = [];
          save();
        }});
        save();
      }})();
    </script>
""".format(by_maker=(
               '\n      <p class="cat-note">By maker: %s.</p>' % ", ".join(
                   '<a href="/boards/family/%s/">%s</a>' % (slug, html.escape(name))
                   for slug, (name, _) in sorted(families(catalog).items()))
               if families(catalog) else ""),
           n=len(devices), buttons=buttons, devices=tiles(devices),
           fit_tune=fit_tune_html("Untick what does not matter to you; the screens and the order "
                                  "follow, and this browser remembers it."),
           fit_tune_js=fit_tune_js("""function (els) {
          var grid = document.getElementById("cat-devices"), add = grid.querySelector(".cat-card-add");
          els.map(function (el, n) { return [el, n]; }).sort(function (a, b) {
            return b[0].dataset.score - a[0].dataset.score || a[1] - b[1];
          }).forEach(function (p) {
            var c = p[0].closest(".cat-card");
            grid.insertBefore(c.parentNode.classList.contains("cat-item") ? c.parentNode : c, add);
          });
        }"""),
           planned=("""
      <h2 class="cat-head" id="planned">In progress <span class="cat-count">%d</span></h2>
      <p class="cat-note">Devices on the same chip that ESP-KVM does not run on yet. There is no image to flash for them.</p>
      <div class="cat-grid">
%s
      </div>
""" % (len(catalog["planned"]), tiles(catalog["planned"]))) if catalog["planned"] else "",
           n_capture=len(catalog["capture"]), capture=tiles(catalog["capture"]),
           n_displays=len(catalog["displays"]), displays=tiles(catalog["displays"]),
           n_clocks=len(catalog["clocks"]), clocks=tiles(catalog["clocks"]),
           n_serial=len(catalog["serial"]), serial=tiles(catalog["serial"]),
           n_control=len(catalog["control"]), control=tiles(catalog["control"]),
           n_terminal=len(catalog["terminal"]), terminal=tiles(catalog["terminal"]),
           n_cases=len(catalog["cases"]), cases=tiles(catalog["cases"]))

    return render_page(shell, {
        "title": "ESP32-P4 boards for an IP-KVM, rated - ESP-KVM boards and cases",
        "og_title": "ESP-KVM boards, rated",
        "description": "The ESP32-P4 boards ESP-KVM runs on, rated for an IP-KVM out of "
                       "five and sorted best first, which ones have been run on "
                       "hardware, the HDMI capture boards, status displays, clocks, "
                       "serial adapters and "
                       "printed cases for them.",
        "canonical": SITE + "/boards/",
        "og_type": "website",
    }, content, json_ld(breadcrumbs(("ESP-KVM", SITE + "/"), ("Boards", SITE + "/boards/"))))


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
    write(os.path.join(ROOT, "boards", "compare", "index.html"), compare_page(shell, catalog))
    write(os.path.join(ROOT, "boards", "compare", "capture", "index.html"),
          compare_page(shell, catalog, capture=True))
    for slug, (name, items) in families(catalog).items():
        write(os.path.join(ROOT, "boards", "family", slug, "index.html"),
              family_page(shell, slug, name, items))


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



# ---------------------------------------------------------------- search

# A release post's title leads with its version, and nobody searches for a
# version number: the tab and the search result lead with the subject instead.
VERSION_LEAD = re.compile(r"^(\d+\.\d+\.\d+(?:\s*(?:to|and|,)\s*\d+\.\d+\.\d+)*)\s+-\s+(.+)$")


def post_title_tag(title):
    m = VERSION_LEAD.match(title)
    if m:
        return "%s - ESP-KVM %s" % (m.group(2), m.group(1))
    return "%s - ESP-KVM" % title


def json_ld(*objs):
    """Structured data for search engines, one <script> per object."""
    return "".join(
        '    <script type="application/ld+json">%s</script>\n'
        % json.dumps(dict({"@context": "https://schema.org"}, **o), ensure_ascii=False)
        .replace("</", "<\\/") for o in objs)


def breadcrumbs(*crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
        for i, (name, url) in enumerate(crumbs)]}


PUBLISHER = {"@type": "Organization", "name": "ESP-KVM", "url": SITE + "/",
             "logo": {"@type": "ImageObject", "url": SITE + "/assets/icon-192.png"}}


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

        # The 404 page: not for search engines and not in the sitemap.
        if meta.get("noindex") == "yes":
            head.insert(0, '    <meta name="robots" content="noindex" />')

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
        if meta.get("noindex") != "yes":
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


def thumb_shape(src):
    """The box takes the picture's own shape, so a hero with words on it is
    never cut. A picture taller than 4:3 is a photo of a board or a logo with
    room around it: it fills a 4:3 box instead of floating in one."""
    path = os.path.join(ROOT, src.lstrip("/"))
    if not src.lower().endswith((".webp", ".png", ".jpg", ".jpeg")):
        return ""  # an SVG scales to any box
    w, h = image_size(path)
    if w * 3 >= h * 4:
        return ' style="aspect-ratio: %d / %d"' % (w, h)
    return ' style="aspect-ratio: 4 / 3" data-fill=""'


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


# Share icons: Simple Icons paths (CC0), 24x24, filled; the link is Feather's.
SHARE_ICONS = {
    "X": "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z",
    "Reddit": "M12 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0zm5.01 4.744c.688 0 1.25.561 1.25 1.249a1.25 1.25 0 0 1-2.498.056l-2.597-.547-.8 3.747c1.824.07 3.48.632 4.674 1.488.308-.309.73-.491 1.207-.491.968 0 1.754.786 1.754 1.754 0 .716-.435 1.333-1.01 1.614a3.111 3.111 0 0 1 .042.52c0 2.694-3.13 4.87-7.004 4.87-3.874 0-7.004-2.176-7.004-4.87 0-.183.015-.366.043-.534A1.748 1.748 0 0 1 4.028 12c0-.968.786-1.754 1.754-1.754.463 0 .898.196 1.207.49 1.207-.883 2.878-1.43 4.744-1.487l.885-4.182a.342.342 0 0 1 .14-.197.35.35 0 0 1 .238-.042l2.906.617a1.214 1.214 0 0 1 1.108-.701zM9.25 12C8.561 12 8 12.562 8 13.25c0 .687.561 1.248 1.25 1.248.687 0 1.248-.561 1.248-1.249 0-.688-.561-1.249-1.249-1.249zm5.5 0c-.687 0-1.248.561-1.248 1.25 0 .687.561 1.248 1.249 1.248.688 0 1.249-.561 1.249-1.249 0-.687-.562-1.249-1.25-1.249zm-5.466 3.99a.327.327 0 0 0-.231.094.33.33 0 0 0 0 .463c.842.842 2.484.913 2.961.913.477 0 2.105-.056 2.961-.913a.361.361 0 0 0 .029-.463.33.33 0 0 0-.464 0c-.547.533-1.684.73-2.512.73-.828 0-1.979-.196-2.512-.73a.326.326 0 0 0-.232-.095z",
    "Hacker News": "M0 24V0h24v24H0zM6.951 5.896l4.112 7.708v5.064h1.583v-4.972l4.148-7.799h-1.749l-2.457 4.875c-.372.745-.688 1.434-.688 1.434s-.297-.708-.651-1.434L8.831 5.896h-1.88z",
    "LinkedIn": "M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z",
    "Telegram": "M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5.71L12.6 16.3l-1.99 1.93c-.23.23-.42.42-.83.42z",
    "Bluesky": "M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 0 1-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.206-.659-.298-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8z",
}
LINK_ICON = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>'
             '<path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>')


def share_links(url, text):
    """A row of plain share links, one icon each. Each is an ordinary link to the
    network's own share form - no script from any of them loads here, so nobody
    is tracked for reading. Mastodon has no one address to send to, which is what
    Copy link is for; the footer's script shows that button and makes it work."""
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
    items = "".join(
        '<a class="btn btn-sm share-icon" href="%s" rel="noopener" target="_blank" '
        'title="Share on %s" aria-label="Share on %s">'
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
        '<path d="%s"/></svg></a>'
        % (html.escape(href), name, name, SHARE_ICONS[name]) for name, href in links)
    return ('<p class="share"><span class="share-label">Share</span>%s'
            '<button type="button" class="btn btn-sm share-icon share-copy" data-url="%s" '
            'title="Copy link" aria-label="Copy link" hidden>%s</button></p>'
            % (items, html.escape(url), LINK_ICON))


def post_page(shell, post, known=frozenset()):
    hero = ""
    if post["image"]:
        hero = ('<figure class="post-hero"><img src="%s" alt="" loading="lazy" />'
                "</figure>" % html.escape(post["image"]))
        # image_link: the hero opens that page, e.g. the table it is a picture of.
        if post["image_link"]:
            hero = hero.replace("<img", '<a href="%s" aria-label="Open the page this picture is from"><img' % html.escape(post["image_link"]), 1)
            hero = hero.replace("</figure>", "</a></figure>", 1)

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
      <section class="post-comments" aria-label="Comments">
        <h2>Comments</h2>
        <script src="https://giscus.app/client.js"
          data-repo="espkvm/espkvm" data-repo-id="R_kgDOTgkzaQ"
          data-category="Blog comments" data-category-id="DIC_kwDOTgkzac4DI71t"
          data-mapping="specific" data-term="{term}" data-strict="1" data-reactions-enabled="1"
          data-emit-metadata="0" data-input-position="bottom"
          data-theme="preferred_color_scheme" data-lang="en" data-loading="lazy"
          crossorigin="anonymous" async></script>
      </section>
    </article>
""".format(
        title=html.escape(post["title"]),
        iso=post["date"].strftime("%Y-%m-%d"),
        human=human_date(post["date"]),
        hero=hero,
        tags=tag_links(post["tags"]),
        body=link_boards(render_markdown(post["body"], post["path"]), known),
        share=share_links("%s/blog/%s/" % (SITE, post["slug"]), post["title"] + " - ESP-KVM"),
        # The discussion is titled after the post; renaming a post loses it.
        term=html.escape(html.unescape(re.sub(r"<[^>]+>", "", post["title"]))),
    )

    url = "%s/blog/%s/" % (SITE, post["slug"])
    image = SITE + post["thumb"] if post["thumb"].startswith("/") else ""
    plain_title = html.unescape(re.sub(r"<[^>]+>", "", post["title"]))
    ld = json_ld(
        {"@type": "BlogPosting", "headline": plain_title,
         "description": html.unescape(post["description"]),
         "datePublished": post["date"].strftime("%Y-%m-%d"),
         "url": url, "mainEntityOfPage": url, "image": image or OG_IMAGE,
         "author": PUBLISHER, "publisher": PUBLISHER,
         "keywords": ", ".join(post["tags"])},
        breadcrumbs(("ESP-KVM", SITE + "/"), ("Blog", SITE + "/blog/"), (plain_title, url)))
    return render_page(shell, {
        "title": post_title_tag(post["title"]),
        "og_title": post["title"],
        "description": post["description"],
        "canonical": url,
        "image": image,
        "og_type": "article",
    }, content, ld)


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
                       'aria-hidden="true"%s><img src="%s" alt="" loading="lazy" /></a>\n'
                       % (p["slug"], thumb_shape(p["thumb"]), html.escape(p["thumb"]))
                       if p["thumb"] else ""),
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
        entries += "  <url>\n    <loc>%s/boards/compare/</loc>\n    <priority>0.7</priority>\n  </url>\n" % SITE
        entries += "  <url>\n    <loc>%s/boards/compare/capture/</loc>\n    <priority>0.6</priority>\n  </url>\n" % SITE
        entries += "".join(
            "  <url>\n    <loc>%s%s</loc>\n    <priority>0.7</priority>\n  </url>\n"
            % (SITE, item["url"]) for item in catalog["all"])
        entries += "".join(
            "  <url>\n    <loc>%s/boards/family/%s/</loc>\n    <priority>0.6</priority>\n  </url>\n"
            % (SITE, slug) for slug in families(catalog))
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

# Links that leave the site open in a new tab, so the page they came from stays
# where it was. Scripts are left alone: links they build are theirs to mark.
OWN_HOSTS = ("espkvm.io", "www.espkvm.io")
EXT_LINK = re.compile(r'<a\b([^>]*?)\bhref="https?://([^/"?#:]+)[^"]*"[^>]*>')
SCRIPT = re.compile(r"(<script\b.*?</script>)", re.S)


def mark_external(html):
    def one(m):
        tag = m.group(0)
        if m.group(2).lower() in OWN_HOSTS or "target=" in tag:
            return tag
        rel = re.search(r'\brel="([^"]*)"', tag)
        if rel:
            if "noopener" not in rel.group(1).split():
                tag = tag.replace(rel.group(0), 'rel="%s noopener"' % rel.group(1))
            return tag[:-1] + ' target="_blank">'
        return tag[:-1] + ' target="_blank" rel="noopener">'
    parts = SCRIPT.split(html)
    return "".join(p if i % 2 else EXT_LINK.sub(one, p) for i, p in enumerate(parts))


def write(path, text):
    if path.endswith(".html"):
        text = mark_external(text)
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
