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


def infra_cost(starting: int, target: int) -> float:
    """
    Calculate the cost to purchase or sell infrastructure.

    :param starting: A starting infrastructure amount.
    :param target: The desired infrastructure amount.
    """
    def unit_cost(amount: int):
        return ((abs(amount - 10) ** 2.2) / 710) + 300

    difference = target - starting
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


def land_cost(starting: int, target: int) -> float:
    """
    Calculate the cost to purchase or sell land.

    :param starting: A starting land amount.
    :param target: The desired land amount.
    :return: The cost to purchase or sell land.
    """
    def unit_cost(amount: int):
        return (.002 * (amount-20) * (amount-20)) + 50

    difference = target - starting
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

    :param wars: A list of wars to be iterated through. Objects must contain "turns_left" and "winner" keys.
    :return: A list of active wars.
    """
    return [war for war in wars if int(war["turns_left"]) > 0 and int(war["winner"]) == 0]
