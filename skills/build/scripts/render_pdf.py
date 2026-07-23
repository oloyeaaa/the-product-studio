#!/usr/bin/env python3
"""Portable HTML renderer for The Product Studio. Stdlib only, no network.

Finds a Chromium-family browser already on the machine (Chrome, Edge,
Chromium, Brave; Edge ships with Windows) and runs it headless to turn a
self-contained HTML file into a PDF or a PNG screenshot.

Usage:
    python render_pdf.py pdf  <in.html> <out.pdf>
    python render_pdf.py shot <in.html> <out.png> [--size WxH]

Exit codes:
    0  rendered, output file verified on disk (prints "RENDERED <path>")
    1  bad arguments, or the browser ran but produced no output
    2  no browser found (prints the manual save-as-PDF path instead)

Never requires pip installs. Never touches the network.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

BROWSER_NAMES = [
    "chrome", "google-chrome", "chromium", "chromium-browser", "msedge", "brave",
]

WINDOWS_RELATIVE_PATHS = [
    r"Google\Chrome\Application\chrome.exe",
    r"Microsoft\Edge\Application\msedge.exe",
    r"BraveSoftware\Brave-Browser\Application\brave.exe",
    r"Chromium\Application\chrome.exe",
]

MAC_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
]

LINUX_PATHS = [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/usr/bin/microsoft-edge",
    "/usr/bin/brave-browser",
    "/snap/bin/chromium",
    "/opt/google/chrome/chrome",
]


def find_browser():
    env_bin = os.environ.get("BROWSER_BIN", "").strip()
    if env_bin and os.path.isfile(env_bin):
        return env_bin
    for name in BROWSER_NAMES:
        found = shutil.which(name)
        if found:
            return found
    candidates = []
    if sys.platform.startswith("win"):
        roots = [os.environ.get("PROGRAMFILES"),
                 os.environ.get("PROGRAMFILES(X86)"),
                 os.environ.get("LOCALAPPDATA")]
        for root in roots:
            if root:
                for rel in WINDOWS_RELATIVE_PATHS:
                    candidates.append(os.path.join(root, rel))
    elif sys.platform == "darwin":
        candidates = MAC_PATHS
    else:
        candidates = LINUX_PATHS
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def no_browser_exit():
    sys.stderr.write(
        "NO-BROWSER: no Chrome, Edge, Chromium, or Brave found on this machine.\n"
        "You can still get the PDF yourself in three steps:\n"
        "  1. Open the HTML file in any browser (double-click it).\n"
        "  2. Press Ctrl+P (Cmd+P on Mac) to print.\n"
        "  3. Choose 'Save as PDF' as the destination and save.\n"
        "The HTML file is the finished document; the PDF is just its print.\n"
        "Tip: set the BROWSER_BIN environment variable to a browser executable "
        "to point this script at one.\n")
    sys.exit(2)


def run_headless(browser, mode_args, url, out_path):
    """Run headless once with --headless=new, retry once with --headless."""
    for headless_flag in ("--headless=new", "--headless"):
        cmd = [browser, headless_flag, "--disable-gpu"] + mode_args + [url]
        try:
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                timeout=120)
        except (OSError, subprocess.TimeoutExpired) as e:
            sys.stderr.write("browser launch failed (%s): %s\n"
                             % (headless_flag, e))
            continue
        if result.returncode == 0 and os.path.isfile(out_path) \
                and os.path.getsize(out_path) > 0:
            return True
        sys.stderr.write("browser run with %s returned %s, output %s\n"
                         % (headless_flag, result.returncode,
                            "present" if os.path.isfile(out_path) else "missing"))
    return os.path.isfile(out_path) and os.path.getsize(out_path) > 0


def parse_size(value):
    try:
        w, h = value.lower().split("x", 1)
        return int(w), int(h)
    except (ValueError, AttributeError):
        return None


def main():
    args = sys.argv[1:]
    if len(args) < 3 or args[0] not in ("pdf", "shot"):
        sys.stderr.write(
            "usage: render_pdf.py pdf <in.html> <out.pdf>\n"
            "       render_pdf.py shot <in.html> <out.png> [--size WxH]\n")
        sys.exit(1)
    mode, in_html, out_path = args[0], args[1], args[2]

    size = (1200, 1600)
    if "--size" in args:
        idx = args.index("--size")
        if idx + 1 >= len(args) or parse_size(args[idx + 1]) is None:
            sys.stderr.write("--size needs a value like 1200x1600\n")
            sys.exit(1)
        size = parse_size(args[idx + 1])

    in_path = Path(in_html).resolve()
    if not in_path.is_file():
        sys.stderr.write("input HTML not found: %s\n" % in_path)
        sys.exit(1)
    out_abs = str(Path(out_path).resolve())
    out_dir = os.path.dirname(out_abs)
    if out_dir and not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    browser = find_browser()
    if not browser:
        no_browser_exit()

    url = in_path.as_uri()  # absolute file:// URL, forward slashes

    if mode == "pdf":
        mode_args = ["--print-to-pdf=%s" % out_abs, "--no-pdf-header-footer"]
    else:
        mode_args = ["--screenshot=%s" % out_abs,
                     "--window-size=%d,%d" % size,
                     "--hide-scrollbars"]

    if run_headless(browser, mode_args, url, out_abs):
        print("RENDERED %s" % out_abs)
        sys.exit(0)
    sys.stderr.write("render failed: browser ran but %s was not produced.\n"
                     % out_abs)
    sys.exit(1)


if __name__ == "__main__":
    main()
