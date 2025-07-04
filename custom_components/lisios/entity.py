"""Base class for Lisios integration entities."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import LisiosDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.helpers.entity import EntityDescription


class LisiosEntity(CoordinatorEntity[LisiosDataUpdateCoordinator]):
    """Base class for Lisios integration entities."""

    def __init__(
        self,
        coordinator: LisiosDataUpdateCoordinator,
        entity_description: EntityDescription,
        did: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}/{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    coordinator.config_entry.domain,
                    did,
                ),
            },
            name=f"WasserAlarm {did}",
            serial_number=did,
        )
