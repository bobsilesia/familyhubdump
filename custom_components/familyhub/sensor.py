from __future__ import annotations

from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
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

    async def _update():
        return await client.get_device_status(device_id)

    coordinator = DataUpdateCoordinator(
        hass,
        name="familyhub_sensors",
        update_method=_update,
        update_interval=timedelta(seconds=30),
    )
    await coordinator.async_config_entry_first_refresh()
    entities = [
        FamilyHubTemperature(coordinator, "cooler"),
        FamilyHubTemperature(coordinator, "freezer"),
        FamilyHubDoor(coordinator, "main"),
        FamilyHubDoor(coordinator, "cvroom"),
        FamilyHubDoor(coordinator, "freezer"),
        FamilyHubIceMaker(coordinator),
        FamilyHubFilterStatus(coordinator),
        FamilyHubRefrigerationMode(coordinator),
        FamilyHubFilterRemaining(coordinator),
    ]
    async_add_entities(entities)


class FamilyHubTemperature(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, component: str):
        super().__init__(coordinator)
        self._component = component
        self._attr_name = f"Family Hub {component} temperature"
        self._attr_native_unit_of_measurement = "°C"

    @property
    def native_value(self):
        try:
            return self.coordinator.data["components"][self._component][
                "temperatureMeasurement"
            ]["temperature"]["value"]
        except Exception:
            return None


class FamilyHubDoor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator, component: str):
        super().__init__(coordinator)
        self._component = component
        self._attr_name = f"Family Hub {component} door state"

    @property
    def native_value(self):
        try:
            comp = self.coordinator.data["components"][self._component]
            v = comp["contactSensor"]["contact"]["value"]
            return "open" if v == "open" else "closed"
        except Exception:
            return None


class FamilyHubIceMaker(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self._attr_name = "Family Hub ice maker state"

    @property
    def native_value(self):
        try:
            comp = self.coordinator.data["components"]["main"]
            for cap_name, cap in comp.items():
                if not isinstance(cap, dict):
                    continue
                if "ice" in cap_name.lower() or cap_name.lower() in [
                    "refrigeration"
                ]:
                    for attr_name, attr in cap.items():
                        if isinstance(attr, dict) and "value" in attr:
                            if (
                                "ice" in attr_name.lower()
                                or cap_name.lower() == "icemaker"
                            ):
                                return attr["value"]
            return None
        except Exception:
            return None


class FamilyHubFilterStatus(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self._attr_name = "Family Hub water filter status"

    @property
    def native_value(self):
        try:
            comp = self.coordinator.data["components"]["main"]
            if "filterStatus" in comp:
                cap = comp["filterStatus"]
                for key in [
                    "filterStatus",
                    "filterLife",
                    "filterRemaining",
                    "lifeRemaining",
                    "status",
                ]:
                    v = cap.get(key)
                    if isinstance(v, dict) and "value" in v:
                        return v["value"]
            return None
        except Exception:
            return None


class FamilyHubRefrigerationMode(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self._attr_name = "Family Hub refrigeration mode"

    @property
    def native_value(self):
        try:
            comp = self.coordinator.data["components"]["main"]
            if "refrigeration" in comp:
                cap = comp["refrigeration"]
                for key in [
                    "mode",
                    "modes",
                    "refrigerationMode",
                    "supportedModes",
                ]:
                    v = cap.get(key)
                    if isinstance(v, dict) and "value" in v:
                        return v["value"]
            return None
        except Exception:
            return None


class FamilyHubFilterRemaining(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: DataUpdateCoordinator):
        super().__init__(coordinator)
        self._attr_name = "Family Hub filter remaining"
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        try:
            comp = self.coordinator.data["components"]["main"]
            if "filterStatus" in comp:
                cap = comp["filterStatus"]
                for key in ["filterRemaining", "lifeRemaining", "remaining"]:
                    v = cap.get(key)
                    if isinstance(v, dict) and "value" in v:
                        return v["value"]
            return None
        except Exception:
            return None
