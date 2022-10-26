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


from pwpy import exceptions, urls, utils

import aiohttp
import typing


TOKEN = None


def set_token(token: str) -> None:
    """
    Sets a global token to be used when one is not provided to a method.
    """
    global TOKEN
    TOKEN = token


def _parse_errors(data: dict) -> None:
    """
    Parse return data for errors and raise accordingly.
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


def _parse_variables(variables: dict) -> list:
    """
    Parse an iterable of provided variables into string format.
    """
    parsed = []

    for section, element in variables.items():
        if isinstance(element, str):
            parsed.append(f"{section} {{{element}}}")

        elif isinstance(element, typing.Iterable):
            local = []

            for item in element:
                if isinstance(item, dict):
                    local.append(" ".join(_parse_variables(item)))

                elif isinstance(item, str):
                    local.append(item)

            parsed.append(f"{section} {{{' '.join(local)}}}")

    return parsed


def _parse_query(query: dict) -> str:
    """
    Parse a provided dictionary into a formatted gql string.
    """
    parsed_queries = []

    for name, entry in query.items():
        parsed_args = " ".join(f"{key}:{value}" for key, value in entry["args"].items())
        parsed_variables = " ".join(_parse_variables(entry["variables"]))
        parsed_queries.append(f"{name}({parsed_args}) {{{parsed_variables}}}")

    return " ".join(parsed_queries)


async def get(
    query: dict, *,
    token: str = TOKEN,
    keys: typing.Iterable[str] = None
) -> typing.Any:
    """
    Fetches a given query from the gql api using a provided api key.

    :param token: A valid Politics and War API key.
    :param query: A query dictionary object.
    :param keys: A list of keys to parse the response with.
    :return: A dictionary response from the server.
    """
    query = _parse_query(query)

    async with aiohttp.ClientSession() as session:
        async with session.post(urls.API + token, json={"query": f"{{{query}}}"}) as response:
            if not response.ok:
                raise exceptions.CloudflareInterrupt("cloudflare error encountered while trying to post query!")

            data = await response.json()

    _parse_errors(data)

    data = data["data"]
    for key in keys:
        data = data[key]

    return data


async def within_war_range(
    score: int, *,
    alliance: int = None,
    powered: bool = True,
    omit_alliance: int = None,
    token: str = TOKEN
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

    targets = await get(query, token=token, keys=("nations", "data"))

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

