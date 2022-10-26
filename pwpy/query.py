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


from pwpy import exceptions, urls, TOKEN

import aiohttp
import typing


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


async def get(query: dict, *, token: str = TOKEN, keys: typing.Iterable[str] = None) -> typing.Any:
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
