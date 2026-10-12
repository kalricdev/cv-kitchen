# Local setup and export

The browser workflow needs only this skill's bundled files. Local PDF export needs
a checkout of `https://github.com/kalricdev/cv-kitchen`, Python 3.10+, and a browser
at a supported path. A local agent must locate the checkout and read its current
`AGENTS.md` and `README.md`; those repository files govern local changes.

## Setup request for an agent

```text
Set up CV Kitchen in [CHECKOUT PATH]. Read its AGENTS.md and README.md and the
cv-kitchen skill. Preserve existing data and unrelated edits. Create a local .venv
if absent and install requirements.txt with its Python. Check the supported browser
paths. Do not install optional packages or configure billable APIs by default.

Copy templates/master.json to people/[NAME]/[LANGUAGE]/master.json only if absent.
Interview me for verified facts, one question at a time, waiting for each answer.
Never invent metrics or credentials. Keep unverified drafts clearly marked.

Run existing renderer and package tests. With verified inputs, render Markdown/PDF,
run extraction checks, compare output with JSON, and inspect PDF pages if possible.
Report exact errors, actual checks, and anything unverified. Do not upload data,
publish, email, subscribe, or submit applications without explicit authorization.
```

## Commands

Run from the repository root. On Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Use `.\.venv\Scripts\python.exe` instead of `python` for export commands.
On macOS/Linux:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Create `people/<name>/<language>/` yourself or ask the local agent to create it.
Save your completed JSON as its `master.json`, then run:

```sh
python scripts/render_md.py people/your-name/en/master.json people/your-name/en/resume.md
python scripts/render_pdf.py people/your-name/en/master.json exports/YourName_Resume.pdf
python scripts/check_pdf.py exports/YourName_Resume.pdf
```

For a job, save a separate `people/<name>/applications/<target>/resume.tailored.json`
and use that path as the renderer input. Compare exports with source and visually
review them. Private local data is ignored by Git; keep your own backup.

The tools make no LLM API calls. Use your existing assistant access; chat subscription
and API billing are separate. PyMuPDF is optional for colored margins and has its
own AGPL/commercial license. Without it, margins stay white.
