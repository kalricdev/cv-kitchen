---
name: cv-kitchen
description: "Trigger: CV, resume, job application, tailor, setup. Prepare verified CVs with the self-contained CV Kitchen workflow."
license: MIT
metadata:
  author: kalricdev
  version: "1.0"
---

## Activation Contract

Load for CV interviews, drafting, tailoring, or local CV Kitchen setup. Resolve bundled references within this skill folder.

## Hard Rules

- Use verified facts only. Never invent experience, dates, credentials, skill levels, or metrics. Keep unresolved checks as draft blockers.
- Preserve the base master and existing work. Use the requested document language and direct prose.
- Ask one question at a time when a fact is missing, then wait.
- Share authorized data only; redact private details. Uploads, billable setup, email, and submissions require explicit authorization.

## Decision Gates

| Context | Action |
| --- | --- |
| Browser chat | Read bundled references; interview and return complete JSON/prose; never pretend local execution |
| Local agent | Locate the actual checkout; read its README and AGENTS; use documented tools |
| Missing evidence | Keep the gap; do not turn it into a claim |

## Execution Steps

1. Read `references/workflow.md`. Start with `references/master-template.json`; use `references/sample-master.json` only as a fictional shape example.
2. Interview for verified facts and fill the master without changing its schema. Synchronize facts across language versions.
3. For tailoring, compare the full posting with evidence. Create a separate variant emphasizing supported experience; return a factual change summary and gaps.
4. Remove placeholders before final output. Compare all claims against the master.
5. For local setup/export, read `references/local-setup.md`. Render Markdown/PDF, check extraction, and inspect pages if tools are available. Report unavailable checks; extraction alone cannot certify readiness.

## Output Contract

Return complete JSON or saved files, a brief change summary, supported matches and gaps, actual checks, and draft blockers. Never promise ATS acceptance.

## References

- `references/workflow.md`
- `references/master-template.json`
- `references/sample-master.json`
- `references/local-setup.md`
