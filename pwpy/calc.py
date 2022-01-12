# This is part of Requiem
# Copyright (C) 2020  God Empress Verin & Zak S

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


import math


def infra_cost(starting_infra: int, ending_infra: int, *, multiplier: float = 1, policy: bool = False) -> float:
    """
    Calculate the cost to purchase or sell infrastructure.

    :param starting_infra: A starting infrastructure amount.
    :param ending_infra: The desired infrastructure amount.
    :param multiplier: A multiplier to adjust the ending result by.
    :param policy: If the infra policy is being used.
    :return: The cost to purchase or sell infrastructure.
    """
    def unit_cost(amount: int):
        return ((abs(amount - 10) ** 2.2) / 710) + 300

    difference = ending_infra - starting_infra
    cost = 0

    if difference < 0:
        return 150 * difference

    if difference > 100 and difference % 100 != 0:
        delta = difference % 100
        cost += (round(unit_cost(starting_infra), 2) * delta)
        starting_infra += delta
        difference -= delta

    for _ in range(math.floor(difference // 100)):
        cost += round(unit_cost(starting_infra), 2) * 100
        starting_infra += 100
        difference -= 100

    if difference:
        cost += (round(unit_cost(starting_infra), 2) * difference)

    if policy:
        cost = cost * 0.95

    return cost * multiplier


def land_cost(starting_land: int, ending_land: int, *, multiplier: float = 1, policy: bool = False) -> float:
    """
    Calculate the cost to purchase or sell land.

    :param starting_land: A starting land amount.
    :param ending_land: The desired land amount.
    :param multiplier: A multiplier to adjust the ending result by.
    :param policy: If the land policy is being used.
    :return: The cost to purchase or sell land.
    """
    def unit_cost(amount: int):
        return (.002*(amount-20)*(amount-20))+50

    difference = ending_land - starting_land
    cost = 0

    if difference < 0:
        return 50 * difference

    if difference > 500 and difference % 500 != 0:
        delta = difference % 500
        cost += round(unit_cost(starting_land), 2) * delta
        starting_land += delta
        difference -= delta

    for _ in range(math.floor(difference // 500)):
        cost += round(unit_cost(starting_land), 2) * 500
        starting_land += 500
        difference -= 500

    if difference:
        cost += (round(unit_cost(starting_land), 2) * difference)

    if policy:
        cost = cost * 0.95

    return cost * multiplier


def city_cost(city: int, *, multiplier: float = 1, ) -> float:
    """
    Calculate the cost to purchase a specified city.

    :param city: The city to be purchased.
    :param multiplier: A multiplier to adjust the ending result by.
    :return: The cost to purchase the specified city.
    """
    if city <= 1:
        raise ValueError("The provided value cannot be less than or equal to 1.")

    city -= 1
    return (50000 * math.pow((city - 1), 3) + 150000 * city + 75000) * multiplier


def expansion_cost(current: int, end: int, infra: int, land: int, *, up: bool = False, aup: bool = False, city_policy: bool = False, infra_policy: bool = False, land_policy: bool = False):
    """
    Calculate the cost to purchase a specified city.

    :param current: The current city
    :param end: The final city to be purchased.
    :param infra: The amount of infra in city to be purchased.
    :param land: The amount of land in city to be purchased.
    :return: The cost to purchase the specified city.
    """
    diff = end - current
    if diff < 1:
        return "Incorrect start and end input"

    output = {
        "total": 0,
        "each_cost": [],
        "infra": infra_cost(10, infra, multiplier=diff, policy=infra_policy),
        "land": land_cost(250, land, multiplier=diff, policy=land_policy)
    }

    while current < end:
        current += 1
        cost = city_cost(current)

        if up:
            cost -= 50000000

        if aup:
            cost -= 150000000

        if city_policy:
            cost = cost * 0.95

        output["total"] += cost
        output["each_cost"].append(cost)

    return output