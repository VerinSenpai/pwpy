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


from pwpy import utils, exceptions


def test_parse_errors():
    example = {"errors": [{"message": "should raise InvalidAPIKey <invalid api_key>"}]}
    try:
        utils.parse_errors(example)
    except Exception as exc:
        assert isinstance(exc, exceptions.InvalidToken)

    example = [{"errors": [{"message": "should raise InvalidQuery <Syntax Error>"}]}]
    try:
        utils.parse_errors(example)
    except Exception as exc:
        assert isinstance(exc, exceptions.InvalidQuery)

    example = {"errors": [{"message": "should raise UnexpectedResponse <>"}]}
    try:
        utils.parse_errors(example)
    except Exception as exc:
        assert isinstance(exc, exceptions.UnexpectedResponse)

    example = "should raise UnexpectedResponse"
    try:
        utils.parse_errors(example)
    except Exception as exc:
        assert isinstance(exc, exceptions.UnexpectedResponse)

    example = {"data": "should raise no errors"}
    utils.parse_errors(example)


def test_parse_query():
    example = {
        "nations": {
            "args": {"id": 34904, "first": 1},
            "variables": {
                "data": (
                    "id",
                    {"alliance": "name"}
                ),
                "paginatorInfo": "lastPage"
            }
        }
    }
    target = "nations(id:34904 first:1) {data {id alliance {name}} paginatorInfo {lastPage}}"

    query = utils.parse_query(example)
    assert query == target


def test_score_range():
    min_att, max_att = utils.score_range(1000)
    assert min_att == 750.0
    assert max_att == 1750.0
    min_att, max_att = utils.score_range(5000)
    assert min_att == 3750.0
    assert max_att == 8750.0


def test_infra_cost():
    cost = utils.infra_cost(1000, 1500)
    assert cost == 4337302.0
    cost = utils.infra_cost(2000, 3000)
    assert cost == 40932054.0


def test_land_cost():
    cost = utils.land_cost(1000, 1500)
    assert cost == 985400.0
    cost = utils.land_cost(2000, 3000)
    assert cost == 10120800.0


def test_city_cost():
    cost = utils.city_cost(15)
    assert cost == 112025000.0
    cost = utils.city_cost(30)
    assert cost == 1102025000.0


def test_sort_ongoing_wars():
    wars = [
        {"turns_left": 14, "winner": 0},
        {"turns_left": 20, "winner": 0},
        {"turns_left": 0, "winner": 100},
        {"turns_left": 3, "winner": 0},
        {"turns_left": 0, "winner": 0}
    ]
    correct = [
        {"turns_left": 14, "winner": 0},
        {"turns_left": 20, "winner": 0},
        {"turns_left": 3, "winner": 0}
    ]
    actual = utils.sort_ongoing_wars(wars)
    assert correct == actual
