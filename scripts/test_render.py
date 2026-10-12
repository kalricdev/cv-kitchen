"""Focused regression checks using fictional CV data only."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from check_pdf import inspect_text
from render_md import render_markdown
from render_pdf import build_html, find_chrome, strip_html
import render_pdf

ROOT = Path(__file__).resolve().parents[1]


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "examples/sample/master.json").read_text(encoding="utf-8"))

    def test_fictional_sample_and_configured_order(self):
        for output in (render_markdown(self.data), build_html(self.data)):
            self.assertIn("Alex Example", output)
            self.assertIn("candidate@example.com", output)
            self.assertLess(output.index("Summary"), output.index("Skills"))
            self.assertLess(output.index("Skills"), output.index("Experience"))
        self.assertIn("FICTIONAL DEMO", self.data["metadata"]["notes"])

    def test_hidden_content_and_nested_role(self):
        self.data["basics"]["customFields"] = [{"text": "HIDDEN CONTACT", "hidden": True}]
        role = copy.deepcopy(self.data["sections"]["experience"]["items"][0])
        role.update(position="Visible Nested Role", company="Example Client", roles=[])
        hidden = copy.deepcopy(role)
        hidden.update(position="HIDDEN ROLE", hidden=True)
        self.data["sections"]["experience"]["items"][0]["roles"] = [role, hidden]
        self.data["sections"]["education"]["hidden"] = True
        for output in (render_markdown(self.data), build_html(self.data)):
            self.assertIn("Visible Nested Role", output)
            self.assertNotIn("HIDDEN ROLE", output)
            self.assertNotIn("HIDDEN CONTACT", output)
            self.assertNotIn("Example College", output)

    def test_certifications_in_both_exports(self):
        self.data["sections"]["certifications"].update(hidden=False, items=[
            {"name": "Fictional Certificate", "issuer": "Example Issuer", "date": "2022"},
            {"name": "HIDDEN CERTIFICATE", "issuer": "Example Issuer", "hidden": True},
        ])
        for output in (render_markdown(self.data), build_html(self.data)):
            self.assertIn("Certificates", output)
            self.assertIn("Fictional Certificate", output)
            self.assertNotIn("HIDDEN CERTIFICATE", output)

    def test_optional_projects_and_credentials_visible_hidden_or_empty(self):
        self.data["sections"]["projects"].update(hidden=False, items=[
            {"name": "Fictional Support Project", "period": "2024", "description": "<p>Wrote a fictional help guide.</p>"},
        ])
        self.data["sections"]["certifications"].update(hidden=False, items=[
            {"name": "Fictional Professional Diploma", "issuer": "Example Institute", "date": "2024"},
        ])
        for render in (render_markdown, build_html):
            with self.subTest(render=render.__name__):
                output = render(self.data)
                self.assertIn("Fictional Support Project", output)
                self.assertIn("Fictional Professional Diploma", output)
                self.assertIn("Wrote a fictional help guide.", output)
                self.assertIn("Example Institute", output)
                for state in ("hidden", "empty"):
                    data = copy.deepcopy(self.data)
                    for key in ("projects", "certifications"):
                        if state == "hidden":
                            data["sections"][key]["hidden"] = True
                        else:
                            data["sections"][key]["items"] = []
                    output = render(data)
                    self.assertNotIn("Fictional Support Project", output)
                    self.assertNotIn("Fictional Professional Diploma", output)
                    self.assertNotIn("Projects", output)
                    self.assertNotIn("Certificates", output)

    def test_rich_text_keeps_only_safe_emphasis(self):
        raw = '<p><strong onclick="run()">A &amp; B</strong><img src="https://example.com/x"> &lt;script&gt;</p>'
        safe = strip_html(raw)
        self.assertEqual(safe, "<strong>A &amp; B</strong> &lt;script&gt;")
        self.data["summary"]["content"] = raw
        html_output = build_html(self.data)
        self.assertNotIn("onclick", html_output)
        self.assertNotIn("<img", html_output)
        self.assertNotIn("<script>", html_output)
        markdown = render_markdown(self.data)
        self.assertIn("**A & B**", markdown)
        self.assertNotIn("&amp;", markdown)

    def test_browser_can_be_discovered_on_path(self):
        with patch("render_pdf.shutil.which", return_value="/example/chromium"):
            self.assertEqual(find_chrome(), "/example/chromium")

    def test_missing_browser_output_preserves_existing_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "resume.pdf"
            destination.write_bytes(b"existing export")
            argv = ["render_pdf.py", str(ROOT / "examples/sample/master.json"), str(destination)]
            with patch("sys.argv", argv), patch("render_pdf.find_chrome", return_value="example-chrome"), patch("render_pdf.subprocess.check_call"):
                with self.assertRaisesRegex(SystemExit, "did not produce"):
                    render_pdf.main()
            self.assertEqual(destination.read_bytes(), b"existing export")


class ExtractionTests(unittest.TestCase):
    def test_readable_text_passes(self):
        self.assertEqual(inspect_text("Alex Example\nSupport Specialist — Example Company\n2023 - 2024"), [])

    def test_blank_text_fails(self):
        self.assertTrue(inspect_text(" \n\t"))

    def test_draft_markers_fail(self):
        for text in ("[NEEDS METRIC: response time]", "DRAFT", "[FULL NAME]", "[EMAIL]", "[Write a short summary from verified facts.]"):
            with self.subTest(text=text):
                self.assertTrue(inspect_text(text))

    def test_extraction_anomalies_fail(self):
        for text in ("202A", "20B4", "Unknown \ufffd glyph"):
            with self.subTest(text=text):
                self.assertTrue(inspect_text(text))


if __name__ == "__main__":
    unittest.main()
