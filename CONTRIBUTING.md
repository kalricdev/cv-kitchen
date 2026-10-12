# Contributing

<img src="assets/cv-kitchen-mascot.png" alt="CV Kitchen's paper chef" width="120">

CV Kitchen's product is the reusable skill. Keep its essential CV and ATS rules
in `skills/cv-kitchen/SKILL.md` so pasting that file alone still works. Put supporting
detail in bundled references. The default result is a complete CV, not technical
setup or JSON.

Use fictional identities and evidence in fixtures. Never commit real CVs, contact
details, credentials, or private files from `people/`, `exports/`, or `tmp/`.
Create a branch and PR; use conventional commits without AI attribution.

## Skill checks

After changing the skill, references, or optional canonical template/example:

```sh
python scripts/package_skill.py
python -m unittest discover -s tests
```

Commit the rebuilt `dist/cv-kitchen-skill.zip` alongside its source. The packager
copies canonical templates and the license, normalizes text to UTF-8 LF, and
packages an explicit allowlist. Tests check privacy boundaries, reference closure,
repeatability, and committed ZIP freshness.

Exercise the skill with fictional facts and a job posting. Check that it asks for
missing evidence, returns a complete CV, preserves facts, and reports unavailable
document checks. Do not replace that workflow check with prose-matching tests.

## Optional renderer maintenance

The Python renderers are developer helpers, not a user installation prerequisite.
Create a local virtual environment and install `requirements.txt` with its Python.
On Windows, use `.\.venv\Scripts\python.exe`; on macOS/Linux, activate the venv.

```sh
python scripts/test_render.py
python scripts/render_md.py examples/sample/master.json tmp/sample.md
python scripts/render_pdf.py examples/sample/master.json tmp/sample.pdf
python scripts/check_pdf.py tmp/sample.pdf
```

Create `tmp/` before rendering Markdown. PDF rendering requires a supported browser
on PATH or at a standard installation path. Without optional PyMuPDF, margins stay
white. Its separate license is documented in [credits](CREDITS.md).

The helpers render summary, experience, projects, education, skills, languages,
certifications, and header contact fields. PDF supports one nested role level;
custom and other schema sections are not rendered. Inspect every PDF page and
compare its content with the source. Report which checks ran and any limitations.
