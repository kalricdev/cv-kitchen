"""Regression checks for the downloadable fictional CV, without a browser."""
from pathlib import Path
import re
import unittest

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


class BobExamplePdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader = PdfReader(ROOT / "examples/bob/resume.pdf")
        cls.text = "\n".join(page.extract_text() or "" for page in cls.reader.pages)
        cls.normalized = re.sub(r"\s+", " ", cls.text)

    def test_one_page_and_complete_identity_dates_and_achievements(self):
        self.assertEqual(len(self.reader.pages), 1)
        self.assertEqual(self.reader.metadata.title, "Bob Example")
        for expected in (
            "Bob Example", "Customer Support Specialist", "bob@example.com",
            "https://example.com/bob", "Fictional example:",
            "Example Software", "Jan 2023 - Sep 2026",
            "Customer Service Associate", "Example Retail", "Jan 2021 - Dec 2022",
            "94% customer satisfaction across 210 survey responses",
            "repeat contacts for those topics fell 22%",
            "Account Setup Help Refresh", "Q4 2025 - Q1 2026",
            "Diploma in Business Administration", "Example College", "2018 - 2020",
            "Diploma in Customer Experience", "Example Learning Institute", "Jun 2024",
            "Certificate in Support Operations", "Nov 2022",
            "English (Native)", "Spanish (Professional working proficiency)",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, self.normalized)

    def test_conventional_headings_extract_as_words_in_reading_order(self):
        # Letter spacing previously extracted SUMMARY as "S U M M A R Y".
        headings = ("SUMMARY", "EXPERIENCE", "PROJECTS", "SKILLS", "EDUCATION", "CERTIFICATES", "LANGUAGES")
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.text)
                self.assertNotIn(" ".join(heading), self.text)
        positions = [self.text.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))
        self.assertLess(self.text.index("Example Software"), self.text.index("Example Retail"))


if __name__ == "__main__":
    unittest.main()
