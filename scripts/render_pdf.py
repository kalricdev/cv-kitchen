# -*- coding: utf-8 -*-
"""Render the supported master.json fields to a single-column PDF.

Usage:
  python scripts/render_pdf.py examples/sample/master.json exports/sample.pdf

Layout is single-column: no tables, no columns, no text inside page
headers or footers, real text only. The look follows tw93/Kami: parchment canvas,
forest-green accent, serif body, wide margins.

Rendering uses local headless Chrome, Chromium, or Edge. Check extraction with
`python scripts/check_pdf.py <pdf>` and inspect the result visually before use.
"""
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

PARCHMENT = "#f5f4ed"
INK = "#006421"

CSS = """
/* Margins live on @page so every page gets them, not only the first. Chrome
   leaves the @page margin area white, so paint_canvas() fills every page with
   parchment underneath the content after printing. */
@page { size: A4; margin: 13mm 16mm 11mm 16mm; }
* { box-sizing: border-box; }
html { background: %(parchment)s; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  margin: 0;
  padding: 0;
  background: %(parchment)s;
  color: #1a1a1a;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 9.3pt;
  line-height: 1.34;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
a { color: %(ink)s; text-decoration: none; }
header { margin-bottom: 9pt; }
h1 {
  font-size: 18.5pt;
  line-height: 1.1;
  letter-spacing: 0.2pt;
  color: %(ink)s;
  margin: 0 0 3pt 0;
  font-weight: 600;
}
.headline { font-size: 10.2pt; color: #46524a; margin: 0 0 6pt 0; font-style: italic; }
.contact { font-size: 9.2pt; color: #4a4a4a; }
.contact span:not(:last-child)::after { content: " · "; color: #9aa2ad; }
.rule { height: 1.3pt; background: %(ink)s; opacity: 0.85; margin: 0 0 10pt 0; }
section { margin-bottom: 7pt; }
h2 { break-after: avoid; }
h2 {
  font-size: 9.4pt;
  letter-spacing: 1.5pt;
  text-transform: uppercase;
  color: %(ink)s;
  font-weight: 700;
  margin: 0 0 5pt 0;
  padding-bottom: 2.5pt;
  border-bottom: 0.6pt solid rgba(0, 100, 33, 0.30);
}
p { margin: 0 0 5pt 0; }
.item { margin-bottom: 6pt; page-break-inside: avoid; }
.item:last-child { margin-bottom: 0; }
.item-head { display: flex; justify-content: space-between; align-items: baseline; gap: 10pt; }
.role { font-weight: 700; color: #12261a; font-size: 10.2pt; }
.org { color: %(ink)s; }
.meta { font-size: 9pt; color: #5d675f; white-space: nowrap; }
.edu-item { margin-bottom: 4pt; }
/* Engagements nested under an umbrella entry, for consultancy work where the
   client roles sit inside the consultancy's own dates. Indent plus a rule, no
   tables and no columns, so the text still extracts in reading order. */
.engagement { margin: 3pt 0 0 6pt; padding-left: 6pt; border-left: 1pt solid rgba(0, 100, 33, 0.22); page-break-inside: avoid; }
.engagement .role { font-size: 9.6pt; }
ul { margin: 3pt 0 0 0; padding-left: 12pt; }
li { margin-bottom: 1.8pt; }
li::marker { color: rgba(0, 100, 33, 0.55); }
.skill { margin-bottom: 2.4pt; }
.skill b { color: #12261a; }
.summary p { text-align: justify; }
"""


def strip_html(raw):
    """Keep basic emphasis, without attributes or executable rich-text markup."""
    if not raw:
        return ""
    pieces = re.split(r"(<[^>]*>)", raw)
    safe = []
    for piece in pieces:
        if piece.startswith("<") and piece.endswith(">"):
            tag = re.fullmatch(r"<(/?)(strong|b|em|i)\b[^>]*>", piece, re.I)
            safe.append("<%s%s>" % (tag[1], tag[2].lower()) if tag else " ")
        else:
            safe.append(html.escape(html.unescape(piece), quote=False))
    txt = "".join(safe)
    return re.sub(r"\s+", " ", txt).strip()


def section_order(data, sections):
    """Read configured sections once, then include supported unlisted sections."""
    order = [key for page in data.get("metadata", {}).get("layout", {}).get("pages", [])
             for column in ("main", "sidebar") for key in page.get(column, [])]
    return list(dict.fromkeys(order + list(sections)))


def bullets(raw):
    if not raw:
        return []
    items = re.findall(r"<li\b[^>]*>(.*?)</li>", raw, re.S)
    return [strip_html(i) for i in items if strip_html(i)]


def paragraphs(raw):
    if not raw:
        return []
    parts = re.findall(r"<p\b[^>]*>(.*?)</p>", raw, re.S) or [raw]
    return [strip_html(p) for p in parts if strip_html(p)]


def meta_line(it, home=None):
    """Location and dates on one right-aligned line; saves a line per entry.

    A location identical to the one in the header adds nothing, so it is dropped.
    Anything else (another city, remote work) still shows.
    """
    loc = it.get("location")
    if home and loc and loc.strip().lower() == home.strip().lower():
        loc = None
    return " · ".join(x for x in (loc, it.get("period")) if x)


def visible(section):
    return section and not section.get("hidden") and section.get("items")


def build_html(d):
    b = d["basics"]
    S = d["sections"]
    out = []
    out.append("<!doctype html><html lang='%s'><head><meta charset='utf-8'>"
               % html.escape(d.get("metadata", {}).get("page", {}).get("locale", "en-US")[:2], quote=True))
    out.append("<title>%s</title>" % html.escape(b["name"]))
    out.append("<style>%s</style></head><body>" % (CSS % {"parchment": PARCHMENT, "ink": INK}))

    contact = [b.get("location"), b.get("email"), b.get("phone")]
    url = (b.get("website") or {}).get("url")
    if url:
        contact.append(url)
    for cf in b.get("customFields") or []:
        if cf.get("hidden"):
            continue
        contact.append((cf.get("link") or cf.get("text") or "").replace("https://www.", "").replace("https://", "").rstrip("/"))
    contact = [c for c in contact if c]
    out.append("<header><h1>%s</h1>" % html.escape(b["name"]))
    if b.get("headline"):
        out.append("<p class='headline'>%s</p>" % html.escape(b["headline"]))
    out.append("<div class='contact'>%s</div></header>"
               % "".join("<span>%s</span>" % html.escape(c) for c in contact))
    out.append("<div class='rule'></div>")

    header, sections = out, {}
    out = []

    summary = d.get("summary") or {}
    if not summary.get("hidden") and strip_html(summary.get("content")):
        out.append("<section class='summary'><h2>%s</h2>" % html.escape(summary.get("title") or "Summary"))
        for p in paragraphs(summary["content"]):
            out.append("<p>%s</p>" % p)
        out.append("</section>")
    sections["summary"], out = out, []

    exp = S.get("experience")
    if visible(exp):
        out.append("<section><h2>%s</h2>" % html.escape(exp["title"]))
        for it in exp["items"]:
            if it.get("hidden"):
                continue
            out.append("<div class='item'><div class='item-head'>"
                       "<div class='role'>%s <span class='org'>· %s</span></div>"
                       "<div class='meta'>%s</div></div>"
                       % (html.escape(it["position"]), html.escape(it["company"]),
                          html.escape(meta_line(it, b.get("location")))))
            bl = bullets(it.get("description"))
            if bl:
                out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in bl))
            else:
                for p in paragraphs(it.get("description")):
                    out.append("<p>%s</p>" % p)
            for r in it.get("roles") or []:
                if r.get("hidden"):
                    continue
                out.append("<div class='engagement'><div class='item-head'>"
                           "<div class='role'>%s <span class='org'>· %s</span></div>"
                           "<div class='meta'>%s</div></div>"
                           % (html.escape(r["position"]), html.escape(r["company"]),
                              html.escape(meta_line(r, b.get("location")))))
                rbl = bullets(r.get("description"))
                if rbl:
                    out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % x for x in rbl))
                else:
                    for p in paragraphs(r.get("description")):
                        out.append("<p>%s</p>" % p)
                out.append("</div>")
            out.append("</div>")
        out.append("</section>")
    sections["experience"], out = out, []

    prj = S.get("projects")
    if visible(prj):
        out.append("<section%s><h2>%s</h2>" % (
            " style='break-before: page'" if prj.get("startOnNewPage") else "",
            html.escape(prj["title"])))
        for it in prj["items"]:
            if it.get("hidden"):
                continue
            out.append("<div class='item'><div class='item-head'>"
                       "<div class='role'>%s</div><div class='meta'>%s</div></div>"
                       % (html.escape(it["name"]), html.escape(it.get("period") or "")))
            for p in paragraphs(it.get("description")):
                out.append("<p>%s</p>" % p)
            out.append("</div>")
        out.append("</section>")
    sections["projects"], out = out, []

    edu = S.get("education")
    if visible(edu):
        out.append("<section><h2>%s</h2>" % html.escape(edu["title"]))
        for it in edu["items"]:
            if it.get("hidden"):
                continue
            out.append("<div class='item'><div class='item-head'>"
                       "<div class='role'>%s <span class='org'>· %s</span></div>"
                       "<div class='meta'>%s</div></div>"
                       % (html.escape(it["degree"]), html.escape(it["school"]),
                          html.escape(meta_line(it, b.get("location")))))
            out.append("</div>")
        out.append("</section>")
    sections["education"], out = out, []

    sk = S.get("skills")
    if visible(sk):
        out.append("<section><h2>%s</h2>" % html.escape(sk["title"]))
        for it in sk["items"]:
            if it.get("hidden"):
                continue
            kws = ", ".join(it.get("keywords") or [])
            out.append("<div class='skill'><b>%s:</b> %s</div>"
                       % (html.escape(it["name"]), html.escape(kws)))
        out.append("</section>")
    sections["skills"], out = out, []

    lang = S.get("languages")
    if visible(lang):
        parts = ["%s, %s" % (i["language"], i["fluency"]) if "(" in i["fluency"] else "%s (%s)" % (i["language"], i["fluency"]) for i in lang["items"] if not i.get("hidden")]
        out.append("<section><h2>%s</h2><p>%s</p></section>"
                   % (html.escape(lang["title"]), html.escape(" · ".join(parts))))
    sections["languages"], out = out, []

    cert = S.get("certifications")
    if visible(cert):
        out.append("<section><h2>%s</h2>" % html.escape(cert["title"]))
        for it in cert["items"]:
            if it.get("hidden"):
                continue
            out.append("<div class='item'><div class='item-head'>"
                       "<div class='role'>%s <span class='org'>· %s</span></div>"
                       "<div class='meta'>%s</div></div></div>"
                       % (html.escape(it.get("name", "")), html.escape(it.get("issuer", "")),
                          html.escape(it.get("date", ""))))
        out.append("</section>")
    sections["certifications"] = out

    out = header + [line for key in section_order(d, sections) for line in sections.get(key, [])]
    out.append("</body></html>")
    return "\n".join(out)


def find_chrome():
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge", "microsoft-edge"):
        found = shutil.which(name)
        if found:
            return found
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("Chrome, Chromium, or Edge not found. Install one locally or add its executable to PATH.")


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    with io.open(src, encoding="utf-8") as source:
        d = json.load(source)
    doc = build_html(d)

    html_path = os.path.splitext(dst)[0] + ".html"
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with io.open(html_path, "w", encoding="utf-8") as target:
        target.write(doc)

    chrome = find_chrome()
    # Preserve an existing export if the browser fails or silently writes nothing.
    with tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(dst))) as work:
        printed = os.path.join(work, "resume.pdf")
        subprocess.check_call([
            chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--print-to-pdf-no-header", "--print-to-pdf=" + printed,
            Path(html_path).resolve().as_uri(),
        ], stdout=subprocess.DEVNULL, timeout=60)
        if not os.path.isfile(printed) or os.path.getsize(printed) == 0:
            raise SystemExit("Browser did not produce a PDF. Review its error output above.")
        paint_canvas(printed)
        os.replace(printed, dst)
    print("html:", html_path)
    print("pdf :", dst, "|", os.path.getsize(dst), "bytes")


def paint_canvas(path):
    """Fill each page with the parchment colour under the printed content.

    Chrome does not paint the @page margin box, so the margins come out white.
    Requires PyMuPDF (uv pip install pymupdf); without it the PDF is left as is.
    """
    try:
        import pymupdf
    except ImportError:
        print("warning: pymupdf missing, page margins stay white")
        return
    rgb = tuple(int(PARCHMENT[i:i + 2], 16) / 255 for i in (1, 3, 5))
    doc = pymupdf.open(path)
    for page in doc:
        page.draw_rect(page.rect, color=None, fill=rgb, overlay=False)
    tmp = path + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close()
    os.replace(tmp, path)


if __name__ == "__main__":
    main()
