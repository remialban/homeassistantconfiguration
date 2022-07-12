"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations
import httpx
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import asyncio
import random
import logging
from datetime import timedelta
from .const import *
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


class Hub:

    def __init__(self, hass: HomeAssistant, host: str, name: str) -> None:
        """Init dummy hub."""
        self.host = host
        self.hass = hass
        self.name = name
        self.coordinator = Coordinator(hass, host)

class Coordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(self, hass, host):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="My sensor",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=3),
        )
        self.host = host
        self.data = None

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        _LOGGER.warning("hello")
    
        async with httpx.AsyncClient() as client:
            response = await client.get('http://' + self.host + "/api/xdevices.json?cmd=20")
            self.data = response.json()
            return self.data

