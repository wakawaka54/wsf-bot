import dataclasses
from enum import Enum

class VehicleSize(Enum):
    MOTORCYCLE = 0
    VEHICLE_UNDER_22 = 1
    VEHICLE_OVER_22 = 2

    @staticmethod
    def from_string(label: str):
        if label == 'motorcycle':
            return VehicleSize.MOTORCYCLE
        if label == 'normal':
            return VehicleSize.VEHICLE_UNDER_22
        if label == 'oversized':
            return VehicleSize.VEHICLE_OVER_22

        raise ValueError(f'Unknown vehicle size: {label}')


class VehicleHeight(Enum):
    UP_TO_7_2_TALL = 0
    FROM_7_2_TO_7_6_TALL = 1
    FROM_7_6_TO_13_TALL = 2

    @staticmethod
    def from_string(label: str):
        if label == 'normal':
            return VehicleHeight.UP_TO_7_2_TALL
        if label == 'tall':
            return VehicleHeight.FROM_7_2_TO_7_6_TALL
        if label == 'tallxl':
            return VehicleHeight.FROM_7_6_TO_13_TALL

        raise ValueError(f'Unknown vehicle height: {label}')


class FerryAvailabilityStatus(Enum):
    AVAILABLE = 0
    NOT_AVAILABLE = 1

@dataclasses.dataclass
class FerryRequest:
    terminal_from: str
    terminal_to: str
    sailing_date: str
    vehicle_size: VehicleSize
    vehicle_height: VehicleHeight

@dataclasses.dataclass
class FerryScheduleEntry:
    sailing_time: str
    available: bool
    vessel: str

@dataclasses.dataclass
class FerrySchedule:
    sailing_date: str
    terminal_from: str
    terminal_to: str
    entries: list[FerryScheduleEntry]



