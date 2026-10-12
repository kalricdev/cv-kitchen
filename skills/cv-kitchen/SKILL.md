---
name: cv-kitchen
description: "Trigger: CV, resume, job application, tailor, ATS. Interview for verified facts and deliver a complete, ATS-readable CV."
license: MIT
metadata:
  author: kalricdev
  version: "1.2"
---

## Activation Contract

Use for CV creation, review, or tailoring with supplied facts and document tools. Require no technical setup.

## Hard Rules

- Never invent employers, dates, experience, credentials, skills, or metrics. Keep unsupported requirements as gaps. Preserve the original CV.
- Ask one question at a time for missing facts, then wait. Use the requested document language.
- Use conventional headings such as Summary, Experience, Education, and Skills, with local-language equivalents. Use a single column, real body text, normal letter spacing, clear dates and titles, and ordinary bullets.
- Put name and contact details in body text, not headers or footers. Avoid tables, text boxes, icons, photos, charts, and scanned-text CVs.
- Include Projects and Certifications & Diplomas only for relevant, verified entries; omit empty sections. Describe course diplomas accurately, never as degrees. Use no decorative emojis in the CV.
- When generating documents, default to burnt-orange accents (#c2410c) and readable dark body text. Honor the user's format and styling requirements first.
- Match supported job terminology naturally; never stuff keywords, fabricate ATS scores, or guarantee acceptance.
- Protect private data. Uploads, email, and submissions need explicit authorization.

## Decision Gates

| Available tools | Deliver |
| --- | --- |
| Document generation | Complete CV in the requested format; default to DOCX or text-based PDF |
| Text only | Complete polished CV text ready to copy; never force Python or JSON setup |
| Missing evidence | Ask and wait, or mark the claim unresolved outside the CV |

## Execution Steps

1. Establish target role, language, existing CV or verified facts, and available full posting. Ask only for missing inputs.
2. Read `references/workflow.md` and `references/ats-checklist.md` when available; these main rules work independently.
3. Interview for responsibilities, achievements, skills, and evidence. Metrics are optional. Distinguish supported qualifications from gaps.
4. Draft the complete CV with specific prose. Tailor emphasis, preserve claims, and compare changes with source facts.
5. Generate the requested format if supported. Check layout, extracted content, reading order, dates, and links against the approved CV. Report unavailable checks.
6. Use JSON only when requested for continuity; bundled examples are optional, never mandatory deliverables.

## Output Contract

Deliver the complete CV first, then changes, gaps, and actual or unverified checks. Keep unsupported claims and blockers outside it. Never pretend file generation or validation.

## References

Resolve within this skill folder:

- `references/workflow.md`
- `references/ats-checklist.md`
- `references/master-template.json` and `references/sample-master.json` (optional)
