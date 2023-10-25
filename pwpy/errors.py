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
    "QueryError",
    "ScrapeError",
    "TargetInvalid",
    "WatcherError",
    "WatcherStateError",
    "SubscribeFailed",
    "AuthorizeFailed",
    "QuerySyntaxError",
    "QueryFieldError",
    "QueryArgumentInvalid",
    "QueryKeyError",
    "QueryMissingSubSelection",
    "RateLimitHit",
    "ServiceUnavailable",
    "UnexpectedResponse",
    "ResponseFormatError",
    "CloudflareError",
    "LoginInvalid",
]


class PWPYException(Exception):
    """
    Exception class to be inherited by all PWPY exceptions.
    """


class QueryError(PWPYException):
    """
    Overarching class for all Query exceptions.
    """


class QuerySyntaxError(QueryError):
    """
    Exception raised when the GraphQL query is invalid.
    """


class QueryFieldError(QueryError):
    """
    Exception raised when attempting to query an invalid field or when a field is used incorrectly.
    """


class QueryArgumentInvalid(QueryError):
    """
    Exception raised when attempting to pass an invalid argument with a query.
    """


class QueryKeyError(QueryError):
    """
    Exception raised when the provided api key provided is invalid.
    """


class QueryMissingSubSelection(QueryError):
    """
    Exception raised when the provided query has a field that is missing a sub selection.
    """


class ServiceUnavailable(QueryError):
    """
    Exception raised when code 503 is returned. Note that this exception will be raised
    if you send a large number of individual requests all at once. In this instance, try
    slowing down.
    """


class RateLimitHit(QueryError):
    """
    Exception raised when the rate limit is hit. This exception should be caught and handled
    by the rate limit script.
    """

    def __init__(self, headers) -> None:
        self.headers = headers


class UnexpectedResponse(QueryError):
    """
    Exception raised when the error message received has no handle.
    """

    def __init__(self, response: str) -> None:
        self.response: str = response


class ResponseFormatError(QueryError):
    """
    Exception raised when the response returned does not match any expected pattern.
    """

    def __init__(self, response: str) -> None:
        self.response: str = response


class CloudflareError(PWPYException):
    """
    Exception raised when Cloudflare interrupts the connection.
    """

    def __init__(self, status: int) -> None:
        self.status: int = status


class ScrapeError(PWPYException):
    """
    Overarching class for all Scraping exceptions.
    """


class LoginInvalid(ScrapeError):
    """
    Exception raised when the login credentials provided for a scrape were invalid.
    """


class TargetInvalid(ScrapeError):
    """
    Exception raised when the provided target for a message send request is invalid.
    """


class WatcherError(PWPYException):
    """
    Overarching class for all Watcher exceptions.
    """


class WatcherStateError(WatcherError):
    """
    Exception raised when an action is carried out during an incorrect state.
    """


class SubscribeFailed(WatcherError):
    """
    Exception raised when a subscribe attempt fails.
    """


class AuthorizeFailed(WatcherError):
    """
    Exception raised when an attempted authorize request fails.
    """