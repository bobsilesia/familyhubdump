## Authorization modes
- PAT: quick start (token + device_id).
- OAuth: full permissions, refresh_token support (client_id/secret, authorization_url, token_url, redirect_url).

## Steps (OAuth)
1. Fill client details and URLs.
2. Open the authorization link to obtain the `code`.
3. Enter the `code` in the `oauth_code` step in HA.
4. Tokens will be stored in the integration configuration.

## Notes
- OAuth supports `refresh_token`; the integration stores tokens in the HA configuration.
- Recommended: OAuth for full permissions scope; PAT for quick start.