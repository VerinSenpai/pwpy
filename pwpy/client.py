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


from pwpy import exceptions, links


import aiohttp
import typing
import asyncio


__all__: typing.List[str] = [
    "TOKEN",
    "set_token",
    "fetch_query",
    "BulkQuery"
]


TOKEN: str = ""


def set_token(token: str) -> None:
    """
    Sets a token to be used by all queries where a token is not provided.
    """
    global TOKEN
    TOKEN = token


def process_errors(errors: list) -> None:
    """
    Parse the first error in a list of errors and raise an exception accordingly.
    """
    message = errors[0]["message"]

    if "invalid api_key" in message:
        raise exceptions.InvalidToken(message)

    elif "Syntax Error" in message:
        raise exceptions.InvalidQuery(message)

    else:
        raise exceptions.UnexpectedResponse(message)


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
        async with session.post(links.API + token, json={"query": "{" + query + "}"}) as response:
            if not response.ok:
                raise exceptions.CloudflareInterrupt("cloudflare error encountered while trying to post query!")

            data = await response.json()

    if isinstance(data, dict):
        if isinstance(data, list):
            process_errors(data[0]["errors"])

        elif "errors" in data.keys():
            process_errors(data["errors"])

        elif "data" in data.keys():
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
        "_chunk_requests",
        "insert",
        "fetch_query"
    ]

    def __init__(self):
        self._page_groups: dict = {}
        self._keys: list = []
        self._queries: list = []

    @staticmethod
    def _chunk_requests(iterable: typing.Sized, length: int) -> typing.Generator[typing.Any]:
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


