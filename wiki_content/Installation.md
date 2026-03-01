# Installation

## Requirements
- Home Assistant Core 2025.2+
- SmartThings Hub (recommended)

## HACS
1. Add the repo as a Custom Repository: `bobsilesia/familyhubdump`.
2. Zainstaluj integrację `Samsung Family Hub`.
3. Restart Home Assistant.
4. Alternatywnie: użyj najnowszego ZIP z Releases.

### ZIP dla HACS
- Pobierz asset `familyhub-x.y.z.zip` z najnowszego wydania: https://github.com/bobsilesia/familyhubdump/releases/latest
- W HACS wskaż lokalny pakiet ZIP (lub rozpakuj do `config/custom_components/familyhub`).

## Manual
Copy `custom_components/familyhub` to `config/custom_components/` and restart HA.
