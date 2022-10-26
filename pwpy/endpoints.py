# This is part of Requiem
# Copyright (C) 2020  God Empress Verin

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pwpy import utils, api, TOKEN


async def within_war_range(
    score: int, *,
    alliance: int = None,
    powered: bool = True,
    omit_alliance: int = None,
    token: str = TOKEN
) -> list:
    """
    Lookup all targets for a given score within an optional target alliance.

    :param score: Score to be calculated with.
    :param alliance: Target alliance to narrow the search. Defaults to 0.
    :param powered: Whether to discriminate against unpowered cities. Defaults to True.
    :param omit_alliance: An alliance to be omitted from search results.
    :param token: A valid Politics and War API key.
    :return: A list of nations that fall within the provided search criteria.
    """
    min_score, max_score = utils.score_range(score)

    query = {
        "nations": {
            "args": {
                "first": 100,
                "min_scored": min_score,
                "max_score": max_score,
                "alliance_id": alliance,
                "vacation_mode": False
            },
            "variables": {
                "data": {
                    "id",
                    "nation_name",
                    "leader_name",
                    "color",
                    "alliance_id",
                    "alliance_position",
                    {"alliance": ("name", "score")},
                    "war_policy",
                    "flag",
                    "num_cities",
                    "score",
                    "espionage_available",
                    "last_active",
                    "soldiers",
                    "tanks",
                    "aircraft",
                    "ships",
                    "missiles",
                    "nukes",
                    {"cities": "powered"},
                    {"offensive_wars": ("id", "winner", "turns_left")},
                    {"defensive_wars": ("id", "winner", "turns_left")}
                }
            }
        }
    }

    targets = await api.get(query, token=token, keys=("nations", "data"))

    for nation in targets[::]:
        ongoing = utils.sort_ongoing_wars(nation["defensive_wars"])
        if nation["alliance_id"] == omit_alliance:
            targets.remove(nation)

        elif nation["color"] == "beige":
            targets.remove(nation)

        elif len(ongoing) == 3:
            targets.remove(nation)

        elif powered:
            for city in nation["cities"]:
                if city["powered"]:
                    continue

                targets.remove(nation)
                break

    return targets
