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
    ...


async def nation_identify(nation_id: int, api_key: str) -> dict:
    ...


async def nation_military(nation_id: int, api_key: str) -> dict:
    ...


async def nation_projects(nation_id: int, api_key: str) -> dict:
    ...


async def nation_vault(nation_id: int, api_key: str) -> dict:
    ...


async def nation_war_stats(nation_id: int, api_key: str) -> dict:
    ...


async def nation_wars(nation_id: int, api_key: str) -> dict:
    ...


async def nation_alliance(nation_id: int, api_key: str) -> dict:
    ...


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
    ...


async def alliance_identify(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_treaties(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_wars(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_members_identifiers(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_members_vault(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_members_military(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_tax_brackets(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_tax_records(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_bank_contents(alliance_id: int, api_key: str) -> dict:
    ...


async def alliance_bank_records(alliance_id: int, api_key: str) -> dict:
    ...