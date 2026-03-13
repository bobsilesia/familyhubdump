Samsung Family Hub  Wiki

Welcome to the wiki for the Samsung Family Hub Home Assistant integration (HACS).

Repository: https://github.com/bobsilesia/familyhubdump

## Contents
- Installation
- Configuration (PAT/OAuth)
- Features & Services
- Troubleshooting

This wiki is synchronized automatically from the repository on each push.

## CI and release automation
- Nightly CI: daily at 03:00 UTC (lint, syntax, auto‑fixes).
- Auto Fix: on branches/PR (except main) – formatting and automatic commits.
- Auto Branch Fix: scheduled/triggered – PR with fixes (ruff/black/isort/autoflake).
- Pre‑publish rules: flake8, compileall, ruff, mypy; SemVer versioning; Release Notes and ZIP asset for HACS.

Sync: performed by the "Wiki Sync" workflow.
Latest release: check Releases or the "Last release date" badge.

## Release & CI policy
- Pre‑publish (required):
  - `flake8 custom_components/familyhub`
  - `python3 -m compileall -q custom_components/familyhub`
  - `ruff check .`
  - `mypy custom_components/familyhub`
- Automation:
  - CI: every push/PR (fix: autoflake → ruff → black → isort; lint: flake8, syntax: compileall)
  - Auto Fix: on branches/PR except main (auto‑commit formatting changes)
  - Auto Branch Fix: schedule 02:00 UTC + manual dispatch (opens PR with fixes)
  - Wiki Sync: sync wiki_content to the wiki repo on push and manually (workflow_dispatch)