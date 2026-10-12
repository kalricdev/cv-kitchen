# Contributing

<img src="assets/cv-kitchen-mascot.png" alt="CV Kitchen's paper chef" width="120">

Keep changes small and describe the user-visible result. Use fictional identities
and evidence in examples and tests. Never include real CVs, contact details,
credentials, or local files from `people/`, `exports/`, or `tmp/`.

Create a branch and open a pull request. Use conventional commits without AI
attribution. Run:

```sh
python scripts/test_render.py
python -m unittest discover -s tests
python scripts/package_skill.py
```

When changing renderers, export the fictional sample, check text extraction, and
inspect the PDF. When changing the skill or its references, commit the rebuilt
`dist/cv-kitchen-skill.zip` alongside the source. Templates and examples are copied
into the skill package by the packaging script; edit their canonical source files.

Report which checks ran and any limitations. Preserve factual-source behavior and
keep the browser skill usable without the repository or a paid subscription.
