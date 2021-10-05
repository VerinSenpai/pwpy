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

    :param score: Score to determine offensive war ranges for.
    :return: Minimum attacking range and maximum attacking range, in that order.
    """
    def unit_cost(amount: int):
        return (math.pow(abs(amount - 10), 2.2) / 710) + 300

    difference = ending_infra - starting_infra
    cost = 0

    for _ in range(math.floor(difference // 100)):
        cost += round(unit_cost(starting_infra), 2) * 100
        starting_infra += 100
        difference -= 100

    cost += round(unit_cost(starting_infra), 2) * (difference % 100)



    return cost
