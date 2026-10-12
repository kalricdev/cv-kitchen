# CV Kitchen agent instructions

## Scope and source data

This project provides reusable CV tools and a portable assistant skill. Read
`skills/cv-kitchen/SKILL.md` for setup, interviews, CV drafting, and tailoring.

Treat each person's `people/<name>/<language>/master.json` as their factual source.
Never invent experience, dates, credentials, skill levels, or metrics. Tailored
copies belong under `people/<name>/applications/<target>/`; keep base masters
unchanged unless the user authorizes a verified correction.

Ask one question at a time when a missing fact blocks drafting, then wait. Respect
draft blockers and report checks actually performed. Never promise ATS acceptance.

## Privacy and artifacts

Use English for project documentation and code. Use the person's requested language
for CV documents. Write direct prose supported by evidence.

`people/`, `exports/`, and `tmp/` hold local private work and remain outside Git.
Do not delete ignored files. Use fictional identities in public fixtures. Never
commit credentials, API keys, .env files, contact details, or private evidence.
Do not upload data, configure billable calls, email, or submit applications without
explicit authorization.

The skill is self-contained: its references resolve within `skills/cv-kitchen/`.
Run `python scripts/package_skill.py` after changing its instructions or canonical
template/example. Keep the tracked ZIP consistent with its source.

## Checks

Use a local virtual environment and `requirements.txt`. Run
`python scripts/test_render.py` and `python -m unittest discover -s tests`.
Exercise affected export workflows. Inspect PDFs visually; text extraction alone
does not establish accuracy or completeness. Report unavailable checks honestly.

## Git workflow

Use a work branch from updated main. Review the diff for secrets and personal data,
commit with a conventional commit message, publish the branch, and open a PR.
Run relevant checks and address failures before merging. Verify the merged PR and
the remote main commit. Never commit or push directly to main, force-push, or add
Co-Authored-By or AI attribution.
