"""Switch platform for the Whirlpool Appliances integration."""

from typing import override

from whirlpool.awsiot.refrigerator import Refrigerator

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import WhirlpoolConfigEntry
from .entity import WhirlpoolEntity

PARALLEL_UPDATES = 1


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: WhirlpoolConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    appliances_manager = config_entry.runtime_data
    async_add_entities(
        WhirlpoolRefrigeratorVacationMode(refrigerator)
        for refrigerator in appliances_manager.refrigerators
        if isinstance(refrigerator, Refrigerator)
    )


class WhirlpoolRefrigeratorVacationMode(WhirlpoolEntity, SwitchEntity):
    """Control refrigerator Vacation Mode."""

    _attr_translation_key = "vacation_mode"

    def __init__(self, appliance: Refrigerator) -> None:
        """Initialize the Vacation Mode switch."""
        super().__init__(appliance, unique_id_suffix="-vacation_mode")

    @override
    @property
    def is_on(self) -> bool | None:
        """Return whether Vacation Mode is enabled."""
        return self._appliance.get_vacation_mode()

    @override
    async def async_turn_on(self, **kwargs: object) -> None:
        """Enable Vacation Mode."""
        await self._appliance.set_vacation_mode(True)

    @override
    async def async_turn_off(self, **kwargs: object) -> None:
        """Disable Vacation Mode."""
        await self._appliance.set_vacation_mode(False)
