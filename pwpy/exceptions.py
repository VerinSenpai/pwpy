class InvalidToken(BaseException):
    """
    Exception raised when the provided API key is invalid.
    """


class InvalidQuery(BaseException):
    """
    Exception raised when the GraphQL query is invalid.
    """


class UnexpectedResponse(BaseException):
    """
    Exception raised when the GraphQL response is unexpected.
    """

    def __init__(self, response: str) -> None:
        self.response = response


class LoginFailure(BaseException):
    """
    Exception raised when the provided login credentials are invalid.
    """