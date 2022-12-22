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


from pwpy import api

import asyncio


async def key_details(api_key: str) -> dict:
    query: dict = {
        "field": "me",
        "data": (
            {"nation": "id"},
            "key",
            "requests",
            "max_requests"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response


async def game_info(api_key: str) -> dict:
    query: dict = {
        "field": "game_info",
        "data": (
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


async def nations_pages(api_key: str, length: int = 500) -> int:
    query: dict = {
        "field": "nations",
        "args": {"first": length},
        "data": {"paginatorInfo": "lastPage"}
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"]["paginatorInfo"]["lastPage"]


async def nation_identifiers(api_key: str, length: int = 500) -> list:
    bulk_query: api.BulkQuery = api.BulkQuery(api_key, chunk_size=100)
    pages: int = await nations_pages(api_key, length)

    for page in range(1, pages + 1):
        query: dict = {
            "field": f"page_{page}: nations",
            "args": {"first": length, "page": page},
            "data": {"data": ("id", "nation_name", "leader_name")}
        }
        bulk_query.insert(query)

    results = await bulk_query.get()

    return [item for key, data in results.items() for item in data["data"]]


async def nation_all(nation_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "data": (
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
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "data": (
            "id",
            "nation_name",
            "leader_name",
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_military(nation_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "data": (
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
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "data": (
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
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
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
            "food",
            "credits"
        )
    }
    response: dict = await api.get_query(query, api_key)
    return response["nations"][0]


async def nation_war_stats(nation_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "data": (
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


async def nation_wars(nation_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "nations",
        "args": {"id": nation_id},
        "data": (
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
    query: dict = {
        "field": "alliances",
        "args": {"first": length},
        "data": {"paginatorInfo": "lastPage"}
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["paginatorInfo"]["lastPage"]


async def alliance_identifiers(api_key: str, length: int = 50) -> list:
    bulk_query: api.BulkQuery = api.BulkQuery(api_key, chunk_size=100)
    pages: int = await alliances_pages(api_key, length)

    for page in range(1, pages + 1):
        query: dict = {
            "field": f"page_{page}: alliances",
            "args": {"first": length, "page": page},
            "data": {"data": ("id", "name", "acronym")}
        }
        bulk_query.insert(query)

    results = await bulk_query.get()

    return [item for key, data in results.items() for item in data["data"]]


async def alliance_all(alliance_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
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
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
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
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
            "data": (
                {
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
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_wars(alliance_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
            "data": (
                {
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
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_members_identifiers(alliance_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
            "data": (
                {
                    "nations": (
                        "id",
                        "nation_name",
                        "leader_name"
                    )
                }
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_members_vault(alliance_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
            "data": (
                {
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
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_members_military(alliance_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
            "data": (
                {
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
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_tax_brackets(alliance_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
            "data": (
                {
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
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_tax_records(alliance_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
            "data": (
                {
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
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]


async def alliance_bank_contents(alliance_id: int, api_key: str) -> dict:
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
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
    query: dict = {
        "field": "alliances",
        "args": {"id": alliance_id},
        "data": {
            "data": (
                {
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
            )
        }
    }
    response: dict = await api.get_query(query, api_key)
    return response["alliances"]["data"][0]
