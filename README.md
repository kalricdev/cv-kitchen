# cv-kitchen

![An illustrated CV kitchen](assets/cv-kitchen-hero.png)

**Fine-dining care for your next CV.**

Start with verified facts, tailor them for a role, and serve a readable CV as Markdown or PDF. Use Gemini, ChatGPT, or Claude in your browser, or run the local tools with an AI agent. The tools do not call an LLM API.

## Start in your browser

1. [Download the CV Kitchen skill ZIP](dist/cv-kitchen-skill.zip?raw=true).
2. In Gemini web, open **Settings → Skills → Upload** and upload the ZIP. You can also extract it and upload the folder containing `SKILL.md` and `references/`.
3. Ask: "Use CV Kitchen to help me build a CV. Interview me one question at a time. My document language is English."
4. Supply your verified facts and, when tailoring, the full job posting. Review the draft before using it.

Gemini skills are available to eligible personal accounts without a paid Google AI subscription. Access rolls out gradually; if Skills is missing, use the paste method below. Google documents the [upload format, eligibility, and 100 MB limit](https://support.google.com/gemini/answer/17094296?hl=en).

For ChatGPT or Claude, paste [the skill instructions](skills/cv-kitchen/SKILL.md) and attach the bundled reference files, or upload them where your account supports files. You do not need native skill import: the [browser prompt](docs/ai-setup.md#browser-prompt) works with ordinary chat. Available file tools and usage limits vary by provider and plan.

The ZIP includes its own workflow, JSON template, fictional example, and license. A browser assistant can interview and return complete JSON or CV prose. It cannot claim to run your local scripts without access to local tools.

## Cook locally

Install Git, Python 3.10+, and Chrome, Chromium, or a supported Edge installation for PDF export.

### Windows PowerShell

```powershell
git clone https://github.com/kalricdev/cv-kitchen.git
Set-Location cv-kitchen
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
New-Item -ItemType Directory -Force people/your-name/en
Copy-Item templates/master.json people/your-name/en/master.json
```

Use `.\.venv\Scripts\python.exe` instead of `python` in the commands below.

### macOS or Linux

```sh
git clone https://github.com/kalricdev/cv-kitchen.git
cd cv-kitchen
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p people/your-name/en
cp templates/master.json people/your-name/en/master.json
```

Edit your master with verified facts. Replace placeholders, remove unused example items, and preserve the JSON structure. Keep a backup of personal files: `people/`, `exports/`, and `tmp/` are ignored by Git.

```sh
python scripts/render_md.py people/your-name/en/master.json people/your-name/en/resume.md
python scripts/render_pdf.py people/your-name/en/master.json exports/YourName_Resume.pdf
python scripts/check_pdf.py exports/YourName_Resume.pdf
```

To try the kitchen before adding personal data, render `examples/sample/master.json` instead. The example identity and career are fictional.

Open every PDF page and compare it with the master. Check contact details, dates, completeness, clipping, and reading order. Text extraction checks cannot certify factual accuracy or ATS acceptance.

Optional: `python -m pip install pymupdf` paints PDF margins to match the parchment background. It has separate AGPL/commercial licensing; see [credits](CREDITS.md).

## Bring your own assistant

| Access | How to use it |
| --- | --- |
| Gemini free or Google AI plan | Upload the browser skill or paste it; use eligible Google sign-in for Gemini CLI |
| ChatGPT free or paid plan | Paste the skill and attach authorized inputs; eligible plans can also use Codex |
| Claude free or paid plan | Paste the skill and attach authorized inputs; eligible subscriptions can also use Claude Code |
| Provider API account | Optional separately billed agent access; no API integration is implemented here |

Chat subscriptions and API billing are separate. The [AI setup guide](docs/ai-setup.md) provides official authentication links and a prompt for a local agent to configure the project. No subscription is needed for local rendering.

Share only information you own or have permission to share. Redact contact details and confidential evidence before sending files to an assistant. Provider data-handling terms differ; review them before uploading a CV.

## The recipe

Keep `people/<name>/<language>/master.json` as the factual source. Put each job-specific copy at `people/<name>/applications/<target>/resume.tailored.json`. Change emphasis and wording, not employers, dates, qualifications, or results. Record missing requirements as gaps. A metric is optional; an invented metric is never acceptable.

Follow the [tailoring workflow](docs/tailoring-workflow.md), or use the [tailoring prompt](docs/ai-setup.md#tailoring-prompt). Keep language masters synchronized when facts change.

```text
templates/master.json                 blank starting structure
examples/sample/master.json           fictional demonstration
skills/cv-kitchen/                     self-contained assistant skill
dist/cv-kitchen-skill.zip              browser upload package
scripts/                              render, check, and package tools
docs/                                 setup and tailoring instructions
people/                               ignored local CV sources
exports/                              ignored local PDF/Markdown outputs
tmp/                                  ignored temporary work
```

## Checks and troubleshooting

```sh
python scripts/test_render.py
python -m unittest discover -s tests
python scripts/package_skill.py
```

If PDF rendering cannot find a browser, add its executable to PATH or check the standard paths in `scripts/render_pdf.py`. If `pypdf` is missing, install `requirements.txt` with the same Python executable you use for the check. Without optional PyMuPDF, page margins remain white.

Both renderers support summary, experience, projects, education, skills, languages, and certifications, plus header contact fields. PDF supports one level of nested experience roles; custom sections and other schema sections are not rendered. Compare each export with the source. AI-drafted claims stay drafts until the person verifies them.

## Credits and license

Created by [kalricdev](https://github.com/kalricdev). [MIT licensed](LICENSE), with [credits](CREDITS.md) for the schema, visual inspiration, and dependencies. See [CONTRIBUTING.md](CONTRIBUTING.md) before contributing. Use fictional data in public examples.
