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
import math


def score_range(score: float) -> typing.Tuple[float, float]:
    """
    Determines the offensive score range for a given score.

    :param score: Score to determine offensive war ranges for.
    :return: Minimum attacking range and maximum attacking range, in that order.
    """
    min_score = score * 0.75
    max_score = score * 1.75
    return min_score, max_score


def infra_cost(starting_infra: int, ending_infra: int, *, multiplier: float = 1) -> float:
    """
    Calculate the cost to purchase or sell infrastructure.

    :param starting_infra: A starting infrastructure amount.
    :param ending_infra: The desired infrastructure amount.
    :param multiplier: A multiplier to adjust the ending result by.
    :return: The cost to purchase or sell infrastructure.
    """
    def unit_cost(amount: int):
        return (math.pow(abs(amount - 10), 2.2) / 710) + 300

    difference = ending_infra - starting_infra
    cost = 0

    if difference < 0:
        return 150 * difference

    for _ in range(math.floor(difference // 100)):
        cost += round(unit_cost(starting_infra), 2) * 100
        starting_infra += 100
        difference -= 100

    if difference:
        cost += round(unit_cost(starting_infra), 2) * (difference % 100)

    return cost


def land_cost(starting_land: int, ending_land: int, *, multiplier: float = 1) -> float:
    """
    Calculate the cost to purchase or sell land.

    :param starting_land: A starting land amount.
    :param ending_land: The desired land amount.
    :param multiplier: A multiplier to adjust the ending result by.
    :return: The cost to purchase or sell land.
    """
    def unit_cost(amount: int):
        return (.002*(amount-20)*(amount-20))+50

    difference = ending_land - starting_land
    cost = 0

    if difference < 0:
        return 50 * difference

    for _ in range(math.floor(difference // 500)):
        cost += round(unit_cost(starting_land), 2) * 500
        starting_land += 500
        difference -= 500

    if difference:
        cost += round(unit_cost(starting_land), 2) * (difference % 500)

    return cost


def city_cost(city: int, *, multiplier: float = 1) -> float:
    """
    Calculate the cost to purchase a specified city.

    :param city: The city to be purchased.
    :param multiplier: A multiplier to adjust the ending result by.
    :return: The cost to purchase the specified city.
    """
    if city <= 1:
        raise ValueError("The provided value cannot be less than or equal to 1.")

    city -= 1
    return 50000 * math.pow((city - 1), 3) + 150000 * city + 75000
