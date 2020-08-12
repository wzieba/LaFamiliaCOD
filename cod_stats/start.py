import asyncio

import callofduty
import nest_asyncio
from callofduty import Mode, Platform, Title
from flask import Flask, render_template

from cod_stats import dimensions
from cod_stats.dimensions import Report, PlayerWeekly

nest_asyncio.apply()

loop = asyncio.get_event_loop()
app = Flask(__name__)

CIKOD_PLAYERS = [
    ("tuksiarz", Platform.Xbox),
    ("Qubris#2232", Platform.BattleNet),
    ("gRabos123", Platform.PlayStation),
    ("ElRuto", Platform.Xbox),
    ("Darion_1993", Platform.PlayStation),
    ("piodreq#2198", Platform.BattleNet),
    ("Kowalsiu#2928", Platform.BattleNet),
]


async def get_data() -> Report:
    client = await callofduty.Login("ceh27359@eoopy.com", "LaFamilia365")

    profiles = [
        await client.GetPlayerProfile(platform=p_to_p[1], username=p_to_p[0], title=Title.ModernWarfare,
                                      mode=Mode.Warzone)
        for p_to_p in CIKOD_PLAYERS]

    most_kills_in_week = max(profiles, key=lambda prof: prof['weekly']['all']['properties']['kills'])
    most_kar_kills_in_lifetime = max(profiles,
                                     key=lambda prof:
                                     prof['lifetime']['itemData']['weapon_marksman']['iw8_sn_kilo98']['properties'][
                                         'kills'])
    best_gulag_ratio_in_week = max(profiles, key=lambda prof: prof['weekly']['all']['properties']['gulagKills'] /
                                                              prof['weekly']['all']['properties']['gulagDeaths'])

    fastest_in_week = max(profiles, key=lambda prof: prof['weekly']['all']['properties']['scorePerMinute'])

    weekly_player = await build_weekly_player(most_kills_in_week)
    kar_player = await build_kar_player(most_kar_kills_in_lifetime)
    gulag_player = await build_gulag_player(best_gulag_ratio_in_week)
    fastest_player = await build_fastest_player(fastest_in_week)

    players_weekly = sorted(list(map(
        lambda profile: PlayerWeekly(
            name=profile['username'],
            damage_given_in_week=profile['weekly']['all']['properties']['damageDone'],
            headshots_in_week=profile['weekly']['all']['properties']['headshots']
        ),
        profiles
    )),
        key=lambda player: player.damage_given_in_week,
        reverse=True
    )

    return Report(
        best_weekly_player=weekly_player,
        best_kar_player=kar_player,
        best_weekly_gulag_player=gulag_player,
        fastest_player=fastest_player,
        players_weekly=players_weekly
    )


async def build_weekly_player(profile):
    kills_in_week = profile['weekly']['all']['properties']['kills']
    kills_per_game = profile['weekly']['all']['properties']['killsPerGame']
    damage_given_in_week = profile['weekly']['all']['properties']['damageDone']
    weekly_player = dimensions.BestWeeklyPlayer(
        name=profile['username'],
        kills_in_week=kills_in_week,
        kills_per_game=kills_per_game,
        damage_given_in_week=damage_given_in_week,
    )
    return weekly_player


async def build_kar_player(profile):
    kills = profile['lifetime']['itemData']['weapon_marksman']['iw8_sn_kilo98']['properties']['kills']
    ratio = profile['lifetime']['itemData']['weapon_marksman']['iw8_sn_kilo98']['properties']['kdRatio']
    headshots = profile['lifetime']['itemData']['weapon_marksman']['iw8_sn_kilo98']['properties']['headshots']
    kar_player = dimensions.BestKarPlayer(
        name=profile['username'],
        kills=kills,
        ratio=ratio,
        headshots=headshots,
    )
    return kar_player


async def build_gulag_player(profile):
    kills = profile['weekly']['all']['properties']['gulagKills']
    deaths = profile['weekly']['all']['properties']['gulagDeaths']
    gulag_player = dimensions.BestWeeklyGulagPlayer(
        name=profile['username'],
        kills=kills,
        deaths=deaths,
    )
    return gulag_player


async def build_fastest_player(profile):
    score_per_minute = profile['weekly']['all']['properties']['scorePerMinute']
    distance_traveled = profile['weekly']['all']['properties']['distanceTraveled']
    score_total = profile['lifetime']['all']['properties']['score']
    fastest_player = dimensions.FastestPlayer(
        name=profile['username'],
        score_per_minute=score_per_minute,
        distance_traveled=distance_traveled,
        score_total=score_total
    )
    return fastest_player


@app.route('/')
def hello_world():
    report_complete = loop.run_until_complete(get_data())

    return render_template("index.html", report=report_complete)


if __name__ == "__main__":
    app.run(debug=True)
