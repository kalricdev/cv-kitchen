---
name: cv-kitchen
description: "Trigger: CV, resume, job application, tailor, ATS. Interview for verified facts and deliver a complete, ATS-readable CV."
license: MIT
metadata:
  author: kalricdev
  version: "1.1"
---

## Activation Contract

Use for CV creation, review, or tailoring. Work directly with the person's facts and available document tools; require no repository checkout or technical setup.

## Hard Rules

- Never invent employers, dates, experience, credentials, skills, or metrics. Keep unsupported requirements as gaps. Preserve the original CV.
- Ask one question at a time for missing facts, then wait. Use the requested document language.
- Use conventional headings such as Summary, Experience, Education, and Skills, with local-language equivalents. Use a single column, real body text, normal letter spacing, clear dates and titles, and ordinary bullets.
- Put name and contact details in body text, not headers or footers. Avoid tables, text boxes, icons, photos, charts, and scanned-text CVs.
- Match supported job terminology naturally; never stuff keywords, fabricate ATS scores, or guarantee acceptance.
- Protect private data. Uploads, email, and submissions need explicit authorization.

## Decision Gates

| Available tools | Deliver |
| --- | --- |
| Document generation | Complete CV in the requested format; default to DOCX or text-based PDF |
| Text only | Complete polished CV text ready to copy; never force Python or JSON setup |
| Missing evidence | Ask and wait, or mark the claim unresolved outside the CV |

## Execution Steps

1. Establish target role, document language, existing CV or verified facts, and full job posting if available. Ask only for missing inputs, one at a time.
2. Read bundled `references/workflow.md` and `references/ats-checklist.md` when available. Follow these main rules if references are unavailable.
3. Interview for relevant responsibilities, achievements, skills, and evidence. Metrics are optional. Compare required and preferred qualifications; distinguish supported matches from gaps.
4. Draft the complete CV with concise, specific prose. Tailor emphasis and wording while preserving factual claims. Review changes against source facts.
5. Generate the user's submission format if supported. Inspect layout and compare extracted text, reading order, dates, visible content, and links against the approved CV. Report unavailable checks honestly.
6. Use structured JSON only when requested for continuity; optional bundled template/example are not required outputs or user setup.

## Output Contract

Deliver the complete CV first, then a brief change summary, genuine gaps, and actual checks or unverified items. Keep unsupported claims and draft blockers outside the CV. Never claim to generate or validate files without doing so.

## References

Resolve within this skill folder:

- `references/workflow.md`
- `references/ats-checklist.md`
- `references/master-template.json` and `references/sample-master.json` (optional)
