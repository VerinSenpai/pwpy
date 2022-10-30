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


from pwpy import api, utils


__all__ = [
    "within_war_range",
    "nations_pages",
    "nation_details",
    "nation_bank_contents",
    "alliances_pages",
    "alliance_details",
    "alliance_bank_contents"
]


async def within_war_range(
    score: int, *,
    alliance: int = None,
    powered: bool = True,
    omit_alliance: int = None,
    token: str = api.TOKEN
) -> list:
    """
    Lookup all targets for a given score meeting optional criteria.

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

    if alliance:
        query["nations"]["args"]["alliance_id"] = alliance

    response = await api.fetch_query(query, token=token)
    targets = response["nations"]["data"]

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


async def nations_pages(*, token: str = api.TOKEN) -> dict:
    query = {
        "nations": {
            "args": {"first": 500},
            "variables": {
                "paginatorInfo": {
                    "lastPage"
                }
            }
        }
    }

    response = await api.fetch_query(query, token=token)
    return response["nations"]["paginatorInfo"]["lastPage"]


async def nation_details(nation: int, *, token: str = api.TOKEN) -> dict:
    query = {
        "nations": {
            "args": {"id": nation, "first": 1},
            "variables": {
                "data": {
                    "id",
                    "nation_name",
                    "leader_name",
                    "alliance_id",
                    "alliance_position",
                    "alliance_position_info",
                    "alliance",
                    "continent",
                    "war_policy",
                    "domestic_policy",
                    "color",
                    "num_cities",
                    "score",
                    "update_tz",
                    "population",
                    "flag",
                    "vacation_mode_turns",
                    "beige_turns",
                    "espionage_available",
                    "last_active",
                    "date",
                    "soldiers",
                    "tanks",
                    "aircraft",
                    "missiles",
                    "nukes",
                    "discord",
                    "discord_id",
                    "turns_since_last_city",
                    "turns_since_last_project",
                    "projects",
                    "project_bits",
                    "iron_works",
                    "bauxite_works",
                    "arms_stockpile",
                    "emergency_gasoline_reserve",
                    "mass_irrigation",
                    "international_trade_center",
                    "missile_launch_pad",
                    "nuclear_research_facility",
                    "iron_dome",
                    "vital_defense_system",
                    "central_intelligence_agency",
                    "center_for_civil_engineering",
                    "propaganda_bureau",
                    "uranium_enrichment_program",
                    "urban_planning",
                    "advanced_urban_planning",
                    "space_program",
                    "spy_satellite",
                    "moon_landing",
                    "pirate_economy",
                    "recycling_initiative",
                    "telecommunications_satellite",
                    "green_technologies",
                    "arable_land_agency",
                    "clinical_research_center",
                    "specialized_police_training_program",
                    "advanced_engineering_corps",
                    "government_support_agency",
                    "research_and_development_center",
                    "resource_production_center",
                    "metropolitan_planning",
                    "military_salvage",
                    "fallout_shelter",
                    "wars_won",
                    "wars_lost",
                    "tax_id",
                    "alliance_seniority",
                    "gross_national_income",
                    "gross_domestic_product",
                    "soldier_casualties",
                    "soldier_kills",
                    "tank_casualties",
                    "tank_kills",
                    "aircraft_casualties",
                    "aircraft_kills",
                    "ship_casualties",
                    "ship_kills",
                    "missile_casualties",
                    "missile_kills",
                    "nuke_casualties",
                    "nuke_kills",
                    "money_looted",
                    "vip"
                }
            }
        }
    }

    response = await api.fetch_query(query, token=token)
    return response["nations"]["data"]


async def nation_military(nation: int, *, token: str = api.TOKEN) -> dict:
    raise NotImplementedError


async def nation_discord(nation: int, *, token: str = api.TOKEN) -> dict:
    raise NotImplementedError


async def nation_bank_contents(nation: int, *, token: str = api.TOKEN) -> dict:
    query = {
        "nations": {
            "args": {"id": nation, "first": 1},
            "variables": {
                "data": {
                    "money",
                    "coal",
                    "uranium",
                    "iron",
                    "bauxite",
                    "steel",
                    "gasoline",
                    "munitions",
                    "oil",
                    "food",
                    "aluminum"
                }
            }
        }
    }

    response = await api.fetch_query(query, token=token)
    return response["nations"]["data"]


async def alliances_pages(*, token: str = api.TOKEN) -> dict:
    query = {
        "nations": {
            "args": {"first": 500},
            "variables": {
                "paginatorInfo": {
                    "lastPage"
                }
            }
        }
    }

    response = await api.fetch_query(query, token=token)
    return response["alliances"]["paginatorInfo"]["lastPage"]


async def alliance_details(alliance: int, *, token: str = api.TOKEN) -> dict:
    query = {
        "alliances": {
            "args": {"id": alliance, "first": 1},
            "variables": {
                "data": {
                    "id",
                    "name",
                    "acronym",
                    "score",
                    "color",
                    "date",
                    "average_score",
                    "accept_members",
                    "discord_link",
                    "forum_link",
                    "wiki_link",
                    "flag"
                }
            }
        }
    }

    response = await api.fetch_query(query, token=token)
    return response["alliances"]["data"]


async def alliance_military(alliance: int, *, token: str = api.TOKEN) -> dict:
    raise NotImplementedError


async def alliance_discord(alliance: int, *, token: str = api.TOKEN) -> dict:
    raise NotImplementedError


async def alliance_bank_contents(alliance: int, *, token: str = api.TOKEN) -> dict:
    query = {
        "alliances": {
            "args": {"id": alliance, "first": 1},
            "variables": {
                "data": {
                    "money",
                    "coal",
                    "uranium",
                    "iron",
                    "bauxite",
                    "steel",
                    "gasoline",
                    "munitions",
                    "oil",
                    "food",
                    "aluminum"
                }
            }
        }
    }

    response = await api.fetch_query(query, token=token)
    return response["alliances"]["data"]
