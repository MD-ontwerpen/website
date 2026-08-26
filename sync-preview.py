"""Copy `version 2/` into `preview/` for publishing.

`version 2/` is git-ignored working space; `preview/` is what GitHub Pages
serves at /preview/. The two differ in exactly one way: every published page
gets a noindex tag, so the work in progress cannot compete with the live site
for ranking. Doing that by hand once per page per sync is how it gets missed.

Only files the pages actually reference are copied - not the playbook or the
decision log, and not unreferenced images.

    python sync-preview.py
"""

import os
import re
import shutil

SRC = "version 2"
DST = "preview"
PAGES = ["index.html", "diensten/index.html",
         "en/index.html", "en/services/index.html"]
ASSETS = [
    "assets/css/styles.css",
    "assets/js/nav.js",
    "assets/img/achtergrond.jpg",
    "assets/img/logo.svg",
    # Apache 2.0 requires the notice to travel with the font files.
    "assets/fonts/roboto-700-latin.woff2",
    "assets/fonts/roboto-700-latin-ext.woff2",
    "assets/fonts/LICENSE.txt",
]

NOINDEX = """
    <!-- Work in progress, published only so it can be looked at on a real URL.
         Kept out of the index deliberately: the live site at / is the one that
         should rank, and this page would otherwise compete with it. Do not add
         a Disallow for this path in robots.txt - crawlers have to be able to
         fetch the page to see this tag. -->
    <meta name="robots" content="noindex, nofollow" />"""


def copy(rel):
    src, dst = os.path.join(SRC, rel), os.path.join(DST, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(src, dst)
    return dst


def main():
    for rel in ASSETS:
        copy(rel)

    for rel in PAGES:
        path = copy(rel)
        with open(path, encoding="utf-8") as fh:
            html = fh.read()

        title = re.search(r"<title>(.*?)</title>", html, re.S)
        if title is None:
            raise SystemExit("%s: no <title> to anchor the noindex against" % rel)
        html = html.replace(
            title.group(0),
            "<title>%s \u2014 preview</title>%s" % (title.group(1), NOINDEX),
            1,
        )
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(html)

        if html.count('content="noindex, nofollow"') != 1:
            raise SystemExit("%s: noindex not applied exactly once" % rel)
        print("  %-24s noindex applied" % rel)

    print("synced %d pages, %d assets" % (len(PAGES), len(ASSETS)))


if __name__ == "__main__":
    main()
