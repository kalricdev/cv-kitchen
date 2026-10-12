"""Protect the browser upload boundary: complete references, no private files."""

import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_skill", ROOT / "scripts/package_skill.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageSkillTests(unittest.TestCase):
    def test_self_contained_deterministic_allowlist(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in package.FILES:
                source = ROOT / package.SKILL / name
                target = root / package.SKILL / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if name not in package.MIRRORS:
                    target.write_bytes(source.read_bytes())
            for source in package.MIRRORS.values():
                target = root / source
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / source).read_bytes())
            private = root / package.SKILL / ".env"
            private.write_text("TEST_SECRET=never-package", encoding="utf-8")
            (root / package.SKILL / "notes.tmp").write_text("private notes", encoding="utf-8")
            (root / package.SKILL / ".hidden").write_text("private", encoding="utf-8")

            archive = package.build(root)
            first = archive.read_bytes()
            with zipfile.ZipFile(archive) as bundle:
                expected = set(package.FILES)
                self.assertEqual(set(bundle.namelist()), expected)
                self.assertIn("SKILL.md", bundle.namelist())
                skill = bundle.read("SKILL.md").decode("utf-8")
                for reference in re.findall(r"`(references/[^`]+)`", skill):
                    self.assertIn(reference, expected)
                self.assertEqual(bundle.read("references/master-template.json"),
                                 (ROOT / "templates/master.json").read_text(encoding="utf-8").encode("utf-8"))
                self.assertEqual(bundle.read("references/sample-master.json"),
                                 (ROOT / "examples/sample/master.json").read_text(encoding="utf-8").encode("utf-8"))
                self.assertFalse(any(b"TEST_SECRET" in bundle.read(name) for name in expected))
            private.write_text("TEST_SECRET=changed", encoding="utf-8")
            self.assertEqual(package.build(root).read_bytes(), first)

            # Git checkouts may use CRLF; the downloadable package must stay identical.
            sources = [root / source for source in package.MIRRORS.values()]
            sources.extend(root / package.SKILL / name for name in package.FILES
                           if name not in package.MIRRORS)
            for source in sources:
                source.write_bytes(source.read_text(encoding="utf-8").replace("\n", "\r\n").encode("utf-8"))
            self.assertEqual(package.build(root).read_bytes(), first)
            for name in package.MIRRORS:
                self.assertNotIn(b"\r\n", (root / package.SKILL / name).read_bytes())

    def test_tracked_archive_matches_current_sources(self):
        with zipfile.ZipFile(ROOT / "dist/cv-kitchen-skill.zip") as bundle:
            self.assertEqual(set(bundle.namelist()), set(package.FILES))
            for name in package.FILES:
                source = ROOT / package.MIRRORS.get(name, package.SKILL / name)
                self.assertEqual(bundle.read(name), source.read_text(encoding="utf-8").encode("utf-8"),
                                 "Stale skill ZIP; run python scripts/package_skill.py")

    def test_missing_input_preserves_existing_archive(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            archive = root / "dist/cv-kitchen-skill.zip"
            archive.parent.mkdir()
            archive.write_bytes(b"previous archive")
            with self.assertRaises(FileNotFoundError):
                package.build(root)
            self.assertEqual(archive.read_bytes(), b"previous archive")


if __name__ == "__main__":
    unittest.main()
