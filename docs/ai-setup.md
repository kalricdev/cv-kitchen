# Use CV Kitchen

## Agent installation

Install the skill globally for Codex and Claude Code:

```sh
npx --yes skills@latest add kalricdev/cv-kitchen --skill cv-kitchen -a codex -a claude-code -g -y
```

The [Vercel skills CLI](https://github.com/vercel-labs/skills) requires Node.js. A private repository requires authorized GitHub access. Open your agent and ask it to use CV Kitchen; no checkout, Python environment, or JSON preparation is required.

For existing account access, consult [Codex authentication](https://learn.chatgpt.com/docs/auth) or [Claude Code authentication](https://code.claude.com/docs/en/authentication). Their browser chat applications use the methods below instead of this terminal installation.

## Browser installation

- Gemini: download `dist/cv-kitchen-skill.zip`, then Settings → Skills → Upload. [Official instructions](https://support.google.com/gemini/answer/17094296?hl=en).
- Claude: download the same ZIP, then Customize → Skills → + Create skill → Upload a skill. [Official instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- ChatGPT: paste the complete `skills/cv-kitchen/SKILL.md` text or attach that file, then ask it to follow the instructions.

The main skill contains the essential workflow and ATS rules. Bundled references provide further detail; ChatGPT does not need several separate uploads to begin. If native skill upload is unavailable in an account, pasting the main skill works in ordinary chat.

## Start prompt

```text
Use CV Kitchen to build an ATS-ready CV. Ask one question at a time.
My preferred document language is [LANGUAGE].
I will provide my existing CV or verified career facts.
Include projects and professional certificates or diplomas only when I provide
relevant verified entries. Use orange accents if you can generate the document.
```

## Tailoring prompt

```text
Use CV Kitchen to tailor my CV for [ROLE] at [COMPANY].
My preferred document language is [LANGUAGE].
Here is my existing CV: [PASTE OR ATTACH].
Here is the complete job posting: [PASTE].
My required submission format is [DOCX, PDF, OR NOT SPECIFIED].
OPTIONAL PROJECTS AND CREDENTIALS: [VERIFIED ENTRIES OR NONE].

Keep all factual claims supported by my experience. Ask one question at a time
when evidence is missing. Deliver the complete tailored CV, identify genuine
gaps, and report which document checks you performed.
```

Use authorized inputs only. Redact private details and confidential evidence before sharing. The skill does not require an API key or subscription purchase. Account limits and available document tools differ; chat subscriptions and API billing remain separate. An assistant without file tools should return a complete, polished CV for you to copy into your document editor.
