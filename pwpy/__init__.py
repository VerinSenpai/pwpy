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
    "api",
    "errors",
    "utils",
    "urls",
    "scrape",
    "converters",
    "get_query",
    "BulkQuery",
    "SocketMonitor",
    "Listener",
    "AttackType",
    "WarType",
    "SocialPolicy",
    "WarPolicy",
    "EconomicPolicy",
    "DomesticPolicy",
    "PostType",
    "TradeType",
    "BountyType",
    "AlliancePosition",
    "GovernmentType",
    "Award",
    "Trade",
    "BankRecord",
    "BulletinReply",
    "Bulletin",
    "BaseballPlayer",
    "BaseballGame",
    "BaseballTeam",
    "AlliancePositionInfo",
    "Bounty",
    "Treaty",
    "Treasure",
    "TaxBracket",
    "CityInfraDamage",
    "WarAttack",
    "War",
    "City",
    "Nation",
    "Alliance",
    "PWPYException",
    "QueryError",
    "ScrapeError",
    "TargetInvalid",
    "MonitorError",
    "MonitorStateError",
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
    "ModelMissingField",
    "login",
    "send_message",
    "MessageSession",
    "NATION_PAGE",
    "ALLIANCE_PAGE",
    "MESSAGE_PAGE",
    "CITY_MANAGER_PAGE",
    "WARS_PAGE",
    "score_range",
    "infra_cost",
    "land_cost",
    "city_cost",
    "sort_ongoing_wars",
    "__version__"
]


from pwpy import api
from pwpy import errors
from pwpy import utils
from pwpy import converters
from pwpy import scrape
from pwpy import urls

from pwpy.api import *
from pwpy.errors import *
from pwpy.utils import *
from pwpy.converters import *
from pwpy.scrape import *
from pwpy.urls import *


__version__ = "0.7.0"
