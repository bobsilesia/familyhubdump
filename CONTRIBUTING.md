# Contributing

Thank you for considering contributing to Samsung Family Hub (HACS).

## Guidelines
- Use SemVer. Functional changes → minor, fixes → patch, fully stable integration → major.
- Before pushing, run lint and syntax checks (flake8, compileall).
- Do not commit secrets. Tokens must stay in HA configuration.

## Getting Started
1. Clone the repo and install dev tools (flake8; ruff optional).
2. Run local checks:
   - `flake8 custom_components/familyhub`
   - `python3 -m compileall -q custom_components/familyhub`
3. Add tests when possible.

## Pull Request
- Short change description, motivation, potential breaking changes.
- Ensure HACS compliance (manifest, hacs.json).
- After PR approval, CI will run (lint + syntax).
