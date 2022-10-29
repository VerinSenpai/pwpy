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


from aioresponses import aioresponses
from pwpy import urls, exceptions
from pwpy import api

import aiohttp
import pytest


def test_set_token():
    api.set_token("test")
    assert api.TOKEN == "test"


@pytest.mark.asyncio
async def test_fetch_query():
    test_query = {
        "nations": {
            "args": {"id": 34904, "first": 1},
            "variables": {
                "data": (
                    "id",
                    {"alliance": "name"}
                ),
                "paginatorInfo": "lastPage"
            }
        }
    }
    test_response = {
        "data": {
            "nations": {
                "data": {
                    "id": 34904,
                    "alliance": {
                        "name": "Name Withheld"
                    }
                },
                "paginatorInfo": {
                    "lastPage": 1
                }
            }
        }
    }
    token = "test"

    try:
        await api.fetch_query(test_query)

    except Exception as exc:
        assert isinstance(exc, exceptions.TokenNotGiven)

    with aioresponses() as mock:
        mock.post(urls.API + token, status=200, payload=test_response)
        response = await api.fetch_query(test_query, token=token)

    assert response == test_response["data"]
