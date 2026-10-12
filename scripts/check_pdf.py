"""Check local PDF text extraction and common unresolved draft markers.

Usage: python scripts/check_pdf.py exports/sample.pdf
Passing these checks does not verify ATS compatibility, factual accuracy,
visual layout, or suitability for a particular application.
"""
import argparse
import re
import sys


def inspect_text(text):
    """Return extraction and draft problems without printing personal content."""
    issues = []
    if not text.strip():
        issues.append("No extractable text; this may be an image-only PDF.")
    if "\ufffd" in text:
        issues.append("Replacement characters found; inspect the extracted text.")
    if re.search(r"\b20\d[A-Z]\b|\b20[A-Z]\d\b", text):
        issues.append("Mangled year-like tokens found; inspect dates in the PDF.")
    if re.search(r"\b(?:NEEDS METRIC|NEEDS VERIFICATION|TODO|TBD|DRAFT)\b", text):
        issues.append("Unresolved draft markers found.")
    if re.search(r"\[(?:FULL NAME|ROLE|EMAIL|CITY|COMPANY|TITLE|LOCATION|CATEGORY|MMM YYYY|What they did|Write a short summary|Only skills)\b", text, re.I):
        issues.append("Unfilled template placeholders found.")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", help="Local PDF to inspect")
    args = parser.parse_args()
    try:
        from pypdf import PdfReader
    except ImportError:
        raise SystemExit("pypdf is missing. Run: python -m pip install -r requirements.txt")
    try:
        reader = PdfReader(args.pdf)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        print("PDF could not be read: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
    print("pages:", len(reader.pages), "| extracted characters:", len(text))
    issues = inspect_text(text)
    if issues:
        for issue in issues:
            print("FAIL:", issue, file=sys.stderr)
        raise SystemExit(1)
    print("OK: extraction checks passed. Inspect layout and verify claims separately.")


if __name__ == "__main__":
    main()
