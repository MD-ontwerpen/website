# -*- coding: utf-8 -*-
"""
Local preview server for the site.

`python -m http.server` only accepts the port as a positional argument, so it
cannot honour an assigned PORT and always collides when 5510 is already taken.
This wrapper reads PORT from the environment and falls back to 5510, which lets
the launcher pick a free port instead of failing.

Serves the directory this file lives in, so it works from any working directory:

    python website/serve.py
    PORT=8123 python website/serve.py
"""
import functools
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 5510


class Handler(http.server.SimpleHTTPRequestHandler):
    """Static handler that asks browsers not to cache during development."""

    def end_headers(self):
        # Without this, edits to styles.css and i18n.js are served from cache
        # and changes appear not to have taken effect.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))


def main():
    port = int(os.environ.get("PORT") or DEFAULT_PORT)
    handler = functools.partial(Handler, directory=ROOT)

    # ThreadingHTTPServer, not TCPServer: a browser opens several connections in
    # parallel for CSS, JS and the thirteen service images. A single-threaded
    # server handles the HTML then blocks, and every asset after it fails.
    http.server.ThreadingHTTPServer.allow_reuse_address = True

    try:
        with http.server.ThreadingHTTPServer(("", port), handler) as httpd:
            print(f"MD-ontwerpen preview: http://localhost:{port}")
            print(f"serving {ROOT}")
            httpd.serve_forever()
    except OSError as e:
        print(f"could not bind port {port}: {e}", file=sys.stderr)
        print("set PORT to a free port, or stop whatever is using this one.", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
