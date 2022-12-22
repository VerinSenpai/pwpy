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


__all__: typing.List[str] = [
    "login",
    "send_message"
]


async def login(email: str, password: str, session: aiohttp.ClientSession) -> None:
    """
    Login to Politics and War.

    :param email: A valid email address for logging in with.
    :param password: A valid password for logging in with.
    :param session: A client session to login on.
    """
    login_data: dict = {"email": email, "password": password, "loginform": "Login"}

    async with session.post("https://politicsandwar.com/login/", data=login_data) as response:
        page_content: str = await response.text()

        if "Login Successful" not in page_content:
            raise exceptions.LoginInvalid("The provided login credentials were invalid!")


async def send_message(
    email: str, password: str, target: str, subject: str, message: str
) -> None:
    """
    Sends a message in Politics and War using provided account information.

    :param email: A valid email address for logging in with.
    :param password: A valid password for logging in with.
    :param target: A valid target leader name to message.
    :param subject: A subject for the message.
    :param message: The message content to be sent.
    :return: None
    """
    message_data: dict = {
        "newconversation": "true",
        "receiver": target,
        "carboncopy": "",
        "subject": subject,
        "body": message,
        "sndmsg": "Send Message",
    }

    async with aiohttp.ClientSession() as session:
        await login(email, password, session)

        async with session.post("https://politicsandwar.com/inbox/message/", data=message_data):
            pass
