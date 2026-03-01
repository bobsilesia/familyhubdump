# Troubleshooting

## Camera (snapshot)
- Tizen >3.x: use SmartThings `execute` + read `status.camera.snapshot` only.
- If the URL is empty, retry after a few seconds.

## Authorization
- 401: refresh token (OAuth) or verify PAT/Device ID.
- Check redirect/token URLs and client credentials.

## Sensors
- Capability mapping is dynamic; some models may use different attribute names.

## CI / Lint
- F401 (nieużyty import): automatycznie usuwany (autoflake) w CI/PR.
- Status CI i ostatnie runy: sprawdź badge w README oraz Actions.
- Przed publikacją: flake8, compileall, ruff, mypy – wymagane.
