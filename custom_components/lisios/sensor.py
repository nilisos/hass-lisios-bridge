"""Sensor platform for Lisios integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorEntityDescription
from homeassistant.const import UnitOfTemperature

from .entity import LisiosEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

    from custom_components.lisios.data import WasserAlarm

    from .coordinator import LisiosDataUpdateCoordinator
    from .data import LisiosConfigEntry


@dataclass(frozen=True, kw_only=True)
class LisiosSensorEntityDescription(SensorEntityDescription):
    """Describes Lisios sensor entity."""

    exists_fn: Callable[[WasserAlarm], bool] = lambda _: True
    value_fn: Callable[[WasserAlarm], StateType]


ENTITY_DESCRIPTIONS = [
    LisiosSensorEntityDescription(
        key="accelerometer_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        has_entity_name=True,
        translation_key="accelerometer_temperature",
        value_fn=lambda data: data.acc_temp,
    ),
    LisiosSensorEntityDescription(
        key="ambient_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        has_entity_name=True,
        translation_key="ambient_temperature",
        value_fn=lambda data: data.amb_temp,
    ),
    LisiosSensorEntityDescription(
        key="pipe_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        has_entity_name=True,
        translation_key="pipe_temperature",
        value_fn=lambda data: data.pipe_temp_mean,
    ),
]


async def async_setup_entry(
    _hass: HomeAssistant,
    entry: LisiosConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        LisiosSensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
            did=did,
        )
        for entity_description in ENTITY_DESCRIPTIONS
        for did in entry.runtime_data.coordinator.data.devices
    )


class LisiosSensor(LisiosEntity, SensorEntity):
    """Lisios Sensor class."""

    entity_description: LisiosSensorEntityDescription

    def __init__(
        self,
        coordinator: LisiosDataUpdateCoordinator,
        entity_description: LisiosSensorEntityDescription,
        did: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, entity_description, did)
        self._did = did

    @property
    def native_value(self) -> StateType:
        """Return the native value of the sensor."""
        return self.entity_description.value_fn(self.coordinator.data.devices[self._did])
