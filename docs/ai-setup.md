# AI setup

## Browser prompt

[Download the skill ZIP](../dist/cv-kitchen-skill.zip?raw=true) and upload it in Gemini web under Settings → Skills → Upload. The ZIP has `SKILL.md` at its root and bundled references. Google's [official upload guide](https://support.google.com/gemini/answer/17094296?hl=en) describes account eligibility and rollout.

If native skills are unavailable, use this in Gemini, ChatGPT, or Claude:

```text
Use CV Kitchen to help me prepare a verified CV.
I am providing SKILL.md and its reference files. Follow that workflow.
My document language is [LANGUAGE]. My target role is [ROLE OR NOT YET CHOSEN].
Interview me one question at a time and wait for each answer.
Use verified facts only; do not invent credentials, metrics, or experience.
Return complete JSON using the bundled template and a readable CV draft.
If you cannot run local scripts, tell me which commands to run instead.
Do not claim that a draft passed checks you did not perform.
```

Paste `skills/cv-kitchen/SKILL.md` and attach or paste its `references/workflow.md` and `references/master-template.json`. The fictional `references/sample-master.json` demonstrates the shape; never reuse its career as yours.

Chat file/tool availability varies. A browser assistant without local execution can draft JSON and prose; PDF export uses the local tools below.

## Local agent setup prompt

Open a checkout in Gemini CLI, Codex, or Claude Code, replace the inputs, and paste:

```text
Set up CV Kitchen in [ABSOLUTE CHECKOUT PATH].
My person folder is [FOLDER NAME]; my CV language is [LANGUAGE].

Read AGENTS.md, README.md, skills/cv-kitchen/SKILL.md, and its references.
Preserve other people's edits and existing local data. Follow the project Git
workflow for tracked changes. Create .venv if absent; use its Python and install
requirements.txt only. Check supported browser paths in scripts/render_pdf.py.
Do not install optional PyMuPDF, AI SDKs, or global tools by default.

Create people/[FOLDER NAME]/[LANGUAGE]/master.json from templates/master.json only
if that file does not exist. Ask me for verified facts one question at a time,
waiting for each answer. Preserve JSON structure. Never fabricate qualifications,
dates, employers, skills, or metrics. Keep unverified information out of final CVs.

Use my existing assistant access. Do not create subscriptions, billable API calls,
upload personal data, publish a repository, email, or submit applications without
explicit authorization. Never print or commit secrets or personal CV data.

Run python scripts/test_render.py and python -m unittest discover -s tests.
When verified inputs are ready, render Markdown and PDF and run scripts/check_pdf.py.
Compare output with the master and visually inspect every PDF page if possible.
Report unavailable checks, exact errors, files changed, and remaining draft blockers.
Do not treat extraction alone as proof of accuracy or ATS acceptance.
```

A browser chat cannot install your environment by reading this prompt. Ask it to guide you through the README commands and return files for you to save.

## Tailoring prompt

```text
Use CV Kitchen to tailor my CV.

PERSON/FOLDER: [NAME OR LOCAL FOLDER]
DOCUMENT LANGUAGE: [LANGUAGE]
ROLE AND COMPANY: [ROLE / COMPANY]
TARGET FOLDER: [UNIQUE APPLICATION NAME]
MASTER JSON: [FULL VERIFIED JSON OR LOCAL PATH]
JOB DESCRIPTION: [FULL POSTING]
SOURCE URL: [URL OR UNKNOWN]
EVIDENCE AND DRAFT BLOCKERS: [AUTHORIZED INPUTS OR NONE]

Compare required and preferred qualifications with my evidence. Return supported
matches and gaps. Ask one question at a time for missing facts and wait.
Keep my base master unchanged. Return complete resume.tailored.json in the same
schema, emphasizing relevant supported experience. Never change facts or add
unearned skills. Do not invent ATS scores or hiring probabilities.

For chat, return the full JSON, a short change summary, gaps, and local render/check
commands. For a local agent, preserve existing application work, save the variant
under people/<name>/applications/<target>/, render Markdown and PDF, run extraction
checks, compare the outputs, and visually inspect if available.
Report actual checks and draft blockers. Do not upload, email, or submit anything.
```

## Account access

| Tool | Official documentation |
| --- | --- |
| Gemini CLI | [Installation](https://geminicli.com/docs/get-started/installation/), [authentication](https://geminicli.com/docs/get-started/authentication/), and [quotas](https://geminicli.com/docs/resources/quota-and-pricing/) |
| Codex | [ChatGPT or API authentication](https://learn.chatgpt.com/docs/auth) and [skills](https://developers.openai.com/codex/skills/) |
| Claude Code | [Authentication](https://code.claude.com/docs/en/authentication), [costs](https://code.claude.com/docs/en/costs), and [skills](https://code.claude.com/docs/en/skills) |

For Gemini CLI, install Node.js 20+ and run:

```sh
npm install -g @google/gemini-cli
gemini
```

Choose eligible Google sign-in for free or Google AI subscription access. Then ask the agent to read the skill in this checkout. Native registration is optional:

```sh
gemini skills link ./skills --scope workspace
```

See [Gemini CLI skill documentation](https://geminicli.com/docs/cli/skills/). Reading a file or pasting its contents remains the universal method.

Chat subscriptions and API billing are separate. This project calls no LLM APIs. Check provider terms and redact private data before sharing it; [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) includes its free-tier data-handling terms.
