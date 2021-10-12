from pwpy import exceptions

import aiohttp


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
    login_url = "https://politicsandwar.com/login/"
    message_url = "https://politicsandwar.com/inbox/message"

    login_data = {"email": email, "password": password, "loginform": "Login"}
    message_data = {
        "newconversation": "true",
        "receiver": target,
        "carboncopy": "",
        "subject": subject,
        "body": message,
        "sndmsg": "Send Message",
    }

    async with aiohttp.ClientSession() as session:
        response = await session.post(login_url, data=login_data)

        if "Login Successful" not in str(await response.read()):
            raise exceptions.LoginFailure("The provided login credentials were invalid!")

        await session.post(message_url, data=message_data)
