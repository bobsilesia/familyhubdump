# Changelog

## 1.1.9
- Fix `hassfest` validation: Remove core dependency `aiohttp` from requirements.
- Fix `hassfest` validation: Remove invalid `target: sensor` from services (services are global per config entry).

## 1.1.8
- Fix `hassfest` validation: Add missing `options` strings and `services` descriptions to `strings.json` and `translations/en.json`.

## 1.1.7
- Fix `hassfest` validation: Add missing `strings.json` and `translations/en.json` for Config Flow.

## 1.1.6
- Fix `hassfest` validation for `upload_media` service (remove invalid `entity_id` field).
- Ensure `manifest.json` sorting and keys.

## 1.1.5
- Fix `services.yaml` selectors (use `text: {}`).
- Update `manifest.json` with `issue_tracker` and `integration_type`.
- Standardize on `ruff` for linting.

## 1.1.3
- Fix `services.yaml` selector syntax.
