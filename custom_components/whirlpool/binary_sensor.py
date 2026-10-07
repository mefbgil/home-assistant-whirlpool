"""Binary sensors for the Whirlpool Appliances integration."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import timedelta
from typing import override

from whirlpool.appliance import Appliance
from whirlpool.awsiot.refrigerator import Refrigerator as AwsRefrigerator

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import WhirlpoolConfigEntry
from .entity import WhirlpoolEntity

PARALLEL_UPDATES = 1
SCAN_INTERVAL = timedelta(minutes=5)


@dataclass(frozen=True, kw_only=True)
class WhirlpoolBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes a Whirlpool binary sensor entity."""

    value_fn: Callable[[Appliance], bool | None]


WASHER_DRYER_SENSORS: list[WhirlpoolBinarySensorEntityDescription] = [
    WhirlpoolBinarySensorEntityDescription(
        key="door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda appliance: appliance.get_door_open(),
    )
]


REFRIGERATOR_BINARY_SENSORS: tuple[WhirlpoolBinarySensorEntityDescription, ...] = (
    WhirlpoolBinarySensorEntityDescription(
        key="refrigerator_left_door",
        translation_key="refrigerator_left_door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda refrigerator: refrigerator.get_refrigerator_left_door_open(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="refrigerator_right_door",
        translation_key="refrigerator_right_door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda refrigerator: refrigerator.get_refrigerator_right_door_open(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="freezer_door",
        translation_key="freezer_door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda refrigerator: refrigerator.get_freezer_door_open(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="pantry_door",
        translation_key="pantry_door",
        device_class=BinarySensorDeviceClass.DOOR,
        value_fn=lambda refrigerator: refrigerator.get_pantry_door_open(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="freezer_ice_maker",
        translation_key="freezer_ice_maker",
        value_fn=lambda refrigerator: refrigerator.get_freezer_ice_maker(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="icebox_ice_maker",
        translation_key="icebox_ice_maker",
        value_fn=lambda refrigerator: refrigerator.get_icebox_ice_maker(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="max_cool",
        translation_key="max_cool",
        value_fn=lambda refrigerator: refrigerator.get_max_cool(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="max_ice",
        translation_key="max_ice",
        value_fn=lambda refrigerator: refrigerator.get_max_ice(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="control_lock",
        translation_key="control_lock",
        value_fn=lambda refrigerator: refrigerator.get_control_lock(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="sabbath_mode",
        translation_key="sabbath_mode",
        value_fn=lambda refrigerator: refrigerator.get_sabbath_mode(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="quiet_mode",
        translation_key="quiet_mode",
        value_fn=lambda refrigerator: refrigerator.get_quiet_mode(),
    ),
    WhirlpoolBinarySensorEntityDescription(
        key="water_filter_overdue",
        translation_key="water_filter_overdue",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda refrigerator: refrigerator.get_water_filter_overdue(),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: WhirlpoolConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Config flow entry for Whirlpool binary sensors."""
    appliances_manager = config_entry.runtime_data

    washer_binary_sensors = [
        WhirlpoolBinarySensor(washer, description)
        for washer in appliances_manager.washers
        for description in WASHER_DRYER_SENSORS
    ]

    dryer_binary_sensors = [
        WhirlpoolBinarySensor(dryer, description)
        for dryer in appliances_manager.dryers
        for description in WASHER_DRYER_SENSORS
    ]

    refrigerator_binary_sensors = [
        WhirlpoolBinarySensor(refrigerator, description)
        for refrigerator in appliances_manager.refrigerators
        if isinstance(refrigerator, AwsRefrigerator)
        for description in REFRIGERATOR_BINARY_SENSORS
    ]

    async_add_entities(
        [
            *washer_binary_sensors,
            *dryer_binary_sensors,
            *refrigerator_binary_sensors,
        ]
    )


class WhirlpoolBinarySensor(WhirlpoolEntity, BinarySensorEntity):
    """A class for the Whirlpool binary sensors."""

    def __init__(
        self, appliance: Appliance, description: WhirlpoolBinarySensorEntityDescription
    ) -> None:
        """Initialize the washer sensor."""
        super().__init__(appliance, unique_id_suffix=f"-{description.key}")
        self.entity_description: WhirlpoolBinarySensorEntityDescription = description

    @property
    @override
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self.entity_description.value_fn(self._appliance)
