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


__all__ = [
    "PWPYException",
    "TokenNotGiven",
    "InvalidToken",
    "InvalidQuery",
    "UnexpectedResponse",
    "LoginFailure"
]


class PWPYException(Exception):
    """
    Base for all exceptions raised by this package.
    """


class TokenNotGiven(PWPYException):
    """
    Exception raised when no API key global or local is provided.
    """


class InvalidToken(PWPYException):
    """
    Exception raised when the provided API key is invalid.
    """


class InvalidQuery(PWPYException):
    """
    Exception raised when the GraphQL query is invalid.
    """


class UnexpectedResponse(PWPYException):
    """
    Exception raised when the GraphQL response is unexpected.
    """

    def __init__(self, response: str) -> None:
        self.response = response


class LoginFailure(PWPYException):
    """
    Exception raised when the provided login credentials are invalid.
    """