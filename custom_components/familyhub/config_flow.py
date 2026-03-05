from __future__ import annotations

from typing import Any, Dict

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from . import DOMAIN

AUTH_SELECT_SCHEMA = vol.Schema(
    {vol.Required("auth"): vol.In(["pat", "oauth"])}
)
PAT_SCHEMA = vol.Schema(
    {vol.Required("token"): str, vol.Required("device_id"): str}
)
OAUTH_SCHEMA = vol.Schema(
    {
        vol.Required("client_id"): str,
        vol.Required("client_secret"): str,
        vol.Required("device_id"): str,
        vol.Required("authorization_url"): str,
        vol.Required("token_url"): str,
        vol.Required("redirect_url"): str,
        vol.Optional("access_token"): str,
        vol.Optional("refresh_token"): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    _oauth_data: Dict[str, Any] = {}

    async def async_step_user(self, user_input: Dict[str, Any] | None = None):
        errors: Dict[str, str] = {}
        if user_input is not None:
            self._auth = user_input["auth"]
            if self._auth == "pat":
                return await self.async_step_pat()
            return await self.async_step_oauth()
        return self.async_show_form(
            step_id="user",
            data_schema=AUTH_SELECT_SCHEMA,
            errors=errors,
        )

    async def async_step_pat(self, user_input: Dict[str, Any] | None = None):
        errors: Dict[str, str] = {}
        if user_input is not None:
            data = {"auth": "pat", **user_input}
            return self.async_create_entry(title="Family Hub", data=data)
        return self.async_show_form(
            step_id="pat",
            data_schema=PAT_SCHEMA,
            errors=errors,
        )

    async def async_step_oauth(self, user_input: Dict[str, Any] | None = None):
        errors: Dict[str, str] = {}
        if user_input is not None:
            self._oauth_data = {"auth": "oauth", **user_input}
            auth_url = (
                f"{self._oauth_data['authorization_url']}?response_type=code"
                f"&client_id={self._oauth_data['client_id']}"
                f"&redirect_uri={self._oauth_data['redirect_url']}"
            )
            return self.async_show_form(
                step_id="oauth_code",
                data_schema=vol.Schema({vol.Required("code"): str}),
                errors=errors,
                description_placeholders={"auth_url": auth_url},
            )
        return self.async_show_form(
            step_id="oauth",
            data_schema=OAUTH_SCHEMA,
            errors=errors,
        )

    async def async_step_oauth_code(
        self,
        user_input: Dict[str, Any] | None = None,
    ):
        errors: Dict[str, str] = {}
        if user_input is not None:
            code = user_input["code"]
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self._oauth_data["client_id"],
                "client_secret": self._oauth_data["client_secret"],
                "redirect_uri": self._oauth_data["redirect_url"],
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self._oauth_data["token_url"],
                    data=data,
                ) as resp:
                    if resp.status != 200:
                        errors["base"] = "auth_failed"
                    else:
                        j = await resp.json()
                        entry_data = {
                            **self._oauth_data,
                            "access_token": j.get("access_token"),
                            "refresh_token": j.get("refresh_token"),
                        }
                        return self.async_create_entry(
                            title="Family Hub (OAuth)",
                            data=entry_data,
                        )
        return self.async_show_form(
            step_id="oauth_code",
            data_schema=vol.Schema({vol.Required("code"): str}),
            errors=errors,
        )

    @callback
    def async_get_options_flow(self, config_entry: config_entries.ConfigEntry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_create_entry(title="", data={})
