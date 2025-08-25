"""DataUpdateCoordinator for Lisios integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from typing import TYPE_CHECKING

from aiohttp import ClientError
from aiohttp.web import HTTPForbidden
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers import device_registry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER
from .data import LisiosCoordinatorData, WasserAlarm

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import LisiosConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class LisiosDataUpdateCoordinator(DataUpdateCoordinator[LisiosCoordinatorData]):
    """Class to manage fetching data from the API."""

    config_entry: LisiosConfigEntry

    dids: set[str]

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        super().__init__(
            hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )
        dr = device_registry.async_get(self.hass)
        devices = device_registry.async_entries_for_config_entry(dr, self.config_entry.entry_id)
        self.dids = {x.serial_number for x in devices if x.serial_number}

    async def _fetch_wasser_alarm_data(self, uid: str) -> WasserAlarm:
        data = await self.config_entry.runtime_data.client.device_data(uid)
        return WasserAlarm(
            uid=data["id"],
            did=data["did"],
            acc_temp=data["t_acc"],
            amb_temp=data["t_a"],
            pipe_temp_mean=data["t_p1_2_3_mean"],
            is_flow=data["f_f_accu"] != 0,
            is_frozen=data["f_fr_acc"] != 0,
            is_leakage=data["f_l_accu"] != 0,
        )

    async def _async_update_data(self) -> LisiosCoordinatorData:
        """Update data from Lisios API."""
        try:
            me = await self.config_entry.runtime_data.client.me()
            devices = [self._fetch_wasser_alarm_data(device["id"]) for device in me["devices"]]
            devices = await asyncio.gather(*devices)
            devices = {device.did: device for device in devices}

            # Remove devices that are not in the API response
            dr = device_registry.async_get(self.hass)
            for did in self.dids:
                if did not in devices:
                    device = dr.async_get_device(identifiers={(DOMAIN, did)})
                    if device:
                        dr.async_update_device(
                            device_id=device.id,
                            remove_config_entry_id=self.config_entry.entry_id,
                        )

            self.dids = set(devices.keys())

            return LisiosCoordinatorData(
                devices=devices,
            )
        except ClientError as ex:
            LOGGER.exception("Failed to fetch data from Lisios API")
            if isinstance(ex, HTTPForbidden):
                raise ConfigEntryAuthFailed from ex
            raise UpdateFailed from ex
