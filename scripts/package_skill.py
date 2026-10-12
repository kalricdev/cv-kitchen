"""Build the self-contained Gemini/browser skill ZIP from an explicit allowlist."""

from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/cv-kitchen")
MIRRORS = {
    "LICENSE": Path("LICENSE"),
    "references/master-template.json": Path("templates/master.json"),
    "references/sample-master.json": Path("examples/sample/master.json"),
}
FILES = (
    "SKILL.md",
    "LICENSE",
    "references/workflow.md",
    "references/local-setup.md",
    "references/master-template.json",
    "references/sample-master.json",
)


def build(root=ROOT):
    """Refresh canonical references and package only the six intended files."""
    root = Path(root)
    skill = root / SKILL
    for target, source in MIRRORS.items():
        destination = skill / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((root / source).read_text(encoding="utf-8").encode("utf-8"))

    # Read everything before replacing the archive so missing inputs preserve it.
    contents = [(name, (skill / name).read_text(encoding="utf-8").encode("utf-8"))
                for name in FILES]
    archive = root / "dist/cv-kitchen-skill.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive.with_suffix(".zip.tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for name, content in contents:
                entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                entry.compress_type = zipfile.ZIP_DEFLATED
                bundle.writestr(entry, content)
        temporary.replace(archive)
    finally:
        temporary.unlink(missing_ok=True)
    return archive


if __name__ == "__main__":
    print("skill:", build())
