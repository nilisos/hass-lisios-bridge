"""Binary sensor platform for Lisios integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorEntityDescription

from .entity import LisiosEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from custom_components.lisios.data import WasserAlarm

    from .coordinator import LisiosDataUpdateCoordinator
    from .data import LisiosConfigEntry


@dataclass(frozen=True, kw_only=True)
class LisiosBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a Lisios binary sensor entity."""

    exists_fn: Callable[[WasserAlarm], bool] = lambda _: True
    value_fn: Callable[[WasserAlarm], bool]


ENTITY_DESCRIPTIONS = [
    LisiosBinarySensorEntityDescription(
        key="flow",
        has_entity_name=True,
        translation_key="flow",
        value_fn=lambda data: data.is_flow,
    ),
]


async def async_setup_entry(
    _hass: HomeAssistant,
    entry: LisiosConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary sensor platform."""
    async_add_entities(
        LisiosBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
            did=did,
        )
        for entity_description in ENTITY_DESCRIPTIONS
        for did in entry.runtime_data.coordinator.data.devices
    )


class LisiosBinarySensor(LisiosEntity, BinarySensorEntity):
    """Lisios binary sensor class."""

    entity_description: LisiosBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: LisiosDataUpdateCoordinator,
        entity_description: LisiosBinarySensorEntityDescription,
        did: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, entity_description, did)
        self._did = did

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        return self.entity_description.value_fn(self.coordinator.data.devices[self._did])
