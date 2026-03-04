from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

DOMAIN = "familyhub"
PLATFORMS = [Platform.SENSOR, Platform.CAMERA]


async def async_setup(hass: HomeAssistant, config: ConfigType):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def _handle_upload_media(call):
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            return
        data = entries[0].data
        auth = data.get("auth", "pat")
        device_id = data.get("device_id")
        from .api import SmartThingsClient

        if auth == "oauth":
            client = SmartThingsClient(
                token=data.get("access_token") or "",
                refresh_token=data.get("refresh_token"),
                token_url=data.get("token_url"),
                client_id=data.get("client_id"),
                client_secret=data.get("client_secret"),
            )
        else:
            client = SmartThingsClient(data.get("token") or "")
        path = call.data.get("path")
        content_type = call.data.get("content_type", "image/jpeg")
        try:
            with open(path, "rb") as f:
                content = f.read()
        except Exception:
            return
        await client.upload_media(
            device_id,
            content,
            path.split("/")[-1],
            content_type,
        )
        await client.close()

    hass.services.async_register(DOMAIN, "upload_media", _handle_upload_media)

    async def _get_client():
        entries = hass.config_entries.async_entries(DOMAIN)
        if not entries:
            return None, None
        data = entries[0].data
        device_id = data.get("device_id")
        from .api import SmartThingsClient

        if data.get("auth", "pat") == "oauth":
            client = SmartThingsClient(
                token=data.get("access_token") or "",
                refresh_token=data.get("refresh_token"),
                token_url=data.get("token_url"),
                client_id=data.get("client_id"),
                client_secret=data.get("client_secret"),
            )
        else:
            client = SmartThingsClient(data.get("token") or "")
        return client, device_id

    async def _handle_execute(call):
        client, device_id = await _get_client()
        if not client:
            return
        component = call.data.get("component")
        capability = call.data.get("capability")
        command = call.data.get("command")
        arguments = call.data.get("arguments", [])
        await client.execute(
            device_id,
            [
                {
                    "component": component,
                    "capability": capability,
                    "command": command,
                    "arguments": arguments,
                }
            ],
        )
        await client.close()

    hass.services.async_register(DOMAIN, "execute", _handle_execute)

    async def _handle_set_ice_maker(call):
        client, device_id = await _get_client()
        if not client:
            return
        state = call.data.get("state")
        args = [{"x": {"iceMaker": state}}]
        await client.execute(
            device_id,
            [
                {
                    "component": "main",
                    "capability": "execute",
                    "command": "execute",
                    "arguments": args,
                }
            ],
        )
        await client.close()

    hass.services.async_register(
        DOMAIN,
        "set_ice_maker",
        _handle_set_ice_maker,
    )

    async def _handle_reset_filter(call):
        client, device_id = await _get_client()
        if not client:
            return
        args = [{"x": {"resetFilter": True}}]
        await client.execute(
            device_id,
            [
                {
                    "component": "main",
                    "capability": "execute",
                    "command": "execute",
                    "arguments": args,
                }
            ],
        )
        await client.close()

    hass.services.async_register(DOMAIN, "reset_filter", _handle_reset_filter)

    async def _handle_set_power_cool(call):
        client, device_id = await _get_client()
        if not client:
            return
        state = call.data.get("state")
        args = [{"x": {"powerCool": state}}]
        await client.execute(
            device_id,
            [
                {
                    "component": "main",
                    "capability": "execute",
                    "command": "execute",
                    "arguments": args,
                }
            ],
        )
        await client.close()

    hass.services.async_register(
        DOMAIN,
        "set_power_cool",
        _handle_set_power_cool,
    )

    async def _handle_set_power_freeze(call):
        client, device_id = await _get_client()
        if not client:
            return
        state = call.data.get("state")
        args = [{"x": {"powerFreeze": state}}]
        await client.execute(
            device_id,
            [
                {
                    "component": "main",
                    "capability": "execute",
                    "command": "execute",
                    "arguments": args,
                }
            ],
        )
        await client.close()

    hass.services.async_register(
        DOMAIN,
        "set_power_freeze",
        _handle_set_power_freeze,
    )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unloaded = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
