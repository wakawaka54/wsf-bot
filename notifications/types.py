import dataclasses

from client.types import FerryScheduleEntry, FerrySchedule


@dataclasses.dataclass
class FoundAvailableNotification:
    schedule: FerrySchedule
