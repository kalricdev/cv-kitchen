# Tailoring workflow

Keep `people/<name>/<language>/master.json` as the factual source. A tailored copy is an application artifact. Verify factual corrections before deliberately updating the master and affected copies.

1. Read the full posting and authorized evidence. List supported matches, missing requirements, and any draft blockers. Avoid invented ATS scores and hiring probabilities.
2. Copy the master to `people/<name>/applications/<target>/resume.tailored.json`. Keep facts and schema intact. Reorder relevant entries and rewrite supported prose for the role.
3. Compare the variant with the master. Verify employers, dates, qualifications, skill levels, and metrics. Ask one question at a time about missing facts; unanswered questions remain gaps.
4. Write direct prose in the requested language. A measurable result is useful only when verified. Remove all placeholders before final export.
5. Render and inspect both outputs. Preserve existing application files and use a unique target name.

Run from the repository root using your virtual environment's Python:

```sh
python scripts/render_md.py people/your-name/applications/target/resume.tailored.json people/your-name/applications/target/resume.md
python scripts/render_pdf.py people/your-name/applications/target/resume.tailored.json exports/YourName_Resume_Role_Company.pdf
python scripts/check_pdf.py exports/YourName_Resume_Role_Company.pdf
```

On PowerShell without activation, replace `python` with `.\.venv\Scripts\python.exe`.

Compare JSON, Markdown, and PDF. Inspect every PDF page for clipping, blank pages, reading order, dates, and contact details. Extraction checks do not certify accuracy, completeness, or ATS acceptance.

Keep the full job description, source URL, gap list, tailored files, and a short change summary with the application. Sending, emailing, or uploading requires a separate explicit instruction.

Use the [portable skill](../skills/cv-kitchen/SKILL.md) or [tailoring prompt](ai-setup.md#tailoring-prompt). No globally installed skills are needed.
