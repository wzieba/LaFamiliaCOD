import asyncio

import callofduty
from callofduty import Mode, Platform, Title
from flask import Flask, render_template

from cod_stats import best_weekly_player

app = Flask(__name__)

CIKOD_PLAYERS = [
    ("tuksiarz", Platform.Xbox),
    # ("Qubris", Platform.PlayStation),
    # ("gRabos123", Platform.PlayStation),
    # ("ElRuto", Platform.Xbox),
    # ("Kowalsiu", Platform.Steam),
    # ("Darion_1993", Platform.PlayStation),
]


async def get_data():
    client = await callofduty.Login("pegoleg850@cartmails.com", "LaFamilia365")

    weekly_player = None

    for player_to_platform in CIKOD_PLAYERS:
        print("Getting" + player_to_platform.__str__())
        player = await client.GetPlayer(platform=player_to_platform[1], username=player_to_platform[0])
        profile = await player.profile(Title.ModernWarfare, Mode.Warzone)

        wins = profile['lifetime']['mode']['br_all']['properties']['wins']
        kills_in_week = profile['weekly']['mode']['br_all']['properties']['kills']

        print(f"\n{player.username} wygrał {wins} razy")

        print(player.__str__())
        weekly_player = best_weekly_player.BestWeeklyPlayer(name=player.username, kills_in_week=kills_in_week)

    return weekly_player


@app.route('/')
def hello_world():
    complete = asyncio.run(get_data())

    return render_template("index.html", best_player=complete)


if __name__ == "__main__":
    app.run(debug=True)
