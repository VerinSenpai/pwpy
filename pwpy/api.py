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


async def fetch_query(key: str, query: str, variables: dict = None) -> dict:
    """
    Fetches a given query from the gql api using a provided api key.

    :param key: A valid politics and war API key.
    :param query: A valid query string.
    :param variables: A valid query string.
    :return: A dict containing the servers response.
    """
    url = f"https://api.politicsandwar.com/graphql?api_key={key}"

    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json={"query": "{" + query + "}"})
        data = await response.json()

    if isinstance(data, list):
        for error in data[0]["errors"]:
            message = error["message"]

            if "invalid api_key" in message:
                raise exceptions.InvalidToken(message)

            elif "Syntax Error" in message:
                raise exceptions.InvalidQuery(message)

            else:
                raise exceptions.UnexpectedResponse(message)

    elif "data" in data.keys():
        return data["data"]

    else:
        raise exceptions.UnexpectedResponse(str(data))


class BulkQueryHandler:
    """
    Handles building and fetching of bulk graphql queries.
    """

    def __init__(self, key: str) -> None:
        self.key = key
        self.queries = []

    def add_query(self, query) -> None:
        """
        Adds a graphql query to the bulk request.

        :param query: A valid query string.
        :return: None
        """
        self.queries.append(query)

    async def fetch_query(self) -> dict:
        """
        Fetches all added queries in one go.

        :return: A dictionary object containing the servers response.
        """
        query = "\n".join(self.queries)
        return await fetch_query(self.key, query)


async def within_war_range(
        key: str, score: int, *, alliance: int = None, powered: bool = True, omit_alliance: int = None
) -> list:
    """
    Lookup all targets for a given score within an optional target alliance.

    :param key: Token to be used to connect to the API.
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

    response = await fetch_query(key, query)
    nations = response["nations"]["data"]

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


async def bank_info(key: str, alliance: int) -> dict:
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

    response = await fetch_query(key, query)
    return response["alliances"]["data"]


async def bank_records(key: str, alliance: int) -> dict:
    query = f"""
         alliances(id:{alliance}, first:1){{
            data{{
              bankrecs{{
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
        }}
    """

    response = await fetch_query(key, query)
    return response["alliances"]["data"]["bankrecs"]
