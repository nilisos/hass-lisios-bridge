"""Config flow for Lisios integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from aiohttp import ClientConnectionError, ClientResponseError
from homeassistant.config_entries import SOURCE_REAUTH, ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_TOKEN, CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import LisiosApiClient
from .const import DOMAIN, LOGGER


class LisiosConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for Lisios integration."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            client = LisiosApiClient(session=async_get_clientsession(self.hass))
            try:
                token = await client.login(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            except ClientResponseError as exception:
                if exception.status in (400, 404):
                    LOGGER.warning("Invalid credentials", exc_info=True)
                    errors["base"] = "auth"
                else:
                    raise
            except ClientConnectionError:
                LOGGER.exception("Connection error")
                errors["base"] = "connection"
            else:
                me = await client.me()
                await self.async_set_unique_id(unique_id=me["user"]["user_id"])
                if self.source == SOURCE_REAUTH:
                    self._abort_if_unique_id_mismatch(reason="wrong_account")
                else:
                    self._abort_if_unique_id_configured()

                data = {
                    CONF_API_TOKEN: token,
                }

                if self.source == SOURCE_REAUTH:
                    return self.async_update_reload_and_abort(
                        self._get_reauth_entry(), data_updates=data
                    )
                return self.async_create_entry(title=user_input[CONF_USERNAME], data=data)

        data_schema = {
            vol.Required(
                CONF_USERNAME,
                default=(user_input or {}).get(CONF_USERNAME, vol.UNDEFINED),
            ): selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT),
            ),
            vol.Required(CONF_PASSWORD): selector.TextSelector(
                selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD),
            ),
        }
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema),
            errors=errors,
        )

    async def async_step_reauth(self, entry_data: dict[str, Any]) -> ConfigFlowResult:
        """Perform reauthentication upon an API authentication error."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm reauthentication dialog."""
        return await self.async_step_user(user_input=user_input)
