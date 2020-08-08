from dataclasses import dataclass


@dataclass
class BestWeeklyPlayer:
    name: str
    kills_in_week: int
    kills_per_game: float
    damage_given_in_week: int


@dataclass
class BestKarPlayer:
    name: str
    kills: int
    ratio: float
    headshots: int


@dataclass
class BestWeeklyGulagPlayer:
    name: str
    kills: int
    deaths: int


@dataclass
class FastestPlayer:
    name: str
    score_per_minute: float
    distance_traveled: float
    score_total: float


@dataclass
class PlayerWeekly:
    name: str
    damage_given_in_week: int
    headshots_in_week: int


@dataclass
class Report:
    best_weekly_player: BestWeeklyPlayer
    best_kar_player: BestKarPlayer
    best_weekly_gulag_player: BestWeeklyGulagPlayer
    fastest_player: FastestPlayer
    players_weekly: list
