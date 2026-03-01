# Samsung Family Hub — Wiki

Welcome to the wiki for the Samsung Family Hub Home Assistant integration (HACS).

Repository: https://github.com/bobsilesia/familyhubdump

## Contents
- Installation
- Configuration (PAT/OAuth)
- Features & Services
- Troubleshooting

This wiki is synchronized automatically from the repository on each push.

## Automatyzacja CI i publikacji
- Nightly CI: codziennie o 03:00 UTC (lint, składnia, auto‑naprawy).
- Auto Fix: na gałęziach/PR (poza main) – formatowanie i automatyczne commity.
- Auto Branch Fix: cyklicznie/ręcznie – PR z poprawkami (ruff/black/isort/autoflake).
- Zasady pre‑publish: flake8, compileall, ruff, mypy; wersjonowanie SemVer; Release Notes i asset ZIP dla HACS.

Sync: wykonywany przez workflow „Wiki Sync”.
Ostatnie wydanie: sprawdź Releases lub odznakę „Last release date”.
