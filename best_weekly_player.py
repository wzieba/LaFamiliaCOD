from dataclasses import dataclass


@dataclass
class BestWeeklyPlayer:
    name: str
    kills_in_week: int
