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


from cattr import global_converter
from typing import Any, List
from pwpy import urls, errors
from enum import Enum

import typing
import attr


class _Base:

    @classmethod
    def convert(cls, data: dict) -> typing.Any:
        return global_converter.structure(data, cls)


@attr.s(auto_attribs=True)
class SocialPolicy(Enum):
    ANARCHIST = "ANARCHIST"
    LIBERTARIAN = "LIBERTARIAN"
    LIBERAL = "LIBERAL"
    MODERATE = "MODERATE"
    CONSERVATIVE = "CONSERVATIVE"
    AUTHORITARIAN = "AUTHORITARIAN"
    FASCIST = "FASCIST"


@attr.s(auto_attribs=True)
class WarPolicy(Enum):
    ATTRITION = "ATTRITION"
    TURTLE = "TURTLE"
    BLITZKRIEG = "BLITZKRIEG"
    FORTRESS = "FORTRESS"
    MONEYBAGS = "MONEYBAGS"
    PIRATE = "PIRATE"
    TACTICIAN = "TACTICIAN"
    GUARDIAN = "GUARDIAN"
    COVERT = "COVERT"
    ARCANE = "ARCANE"


@attr.s(auto_attribs=True)
class EconomicPolicy(Enum):
    EXTREME_LEFT = "EXTREME_LEFT"
    FAR_LEFT = "FAR_LEFT"
    LEFT = "LEFT"
    MODERATE = "MODERATE"
    RIGHT = "RIGHT"
    FAR_RIGHT = "FAR_RIGHT"
    EXTREME_RIGHT = "EXTREME_RIGHT"


@attr.s(auto_attribs=True)
class DomesticPolicy(Enum):
    MANIFEST_DESTINY = "MANIFEST_DESTINY"
    OPEN_MARKETS = "OPEN_MARKETS"
    TECHNOLOGICAL_ADVANCEMENT = "TECHNOLOGICAL_ADVANCEMENT"
    IMPERIALISM = "IMPERIALISM"
    URBANIZATION = "URBANIZATION"
    RAPID_EXPANSION = "RAPID_EXPANSION"


@attr.s(auto_attribs=True)
class BulletinType(Enum):
    nation: int = 1
    alliance: int = 2


@attr.s(auto_attribs=True)
class GovernmentType(Enum):
    ABSOLUTE_MONARCHY = "ABSOLUTE_MONARCHY"
    ANARCHY = "ANARCHY"
    ARISTOCRACY = "ARISTOCRACY"
    BANANA_REPUBLIC = "BANANA_REPUBLIC"
    COMMUNIST_DEMOCRACY = "COMMUNIST_DEMOCRACY"
    COMMUNIST_DICTATORSHIP = "COMMUNIST_DICTATORSHIP"
    COMMUNIST_MONARCHY = "COMMUNIST_MONARCHY"
    COMMUNIST_REPUBLIC = "COMMUNIST_REPUBLIC"
    COMMUNIST_THEOCRACY = "COMMUNIST_THEOCRACY"
    CONSTITUTIONAL_MONARCHY = "CONSTITUTIONAL_MONARCHY"
    CONSTITUTIONAL_REPUBLIC = "CONSTITUTIONAL_REPUBLIC"
    DEMARCHY = "DEMARCHY"
    DEMOCRACY = "DEMOCRACY"
    DEMOCRATIC_REPUBLIC = "DEMOCRATIC_REPUBLIC"
    DICTATORSHIP = "DICTATORSHIP"
    FEDERAL_REPUBLIC = "FEDERAL_REPUBLIC"
    MONARCHY = "MONARCHY"
    NOOCRACY = "NOOCRACY"
    OLIGARCHY = "OLIGARCHY"
    PARLIAMENTARY_DEMOCRACY = "PARLIAMENTARY_DEMOCRACY"
    PARLIAMENTARY_REPUBLIC = "PARLIAMENTARY_REPUBLIC"
    PEOPLES_REPUBLIC = "PEOPLES_REPUBLIC"
    REPUBLIC = "REPUBLIC"
    SOCIAL_DEMOCRACY = "SOCIAL_DEMOCRACY"
    SOCIALIST_DICTATORSHIP = "SOCIALIST_DICTATORSHIP"
    SOCIALIST_REPUBLIC = "SOCIALIST_REPUBLIC"
    SOCIALIST_THEOCRACY = "SOCIALIST_THEOCRACY"
    STRATOCRACY = "STRATOCRACY"
    TECHNOCRACY = "TECHNOCRACY"
    THEOCRACY = "THEOCRACY"
    THEOCRATIC_DEMOCRACY = "THEOCRATIC_DEMOCRACY"
    THEOCRATIC_DICTATORSHIP = "THEOCRATIC_DICTATORSHIP"
    THEOCRATIC_REPUBLIC = "THEOCRATIC_REPUBLIC"
    MINDHIVE = "MINDHIVE"


@attr.s(auto_attribs=True)
class BulletinReply(_Base):
    id: int = None
    date: Any = None
    nation_id: int = None
    nation: "Nation" = attr.ib(factory=lambda: Nation)
    bulletin_id: int = None
    message: str = None
    edit_date: int = None
    nation_name: str = None
    leader_name: str = None
    like_count: int = None


@attr.s(auto_attribs=True)
class Bulletin(_Base):
    id: int = None
    nation_id: int = None
    nation: "Nation" = attr.ib(factory=lambda: Nation)
    alliance_id: int = None
    alliance: "Alliance" = attr.ib(factory=lambda: Alliance)
    type: BulletinType = None
    headline: str = None
    excerpt: str = None
    image: str = None
    body: str = None
    author: str = None
    pinned: bool = None
    like_count: int = None
    replies_enabled: bool = None
    locked: bool = None
    date: Any = None  # <---- Type and conversion
    edit_date: Any = None  # <---- Type and conversion
    archived: bool = None
    replies: List[BulletinReply] = None



@attr.s(auto_attribs=True)
class War(_Base):
    id: int = None
    date: Any = None  # <---- Type and conversion
    end_date: Any = None  # <---- Type and conversion
    reason: str = None
    war_type: Any = None  # <---- Type and conversion
    ground_control: int = None
    air_superiority: int = None
    naval_blockade: int = None
    winner_id: int = None
    attacks: Any = None  # <---- Type and conversion
    turns_left: int = None
    att_id: int = None
    att_alliance_id: int = None
    att_alliance_position: Any = None  # <---- Type and conversion
    attacker: "Nation" = attr.ib(factory=lambda: Nation)
    def_id: int = None
    def_alliance_id: int = None
    def_alliance_position: Any = None
    defender: "Nation" = attr.ib(factory=lambda: Nation)
    att_points: int = None
    def_points: int = None
    att_peace: bool = None
    def_peace: bool = None
    att_resistance: int = None
    def_resistance: int = None
    att_fortify: bool = None
    def_fortify: bool = None
    att_gas_used: float = None
    def_gas_used: float = None
    att_mun_used: float = None
    def_mun_used: float = None
    att_alum_used: float = None
    def_alum_used: float = None
    att_steel_used: float = None
    def_steel_used: float = None
    att_infra_destroyed: float = None
    def_infra_destroyed: float = None
    att_money_looted: float = None
    def_money_looted: float = None
    def_soldiers_lost: int = None
    att_soldiers_lost: int = None
    def_tanks_lost: int = None
    att_tanks_lost: int = None
    def_aircraft_lost: int = None
    att_aircraft_lost: int = None
    def_ships_lost: int = None
    att_ships_lost: int = None
    att_missiles_used: int = None
    def_missiles_used: int = None
    att_nukes_used: int = None
    def_nukes_used: int = None
    att_infra_destroyed_value: float = None
    def_infra_destroyed_value: float = None


@attr.s(auto_attribs=True)
class City(_Base):
    aluminum_refinery: int = None
    bank: int = None
    barracks: int = None
    bauxite_mine: int = None
    coal_mine: int = None
    coal_power: int = None
    date: Any = None  # <---- Type and conversion
    drydock: int = None
    factory: int = None
    farm: int = None
    hangar: int = None
    hospital: int = None
    id: int = None
    infrastructure: float = None
    iron_mine: int = None
    land: float = None
    lead_mine: int = None
    munitions_factory: int = None
    name: str = None
    nation: "Nation" = attr.ib(factory=lambda: Nation)
    nation_id: int = None
    nuclear_power: int = None
    nuke_date: Any = None  # <---- Type and conversion
    oil_power: int = None
    oil_refinery: int = None
    oil_well: int = None
    police_station: int = None
    powered: bool = None
    recycling_center: int = None
    shopping_mall: int = None
    stadium: int = None
    steel_mill: int = None
    subway: int = None
    supermarket: int = None
    uranium_mine: int = None
    wind_power: int = None


@attr.s(auto_attribs=True)
class Nation(_Base):
    activity_center: bool = None
    advanced_engineering_corps: bool = None
    advanced_pirate_economy: bool = None
    advanced_urban_planning: bool = None
    aircraft: int = None
    aircraft_casualties: int = None
    aircraft_kills: int = None
    aircraft_today: int = None
    alliance: "Alliance" = attr.ib(factory=lambda: Alliance)
    alliance_id: int = None
    alliance_join_date: Any = None  # <---- Type and conversion
    alliance_position: Any = None  # <---- Type and conversion
    alliance_position_id: int = None
    alliance_position_info: Any = None  # <---- Type and conversion
    alliance_seniority: int = None
    aluminum: float = None
    arable_land_agency: bool = None
    arms_stockpile: bool = None
    awards: Any = None  # <---- Type and conversion
    bankrecs: Any = None  # <---- Type and conversion
    baseball_team: Any = None  # <---- Type and conversion
    bauxite: float = None
    bauxite_works: bool = None
    beige_turns: int = None
    bounties: Any = None  # <---- Type and conversion
    bulletin_replies: List[BulletinReply] = None
    bulletins: List[Bulletin] = None
    bureau_of_domestic_affairs: bool = None
    center_for_civil_engineering: bool = None
    central_intelligence_agency: bool = None
    cities: List[City] = None
    clinical_research_center: bool = None
    coal: float = None
    color: str = None
    commendations: int = None
    continent: str = None
    credits: int = None
    credits_redeemed_this_month: int = None
    date: Any = None  # <---- Type and conversion
    defensive_wars_count: int = None
    denouncements: int = None
    discord: str = None
    discord_id: int = None
    domestic_policy: DomesticPolicy = None
    domestic_policy_turns: int = None
    economic_policy: EconomicPolicy = None
    emergency_gasoline_reserve: bool = None
    espionage_available: bool = None
    fallout_shelter: bool = None
    flag: str = None
    food: float = None
    gasoline: float = None
    government_support_agency: bool = None
    government_type: GovernmentType = None
    green_technologies: bool = None
    gross_domestic_product: float = None
    gross_national_income: float = None
    guiding_satellite: bool = None
    id: int = None
    international_trade_center: bool = None
    iron: float = None
    iron_dome: bool = None
    iron_works: bool = None
    last_active: Any = None  # <---- Type and conversion
    lead: float = None
    leader_name: str = None
    mars_landing: bool = None
    mars_landing_date: Any = None  # <---- Type and conversion
    mass_irrigation: bool = None
    metropolitan_planning: bool = None
    military_salvage: bool = None
    missile_casualties: int = None
    missile_kills: int = None
    missile_launch_pad: bool = None
    missiles: int = None
    missiles_today: int = None
    money: float = None
    money_looted: float = None
    moon_landing: bool = None
    moon_landing_date: Any = None  # <---- Type and conversion
    munitions: float = None
    nation_name: str = None
    nuclear_launch_facility: bool = None
    nuclear_research_facility: bool = None
    nuke_casualties: int = None
    nuke_kills: int = None
    nukes: int = None
    nukes_today: int = None
    num_cities: int = None
    offensive_wars_count: int = None
    oil: float = None
    pirate_economy: bool = None
    population: int = None
    project_bits: str = None
    projects: int = None
    propaganda_bureau: bool = None
    received_bankrecs: Any = None  # <---- Type and conversion
    recycling_initiative: bool = None
    research_and_development_center: bool = None
    resource_production_center: bool = None
    score: float = None
    sent_bankrecs: Any = None  # <---- Type and conversion
    ship_casualties: int = None
    ship_kills: int = None
    ships: int = None
    ships_today: int = None
    social_policy: SocialPolicy = None
    soldier_casualties: int = None
    soldier_kills: int = None
    soldiers: int = None
    soldiers_today: int = None
    space_program: bool = None
    specialized_police_training_program: bool = None
    spies: int = None
    spies_today: int = None
    spy_attacks: int = None
    spy_casualties: int = None
    spy_kills: int = None
    spy_satellite: bool = None
    steel: float = None
    surveillance_network: bool = None
    tank_casualties: int = None
    tank_kills: int = None
    tanks: int = None
    tanks_today: int = None
    tax_id: int = None
    tax_recs: Any = None  # <---- Type and conversion
    telecommunications_satellite: bool = None
    total_infrastructure_destroyed: float = None
    total_infrastructure_lost: float = None
    trades: Any = None  # <---- Type and conversion
    treasures: Any = None  # <---- Type and conversion
    turns_since_last_city: int = None
    turns_since_last_project: int = None
    update_tz: float = None
    uranium: float = None
    uranium_enrichment_program: bool = None
    urban_planning: bool = None
    vacation_mode_turns: int = None
    vip: bool = None
    vital_defense_system: bool = None
    war_policy: WarPolicy = None
    war_policy_turns: int = None
    wars: List[War] = None
    wars_lost: int = None
    wars_won: int = None

    @property
    def url(self) -> str:
        if not self.id:
            raise errors.ModelMissingField("id")

        return f"{urls.NATION_PAGE}/id={self.id}"

    @property
    def message_url(self) -> str:
        if not self.leader_name:
            raise errors.ModelMissingField("leader_name")

        return f"{urls.MESSAGE_PAGE}/receiver={self.leader_name}".replace(" ", "%20")

    @property
    def total_infra(self) -> float:
        if not self.cities:
            raise errors.ModelMissingField("cities")

        infra = 0

        for city in self.cities:
            if not city.infrastructure:
                raise errors.ModelMissingField("infrastructure")

            infra += city.infrastructure

        return infra

    @property
    def total_land(self) -> float:
        if not self.cities:
            raise errors.ModelMissingField("cities")

        land = 0

        for city in self.cities:
            if not city.land:
                raise errors.ModelMissingField("land")

            land += city.land

        return land


@attr.s(auto_attribs=True)
class Alliance(_Base):
    accept_members: bool = None
    acronym: str = None
    alliance_positions: Any = None  # <---- Type and conversion
    aluminum: float = None
    average_score: float = None
    awards: Any = None  # <---- Type and conversion
    bankrecs: Any = None  # <---- Type and conversion
    bauxite: float = None
    bulletins: List[Bulletin] = None
    coal: float = None
    color: str = None
    date: Any = None
    discord_link: str = None
    flag: str = None
    food: float = None
    forum_link: str = None
    gasoline: float = None
    id: int = None
    iron: float = None
    lead: float = None
    money: float = None
    munitions: float = None
    name: str = None
    nations: List[Nation] = None
    oil: float = None
    rank: int = None
    received_treaties: Any = None  # <---- Type and conversion
    score: float = None
    sent_treaties: Any = None  # <---- Type and conversion
    steel: float = None
    tax_brackets: Any = None  # <---- Type and conversion
    taxrecs: Any = None  # <---- Type and conversion
    treaties: Any = None  # <---- Type and conversion
    uranium: float = None
    wars: List[War] = None
    wiki_link: str = None

    @property
    def url(self) -> str:
        if not self.id:
            raise errors.ModelMissingField("id")

        return f"{urls.ALLIANCE_PAGE}/id={self.id}"
