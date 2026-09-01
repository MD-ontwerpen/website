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
def find_pages():
    """Every index.html under SRC, excluding assets. Discovered rather than
    listed: the page set grows, and a stale list silently ships fewer pages."""
    found = []
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if d not in ("assets", "__pycache__")]
        for name in files:
            if name == "index.html":
                rel = os.path.relpath(os.path.join(root, name), SRC)
                found.append(rel.replace(os.sep, "/"))
    return sorted(found)
ASSETS = [
    "assets/css/styles.css",
    "assets/js/nav.js",
    "assets/img/home.jpg",
    "assets/img/diensten.jpg",
    "assets/img/logo.svg",
    # Apache 2.0 requires the notice to travel with the font files.
    "assets/fonts/roboto-700-latin.woff2",
    "assets/fonts/roboto-700-latin-ext.woff2",
    "assets/fonts/roboto-400-latin.woff2",
    "assets/fonts/roboto-400-latin-ext.woff2",
    "assets/fonts/LICENSE.txt",
    # landing page only
    "assets/js/stage.js",
    "assets/js/vendor/three.module.min.js",
    "assets/js/vendor/GLTFLoader.js",
    # GLTFLoader imports this as ../utils/, so the path must mirror upstream
    "assets/js/utils/BufferGeometryUtils.js",
    "assets/js/vendor/LICENSE.txt",
    "assets/models/gebouw-lagen.glb",
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

    for rel in find_pages():
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

    print("synced %d pages, %d assets" % (len(find_pages()), len(ASSETS)))


if __name__ == "__main__":
    main()
