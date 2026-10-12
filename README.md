# cv-kitchen

![An illustrated CV kitchen](assets/cv-kitchen-hero-v2.png)

**Fine-dining care for your next CV.**

An AI skill for building clear, evidence-based CVs that applicant tracking systems can read. It interviews you, tailors your experience to a role, and delivers a complete CV. Use it with Codex, Claude Code, Gemini, Claude, or ChatGPT.

[See Bob's example CV (PDF)](examples/bob/resume.pdf) · [Read the CV text](examples/bob/resume.md). Bob and every career detail in the example are fictional.

## Install

Install for Codex and Claude Code with one command:

```sh
npx --yes skills@latest add kalricdev/cv-kitchen --skill cv-kitchen -a codex -a claude-code -g -y
```

This uses the [Vercel skills CLI](https://github.com/vercel-labs/skills) and requires Node.js. It installs the skill globally for both agents. If the repository is private, your GitHub account needs access.

Codex is the coding agent available with eligible ChatGPT access; installing here does not install a skill in the ChatGPT browser app. Claude Code is likewise separate from Claude chat.

## Use in your browser

| Assistant | Install or load |
| --- | --- |
| Gemini | [Download the ZIP](dist/cv-kitchen-skill.zip?raw=true), then Settings → Skills → Upload |
| Claude | [Download the ZIP](dist/cv-kitchen-skill.zip?raw=true), then Customize → Skills → + Create skill → Upload a skill |
| ChatGPT | [Open SKILL.md](skills/cv-kitchen/SKILL.md?raw=true), then paste its full text or attach the file to your chat |

Gemini skills can be used without a paid Google AI subscription on eligible personal accounts; availability rolls out gradually. If upload is unavailable, paste the skill text. See the official [Gemini](https://support.google.com/gemini/answer/17094296?hl=en) and [Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) instructions.

Use your existing free or paid assistant access. Account limits and document-generation tools vary; CV Kitchen needs no paid API integration.

## Start your CV

Ask your assistant:

> Use CV Kitchen to build an ATS-ready CV. Ask one question at a time.

Bring your existing CV or verified career facts. For a specific application, add the full job posting and your preferred document language. The skill will identify gaps, improve wording, and use relevant keywords only when your experience supports them.

You receive a complete CV, plus a DOCX or text-based PDF when your assistant has document tools. If it cannot create a file, it returns polished text ready to copy into your document editor. It also reports missing evidence and checks it could not perform.

The recipe uses conventional headings, a single column, clear dates, and real body text. It keeps contact details out of headers and avoids tables, icons, photos, and text boxes. These choices reduce parsing problems; no skill can guarantee acceptance by every ATS.

Share only authorized information. Redact private contact details and confidential evidence before sending files to an assistant.

## Example CV

<a href="examples/bob/resume.pdf"><img src="examples/bob/preview.png" alt="Preview of Bob Example's fictional, single-column CV" width="420"></a>

## Credits

- [kalricdev](https://github.com/kalricdev) created CV Kitchen and its original skill.
- [Matt Pocock's skills](https://github.com/mattpocock/skills) inspired the straightforward installation approach.
- [Vercel skills](https://github.com/vercel-labs/skills) provides the installer.
- [Reactive Resume](https://github.com/amruthpillai/reactive-resume) inspired the optional structured-data format.
- [Kami](https://github.com/tw93/Kami) inspired the project's visual style.
- The original hero and mascot were generated with imagegen; [source prompts](assets/image-prompts.md) are included.

[MIT licensed](LICENSE). See [full credits](CREDITS.md), [usage prompts](docs/ai-setup.md), and [contributor instructions](CONTRIBUTING.md).
