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

## RS232 — zawieszanie przy zbyt dużej liczbie zapytań
- Objawy: urządzenie przestaje odpowiadać, bufor się zapycha, połączenie wymaga restartu.
- Przyczyna: zbyt częste zapytania (tight loop, brak limitów) przeciążają interfejs szeregowy.
- Zalecenia:
  - Ustaw polling na „normal” (np. co 30 s) zamiast „minimum”/ciągłego odpytywania.
  - Grupuj odczyty i ogranicz liczbę komend na cykl; unikaj wielokrotnych zapytań do tych samych parametrów.
  - Włącz mechanizmy rate‑limit i backoff; po błędzie wydłuż interwał.
  - Dla snapshotów kamery wywołuj on‑demand; unikaj automatycznych wywołań co kilka sekund.
  - W przypadku braku odpowiedzi, zatrzymaj odpytywanie na kilkanaście sekund i wznowij z normalnym interwałem.
