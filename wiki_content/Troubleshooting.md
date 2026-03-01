# Troubleshooting

## Camera (snapshot)
- Tizen >3.x: use SmartThings `execute` + read `status.camera.snapshot` only.
- If the URL is empty, retry after a few seconds.

## Authorization
- 401: refresh token (OAuth) or verify PAT/Device ID.
- Check redirect/token URLs and client credentials.

## Sensors
- Capability mapping is dynamic; some models may use different attribute names.
