#!/usr/bin/env python3
"""Put the site's analytics tag into a page this site did not render.

The interactive demo at /demo/ is the console's own single-file build, copied in
from the espkvm/console submodule. That build is the same code the device ships,
so it carries no tag of its own and must not: a KVM in someone's basement has no
business talking to Google. The counter belongs to the copy served from the
site, and this is where it is added - after the page is built, never in it.

The tag itself is not written here. It is read from _templates/page.html between
the analytics markers, so the demo counts in the same property as every other
page and there is only one place to change it.

    python3 tools/add-analytics.py _site/demo/index.html
"""

import re
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "_templates" / "page.html"
BLOCK = re.compile(r"<!-- analytics:start.*?<!-- analytics:end -->", re.S)


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    found = BLOCK.search(TEMPLATE.read_text())
    if not found:
        print(f"{TEMPLATE}: no analytics block between the markers", file=sys.stderr)
        return 1
    tag = found.group(0)

    page = Path(sys.argv[1])
    html = page.read_text()
    if "googletagmanager.com" in html:
        print(f"{page}: already tagged, leaving it alone")
        return 0
    if "<head>" not in html:
        print(f"{page}: no <head> to put the tag in", file=sys.stderr)
        return 1

    page.write_text(html.replace("<head>", "<head>\n" + tag + "\n", 1))
    print(f"{page}: analytics tag added")
    return 0


if __name__ == "__main__":
    sys.exit(main())
