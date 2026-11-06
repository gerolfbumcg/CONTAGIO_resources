#!/usr/bin/env python3
"""Local server for the CONTAGIO wording editor.

    python3 wording_server.py            # opens http://127.0.0.1:8765/editor.html
    python3 wording_server.py --port 9000 --no-browser
    python3 wording_server.py --export-static   # writes roadmap_static.html

- Serves this folder (editor.html, roadmap_verona.html, wording.json, ...).
- PUT /api/wording saves wording.json and regenerates the comparison table
  in CLAUDE.md (between the wording-table markers).
- Listens on 127.0.0.1 only. Standard library only, no dependencies.
"""
import argparse
import json
import os
import re
import sys
import tempfile
import webbrowser
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
WORDING = os.path.join(ROOT, "wording.json")
CLAUDE_MD = os.path.join(ROOT, "CLAUDE.md")
START, END = "<!-- wording-table:start -->", "<!-- wording-table:end -->"
ROADMAP = os.path.join(ROOT, "roadmap_verona.html")
STATIC_MARKER = "<!-- static-export: embedded wording data -->"


# ── Validation ──────────────────────────────────────────────────────────────

def validate(data):
    if not isinstance(data, dict):
        raise ValueError("top level must be an object")
    stages, topics = data.get("stages"), data.get("topics")
    if not isinstance(stages, list) or len(stages) != 5:
        raise ValueError("expected 5 stages")
    if not isinstance(topics, dict):
        raise ValueError("topics must be an object")
    seen = set()
    for st in stages:
        for tid in st.get("topics", []):
            if tid not in topics:
                raise ValueError("stage %s lists unknown topic %s" % (st.get("stage"), tid))
            if tid in seen:
                raise ValueError("topic %s appears in more than one stage" % tid)
            seen.add(tid)
    missing = set(topics) - seen
    if missing:
        raise ValueError("topics not placed in any stage: %s" % ", ".join(sorted(missing)))


# ── CLAUDE.md table ─────────────────────────────────────────────────────────

def _cell(text):
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def _tid_key(tid):
    return [int(x) for x in re.findall(r"\d+", tid)]


def _new_cell(new, status, a="title", b="desc"):
    na, nb = _cell(new.get(a)), _cell(new.get(b))
    if not (na or nb):
        return ""
    txt = ("**%s**" % na if na else "") + (": " if na and nb else "") + nb
    return txt + (" *(%s)*" % status if status else "")


def build_table(data):
    topics, stages = data["topics"], data["stages"]
    where = {}
    for st in stages:
        shown = [t for t in st["topics"] if topics[t].get("show")]
        for t in st["topics"]:
            where[t] = (st["stage"], shown.index(t) + 1 if t in shown else None)

    out = [START,
           "_Generated from `wording.json` by `wording_server.py` on every save. Do not edit this table by hand._",
           "",
           "### Stage headers",
           "",
           "| Stage | Slide 4 | Slide 5 | New wording |",
           "|---|---|---|---|"]
    for st in stages:
        out.append("| %s | %s | %s | %s |" % (
            st["stage"], _cell(st["slide4"]), _cell(st["slide5"]),
            _new_cell(st.get("new", {}), st.get("status", ""), "label", "sublabel")))

    out += ["", "### Item comparison", "",
            "| ID | Slide 4 | Slide 5 | Match | Verona | New wording |",
            "|---|---|---|---|---|---|"]
    counts = {"Same": 0, "Similar": 0, "Partial": 0, "New": 0}
    for tid in sorted(topics, key=_tid_key):
        t = topics[tid]
        s4, s5 = t.get("slide4"), t.get("slide5")
        s4c = "**%s** %s: %s" % (s4["ref"], _cell(s4["title"]), _cell(s4["desc"])) if s4 else "\u2014"
        s5c = "**%s** %s: %s" % (s5["ref"], _cell(s5["title"]), _cell(s5["desc"])) if s5 else "\u2014"
        match = t.get("match", "")
        if match in counts:
            counts[match] += 1
        if t.get("note"):
            match += " (%s)" % _cell(t["note"])
        stage, pos = where[tid]
        verona = "\u2713 stage %d, #%d" % (stage, pos) if pos else "\u2013 (stage %d, hidden)" % stage
        out.append("| **%s** | %s | %s | %s | %s | %s |" % (
            tid, s4c, s5c, match, verona, _new_cell(t.get("new", {}), t.get("status", ""))))

    shown = sum(1 for t in topics.values() if t.get("show"))
    worded = sum(1 for t in topics.values() if (t.get("new", {}).get("title") or t.get("new", {}).get("desc")))
    final = sum(1 for t in topics.values() if t.get("status") == "final")
    out += ["",
            "**Summary:** %d topics; slide 5 has %d of them (%d Same, %d Similar) and %d more partly. "
            "%s`roadmap_verona.html` shows %d. New wording entered for %d, of which %d final." % (
                len(topics), counts["Same"] + counts["Similar"], counts["Same"], counts["Similar"],
                counts["Partial"],
                ("%d added in the editor (on neither slide). " % counts["New"]) if counts["New"] else "",
                shown, worded, final),
            END]
    return "\n".join(out)


def update_claude_md(data):
    if not os.path.exists(CLAUDE_MD):
        return
    with open(CLAUDE_MD, encoding="utf-8") as f:
        md = f.read()
    if START not in md or END not in md:
        return
    head, rest = md.split(START, 1)
    _, tail = rest.split(END, 1)
    _atomic_write(CLAUDE_MD, head + build_table(data) + tail)


def _atomic_write(path, text):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".tmp-", suffix=".part")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


# ── Static export ───────────────────────────────────────────────────────────

def build_static(data):
    """roadmap_verona.html with the wording embedded, so it works as a standalone file."""
    with open(ROADMAP, encoding="utf-8") as f:
        html = f.read()
    if STATIC_MARKER not in html:
        raise ValueError("marker not found in roadmap_verona.html")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    block = ('<!-- Static export of roadmap_verona.html, generated %s. Texts are embedded below. -->\n'
             '<script type="application/json" id="wording-data">%s</script>'
             % (datetime.now().strftime("%Y-%m-%d %H:%M"), payload))
    return html.replace(STATIC_MARKER, block, 1)


# ── HTTP ────────────────────────────────────────────────────────────────────

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "/api/" in (self.path or ""):
            sys.stderr.write("[%s] %s\n" % (datetime.now().strftime("%H:%M:%S"), fmt % args))

    def _local_host(self):
        host = (self.headers.get("Host") or "").split(":")[0]
        return host in ("127.0.0.1", "localhost")

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/editor.html")
            self.end_headers()
            return
        if self.path == "/api/ping":
            return self._json(200, {"ok": True, "writable": True})
        return super().do_GET()

    def do_PUT(self):
        if self.path != "/api/wording":
            return self._json(404, {"ok": False, "error": "not found"})
        if not self._local_host() or "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._json(403, {"ok": False, "error": "forbidden"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            validate(data)
        except Exception as e:  # noqa: BLE001 - report any bad payload to the editor
            return self._json(400, {"ok": False, "error": str(e)})
        _atomic_write(WORDING, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        try:
            update_claude_md(data)
        except Exception as e:  # noqa: BLE001
            return self._json(200, {"ok": True, "warning": "CLAUDE.md not updated: %s" % e,
                                    "savedAt": datetime.now().strftime("%H:%M:%S")})
        return self._json(200, {"ok": True, "savedAt": datetime.now().strftime("%H:%M:%S")})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--export-md", action="store_true", help="only regenerate the CLAUDE.md table and exit")
    ap.add_argument("--export-static", nargs="?", const="roadmap_static.html", metavar="FILE",
                    help="write a standalone copy of the roadmap with the wording embedded "
                         "(default: roadmap_static.html) and exit")
    args = ap.parse_args()

    if args.export_static:
        with open(WORDING, encoding="utf-8") as f:
            data = json.load(f)
        validate(data)
        out = os.path.join(ROOT, args.export_static) if not os.path.isabs(args.export_static) else args.export_static
        _atomic_write(out, build_static(data))
        print("Wrote %s" % out)
        return

    if args.export_md:
        with open(WORDING, encoding="utf-8") as f:
            data = json.load(f)
        validate(data)
        update_claude_md(data)
        print("CLAUDE.md table regenerated")
        return

    url = "http://127.0.0.1:%d/editor.html" % args.port
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    except OSError:
        print("Port %d is already in use: the editor is probably already running.\n"
              "Open %s, or use another port: python3 main.py --port 8766" % (args.port, url))
        if not args.no_browser:
            webbrowser.open(url)
        return
    print("Wording editor: %s   (Ctrl+C to stop)" % url)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
