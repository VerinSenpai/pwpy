# This is part of Requiem
# Copyright (C) 2020  Verin Senpai

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


from typing import Optional, Iterable


class City:

    def __init__(self, data: dict) -> None:
        self.infra: float | None = data.get("infrastructure")
        self.land: float | None = data.get("land")


class Alliance:

    def __init__(self, data: dict) -> None:
        self.name: str | None = data.get("name")
        self.id: int | None = data.get("id")


class Nation:

    def __init__(self, data: dict) -> None:
        self.nation_name: Optional[str] = data.get("nation_name")
        self.leader_name: Optional[str] = data.get("leader_name")
        self.id: Optional[int] = data.get("id")
        alliance: Optional[dict] = data.get("alliance")
        self.alliance: Optional[Alliance] = Alliance(alliance) if alliance else None
        cities: Optional[Iterable] = data.get("cities")
        self.cities: Optional[Iterable] = [City(city) for city in cities] if cities is not None else None
        self.num_cities: Optional[int] = data.get("num_cities") or len(self.cities) if self.cities else None
        color: Optional[str] = data.get("color")
        self.color: Optional[str] = color.title() if color else None
        war_policy: Optional[str] = data.get("war_policy")
        self.war_policy: Optional[str] = war_policy.title().replace("_", " ") if war_policy else None
        domestic_policy: Optional[str] = data.get("domestic_policy")
        self.domestic_policy: Optional[str] = domestic_policy.title().replace("_", " ") if domestic_policy else None
        self.population: Optional[int] = data.get("population")
        self.score: Optional[float] = data.get("score")
        self.soldiers: Optional[int] = data.get("soldiers")
        self.tanks: Optional[int] = data.get("tanks")
        self.aircraft: Optional[int] = data.get("aircraft")
        self.ships: Optional[int] = data.get("ships")
        self.missiles: Optional[int] = data.get("missiles")
        self.nukes: Optional[int] = data.get("nukes")
        self.flag: Optional[str] = data.get("flag")
