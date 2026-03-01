# Samsung Family Hub — Home Assistant Integration (HACS)

[![License](https://img.shields.io/github/license/bobsilesia/familyhubdump?color=blue)](LICENSE)
[![Latest release](https://img.shields.io/github/v/release/bobsilesia/familyhubdump?style=flat-square&color=b44e88&label=Latest%20release)](https://github.com/bobsilesia/familyhubdump/releases/latest)
[![CI](https://img.shields.io/github/actions/workflow/status/bobsilesia/familyhubdump/ci.yml?branch=main&style=flat-square)](https://github.com/bobsilesia/familyhubdump/actions/workflows/ci.yml)
[![Downloads](https://img.shields.io/github/downloads/bobsilesia/familyhubdump/total.svg)](https://github.com/bobsilesia/familyhubdump/releases)
[![Stars](https://img.shields.io/github/stars/bobsilesia/familyhubdump?style=flat-square)](https://github.com/bobsilesia/familyhubdump/stargazers)
[![Open issues](https://img.shields.io/github/issues/bobsilesia/familyhubdump?style=flat-square)](https://github.com/bobsilesia/familyhubdump/issues)
[![Last commit](https://img.shields.io/github/last-commit/bobsilesia/familyhubdump?style=flat-square)](https://github.com/bobsilesia/familyhubdump/commits/main)
[![Open PRs](https://img.shields.io/github/issues-pr/bobsilesia/familyhubdump?style=flat-square)](https://github.com/bobsilesia/familyhubdump/pulls)
[![Last release date](https://img.shields.io/github/release-date-latest/bobsilesia/familyhubdump?style=flat-square)](https://github.com/bobsilesia/familyhubdump/releases/latest)

HACS integration for Samsung Family Hub (Tizen >3.x) via SmartThings API: sensors, camera snapshot (“View Inside”), and media upload service.

Repository: https://github.com/bobsilesia/familyhubdump

## Requirements
- Home Assistant Core 2025.2+
- SmartThings Hub (recommended)
- Authorization: SmartApp OAuth (preferred) or PAT

## Installation (HACS)
1. Ensure the repository contains `custom_components/familyhub`.
2. In HACS, add the repository as a Custom Repository: `bobsilesia/familyhubdump`.
3. Install the integration and restart Home Assistant.

## Installation (Manual)
Copy `custom_components/familyhub` to `config/custom_components/` in your Home Assistant installation and restart HA.

## Configuration (Config Flow)
Settings → Devices & Services → Add Integration → Samsung Family Hub

Options:
- PAT: Token + Device ID
- OAuth: Client ID/Secret, Authorization URL, Token URL, Redirect URL, Device ID (with refresh_token support)

## Platforms and Features
- Sensor:
  - Temperatures: cooler, freezer
  - Doors: main, cvroom, freezer
  - Filter: status, remaining percentage
  - Ice maker: state
  - Refrigeration mode
- Camera:
  - Snapshot “View Inside” via `execute` and reading `status.camera.snapshot`
- Services:
  - `familyhub.upload_media` (upload to device via SmartThings)
  - `familyhub.execute` (arbitrary capability commands)
  - `familyhub.set_ice_maker` (on/off)
  - `familyhub.reset_filter`
  - `familyhub.set_power_cool`, `familyhub.set_power_freeze`

## Project Standards
- Async/await
- Dynamic capability mapping; camera via `execute` + status read
- Tokens stored in HA config; OAuth with refresh_token

## Issue Reporting
Check SmartThings and Home Assistant logs. For authorization errors, refresh the OAuth token or verify PAT/Device ID. Camera on Tizen >3.x is supported exclusively via SmartThings.

## License
Apache 2.0 — see LICENSE.
