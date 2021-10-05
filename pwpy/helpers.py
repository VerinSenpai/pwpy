from pwpy import calc, api


async def within_war_range(
    key: str, score: int, *, alliance: int = 0, powered: bool = True
) -> None:
    """
    Lookup all targets for a given score within an optional target alliance.

    :param key: Token to be used to connect to the API.
    :param score: Score to be calculated with.
    :param alliance: Target alliance to narrow the search. Defaults to 0.
    :param powered: Whether to discriminate against unpowered cities. Defaults to True.
    :return: A list of nations that fall within the provided search criteria.
    """
    min_score, max_score = calc.offensive_score_range(score)
    query = f"""
    nations(first: 100, min_score: {min_score}, max_score: {max_score}, alliance_id: {alliance}, vmode: false) {{
        data {{
            id
            nation_name
            leader_name
            alliance_id
            warpolicy
            num_cities
            score
            espionage_available
            last_active
            soldiers
            tanks
            aircraft
            ships
            missiles
            nukes
            cities {{
                powered
            }}
            defensive_wars {{
                id
            }}
        }}
    }}
    """
    response = await api.fetch_query(key, query)
    nations = response["nations"]["data"]

    for nation in nations:
        if len(nation["defensive_wars"]) > 3:
            nations.remove(nation)

        if not powered:
            continue

        for city in nation["cities"]:
            if city["powered"]:
                continue
            nations.remove(nation)
            break

    return nations


