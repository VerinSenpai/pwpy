# MIT License
#
# Copyright (c) 2021 God Empress Verin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from pwpy import api, utils


async def key_details(api_key: str) -> dict:
    """
    Fetch information about the API key used to make this request.

    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "me",
        "return": (
            {"nation": "id"},
            "key",
            "requests",
            "max_requests"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response


async def game_info(api_key: str) -> dict:
    """
    Fetch the current game date and all radiation levels.

    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "game_info",
        "return": (
            "game_date",
            {
                "radiation": (
                    "global",
                    "north_america",
                    "south_america",
                    "europe",
                    "africa",
                    "asia",
                    "australia",
                    "antarctica"
                )
            }
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response


async def within_war_range(
    api_key: str,
    score: int, *,
    alliance: int = None,
    powered: bool = True,
    omit_alliance: int = None,
) -> list:
    """
    Lookup all targets for a given score meeting optional criteria.

    :param api_key: A valid Politics and War API key.
    :param score: Score to be calculated with.
    :param alliance: Target alliance to narrow the search. Defaults to 0.
    :param powered: Whether to discriminate against unpowered cities. Defaults to True.
    :param omit_alliance: An alliance to be omitted from search results.
    :return: A list of nations that fall within the provided search criteria.
    """
    min_score, max_score = utils.score_range(score)

    query = {
        "field": "nations",
        "args": {
            "first": 100,
            "min_scored": min_score,
            "max_score": max_score,
            "vacation_mode": False
        },
        "return": {
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

    if alliance:
        query["nations"]["args"]["alliance_id"] = alliance

    response = await api.get_query(query, api_key)
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


async def nations_pages(api_key: str, length: int = 500) -> int:
    """
    Fetch the current number of pages for the nations' endpoint.

    :param api_key: A valid Politics And War API key.
    :param length: The desired length of each page. MAX 500.
    :return: A number representing how many nations pages there are.
    """
    query: dict = {
        "field": "nations",
        "args": {"first": length},
        "return": {"paginatorInfo": "lastPage"}
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"]["paginatorInfo"]["lastPage"]


async def nation_identifiers(api_key: str, length: int = 500) -> list:
    """
    Fetch the id, name, and leader of every nation.

    :param api_key: A valid Politics And War API key.
    :param length: The desired length of each page. MAX 500.
    :return: A list of dicts containing the id, name, and leader of all nations.
    """
    bulk_query: api.BulkQuery = api.BulkQuery(api_key, chunk_size=100)
    pages: int = await nations_pages(api_key, length)

    for page in range(1, pages + 1):
        query: dict = {
            "field": f"page_{page}: nations",
            "args": {"first": length, "page": page},
            "return": {"data": ("id", "nation_name", "leader_name")}
        }
        bulk_query.insert(query)

    results = await bulk_query.get()

    return [item for key, data in results.items() for item in data["data"]]


async def nation_all(nation_id: int, api_key: str) -> dict:
    """
    Fetch all non-subfield information about a specified nation.

    :param nation_id: the id of the nation to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "return": (
            "id",
            "nation_name",
            "leader_name",
            "discord",
            "discord_id",
            "alliance_id",
            "alliance_position",
            "alliance_position_id",
            "alliance_seniority",
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
            "turns_since_last_city",
            "turns_since_last_project",
            "tax_id",
            "baseball_team",
            "gross_national_income",
            "gross_domestic_product",
            "vip"
            "soldiers",
            "tanks",
            "aircraft",
            "ships",
            "missiles",
            "nukes",
            "spies"
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
            "fallout_shelter"
            "money",
            "coal",
            "oil",
            "uranium",
            "iron",
            "bauxite",
            "lead",
            "gasoline",
            "munitions",
            "steel",
            "aluminum",
            "food",
            "credits"
            "wars_won",
            "wars_lost",
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
            "spy_casualties",
            "spy_kills",
            "spy_attacks",
            "money_looted"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_basic(nation_id: int, api_key: str) -> dict:
    """
    Fetch basic non-subfield information about a specified nation.

    :param nation_id: the id of the nation to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "return": (
            "id",
            "nation_name",
            "leader_name",
            "discord",
            "discord_id",
            "alliance_id",
            "alliance_position",
            "alliance_position_id",
            "alliance_seniority",
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
            "turns_since_last_city",
            "turns_since_last_project",
            "tax_id",
            "baseball_team",
            "gross_national_income",
            "gross_domestic_product",
            "vip"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_identify(nation_id: int, api_key: str) -> dict:
    """
    Fetch the id, name, and leader of a specified nation.

    :param nation_id: the id of the nation to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "return": (
            "id",
            "nation_name",
            "leader_name",
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_military(nation_id: int, api_key: str) -> dict:
    """
    Fetch the military of a specified nation.

    :param nation_id: the id of the nation to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "return": (
            "soldiers",
            "tanks",
            "aircraft",
            "ships",
            "missiles",
            "nukes",
            "spies"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_projects(nation_id: int, api_key: str) -> dict:
    """
    Fetch the projects of a specified nation.

    :param nation_id: the id of the nation to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "return": (
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
            "fallout_shelter"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_vault(nation_id: int, api_key: str) -> dict:
    """
    Fetch the warchest of a specified nation. You must be authorized to view this information.

    :param nation_id: the id of the nation to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "return": (
            "money",
            "coal",
            "oil",
            "uranium",
            "iron",
            "bauxite",
            "lead",
            "gasoline",
            "munitions",
            "steel",
            "aluminum",
            "food",
            "credits"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_war_stats(nation_id: int, api_key: str) -> dict:
    """
    Fetch the war stats of a specified nation.

    :param nation_id: the id of the nation to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "return": (
            "wars_won",
            "wars_lost",
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
            "spy_casualties",
            "spy_kills",
            "spy_attacks",
            "money_looted"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_wars(nation_id: int, api_key: str) -> list:
    """
    Fetch all recent and ongoing wars for a specified nation.

    :param nation_id: the id of the nation to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A list of wars.
    """
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "return": (
            "id",
            "date",
            "reason",
            "war_type",
            "ground_control",
            "air_superiority",
            "naval_blockade",
            "winner_id",
            "turns_left",
            "att_id",
            "att_alliance_id",
            "att_alliance_position",
            "def_id",
            "def_alliance_id",
            "def_alliance_position",
            "att_points",
            "def_points",
            "att_peace",
            "def_peace",
            "att_resistance",
            "def_resistance",
            "att_fortify",
            "def_fortify",
            "att_gas_used",
            "def_gas_used",
            "att_mun_used",
            "def_mun_used",
            "att_alum_used",
            "def_alum_used",
            "att_steel_used",
            "def_steel_used",
            "att_infra_destroyed",
            "def_infra_destroyed",
            "att_money_looted",
            "def_money_looted",
            "att_soldiers_killed",
            "def_soldiers_killed",
            "att_tanks_killed",
            "def_tanks_killed",
            "att_aircraft_killed",
            "def_aircraft_killed",
            "att_ships_killed",
            "def_ships_killed",
            "att_missiles_used",
            "def_missiles_used",
            "att_nukes_used",
            "def_nukes_used",
            "att_infra_destroyed_value",
            "def_infra_destroyed_value"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def alliances_pages(api_key: str, length: int = 50) -> int:
    """
    Fetch the current number of pages for the alliances' endpoint.

    :param api_key: A valid Politics And War API key.
    :param length: The desired length of each page. MAX 50.
    :return: A number representing how many alliances pages there are.
    """
    query: dict = {
        "field": "alliances",
        "args": {"first": length},
        "return": {"paginatorInfo": "lastPage"}
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["paginatorInfo"]["lastPage"]


async def alliance_identifiers(api_key: str, length: int = 50) -> list:
    """
    Fetch the id, name, and acronym of every alliance.

    :param api_key: A valid Politics And War API key.
    :param length: The desired length of each page. MAX 50.
    :return: A list of dicts containing the id, name, and leader of all nations
    """
    bulk_query: api.BulkQuery = api.BulkQuery(api_key, chunk_size=100)
    pages: int = await alliances_pages(api_key, length)

    for page in range(1, pages + 1):
        query: dict = {
            "field": f"page_{page}: alliances",
            "args": {"first": length, "page": page},
            "return": {"data": ("id", "name", "acronym")}
        }
        bulk_query.insert(query)

    results = await bulk_query.get()

    return [item for key, data in results.items() for item in data["data"]]


async def alliance_all(alliance_id: int, api_key: str) -> dict:
    """
    Fetch all non-subfield information about a specified alliance.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": (
                "id",
                "name",
                "acronym",
                "score",
                "color",
                "date",
                "average_score",
                "accept_members",
                "flag",
                "forum_link",
                "discord_link",
                "wiki_link"
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_identify(alliance_id: int, api_key: str) -> dict:
    """
    Fetch the id, name, and leader of a specified alliance.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": (
                "id",
                "name",
                "acronym"
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_treaties(alliance_id: int, api_key: str) -> dict:
    """
    Fetch the active treaties of a specified alliance.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": {
                "treaties": (
                    "id",
                    "date",
                    "treat_type",
                    "treaty_url",
                    "turns_left"
                    "alliance1_id",
                    "alliance2_id"
                )
            }
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_wars(alliance_id: int, api_key: str) -> dict:
    """
    Fetch all recent and ongoing wars for a specified alliance.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": {
                "wars": (
                    "id",
                    "date",
                    "reason",
                    "war_type",
                    "ground_control",
                    "air_superiority",
                    "naval_blockade",
                    "winner_id",
                    "turns_left",
                    "att_id",
                    "att_alliance_id",
                    "att_alliance_position",
                    "def_id",
                    "def_alliance_id",
                    "def_alliance_position",
                    "att_points",
                    "def_points",
                    "att_peace",
                    "def_peace",
                    "att_resistance",
                    "def_resistance",
                    "att_fortify",
                    "def_fortify",
                    "att_gas_used",
                    "def_gas_used",
                    "att_mun_used",
                    "def_mun_used",
                    "att_alum_used",
                    "def_alum_used",
                    "att_steel_used",
                    "def_steel_used",
                    "att_infra_destroyed",
                    "def_infra_destroyed",
                    "att_money_looted",
                    "def_money_looted",
                    "att_soldiers_killed",
                    "def_soldiers_killed",
                    "att_tanks_killed",
                    "def_tanks_killed",
                    "att_aircraft_killed",
                    "def_aircraft_killed",
                    "att_ships_killed",
                    "def_ships_killed",
                    "att_missiles_used",
                    "def_missiles_used",
                    "att_nukes_used",
                    "def_nukes_used",
                    "att_infra_destroyed_value",
                    "def_infra_destroyed_value"
                )
            }
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_members_identifiers(alliance_id: int, api_key: str) -> dict:
    """
    Fetch all ids, names, and leaders of members of a specified alliance.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": {
                "nations": (
                    "id",
                    "nation_name",
                    "leader_name"
                )
            }
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_members_vault(alliance_id: int, api_key: str) -> dict:
    """
    Fetch alliance member warchests. Must be authorized to do this normally.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": {
                "nations": (
                    "id",
                    "money",
                    "coal",
                    "oil",
                    "uranium",
                    "iron",
                    "bauxite",
                    "lead",
                    "gasoline",
                    "munitions",
                    "steel",
                    "aluminum",
                    "food",
                    "credits"
                )
            }
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_members_military(alliance_id: int, api_key: str) -> dict:
    """
    Fetch the military of all members of a specified nation.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": {
                "nations": (
                    "id",
                    "soldiers",
                    "tanks",
                    "aircraft",
                    "ships",
                    "spies",
                    "missiles",
                    "nukes"
                )
            }
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_tax_brackets(alliance_id: int, api_key: str) -> dict:
    """
    Fetch all tax brackets for a specified alliance. Must be authorized to do this normally.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": {
                "taxrecs": (
                    "id",
                    "date",
                    "sender_id",
                    "sender_type",
                    "sender",
                    "receiver_id",
                    "receiver",
                    "receiver_type",
                    "banker_id",
                    "banker",
                    "note",
                    "money",
                    "coal",
                    "oil",
                    "uranium",
                    "iron",
                    "bauxite",
                    "lead",
                    "gasoline",
                    "munitions",
                    "steel",
                    "aluminum",
                    "food",
                    "tax_id"
                )
            }
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_tax_records(alliance_id: int, api_key: str) -> dict:
    """
    Fetch all tax records for a specified alliance.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": {
                "tax_brackets": (
                    "id",
                    "alliance_id",
                    "alliance",
                    "date",
                    "date_modified",
                    "last_modifier_id",
                    "last_modifier",
                    "tax_rate",
                    "resource_tax_rate",
                    "bracket_name"
                )
            }
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_bank_contents(alliance_id: int, api_key: str) -> dict:
    """
    Fetch alliance bank contents. Must be authorized to do this normally.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": (
                "money",
                "coal",
                "oil",
                "uranium",
                "iron",
                "bauxite",
                "lead",
                "gasoline",
                "munitions",
                "steel",
                "aluminum",
                "food"
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_bank_records(alliance_id: int, api_key: str) -> dict:
    """
    Fetch alliance bank records.

    :param alliance_id: the id of the alliance to be looked up.
    :param api_key: A valid Politics And War API key.
    :return: A dict containing the requested information.
    """
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "return": {
            "data": {
                "bankrecs": (
                    "id",
                    "date",
                    "sender_id",
                    "sender_type",
                    "sender",
                    "receiver_id",
                    "receiver",
                    "receiver_type",
                    "banker_id",
                    "banker",
                    "note",
                    "money",
                    "coal",
                    "oil",
                    "uranium",
                    "iron",
                    "bauxite",
                    "lead",
                    "gasoline",
                    "munitions",
                    "steel",
                    "aluminum",
                    "food",
                    "tax_id"
                )
            }
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]
