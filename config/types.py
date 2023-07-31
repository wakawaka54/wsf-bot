from typing import TypedDict
import datetime

class ConfigRequest(TypedDict):
    terminal_from: str
    terminal_to: str
    sailing_date: str
    sailing_time_from: str
    sailing_time_to: str
    vehicle_size: str
    vehicle_height: str


class ConfigDiscord(TypedDict):
    webhook: str

class Config(TypedDict):
    interval: int
    requests: list[ConfigRequest]
    discord: ConfigDiscord


class ConfigParser:
    @staticmethod
    def time(time_str: str) -> datetime.time:
        return datetime.datetime.strptime(time_str, '%I:%M%p').time()
