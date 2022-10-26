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


from pwpy import exceptions

import aiohttp
import typing
import asyncio


__all__: typing.List[str] = [
    "TOKEN",
    "NATION",
    "ALLIANCE",
    "MESSAGE",
    "API",
    "LOGIN",
    "set_token",
    "fetch_query",
]


TOKEN: str = ""
NATION: str = "https://politicsandwar.com/nation/id="
ALLIANCE: str = "https://politicsandwar.com/alliance/id="
MESSAGE: str = "https://politicsandwar.com/inbox/message/receiver="
API: str = f"https://api.politicsandwar.com/graphql?api_key="
LOGIN: str = "https://politicsandwar.com/login/"


def set_token(token: str) -> None:
    """
    Set a global token.
    """
    global TOKEN
    TOKEN = token


def _parse_errors(data) -> None:
    """
    Parse data for errors, raising the first one encountered.
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


def _parse_query(query: dict) -> str:
    """
    Parse a provided dictionary and return a gql query string.
    """
    def parse_variables(variables) -> list:
        parsed = []

        for section, element in variables.items():
            if isinstance(element, str):
                parsed.append(f"{section} {{{element}}}")

            elif isinstance(element, typing.Iterable):
                local = []

                for item in element:
                    if isinstance(item, dict):
                        local.append(" ".join(parse_variables(item)))

                    elif isinstance(item, str):
                        local.append(item)

                parsed.append(f"{section} {{" + " ".join(local) + "}")

        return parsed

    parsed_queries = []

    for name, entry in query.items():
        parsed_args = ", ".join(f"{key}:{value}" for key, value in entry["args"].items())
        parsed_variables = " ".join(parse_variables(entry["variables"]))
        parsed_queries.append(f"{name}({parsed_args}) {{{parsed_variables}}}")

    return " ".join(parsed_queries)


async def fetch_query(
    query: dict, *,
    token: typing.Optional[str] = None,
    keys: typing.Iterable = None
) -> typing.Any:
    """
    Fetches a given query from the gql api using a provided api key.

    :param token: A valid Politics and War API key.
    :param query: A query dictionary object.
    :param keys: A list of keys to parse the response with.
    :return: A dictionary response from the server.
    """
    token = token or TOKEN

    if not token:
        raise exceptions.NoTokenProvided("no api key was passed for this query call!")

    query = _parse_query(query)

    async with aiohttp.ClientSession() as session:
        async with session.post(API + token, json={"query": f"{{{query}}}"}) as response:
            if not response.ok:
                raise exceptions.CloudflareInterrupt("cloudflare error encountered while trying to post query!")

            data = await response.json()

    _parse_errors(data)

    data = data["data"]
    for key in keys:
        data = data[key]

    return data


class BulkQuery:

    __slots__: typing.List = [
        "_page_groups",
        "_queries",
    ]

    def __init__(self):
        self._queries: list = []

    @staticmethod
    def _chunk_requests(iterable: typing.Sized, length):
        for count in range(0, len(iterable), length):
            chunk = {}

            for entry in iterable[count:count + length]:
                chunk.update(entry)

            yield chunk

    def insert(self, query: dict) -> None:
        self._queries.append(query)

    async def fetch_query(self, *, token: str = None, chunk_size: int = 10) -> dict:
        results = {}

        chunk_size = chunk_size if chunk_size > 0 else 1
        chunks = self._chunk_requests(self._queries, chunk_size)
        tasks = set()

        for chunk in chunks:
            tasks.add(asyncio.create_task(fetch_query(chunk, token=token)))

        response = await asyncio.gather(*tasks)

        for chunk in response:
            results.update(chunk)

        return results
