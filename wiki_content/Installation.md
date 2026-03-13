## Requirements
- Home Assistant Core 2025.2+
- SmartThings Hub (recommended)

## HACS
1. Add the repo as a Custom Repository: `bobsilesia/familyhubdump`.
2. Install the `Samsung Family Hub` integration.
3. Restart Home Assistant.
4. Alternatively: use the latest ZIP from Releases.

### ZIP for HACS
- Download the `familyhub-x.y.z.zip` asset from the latest release: https://github.com/bobsilesia/familyhubdump/releases/latest
- In HACS, point to the local ZIP package (or extract to `config/custom_components/familyhub`).

## Manual
Copy `custom_components/familyhub` to `config/custom_components/` and restart HA.