"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
import random

from homeassistant.const import (
    ATTR_VOLTAGE,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_ILLUMINANCE,
    PERCENTAGE,
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.switch import SwitchEntity
from .const import DOMAIN
from .hub import Hub
import logging
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)

# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.
async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    hub = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for i in range(1, 33):
        new_devices.append(Switch(hub, i))
    if new_devices:
        async_add_entities(new_devices)

class Switch(CoordinatorEntity, SwitchEntity):
    def __init__(self, hub: Hub, number: int):
        super().__init__(hub.coordinator)
        self._hub = hub
        self._number = number
        self._attr_unique_id = f"{self._hub.name}_{str(self._number)}"

    @property
    def name(self):
        """Name of the entity."""
        return self._hub.name + " " + str(self._number)
    

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._hub.name)
            },
            "name": self._hub.name,
            "manufacturer": "GCE Electronics",
            "model": "IPX800v3",
            "sw_version": 3,
        }

    @property
    def is_on(self):
        _LOGGER.warning(self._hub.coordinator.data)
        if self._hub.coordinator.data is not None:
            return self._hub.coordinator.data['OUT' + str(self._number)] == 1

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        pass
    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        pass