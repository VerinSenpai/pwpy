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

import typing
import aiohttp
import asyncio
import time


def _ratelimit(func):
    remaining: int = 0
    reset: int = 0

    async def wrapper(*args, **kwargs):
        nonlocal remaining
        nonlocal reset

        if remaining == 0:
            await asyncio.sleep(reset - time.time())

        try:
            result: dict = await func(*args, **kwargs)

        except exceptions.RateLimitHit as exc:
            remaining = int(exc.headers["X-RateLimit-Remaining"])
            reset = int(exc.headers["X-RateLimit-Reset"])
            result: dict = await wrapper(*args, **kwargs)

        return result

    return wrapper


def _convert_args_to_string(args: dict) -> typing.Generator:
    """Converts dict of args to string."""
    for key, value in args.items():
        if isinstance(value, str):
            yield f'{key}:"{value}"'

        else:
            yield f'{key}:{value}'


def _convert_sequence_to_string(field_data: typing.Sequence) -> typing.Generator:
    """Converts tuples/lists into strings."""
    for field in field_data:
        if isinstance(field, dict):
            yield ' '.join(_convert_fields_to_string(field))

        elif isinstance(field, str):
            yield field


def _convert_fields_to_string(data: typing.Union[str, dict, typing.Sequence]) -> typing.Generator:
    """Converts the data fields into a string."""
    if isinstance(data, dict):
        for field_name, field_value in data.items():
            if isinstance(field_value, str):
                yield f"{field_name}{{{field_value}}}"

            elif isinstance(field_value, typing.Sequence):
                converted_fields: str = ' '.join(_convert_sequence_to_string(field_value))
                yield f"{field_name}{{{converted_fields}}}"

    elif isinstance(data, typing.Sequence):
        yield ' '.join(_convert_sequence_to_string(data))

    else:
        yield f"data{{{data}}}"


def _convert_dict_to_query(query_data: typing.Union[str, dict]) -> str:
    """
    Convert a properly formatted dict into a graphql string.

    :param query_data: A properly formatted GQL string or a dict that can be converted into a GQL string.
    :return: A converted GQL string or the provided query string.
    """
    if isinstance(query_data, str):
        return query_data

    converted_query: str = f"{query_data['field']}"

    if query_args := query_data.get("args"):
        converted_args: str = ' '.join(_convert_args_to_string(query_args))
        converted_query += f"({converted_args})"

    if query_fields := query_data.get("data"):
        converted_fields: str = ' '.join(_convert_fields_to_string(query_fields))
        converted_query += f"{{{converted_fields}}}"

    return converted_query


def _raise_message_exception(errors: list) -> None:
    message: str = errors[0]["message"]

    if "cannot query field" in message:
        raise exceptions.QueryFieldError(message)

    elif "must have a sub selection" in message:
        raise exceptions.QueryMissingSubSelection(message)

    elif "syntax error" in message:
        raise exceptions.QuerySyntaxError(message)

    elif "unknown argument" in message:
        raise exceptions.QueryArgumentInvalid(message)

    else:
        raise exceptions.UnexpectedResponse(message)


def _raise_status_exception(status, headers) -> None:
    if status in (520, 521, 522):
        raise exceptions.CloudflareError(status)

    elif status == 401:
        raise exceptions.QueryKeyError("you specified an invalid api_key.")

    elif status == 503:
        raise exceptions.ServiceUnavailable()

    elif status == 429:
        raise exceptions.RateLimitHit(headers)


@_ratelimit
async def get_query(query: typing.Union[str, dict], api_key: str) -> dict:
    """
    Post a GQL query, parsing for errors and returning the data.

    :param query: A properly formatted GQL string or a dict that can be converted into a GQL string.
    :param api_key: A valid Politics And War API key.
    :return: API response data.
    """
    payload: dict = {"api_key": api_key, "query": f"{{{_convert_dict_to_query(query)}}}"}

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.politicsandwar.com/graphql", json=payload) as response:
            _raise_status_exception(response.status, response.headers)
            response_data: dict = await response.json()

    if errors := response_data.get("errors"):
        _raise_message_exception(errors)

    elif data := response_data.get("data"):
        return data

    else:
        raise exceptions.ResponseFormatError(str(response_data))


class BulkQuery:
    """
    Build and request chunks of multiple queries.
    """
    def __init__(self, api_key: str, *, payloads: typing.Optional[list] = None, chunk_size: int = 10):
        """
        :param api_key: A valid Politics And War API key.
        :param payloads: A list of dicts which can be converted to GQL strings.
        :param chunk_size: The number of queries to send in each payload.
        """
        self._api_key: str = api_key
        self._payloads: list = payloads or []
        self._chunk_size: int = chunk_size

    @property
    def _chunk_requests(self) -> typing.Generator:
        """
        Splits the queries into chunks.

        :return: Groups of joined GQL query strings.
        """
        payloads: list = self._payloads
        chunk_size: int = self._chunk_size

        for count in range(0, len(payloads), chunk_size):
            chunk: list[str] = []

            for payload in payloads[count:count + chunk_size]:
                chunk.append(_convert_dict_to_query(payload))

            yield "\n".join(chunk)

    def insert(self, query: dict or str) -> None:
        """
        Attach a query to the bulk query request.

        :param query: A properly formatted GQL string or a dict that can be converted into a GQL string.
        """
        self._payloads.append(query)

    async def get(self) -> dict:
        """
        Post the bulk GQL query, parsing for errors and returning the data.

        :return: A dict containing all returned API response data.
        """
        results: dict = {}
        tasks: set = set()

        async with asyncio.TaskGroup() as tg:
            for chunk in self._chunk_requests:
                tasks.add(tg.create_task(get_query(chunk, self._api_key)))

        for task in tasks:
            results.update(task.result())

        return results
