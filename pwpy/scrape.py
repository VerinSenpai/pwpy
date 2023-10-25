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


from pwpy import errors

import typing
import aiohttp


__all__: typing.List[str] = [
    "login",
    "send_message",
    "MessageSession"
]


async def login(session: aiohttp.ClientSession, email: str, password: str) -> None:
    """
    Log in to Politics and War.

    :param session: An aiohttp.ClientSession instance.
    :param email: A valid email address.
    :param password: A valid password.
    """
    login_data: dict = {"email": email, "password": password, "loginform": "Login"}
    response = await session.post("https://politicsandwar.com/login/", data=login_data)
    page_content: str = await response.text()

    if "Login Successful" not in page_content:
        raise errors.LoginInvalid("The provided login credentials were invalid!")


async def send_message(session: aiohttp.ClientSession, target: str, subject: str, message: str) -> None:
    """
    Sends a message in Politics and War using provided account information.

    :param session: An aiohttp.ClientSession instance.
    :param target: A valid target leader name.
    :param subject: A subject for the message.
    :param message: The message content.
    """
    message_data = {
        "newconversation": "true",
        "receiver": target,
        "carboncopy": "",
        "subject": subject,
        "body": message,
        "sndmsg": "Send Message",
    }

    response = await session.post("https://politicsandwar.com/inbox/message/", data=message_data)
    page_content: str = await response.text()

    if "name does not exist" in page_content:
        raise errors.TargetInvalid("The provided target name is invalid!")

    elif "must be logged in" in page_content:
        raise errors.LoginInvalid("You must be logged in to perform that action!")


class MessageSession:

    def __init__(self, email: str, password: str) -> None:
        self._email: str = email
        self._password: str = password
        self._session: typing.Optional[aiohttp.ClientSession] = None

    async def __aenter__(self) -> "MessageSession":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()

    async def send_message(self, targets: str, subject: str, message: str) -> None:
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession()

            await login(self._session, self._email, self._password)

        await send_message(self._session, targets, subject, message)
