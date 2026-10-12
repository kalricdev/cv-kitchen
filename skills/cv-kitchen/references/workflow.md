# Verified CV workflow

This skill works without a repository checkout. Start with the bundled
`master-template.json`. The bundled `sample-master.json` uses a fictional person
and demonstrates structure, not facts to copy.

## Interview and draft

Ask the person about their target role and document language, one question at a
time. Collect verified employers, positions, dates, responsibilities, education,
skills, projects, and contact details they choose to disclose. Ask for evidence
when a metric or credential is uncertain. A real achievement needs no invented
number. Keep missing information as a gap outside the final CV.

Fill the template's existing JSON keys. Use plain text or simple paragraph/list
HTML in rich-text content. Preserve section metadata and empty unused item arrays.
Never carry template placeholders or fictional sample claims into a final CV.

Write directly in the requested language. Review dates, credentials, skill levels,
contact details, and every claim with the person. Keep factual content consistent
across language versions.

## Tailor

Read the full job posting. Compare required and preferred qualifications with
verified facts. Explain supported matches and gaps, without invented ATS scores
or hiring probabilities. Preserve the base master; create a separate complete
tailored JSON with the same schema. Reorder relevant items and rewrite supported
prose. Do not promote integration work into implementation experience or add a
skill merely because the posting mentions it.

Return the complete JSON, a readable CV draft, a short change summary, and unresolved
draft blockers. Keep gaps in notes, not disguised as credentials.

## Export and review

A browser assistant without local execution should provide complete JSON for the
person to save and the commands in `local-setup.md`. Never claim to have rendered
or checked a file without doing it. Local agents should compare exported Markdown
and PDF with JSON and inspect every PDF page for clipping and reading order.
Extraction cannot prove accuracy, completeness, or hiring-system acceptance.

The person must resolve placeholders, unsupported claims, and missing checks before
sending. Uploading, emailing, or submitting a CV requires an explicit instruction.
