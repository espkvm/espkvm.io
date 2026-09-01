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
blog/tags/<tag>/index.html and blog/feed.xml, and rewrites sitemap.xml. All of
those are generated and none of them are committed.
"""

import argparse
import html
import os
import re
import sys
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
        thumb = meta.get("image", "")
        if not thumb:
            first = re.search(r"^!\[([^\]]*)\]\(([^)\s]+)\)$", body, re.M)
            if first:
                thumb = first.group(2)

        slug = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name[:-3])
        try:
            date = datetime.strptime(meta["date"], "%Y-%m-%d")
        except ValueError:
            sys.exit("%s: date must be YYYY-MM-DD" % path)

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
        })

    slugs = [p["slug"] for p in posts]
    duplicate = next((s for s in slugs if slugs.count(s) > 1), None)
    if duplicate:
        sys.exit("two posts want the same URL: /blog/%s/" % duplicate)

    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


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

def build_pages(shell):
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

        body = re.sub(r"\n{3,}", "\n\n", body).strip("\n")
        write(os.path.join(ROOT, meta["output"]),
              render_page(shell, meta, body, "\n".join(head)))
        written.append(meta["output"])
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

        if stripped.startswith("|"):
            sys.exit("%s: tables are not supported - write the HTML by hand "
                     "or add them to tools/build-blog.py" % where)

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


def post_page(shell, post):
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
      </footer>
    </article>
""".format(
        title=html.escape(post["title"]),
        iso=post["date"].strftime("%Y-%m-%d"),
        human=human_date(post["date"]),
        hero=hero,
        tags=tag_links(post["tags"]),
        body=render_markdown(post["body"], post["path"]),
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


def page_urls(pages):
    """Rendered output paths as URLs: "flash/index.html" -> "/flash/"."""
    urls = []
    for out in pages or []:
        url = "/" + out[: -len("index.html")] if out.endswith("index.html") else "/" + out
        urls.append((url, "1.0" if url == "/" else "0.8"))
    return urls


def sitemap(posts, tags=None, pages=None):
    entries = "".join(
        "  <url>\n    <loc>%s%s</loc>\n    <priority>%s</priority>\n  </url>\n"
        % (SITE, path, priority)
        for path, priority in page_urls(pages)
    )
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

    pages = build_pages(shell)

    for post in posts:
        write(os.path.join(OUT_DIR, post["slug"], "index.html"),
              post_page(shell, post))

    tags = tags_index(posts)
    for tag, tagged in tags.items():
        write(os.path.join(OUT_DIR, "tags", tag, "index.html"),
              index_page(shell, tagged, tag=tag, all_tags=tags))

    write(os.path.join(OUT_DIR, "index.html"),
          index_page(shell, posts, all_tags=tags))
    write(os.path.join(OUT_DIR, "feed.xml"), feed(posts))
    write(os.path.join(ROOT, "sitemap.xml"), sitemap(posts, tags, pages))

    print("pages:")
    for output in pages:
        print("  /%s" % output)
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
