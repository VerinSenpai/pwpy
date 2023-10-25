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
from pwpy import scrape, errors

import aiohttp
import pytest


@pytest.mark.asyncio
async def test_login():
    login_url = "https://politicsandwar.com/login/"

    async with aiohttp.ClientSession() as session:
        with aioresponses() as mock:
            mock.post(login_url, status=200, body="Login Successful")

            await scrape.login(session, "", "")

            mock.post(login_url, status=200, body="Login Failed")

            try:
                await scrape.login(session, "", "")

            except Exception as exc:
                assert isinstance(exc, errors.LoginInvalid)


@pytest.mark.asyncio
async def test_send_message():
    message_url = "https://politicsandwar.com/inbox/message/"
    async with aiohttp.ClientSession() as session:
        with aioresponses() as mock:
            mock.post(message_url, status=200)

            await scrape.send_message(session, "", "", "")

            mock.post(message_url, status=200, body="name does not exist")

            try:
                await scrape.send_message(session, "", "", "")

            except Exception as exc:
                assert isinstance(exc, errors.TargetInvalid)

            mock.post(message_url, status=200, body="must be logged in")

            try:
                await scrape.send_message(session, "", "", "")

            except Exception as exc:
                assert isinstance(exc, errors.LoginInvalid)
