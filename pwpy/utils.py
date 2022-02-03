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


import typing
import math


__all__: typing.List[str] = [
    "score_range",
    "infra_cost",
    "land_cost",
    "city_cost",
    "sort_ongoing_wars"
]


def score_range(score: float) -> typing.Tuple[float, float]:
    """
    Determines the offensive score range for a given score.

    :param score: Score to determine offensive war ranges for.
    :return: Minimum attacking range and maximum attacking range, in that order.
    """
    min_score = score * 0.75
    max_score = score * 1.75
    return min_score, max_score


def infra_cost(starting: int, ending: int) -> float:
    """
    Calculate the cost to purchase or sell infrastructure.

    :param starting: A starting infrastructure amount.
    :param ending: The desired infrastructure amount.
    """
    def unit_cost(amount: int):
        return ((abs(amount - 10) ** 2.2) / 710) + 300

    difference = starting - ending
    cost = 0

    if difference < 0:
        return 150 * difference

    if difference > 100 and difference % 100 != 0:
        delta = difference % 100
        cost += (round(unit_cost(starting), 2) * delta)
        starting += delta
        difference -= delta

    for _ in range(math.floor(difference // 100)):
        cost += round(unit_cost(starting), 2) * 100
        starting += 100
        difference -= 100

    if difference:
        cost += (round(unit_cost(starting), 2) * difference)

    return cost


def land_cost(starting: int, ending: int) -> float:
    """
    Calculate the cost to purchase or sell land.

    :param starting: A starting land amount.
    :param ending: The desired land amount.
    :return: The cost to purchase or sell land.
    """
    def unit_cost(amount: int):
        return (.002 * (amount-20) * (amount-20)) + 50

    difference = ending - starting
    cost = 0

    if difference < 0:
        return 50 * difference

    if difference > 500 and difference % 500 != 0:
        delta = difference % 500
        cost += round(unit_cost(starting), 2) * delta
        starting += delta
        difference -= delta

    for _ in range(math.floor(difference // 500)):
        cost += round(unit_cost(starting), 2) * 500
        starting += 500
        difference -= 500

    if difference:
        cost += (round(unit_cost(starting), 2) * difference)

    return cost


def city_cost(city: int) -> float:
    """
    Calculate the cost to purchase a specified city.

    :param city: The city to be purchased.
    :return: The cost to purchase the specified city.
    """
    city -= 1
    return 50000 * math.pow((city - 1), 3) + 150000 * city + 75000


def sort_ongoing_wars(wars: list) -> list:
    """
    Sort a provided list of wars for ongoing wars.

    :param wars: A list of wars to be iterated through. Objects must contain "turnsleft" and "winner" keys.
    :return: A list of active wars.
    """
    return [war for war in wars if int(war["turnsleft"]) > 0 and int(war["winner"]) == 0]
