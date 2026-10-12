# CV Kitchen agent instructions

## Product

CV Kitchen is a reusable skill for verified, ATS-readable CVs. Read
`skills/cv-kitchen/SKILL.md` for interviews, drafting, review, and tailoring.
Its main rules must work when pasted alone; bundled references add detail.

Deliver the complete CV first. Use available document tools for the requested
format, or return polished CV text ready to copy. Do not require a repository,
Python environment, or JSON setup from the person. Structured JSON and local
renderers are optional continuity and maintenance helpers.

Never invent experience, employers, dates, credentials, skills, or metrics.
Preserve source facts and original CVs. Ask one question at a time for missing
facts, then wait. Keep gaps and draft blockers outside the CV. Report actual
checks; never fabricate ATS scores or promise universal acceptance.

## Privacy and artifacts

Use English for code and project documentation. Use the person's requested
language for CV documents. Write direct prose supported by evidence.

`people/`, `exports/`, and `tmp/` hold ignored private local work. Do not delete
ignored files. Use fictional identities in public fixtures. Never commit secrets,
contact details, real CVs, or private evidence. Uploads, billable setup, email,
and submissions require explicit authorization.

For optional structured data, treat verified master facts as the source and
preserve them across tailored copies and languages. Never reuse fictional sample
claims as someone's experience.

## Maintenance checks

After changing the skill, references, or optional canonical template/example,
run `python scripts/package_skill.py` and `python -m unittest discover -s tests`.
Keep the tracked ZIP consistent with its allowlisted source.

For renderer changes, use a local venv and requirements, run
`python scripts/test_render.py`, and exercise the fictional export workflow.
Inspect PDFs visually and compare extraction with source content. Report unavailable
checks honestly. See `CONTRIBUTING.md` for developer commands.

## Git workflow

Use a work branch from updated main. Review changes for secrets and personal data,
commit with a conventional commit message, publish the branch, and open a PR.
Run relevant checks and repair failures before merging. Verify the merged PR and
remote main commit. Never commit or push directly to main, force-push, or add
Co-Authored-By or AI attribution.
