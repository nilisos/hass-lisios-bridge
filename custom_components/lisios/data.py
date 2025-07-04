"""Custom types for Lisios integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import LisiosApiClient
    from .coordinator import LisiosDataUpdateCoordinator


type LisiosConfigEntry = ConfigEntry[LisiosRuntimeData]


@dataclass
class LisiosRuntimeData:
    """Lisios integration runtime data."""

    client: LisiosApiClient
    coordinator: LisiosDataUpdateCoordinator
    integration: Integration


@dataclass
class WasserAlarm:
    """WasserAlarm data model."""

    uid: str
    did: str
    acc_temp: float
    amb_temp: float
    pipe_temp_mean: float


@dataclass
class LisiosCoordinatorData:
    """Lisios data update coordinator data."""

    devices: dict[str, WasserAlarm]
