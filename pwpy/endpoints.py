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


from pwpy import client, utils

import typing


__all__: typing.List[str] = [
    "within_war_range",
    "nations_pages",
    "alliances_pages",
    "alliance_details",
    "alliance_bank_contents",
    "alliance_bank_records",
    "alliance_treaties",
    "alliance_members_details"
]


async def within_war_range(
    score: int, *,
    alliance: int = None,
    powered: bool = True,
    omit_alliance: int = None
) -> list:
    """
    Lookup all targets for a given score within an optional target alliance.

    :param score: Score to be calculated with.
    :param alliance: Target alliance to narrow the search. Defaults to 0.
    :param powered: Whether to discriminate against unpowered cities. Defaults to True.
    :param omit_alliance: An alliance to be omitted from search results.
    :return: A list of nations that fall within the provided search criteria.
    """
    min_score, max_score = utils.score_range(score)

    alliance_query = f"alliance_id: {alliance}" if alliance is not None else ""

    query = f"""
    nations(first: 100, min_score: {min_score}, max_score: {max_score}, {alliance_query}, vmode: false) {{
        data {{
            id
            nation_name
            leader_name
            color
            alliance_id
            alliance_position
            alliance {{
                name
                score
            }}
            warpolicy
            flag
            num_cities
            score
            espionage_available
            last_active
            soldiers
            tanks
            aircraft
            ships
            missiles
            nukes
            cities {{
                powered
            }}
            offensive_wars {{
                id
                winner
                turnsleft
            }}
            defensive_wars {{
                id
                winner
                turnsleft
            }}
        }}
    }}
    """

    nations = await client.fetch_query(query, keys=("nations", " data"))

    for nation in nations[::]:
        ongoing = utils.sort_ongoing_wars(nation["defensive_wars"])
        if nation["alliance_id"] == omit_alliance:
            nations.remove(nation)

        elif nation["color"] == "beige":
            nations.remove(nation)

        elif len(ongoing) == 3:
            nations.remove(nation)

        elif powered:
            for city in nation["cities"]:
                if city["powered"]:
                    continue

                nations.remove(nation)
                break

    return nations


async def nations_pages(*, token: str = None) -> int:
    query = """
    nations(first: 500) {
        paginatorInfo {
            lastPage
        }
    }
    """
    return await client.fetch_query(query, token=token, keys=("nations", "paginatorInfo", "lastPage"))


async def alliances_pages(*, token: str = None) -> int:
    query = """
    alliances(first: 50) {
        paginatorInfo {
            lastPage
        }
    }
    """
    return await client.fetch_query(query, token=token, keys=("alliances", "paginatorInfo", "lastPage"))


async def alliance_details(alliance: int, *, token: str = None) -> dict:
    query = f"""
    alliances(id:{alliance}, first:1) {{
        data{{
            name
            acronym
            score
            color
            acceptmem
            irclink
            forumlink
            flag
        }}
    }}
    """
    return await client.fetch_query(query, token=token, keys=("alliances", "data"))


async def alliance_bank_contents(alliance: int, *, token: str = None) -> dict:
    query = f"""
    alliances(id:{alliance}, first:1) {{
        data {{
            money
            coal
            uranium
            iron
            bauxite
            steel
            gasoline
            munitions
            oil
            food
            aluminum
        }}
    }}
    """
    return await client.fetch_query(query, token=token, keys=("alliances", "data"))


async def alliance_bank_records(alliance: int, *, token: str = None) -> dict:
    query = f"""
    alliances(id:{alliance}, first:1) {{
        data {{
            bankrecs {{
                id
                note
                pid
                sid
                rid
                stype
                rtype
                money
                coal
                uranium
                iron
                bauxite
                steel
                gasoline
                munitions
                oil
                food
                aluminum
            }}
        }}
    }}
    """
    return await client.fetch_query(query, token=token, keys=("alliances", "data", "bankrecs"))


async def alliance_treaties(alliance: int, *, token: str = None) -> dict:
    query = f"""
    alliances(id:{alliance}, first:1){{
        data{{
            sent_treaties {{
                id
                date
                treaty_type
                turns_left
                alliance1 {{
                    id
                }}
                alliance2 {{
                    id
                }}
            }}
            received_treaties {{
                id
                date
                treaty_type
                turns_left
                alliance1 {{
                    id
                }}
                alliance2 {{
                    id
                }}
            }}
        }}
    }}
    """
    return await client.fetch_query(query, token=token, keys=("alliances", "data"))


async def alliance_members_details(alliance: int, *, token: str = None) -> list:
    query = f"""
    alliances(id:{alliance}, first:1){{
        data{{
            nations {{
                id
                alliance_position
                nation_name
                leader_name
                score
                warpolicy
                dompolicy
                color
                num_cities
                flag
                espionage_available
                last_active
                date
                soldiers
                tanks
                aircraft
                ships
                missiles
                nukes
                treasures {{
                    name
                    bonus
                }}
                offensive_wars {{
                    turnsleft
                    winner
                }}
                defensive_wars {{
                    turnsleft
                    winner
                }}
            }}
        }}
    }}
    """
    return await client.fetch_query(query, token=token, keys=("alliances", "data", "nations"))
