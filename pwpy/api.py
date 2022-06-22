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


from pwpy import exceptions, utils

import aiohttp
import typing
import asyncio


__all__: typing.List[str] = [
    "TOKEN",
    "set_token",
    "fetch_query",
    "BulkQuery",
    "within_war_range",
    "nations_pages",
    "alliances_pages",
    "alliance_details",
    "alliance_treaties",
    "alliance_members_details",
    "alliance_bank_records",
    "alliance_bank_contents"
]


TOKEN: str = ""


def set_token(token: str) -> None:
    """
    Sets a token to be used by all queries where a token is not provided.
    """
    global TOKEN
    TOKEN = token


def parse_errors(data) -> None:
    """
    Parse return data for errors, raising the first one encountered.
    """
    def interpret_errors(errors):
        message = errors[0]["message"]

        if "invalid api_key" in message:
            raise exceptions.InvalidToken(message)

        elif "Syntax Error" in message:
            raise exceptions.InvalidQuery(message)

        else:
            raise exceptions.UnexpectedResponse(message)

    if isinstance(data, dict):
        if "errors" in data.keys():
            interpret_errors(data["errors"])

        elif "data" in data.keys():
            return

    elif isinstance(data, list):
        interpret_errors(data[0]["errors"])

    raise exceptions.UnexpectedResponse(str(data))


async def fetch_query(
    query: str, *,
    token: typing.Optional[str] = None,
    keys: typing.Optional[typing.Iterable] = None
) -> typing.Any:
    """
    Fetches a given query from the gql api using a provided api key.

    :param token: A valid Politics and War API key.
    :param query: A valid query string.
    :param keys: An iterable of keys to retrieve from the response.
    :return: A dict containing the servers response.
    """
    token = token or TOKEN

    if not token:
        raise exceptions.NoTokenProvided("no api key was passed for this query call!")

    async with aiohttp.ClientSession() as session:
        async with session.post(utils.API + token, json={"query": "{" + query + "}"}) as response:
            if not response.ok:
                raise exceptions.CloudflareInterrupt("cloudflare error encountered while trying to post query!")

            data = await response.json()

    parse_errors(data)

    data = data["data"]

    if keys:
        for key in keys:
            data = data[key]

        return data

    raise exceptions.UnexpectedResponse(str(data))


class BulkQuery:

    __slots__: typing.List = [
        "_page_groups",
        "_keys",
        "_queries",
    ]

    def __init__(self):
        self._page_groups: dict = {}
        self._keys: list = []
        self._queries: list = []

    @staticmethod
    def _chunk_requests(iterable: typing.Sized, length: int):
        for count in range(0, len(iterable), length):
            yield iterable[count:count + length]

    def insert(self, query: str, page_group: str = None) -> None:
        if page_group:
            page_num, _ = self._page_groups.get(page_group)

            if page_num:
                page_num += 1
            else:
                page_num = 1

            self._page_groups[page_group] = page_num
            query = f"{page_group}_{page_num}: " + query

        self._queries.append(query)

    async def fetch_query(self, *, token: str = None, payloads: int = 10) -> None:
        results = {}

        if payloads > 0:
            chunks = self._chunk_requests(self._queries, payloads)
            tasks = set()

            for chunk in chunks:
                query = "\n".join(chunk)
                tasks.add(asyncio.create_task(fetch_query(query, token=token)))

            response = await asyncio.gather(*tasks)

            for chunk in response:
                for result in chunk:
                    results.update(result)

        else:
            query = "\n".join(self._queries)
            results = await fetch_query(query, token=token)

        for page_group, page_nums in self._page_groups.items():
            combined = list()

            for page_num in page_nums:
                page_key = f"{page_group}_{page_num}"
                combined.extend(results[page_key])
                results.pop(page_key)

            results[page_group] = combined

        return results


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

    nations = await fetch_query(query, keys=("nations", " data"))

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
    return await fetch_query(query, token=token, keys=("nations", "paginatorInfo", "lastPage"))


async def alliances_pages(*, token: str = None) -> int:
    query = """
    alliances(first: 50) {
        paginatorInfo {
            lastPage
        }
    }
    """
    return await fetch_query(query, token=token, keys=("alliances", "paginatorInfo", "lastPage"))


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
    return await fetch_query(query, token=token, keys=("alliances", "data"))


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
    return await fetch_query(query, token=token, keys=("alliances", "data"))


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
    return await fetch_query(query, token=token, keys=("alliances", "data", "bankrecs"))


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
    return await fetch_query(query, token=token, keys=("alliances", "data"))


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
    return await fetch_query(query, token=token, keys=("alliances", "data", "nations"))
