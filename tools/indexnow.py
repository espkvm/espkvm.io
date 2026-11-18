#!/usr/bin/env python3
"""Tell search engines which pages changed, by IndexNow (Bing, Yandex and others).

  indexnow.py diff SITE_DIR   hash every page in SITE_DIR/sitemap.xml, write the
                              hashes to SITE_DIR/indexnow-hashes.txt, compare them
                              with the ones the live site has, and print the URLs
                              that are new, changed or gone, one per line
  indexnow.py send FILE       send the URLs listed in FILE to api.indexnow.org

The build is deterministic, so a page whose HTML did not change is not sent.
The key is public by design: search engines fetch /<key>.txt to check that the
request came from the site's owner.
"""
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

SITE = "https://espkvm.io"
HOST = "espkvm.io"
KEY = "cd24dc9eb3b349052cef02c827968b9c"
HASHES = "indexnow-hashes.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"


def page_file(site_dir, url):
    path = url[len(SITE):].lstrip("/")
    if path == "" or path.endswith("/"):
        path += "index.html"
    return os.path.join(site_dir, path)


def read_hashes(text):
    out = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) == 2:
            out[parts[1]] = parts[0]
    return out


def diff(site_dir):
    with open(os.path.join(site_dir, "sitemap.xml"), encoding="utf-8") as f:
        urls = re.findall(r"<loc>([^<]+)</loc>", f.read())
    now = {}
    for url in urls:
        try:
            with open(page_file(site_dir, url), "rb") as f:
                now[url] = hashlib.sha256(f.read()).hexdigest()
        except FileNotFoundError:
            print("indexnow: %s is in the sitemap but not built" % url, file=sys.stderr)
    with open(os.path.join(site_dir, HASHES), "w", encoding="utf-8") as f:
        f.writelines("%s %s\n" % (h, u) for u, h in sorted(now.items()))

    try:
        with urllib.request.urlopen("%s/%s" % (SITE, HASHES), timeout=30) as r:
            old = read_hashes(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        old = {}  # the first deploy with this script: every page is new
    changed = sorted(u for u, h in now.items() if old.get(u) != h)
    gone = sorted(u for u in old if u not in now)
    for url in changed + gone:
        print(url)
    print("indexnow: %d pages, %d changed or new, %d gone"
          % (len(now), len(changed), len(gone)), file=sys.stderr)


def send(list_file):
    with open(list_file, encoding="utf-8") as f:
        urls = [u.strip() for u in f if u.strip()]
    if not urls:
        print("indexnow: nothing changed")
        return
    for i in range(0, len(urls), 10000):  # the protocol's limit per request
        body = json.dumps({
            "host": HOST,
            "key": KEY,
            "keyLocation": "%s/%s.txt" % (SITE, KEY),
            "urlList": urls[i:i + 10000],
        }).encode("utf-8")
        req = urllib.request.Request(ENDPOINT, data=body, method="POST", headers={
            "Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=30) as r:
            print("indexnow: sent %d URLs, HTTP %d" % (len(urls[i:i + 10000]), r.status))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("diff", "send"):
        sys.exit(__doc__)
    {"diff": diff, "send": send}[sys.argv[1]](sys.argv[2])
