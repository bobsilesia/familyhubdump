Zasady projektu: Samsung Family Hub (HACS)

Wydania
- Używaj SemVer: patch dla poprawek, minor dla nowych funkcji, major dla stabilnej pełnej integracji
- Każde wydanie ma Release Notes w GitHub Release zgodne ze zmianami

Autoryzacja
- Preferuj SmartApp OAuth dla pełnych uprawnień; PAT używaj do szybkiej konfiguracji
- Tokeny przechowuj w konfiguracji integracji HA; odświeżanie przez refresh_token

Integracja
- Sensory mapuj dynamicznie po capabilities; kamera przez execute i odczyt statusu
- Upload mediów przez usługę HA; docelowo pełna publikacja na panelu Family Hub

CI
- Uruchamiaj lint i sprawdzenie składni przy każdym push/PR (flake8 + compileall) na wszystkich gałęziach
- Auto Fix na PR i push (z wyłączeniem main): ruff --fix, black (79), isort (79), auto-commit
- Sync wiki: workflow warunkowy (has_wiki), permissions contents: write, skip gdy brak uprawnień
- Przed wypchnięciem zawsze uruchom lokalnie: `flake8 custom_components/familyhub` oraz `python3 -m compileall -q custom_components/familyhub`
