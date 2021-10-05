from pwpy import exceptions, calc

import aiohttp


async def fetch_query(key: str, query: str, variables: dict = None) -> dict:
    """
    Fetches a given query from the gql api using a provided api key.

    :param key: A valid politics and war API key.
    :param query: A valid query string.
    :param variables: A valid query string.
    :return: A dict containing the servers response.
    """
    url = f"https://api.politicsandwar.com/graphql?api_key={key}"

    async with aiohttp.ClientSession() as session:
        response = await session.post(url, json={"query": "{" + query + "}"})
        data = await response.json()

    if "errors" in data.keys():
        for error in data["errors"]:
            message = error["message"]

            if "invalid api_key" in message:
                raise exceptions.InvalidToken(message)

            elif "Syntax Error" in message:
                raise exceptions.InvalidQuery(message)

            else:
                raise exceptions.UnexpectedResponse(message)

    elif "data" in data.keys():
        return data["data"]

    else:
        raise exceptions.UnexpectedResponse(str(data))


class BulkQueryHandler:
    """
    Handles building and fetching of bulk graphql queries.
    """

    def __init__(self, key: str) -> None:
        self.key = key
        self.queries = []

    def add_query(self, query) -> None:
        """
        Adds a graphql query to the bulk request.

        :param query: A valid query string.
        :return: None
        """
        self.queries.append(query)

    async def fetch_query(self) -> dict:
        """
        Fetches all added queries in one go.

        :return: A dictionary object containing the servers response.
        """
        query = "\n".join(self.queries)
        return await fetch_query(self.key, query)
