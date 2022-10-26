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


import typing


__all__: typing.List[str] = [
    "InvalidToken",
    "InvalidQuery",
    "UnexpectedResponse",
    "CloudflareInterrupt",
    "LoginFailure"
]


class InvalidToken(Exception):
    """
    Exception raised when the provided API key is invalid.
    """


class InvalidQuery(Exception):
    """
    Exception raised when the GraphQL query is invalid.
    """


class UnexpectedResponse(Exception):
    """
    Exception raised when the GraphQL response is unexpected.
    """

    def __init__(self, response: str) -> None:
        self.response = response


class CloudflareInterrupt(Exception):
    """
    Exception raised when response status not OK, likely due to cloudflare.
    """


class LoginFailure(Exception):
    """
    Exception raised when the provided login credentials are invalid.
    """