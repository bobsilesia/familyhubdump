## Camera (snapshot)
- Tizen >3.x: use SmartThings `execute` + read `status.camera.snapshot` only.
- If the URL is empty, retry after a few seconds.

## Authorization
- 401: refresh token (OAuth) or verify PAT/Device ID.
- Check redirect/token URLs and client credentials.

## Sensors
- Capability mapping is dynamic; some models may use different attribute names.

## CI / Lint
- F401 (unused import): automatically removed (autoflake) in CI/PR.
- CI status and recent runs: check the badge in README and Actions.
- Before publishing: flake8, compileall, ruff, mypy – required.

## RS232 — freezing with too many requests
- Symptoms: device stops responding, buffer fills up, connection requires restart.
- Cause: too frequent requests (tight loop, no rate limits) overload the serial interface.
- Recommendations:
  - Set polling to "normal" (e.g. every 30 s) instead of "minimum"/continuous polling.
  - Group reads and limit the number of commands per cycle; avoid multiple requests for the same parameters.
  - Enable rate‑limit and backoff mechanisms; after an error, increase the interval.
  - For camera snapshots, call on‑demand; avoid automatic calls every few seconds.
  - If there is no response, stop polling for several seconds and resume with the normal interval.