from __future__ import annotations

from datetime import timedelta

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import (CoordinatorEntity,
                                                      DataUpdateCoordinator)

from .api import SmartThingsClient


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities,
):
    auth = entry.data.get("auth", "pat")
    device_id = entry.data.get("device_id")
    if auth == "oauth":
        client = SmartThingsClient(
            token=entry.data.get("access_token") or "",
            refresh_token=entry.data.get("refresh_token"),
            token_url=entry.data.get("token_url"),
            client_id=entry.data.get("client_id"),
            client_secret=entry.data.get("client_secret"),
        )
    else:
        client = SmartThingsClient(entry.data.get("token") or "")
    coordinator = DataUpdateCoordinator(
        hass,
        name="familyhub_camera",
        update_method=lambda: client.get_device_status(device_id),
        update_interval=timedelta(seconds=30),
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([FamilyHubCamera(coordinator, client, device_id)])


class FamilyHubCamera(CoordinatorEntity, Camera):
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        client: SmartThingsClient,
        device_id: str,
    ):
        super().__init__(coordinator)
        Camera.__init__(self)
        self._client = client
        self._device_id = device_id
        self._attr_name = "Family Hub Camera"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

    async def async_camera_image(self):
        return await self._client.get_snapshot_image(self._device_id)
