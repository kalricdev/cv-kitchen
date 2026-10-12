# -*- coding: utf-8 -*-
"""Render a master.json to a single-column Markdown document.

Usage:
  python scripts/render_md.py examples/sample/master.json exports/sample.md

Plain text, one column, no tables. This is the file you paste into a form that
refuses PDFs, and the one to diff when you want to see what changed in the master.
"""
import io
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_pdf import bullets, meta_line, paragraphs, section_order, strip_html, visible  # noqa: E402


def md(text):
    """The shared parser keeps <strong>/<em> for HTML; markdown wants asterisks."""
    text = re.sub(r"</?(strong|b)\b[^>]*>", "**", text)
    text = re.sub(r"</?(em|i)\b[^>]*>", "*", text)
    return html.unescape(re.sub(r"<[^>]+>", "", text))


def render_markdown(d):
    """Preserve visible master content in its configured reading order."""
    b, S = d["basics"], d["sections"]
    L = []

    L.append("# %s" % b["name"])
    L.append("")
    if b.get("headline"):
        L.append(b["headline"])
        L.append("")
    L.append(b.get("location", ""))
    contact = [x for x in (b.get("email"), b.get("phone"), (b.get("website") or {}).get("url")) if x]
    contact.extend(cf.get("link") or cf.get("text") for cf in b.get("customFields") or []
                   if not cf.get("hidden") and (cf.get("link") or cf.get("text")))
    L.append(" · ".join(contact))
    L.append("")

    sections = {}
    header = L
    L = []
    summary = d.get("summary") or {}
    if not summary.get("hidden") and strip_html(summary.get("content")):
        L.append("## %s" % (summary.get("title") or "Summary"))
        L.append("")
        for p in paragraphs(summary["content"]):
            L.append(md(p))
            L.append("")
    sections["summary"] = L
    L = []

    def experience_item(it, depth=3):
        if it.get("hidden"):
            return
        L.append("%s %s - %s" % ("#" * depth, it["position"], it["company"]))
        L.append(meta_line(it, b.get("location")))
        L.append("")
        for x in bullets(it.get("description")) or paragraphs(it.get("description")):
            L.append("- %s" % md(x))
        L.append("")
        for role in it.get("roles") or []:
            experience_item(role, depth + 1)

    exp = S.get("experience")
    if visible(exp):
        L.append("## %s" % exp["title"])
        L.append("")
        for it in exp["items"]:
            experience_item(it)
    sections["experience"] = L
    L = []

    projects = S.get("projects")
    if visible(projects):
        L.append("## %s" % projects["title"])
        L.append("")
        for it in projects["items"]:
            if it.get("hidden"):
                continue
            L.append("### %s" % it["name"])
            if it.get("period"):
                L.append(it["period"])
            L.append("")
            bl = bullets(it.get("description"))
            for x in bl or paragraphs(it.get("description")):
                L.append(("- " if bl else "") + md(x))
                L.append("")
    sections["projects"] = L
    L = []

    edu = S.get("education")
    if visible(edu):
        L.append("## %s" % edu["title"])
        L.append("")
        for it in edu["items"]:
            if it.get("hidden"):
                continue
            L.append("**%s** - %s" % (it["degree"], it["school"]))
            L.append(meta_line(it, b.get("location")))
            L.append("")
    sections["education"] = L
    L = []

    sk = S.get("skills")
    if visible(sk):
        L.append("## %s" % sk["title"])
        L.append("")
        for it in sk["items"]:
            if it.get("hidden"):
                continue
            L.append("**%s:** %s" % (it["name"], ", ".join(it.get("keywords") or [])))
        L.append("")
    sections["skills"] = L
    L = []

    lang = S.get("languages")
    if visible(lang):
        L.append("## %s" % lang["title"])
        L.append("")
        L.append(" · ".join("%s, %s" % (i["language"], i["fluency"]) if "(" in i["fluency"]
                            else "%s (%s)" % (i["language"], i["fluency"])
                            for i in lang["items"] if not i.get("hidden")))
        L.append("")
    sections["languages"] = L
    L = []
    cert = S.get("certifications")
    if visible(cert):
        L.append("## %s" % cert["title"])
        L.append("")
        for it in cert["items"]:
            if it.get("hidden"):
                continue
            L.append("**%s** - %s" % (it.get("name", ""), it.get("issuer", "")))
            if it.get("date"):
                L.append(it["date"])
            L.append("")
    sections["certifications"] = L

    L = header + [line for key in section_order(d, sections) for line in sections.get(key, [])]
    return "\n".join(L).rstrip() + "\n"


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    with io.open(sys.argv[1], encoding="utf-8") as source:
        d = json.load(source)
    text = render_markdown(d)
    os.makedirs(os.path.dirname(os.path.abspath(sys.argv[2])), exist_ok=True)
    with io.open(sys.argv[2], "w", encoding="utf-8") as target:
        target.write(text)
    print("markdown:", sys.argv[2], "|", len(text), "chars")


if __name__ == "__main__":
    main()
