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


from pwpy import urls, utils, exceptions

import asyncio
import aiohttp
import typing


__all__ = [
    "set_token",
    "fetch_query",
    "BulkQuery"
]


TOKEN = None


def set_token(token: str) -> None:
    """
    Set a package level api key to be used for all queries where no key is provided.
    """
    global TOKEN
    TOKEN = token


async def fetch_query(query: dict or str, *, token: str = TOKEN) -> typing.Any:
    """
    Fetches a given query from the gql api using a provided api key.

    :param query: A query formatted as a dict.
    :param token: A valid Politics and War API key.
    :return: A dictionary response from the server.
    """
    if not token:
        raise exceptions.TokenNotGiven("an api key was not provided for this request!")

    if isinstance(query, dict):
        query = utils.parse_query(query)

    async with aiohttp.ClientSession() as session:
        async with session.post(urls.API + token, json={"query": f"{{{query}}}"}) as response:
            response = await response.json()

    utils.parse_errors(response)

    return response["data"]


class BulkQuery:

    __slots__: typing.List = [
        "_queries"
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

    async def fetch_query(self, *, token: str = TOKEN, chunk_size: int = 10) -> dict:
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
