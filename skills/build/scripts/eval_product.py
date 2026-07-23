#!/usr/bin/env python3
"""Deterministic eval gate for The Product Studio.

Scores one build run against the rules that make a product honest and
sellable. Pure regex, length, and file checks: no model, no network, no state.

Usage:
    python eval_product.py <run.json> <profile.json>

Output: one line starting with @@EVAL_JSON@@ followed by the verdict JSON.
    ok true  -> {ok, product, format, passed, total, checks: [{name, passed, detail}]}
    ok false -> {ok: false, error: "..."} and exit code 1 (unreadable input)

The run JSON carries absolute paths to the product files (run["files"]); the
script reads them. A referenced non-null file that is missing on disk is a
FAILED CHECK, never a crash.

Skip-pass rule: a check that depends on a profile value the tenant has not
configured records passed=true with detail "skip-pass: <field> empty", so an
unconfigured profile never fails on tenant-specific rules.

A crashing check is a failed check, never a crash out.
"""

import json
import os
import re
import sys
from pathlib import Path

EM_DASH = "\u2014"

KNOWN_FORMATS = {
    "pdf-guide", "ebook", "template-pack", "worksheet", "checklist",
    "prompt-pack", "course", "video-script",
}

VALID_STATUSES = {"drafting", "built", "listed", "selling", "killed"}

PLACEHOLDER_TOKENS = [
    "lorem ipsum", "[insert", "[add ", "[your text", "todo", "tbd",
    "{{", "<placeholder", "content goes here", "coming soon", "xxx",
    "[example]", "fill this in",
]

FILLIN_RE = re.compile(r"\[FILL-IN:\s*([^\]]*)\]", re.IGNORECASE)

BRACKET_RE = re.compile(r"\[[^\]\n]*\]")

PRICE_RE = re.compile(r"[£$€]\s*(\d+(?:\.\d{1,2})?)")

HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+\S", re.MULTILINE)

NUMBERED_OR_CHECKBOX_RE = re.compile(r"^\s*(\d+[\.\)]|[-*]\s*\[ \])", re.MULTILINE)

CHECKLIST_ITEM_RE = re.compile(r"^\s*(\d+[\.\)]|[-*]\s*\[[ xX]?\])", re.MULTILINE)

TIMEFRAME_RE = re.compile(
    r"\b(\d+\s*(minutes?|mins?|hours?|hrs?|days?|weeks?|months?)|"
    r"a\s+(day|week|month)|per\s+(day|week|month)|daily|weekly|monthly)\b",
    re.IGNORECASE,
)

OUTCOME_MARKERS_RE = re.compile(
    r"(so you can|so that|without\s|instead of|even if|in \d+)", re.IGNORECASE
)

TOPIC_PROMISE_RE = re.compile(
    r"^(a|an|the)?\s*(course|guide|ebook|e-book|book|template|templates|"
    r"community|newsletter|masterclass|workshop|program|programme)s?\s+"
    r"(about|on|for|covering)\b",
    re.IGNORECASE,
)


def fail_out(message):
    print("@@EVAL_JSON@@ " + json.dumps({"ok": False, "error": message}))
    sys.exit(1)


def load_json(path, label):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        fail_out("%s: %s" % (label, e))


def read_text(path):
    """Return (text, error). Missing or unreadable file -> (None, message)."""
    if not path:
        return None, "path is empty"
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read(), None
    except OSError as e:
        return None, "cannot read %s: %s" % (path, e)


def word_count(text):
    return len([w for w in re.split(r"\s+", text.strip()) if w])


def strip_fillins(text):
    return FILLIN_RE.sub("", text)


def build_context(run):
    """Read the product files once. Records per-file errors, never raises."""
    files = run.get("files") or {}
    ctx = {"errors": [], "product_text": None, "sales_text": None,
           "course_files": [], "files": files}

    product_md = files.get("productMd")
    text, err = read_text(product_md)
    if err:
        ctx["errors"].append("productMd: %s" % err)
    parts = [text] if text is not None else []

    fmt = (run.get("format") or "").strip().lower()
    if fmt in ("course", "video-script") and product_md:
        course_dir = Path(os.path.dirname(os.path.abspath(product_md))) / "course"
        found = []
        if course_dir.is_dir():
            for p in sorted(course_dir.glob("*.md")):
                t, e = read_text(str(p))
                if e:
                    ctx["errors"].append("course file: %s" % e)
                else:
                    found.append((str(p), t))
        else:
            for extra in files.get("extras") or []:
                if isinstance(extra, str) and extra.lower().endswith(".md"):
                    t, e = read_text(extra)
                    if e:
                        ctx["errors"].append("extras file: %s" % e)
                    else:
                        found.append((extra, t))
        ctx["course_files"] = found
        parts.extend(t for _, t in found)

    if parts:
        ctx["product_text"] = "\n\n".join(parts)

    sales = files.get("salesPage")
    if sales:
        stext, serr = read_text(sales)
        if serr:
            ctx["errors"].append("salesPage: %s" % serr)
        else:
            ctx["sales_text"] = stext
    return ctx


def check_format_known(run, _profile, _ctx):
    fmt = (run.get("format") or "").strip().lower()
    if fmt not in KNOWN_FORMATS:
        return False, "format must be one of %s, got %r" % (
            "/".join(sorted(KNOWN_FORMATS)), fmt)
    return True, "format: %s" % fmt


def check_no_placeholder_filler(run, _profile, ctx):
    if ctx["product_text"] is None:
        return False, "product text unreadable: %s" % "; ".join(ctx["errors"])
    combined = strip_fillins(ctx["product_text"])
    if ctx["sales_text"]:
        combined += "\n" + strip_fillins(ctx["sales_text"])
    low = combined.lower()
    hits = [tok for tok in PLACEHOLDER_TOKENS if tok in low]
    if hits:
        return False, "placeholder filler found: %s" % ", ".join(repr(h) for h in hits)
    return True, "no placeholder filler in product or sales text"


def check_fillins_marked_not_faked(run, _profile, ctx):
    if ctx["product_text"] is None:
        return False, "product text unreadable: %s" % "; ".join(ctx["errors"])
    text = ctx["product_text"]
    fill_ins = run.get("fillIns") or []
    if len(fill_ins) > 10:
        return False, "%d fill-ins, max 10 (more is a scaffold)" % len(fill_ins)
    declared = [str(f).casefold() for f in fill_ins]
    for m in BRACKET_RE.finditer(text):
        span = m.group(0)
        inner = span[1:-1]
        if inner.strip().lower() in ("", "x"):
            continue  # markdown checkbox [ ] / [x]
        if FILLIN_RE.match(span):
            body = FILLIN_RE.match(span).group(1).strip().casefold()
            if not any(body in d or d in body for d in declared):
                return False, "fill-in not listed in run.fillIns: %r" % span
            continue
        if m.end() < len(text) and text[m.end()] == "(":
            continue  # markdown link [text](url)
        return False, "bracket span is neither [FILL-IN: ...] nor a link: %r" % span
    return True, "%d fill-ins, all marked and declared" % len(fill_ins)


def _substance_written(text, min_words, min_headings, label):
    words = word_count(text)
    headings = len(HEADING_RE.findall(text))
    if words < min_words:
        return False, "%s: %d words, needs >= %d" % (label, words, min_words)
    if headings < min_headings:
        return False, "%s: %d headings, needs >= %d" % (label, headings, min_headings)
    return True, "%s: %d words, %d headings" % (label, words, headings)


def check_substance_per_format(run, _profile, ctx):
    fmt = (run.get("format") or "").strip().lower()
    if ctx["product_text"] is None:
        return False, "product text unreadable: %s" % "; ".join(ctx["errors"])
    text = ctx["product_text"]

    if fmt in ("pdf-guide", "ebook"):
        return _substance_written(text, 2000, 4, fmt)

    if fmt == "template-pack":
        files = ctx["files"]
        product_md = files.get("productMd") or ""
        tdir = Path(os.path.dirname(os.path.abspath(product_md))) / "templates"
        candidates = []
        if tdir.is_dir():
            candidates = [str(p) for p in sorted(tdir.iterdir())
                          if p.suffix.lower() in (".md", ".csv")
                          and p.name.lower() != "import.md"]
        if not candidates:
            candidates = [e for e in files.get("extras") or []
                          if isinstance(e, str)
                          and e.lower().endswith((".md", ".csv"))]
        usable = 0
        thin = []
        for c in candidates:
            t, e = read_text(c)
            if e:
                thin.append("%s (missing)" % c)
            elif word_count(t) >= 100:
                usable += 1
            else:
                thin.append("%s (%d words)" % (c, word_count(t)))
        if usable < 4:
            return False, ("template-pack: %d usable templates (>=100 words each), "
                           "needs >= 4; thin/missing: %s" % (usable, thin or "none"))
        return True, "template-pack: %d usable templates" % usable

    if fmt == "worksheet":
        prompts = len(NUMBERED_OR_CHECKBOX_RE.findall(text))
        words = word_count(text)
        if prompts < 8:
            return False, "worksheet: %d prompts/exercises, needs >= 8" % prompts
        if words < 300:
            return False, "worksheet: %d words, needs >= 300" % words
        return True, "worksheet: %d prompts, %d words" % (prompts, words)

    if fmt == "checklist":
        items = len(CHECKLIST_ITEM_RE.findall(text))
        if items < 15:
            return False, "checklist: %d items, needs >= 15" % items
        return True, "checklist: %d items" % items

    if fmt == "prompt-pack":
        blocks = len(HEADING_RE.findall(text)) + len(
            re.findall(r"^\s*\d+[\.\)]\s+\S", text, re.MULTILINE))
        words = word_count(text)
        if blocks < 15:
            return False, "prompt-pack: %d prompt blocks, needs >= 15" % blocks
        if words < 800:
            return False, "prompt-pack: %d words, needs >= 800" % words
        return True, "prompt-pack: %d blocks, %d words" % (blocks, words)

    if fmt in ("course", "video-script"):
        lesson_count = run.get("lessonCount") or 0
        record_count = run.get("recordCount") or 0
        if lesson_count < 3:
            return False, "%s: lessonCount %s, needs >= 3" % (fmt, lesson_count)
        lesson_files = [(p, t) for p, t in ctx["course_files"]
                        if "outline" not in os.path.basename(p).lower()
                        and not os.path.basename(p).startswith("00")]
        short = [(p, word_count(t)) for p, t in lesson_files if word_count(t) < 300]
        if short:
            return False, "%s: lesson files under 300 words: %s" % (
                fmt, ["%s (%d)" % (os.path.basename(p), w) for p, w in short])
        if record_count < lesson_count:
            return False, "%s: recordCount %d < lessonCount %d" % (
                fmt, record_count, lesson_count)
        records_in_text = text.count("RECORD:")
        if records_in_text < lesson_count:
            return False, "%s: %d RECORD: lines in text, needs >= %d" % (
                fmt, records_in_text, lesson_count)
        return True, "%s: %d lessons, %d RECORD: lines, %d lesson files all >= 300 words" % (
            fmt, lesson_count, records_in_text, len(lesson_files))

    return False, "no substance rule for format %r" % fmt


def check_promise_delivered(run, _profile, ctx):
    promise = (run.get("promise") or "").strip()
    if not promise:
        return False, "promise is empty"
    if TOPIC_PROMISE_RE.match(promise):
        return False, "promise is a topic, not an outcome: %r" % promise
    has_number = bool(re.search(r"\d", promise))
    has_timeframe = bool(TIMEFRAME_RE.search(promise))
    has_marker = bool(OUTCOME_MARKERS_RE.search(promise))
    if not (has_number or has_timeframe or has_marker):
        return False, (
            "promise has no outcome signal (number, timeframe, or "
            "'so you can / without / instead of'): %r" % promise)
    delivery = [d for d in (run.get("promiseDelivery") or [])
                if isinstance(d, str) and d.strip()]
    if not delivery:
        return False, "promiseDelivery is empty: name the section(s) that deliver it"
    if ctx["product_text"] is None:
        return False, "product text unreadable: %s" % "; ".join(ctx["errors"])
    folded = ctx["product_text"].casefold()
    lines = [ln.strip() for ln in ctx["product_text"].splitlines()]
    structural = [ln.casefold() for ln in lines
                  if ln.startswith("#") or (ln.startswith("**") and ln.endswith("**"))]
    missing = []
    for section in delivery:
        target = section.strip().casefold()
        if not any(target in s for s in structural) and target not in folded:
            missing.append(section)
    if missing:
        return False, "promiseDelivery sections not found in product: %s" % missing
    return True, "promise delivered by: %s" % delivery


def check_price_carried(run, profile, ctx):
    price = (run.get("price") or "").strip()
    amounts = [float(m) for m in PRICE_RE.findall(price)]
    if not amounts:
        return False, "no currency amount found in price: %r" % price
    pricing = profile.get("pricing") or {}
    floor = pricing.get("floor")
    ceiling = pricing.get("ceiling")
    band_note = "skip-pass: pricing.floor/ceiling empty"
    if isinstance(floor, (int, float)) and isinstance(ceiling, (int, float)):
        low, high = min(amounts), max(amounts)
        if low < floor or high > ceiling:
            return False, "price %s-%s outside comfort %s-%s" % (
                low, high, floor, ceiling)
        band_note = "inside comfort %s-%s" % (floor, ceiling)
    if ctx["sales_text"] is not None:
        missing = []
        for a in amounts:
            token = str(int(a)) if a == int(a) else ("%.2f" % a)
            if token not in ctx["sales_text"]:
                missing.append(token)
        if missing:
            return False, "price number(s) %s not found in sales page" % missing
        return True, "price %r carried into sales page (%s)" % (price, band_note)
    return True, "price %r (%s; no sales page yet)" % (price, band_note)


def check_voice_and_cta(run, profile, ctx):
    if ctx["product_text"] is None:
        return False, "product text unreadable: %s" % "; ".join(ctx["errors"])
    combined = ctx["product_text"]
    if ctx["sales_text"]:
        combined += "\n" + ctx["sales_text"]
    if EM_DASH in combined:
        return False, "em dash found in product or sales text"
    banned = (profile.get("brand") or {}).get("bannedWords") or []
    banned_note = "skip-pass: brand.bannedWords empty" if not banned else \
        "no banned words"
    for word in banned:
        if word and re.search(r"\b%s\b" % re.escape(word), combined, re.IGNORECASE):
            return False, "banned word %r in product or sales text" % word
    if ctx["sales_text"] is None:
        return True, "voice clean (%s; no sales page yet)" % banned_note
    anchors = re.findall(r"<a\b[^>]*data-cta=\"buy\"[^>]*>", ctx["sales_text"],
                         re.IGNORECASE)
    if not anchors:
        return False, "sales page has no data-cta=\"buy\" anchor"
    hrefs = set()
    for a in anchors:
        m = re.search(r"href=\"([^\"]*)\"", a)
        hrefs.add(m.group(1) if m else "(no href)")
    if len(hrefs) != 1:
        return False, "buy CTAs point at %d different targets: %s" % (
            len(hrefs), sorted(hrefs))
    return True, "voice clean, %d buy CTA(s), one target (%s)" % (
        len(anchors), next(iter(hrefs)))


def check_cover_present(run, _profile, ctx):
    files = ctx["files"]
    cover = files.get("cover")
    if not cover:
        return False, "files.cover is not set"
    if not os.path.isfile(cover):
        return False, "cover html missing on disk: %s" % cover
    png = files.get("coverPng")
    png_note = "coverPng also on disk" if (png and os.path.isfile(png)) else \
        "coverPng not rendered (html only)"
    return True, "cover html on disk; %s" % png_note


def check_status_valid(run, _profile, _ctx):
    status = (run.get("status") or "").strip().lower()
    if status not in VALID_STATUSES:
        return False, "status must be one of %s, got %r" % (
            "/".join(sorted(VALID_STATUSES)), status)
    return True, "status: %s" % status


CHECKS = [
    ("format_known", check_format_known),
    ("no_placeholder_filler", check_no_placeholder_filler),
    ("fillins_marked_not_faked", check_fillins_marked_not_faked),
    ("substance_per_format", check_substance_per_format),
    ("promise_delivered", check_promise_delivered),
    ("price_carried", check_price_carried),
    ("voice_and_cta", check_voice_and_cta),
    ("cover_present", check_cover_present),
    ("status_valid", check_status_valid),
]


def main():
    if len(sys.argv) != 3:
        fail_out("usage: eval_product.py <run.json> <profile.json>")
    run = load_json(sys.argv[1], "run")
    profile = load_json(sys.argv[2], "profile")
    if not isinstance(run, dict) or not isinstance(profile, dict):
        fail_out("run and profile must both be JSON objects")
    try:
        ctx = build_context(run)
    except Exception as e:
        ctx = {"errors": ["context build crashed: %s" % e], "product_text": None,
               "sales_text": None, "course_files": [], "files": run.get("files") or {}}
    results = []
    for name, fn in CHECKS:
        try:
            passed, detail = fn(run, profile, ctx)
        except Exception as e:  # a crash is a failed check, never a crash out
            passed, detail = False, "check crashed: %s" % e
        results.append({"name": name, "passed": bool(passed), "detail": detail})
    passed_count = sum(1 for r in results if r["passed"])
    print("@@EVAL_JSON@@ " + json.dumps({
        "ok": True,
        "product": run.get("product", ""),
        "format": run.get("format", ""),
        "passed": passed_count,
        "total": len(results),
        "checks": results,
    }))


if __name__ == "__main__":
    main()
