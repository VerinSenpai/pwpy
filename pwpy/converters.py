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


from cattr import Converter
from typing import List
from pwpy import urls, errors, utils
from enum import Enum
from datetime import datetime

import typing
import attr


_CONVERTER = Converter()


def _str_to_datetime(date_str: str, _) -> datetime:
    return datetime.fromisoformat(date_str)


_CONVERTER.register_structure_hook(datetime, _str_to_datetime)


def _global_to_world(value, cls):
    if _global := value.pop("global", None):
        value["world"] = _global

    return _CONVERTER.structure_attrs_fromdict(value, cls)


class _BaseConverter:

    @classmethod
    def convert(cls, data: dict) -> typing.Any:
        return _CONVERTER.structure(data, cls)


class _BaseEnum(Enum):

    def __str__(self) -> str:
        return str(self.value).replace("_", " ").title()


@attr.s(auto_attribs=True)
class PaginatorInfo(_BaseConverter):
    count: int = None
    currentPage: int = None
    firstItem: int = None
    hasMorePages: bool = None
    lastItem: int = None
    lastPage: int = None
    perPage: int = None
    total: int = None


@attr.s(auto_attribs=True)
class QueryResponse(_BaseConverter):
    activity_stats: "ActivityStatPaginator" = None
    alliances: "AlliancePaginator" = None
    bankrecs: "BankRecordPaginator" = None
    banned_nations: "BannedNationPaginator" = None
    baseball_games: "BaseballGamePaginator" = None
    baseball_players: "BaseballPlayerPaginator" = None
    baseball_teams: "BaseballTeamPaginator" = None
    bounties: "BountyPaginator" = None
    bulletin_replies: "BulletinReplyPaginator" = None
    bulletins: "BulletinPaginator" = None
    cities: "CityPaginator" = None
    colors: List["Color"] = None
    embargoes: "EmbargoPaginator" = None
    game_info: "GameInfo" = None
    me: "Me" = None
    nation_resource_stats: "ResourceStat" = None
    nations: "NationPaginator" = None
    resource_stats: List["ResourceStat"] = None
    top_trade_info: "TopTradeInfo" = None
    trade_prices: "TradePricePaginator" = None
    trades: "TradePaginator" = None
    treasure_trades: "TreasureTradePaginator" = None
    treasures: List["Treasure"] = None
    treaties: "TreatyPaginator" = None
    warattacks: "WarAttackPaginator" = None
    wars: "WarPaginator" = None

@attr.s(auto_attribs=True)
class ActivityStat(_BaseConverter):
    active_1_day: int = None
    active_1_month: int = None
    active_1_week: int = None
    active_2_days: int = None
    active_3_days: int = None
    date: datetime = None
    nations_created: int = None
    total_nations: int = None


@attr.s(auto_attribs=True)
class ActivityStatPaginator(_BaseConverter):
    data: ActivityStat = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class Alliance(_BaseConverter):
    accept_members: bool = None
    acronym: str = None
    alliance_positions: List["AlliancePositionInfo"] = None
    aluminum: float = None
    average_score: float = None
    awards: List["Award"] = None
    bankrecs: List["BankRecord"] = None
    bauxite: float = None
    bulletins: List["Bulletin"] = None
    coal: float = None
    color: str = None
    date: datetime = None
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
    nations: List["Nation"] = None
    oil: float = None
    rank: int = None
    received_treaties: List["Treaty"] = None
    score: float = None
    sent_treaties: List["Treaty"] = None
    steel: float = None
    tax_brackets: List["TaxBracket"] = None
    taxrecs: List["BankRecord"] = None
    treaties: List["Treaty"] = None
    uranium: float = None
    wars: List["War"] = None
    wiki_link: str = None

    @property
    def url(self) -> str:
        if not self.id:
            raise errors.ModelMissingField("id")

        return f"{urls.ALLIANCE_PAGE}/id={self.id}"


@attr.s(auto_attribs=True)
class AlliancePaginator(_BaseConverter):
    data: List["Alliance"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class BankRecord(_BaseConverter):
    id: int = None
    date: datetime = None
    sender_id: int = None
    sender_type: "PostType" = None
    sender: "Nation" = None
    receiver_id: int = None
    receiver_type: "PostType" = None
    receiver: "Nation" = None
    banker_id: int = None
    banker: "Nation" = None
    note: str = None
    money: float = None
    coal: float = None
    oil: float = None
    uranium: float = None
    iron: float = None
    bauxite: float = None
    lead: float = None
    gasoline: float = None
    munitions: float = None
    steel: float = None
    aluminum: float = None
    food: float = None
    tax_id: int = None


@attr.s(auto_attribs=True)
class BankRecordPaginator(_BaseConverter):
    data: List["BankRecord"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class BannedNation(_BaseConverter):
    date: datetime = None
    days_left: int = None
    nation_id: int = None
    reason: str = None


@attr.s(auto_attribs=True)
class BannedNationPaginator(_BaseConverter):
    data: List["BannedNation"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class BaseballGame(_BaseConverter):
    id: int = None
    date: datetime = None
    home_id: int = None
    away_id: int = None
    home_team: "BaseballTeam" = None
    away_team: "BaseballTeam" = None
    home_nation_id: int = None
    away_nation_id: int = None
    home_nation: "Nation" = None
    away_nation: "Nation" = None
    stadium_name: str = None
    home_score: int = None
    away_score: int = None
    sim_text: str = None
    highlights: str = None
    home_revenue: float = None
    spoils: float = None
    open: int = None
    wager: float = None


@attr.s(auto_attribs=True)
class BaseballGamePaginator(_BaseConverter):
    data: List["BaseballGame"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class BaseballPlayer(_BaseConverter):
    id: int = None
    date: datetime = None
    nation_id: int = None
    nation: "Nation" = None
    team_id: int = None
    team: "BaseballTeam" = None
    name: str = None
    age: int = None
    position: str = None
    pitching: float = None
    batting: float = None
    speed: float = None
    awareness: float = None
    overall: float = None
    birthday: int = None


@attr.s(auto_attribs=True)
class BaseballPlayerPaginator(_BaseConverter):
    data: List["BaseballPlayer"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class BaseballTeam(_BaseConverter):
    id: int = None
    date: datetime = None
    nation_id: int = None
    nation: "Nation" = None
    name: str = None
    logo: str = None
    home_jersey: str = None
    away_jersey: str = None
    stadium: str = None
    quality: int = None
    seating: int = None
    rating: float = None
    wins: int = None
    glosses: int = None
    runs: int = None
    homers: int = None
    strikeouts: int = None
    games_played: int = None
    games: BaseballGame = None
    players: BaseballPlayer = None


@attr.s(auto_attribs=True)
class BaseballTeamPaginator(_BaseConverter):
    data: List["BaseballTeam"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class Bounty(_BaseConverter):
    id: int = None
    date: datetime = None
    nation_id: int = None
    nation: "Nation" = None
    amount: int = None
    type: "BountyType" = None


@attr.s(auto_attribs=True)
class BountyPaginator(_BaseConverter):
    data: List["Bounty"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class BulletinReply(_BaseConverter):
    id: int = None
    date: datetime = None
    nation_id: int = None
    nation: "Nation" = None
    bulletin_id: int = None
    message: str = None
    edit_date: datetime = None
    nation_name: str = None
    leader_name: str = None
    like_count: int = None


@attr.s(auto_attribs=True)
class BulletinReplyPaginator(_BaseConverter):
    data: List["BulletinReply"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class Bulletin(_BaseConverter):
    id: int = None
    nation_id: int = None
    nation: "Nation" = None
    alliance_id: int = None
    alliance: "Alliance" = None
    type: "PostType" = None
    headline: str = None
    excerpt: str = None
    image: str = None
    body: str = None
    author: str = None
    pinned: bool = None
    like_count: int = None
    replies_enabled: bool = None
    locked: bool = None
    date: datetime = None
    edit_date: datetime = None
    archived: bool = None
    replies: List["BulletinReply"] = None


@attr.s(auto_attribs=True)
class BulletinPaginator(_BaseConverter):
    data: List["Bulletin"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class City(_BaseConverter):
    aluminum_refinery: int = None
    bank: int = None
    barracks: int = None
    bauxite_mine: int = None
    coal_mine: int = None
    coal_power: int = None
    date: datetime = None
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
    nation: "Nation" = None
    nation_id: int = None
    nuclear_power: int = None
    nuke_date: datetime = None
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
class CityPaginator(_BaseConverter):
    data: List["City"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class Color(_BaseConverter):
    bloc_name: str = None
    color: str = None
    turn_bonus: int = None

@attr.s(auto_attribs=True)
class Embargo(_BaseConverter):
    date: datetime = None
    id: int = None
    reason: str = None
    receiver: "Nation" = None
    receiver_id: int = None
    sender: "Nation" = None
    sender_id: int = None
    type: "EmbargoType" = None


@attr.s(auto_attribs=True)
class EmbargoPaginator(_BaseConverter):
    data: List["Embargo"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class GameInfo(_BaseConverter):
    game_date: datetime = None
    radiation: "Radiation" = None


@attr.s(auto_attribs=True)
class Radiation(_BaseConverter):
    africa: float = None
    antarctica: float = None
    asia: float = None
    australia: float = None
    europe: float = None
    north_america: float = None
    south_america: float = None
    world: float = None


_CONVERTER.register_structure_hook(Radiation, _global_to_world)


@attr.s(auto_attribs=True)
class Me(_BaseConverter):
    key: str = None
    max_requests: int = None
    nation: "Nation" = None
    permission_bits: int = None
    permissions: "APIKeyPermissions" = None
    requests: int = None


@attr.s(auto_attribs=True)
class APIKeyPermissions(_BaseConverter):
    alliance_accept_applicants: bool = None 
    alliance_change_permissions: bool = None
    alliance_manage_treaties: bool = None
    alliance_promote_self_to_leader: bool = None
    alliance_remove_members: bool = None
    alliance_see_reset_timers: bool = None
    alliance_see_spies: bool = None
    alliance_tax_brackets: bool = None
    alliance_view_bank: bool = None
    alliance_withdraw_bank: bool = None
    nation_accept_trade: bool = None
    nation_deposit_to_bank: bool = None
    nation_military_buys: bool = None
    nation_see_reset_timers: bool = None
    nation_see_spies: bool = None
    nation_send_message: bool = None
    nation_view_resources: bool = None
    nation_view_trades: bool = None


@attr.s(auto_attribs=True)
class Nation(_BaseConverter):
    activity_center: bool = None
    advanced_engineering_corps: bool = None
    advanced_pirate_economy: bool = None
    advanced_urban_planning: bool = None
    aircraft: int = None
    aircraft_casualties: int = None
    aircraft_kills: int = None
    aircraft_today: int = None
    alliance: "Alliance" = None
    alliance_id: int = None
    alliance_join_date: datetime = None
    alliance_position: "AlliancePosition" = None
    alliance_position_id: int = None
    alliance_position_info: "AlliancePositionInfo" = None
    alliance_seniority: int = None
    aluminum: float = None
    arable_land_agency: bool = None
    arms_stockpile: bool = None
    awards: List["Award"] = None
    bankrecs: List[BankRecord] = None
    baseball_team: BaseballTeam = None
    bauxite: float = None
    bauxite_works: bool = None
    beige_turns: int = None
    bounties: List[Bounty] = None
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
    date: datetime = None
    defensive_wars_count: int = None
    denouncements: int = None
    discord: str = None
    discord_id: int = None
    domestic_policy: "DomesticPolicy" = None
    domestic_policy_turns: int = None
    economic_policy: "EconomicPolicy" = None
    emergency_gasoline_reserve: bool = None
    espionage_available: bool = None
    fallout_shelter: bool = None
    flag: str = None
    food: float = None
    gasoline: float = None
    government_support_agency: bool = None
    government_type: "GovernmentType" = None
    green_technologies: bool = None
    gross_domestic_product: float = None
    gross_national_income: float = None
    guiding_satellite: bool = None
    id: int = None
    international_trade_center: bool = None
    iron: float = None
    iron_dome: bool = None
    iron_works: bool = None
    last_active: datetime = None
    lead: float = None
    leader_name: str = None
    mars_landing: bool = None
    mars_landing_date: datetime = None
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
    moon_landing_date: datetime = None
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
    received_bankrecs: List[BankRecord] = None
    recycling_initiative: bool = None
    research_and_development_center: bool = None
    resource_production_center: bool = None
    score: float = None
    sent_bankrecs: List[BankRecord] = None
    ship_casualties: int = None
    ship_kills: int = None
    ships: int = None
    ships_today: int = None
    social_policy: "SocialPolicy" = None
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
    taxrecs: List[BankRecord] = None
    telecommunications_satellite: bool = None
    total_infrastructure_destroyed: float = None
    total_infrastructure_lost: float = None
    trades: List["Trade"] = None
    treasures: List["Treasure"] = None
    turns_since_last_city: int = None
    turns_since_last_project: int = None
    update_tz: float = None
    uranium: float = None
    uranium_enrichment_program: bool = None
    urban_planning: bool = None
    vacation_mode_turns: int = None
    vip: bool = None
    vital_defense_system: bool = None
    war_policy: "WarPolicy" = None
    war_policy_turns: int = None
    wars: List["War"] = None
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
    def city_manager_url(self) -> str:
        if not self.leader_name:
            raise errors.ModelMissingField("leader_name")

        return f"{urls.CITY_MANAGER_PAGE}&l={self.leader_name}"

    @property
    def war_range_url(self) -> str:
        if not self.score:
            raise errors.ModelMissingField("score")

        return (f"{urls.WARS_PAGE}&keyword={self.score}&cat=war_range"
                f"&ob=score&od=ASC&beige=true&vmode=false&openslots=true")

    @property
    def score_range(self) -> (float, float):
        if not self.score:
            raise errors.ModelMissingField("score")

        return utils.score_range(self.score)

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
class NationPaginator(_BaseConverter):
    data: List["Nation"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class ResourceStat(_BaseConverter):
    aluminum: str = None
    bauxite: str = None
    coal: str = None
    date: datetime = None
    food: str = None
    gasoline: str = None
    iron: str = None
    lead: str = None
    money: str = None
    munitions: str = None
    oil: str = None
    steel: str = None
    uranium: str = None


@attr.s(auto_attribs=True)
class TopTradeInfo(_BaseConverter):
    market_index: int = None
    resources: List["TopTradeResourcesInfo"] = None


@attr.s(auto_attribs=True)
class TopTradeResourcesInfo(_BaseConverter):
    average_price: int = None
    best_buy_offer: "Trade" = None
    best_sell_offer: "Trade" = None
    resource: str = None


@attr.s(auto_attribs=True)
class TradePrice(_BaseConverter):
    aluminum: float = None
    bauxite: float = None
    coal: float = None
    credits: float = None
    date: datetime = None
    food: float = None
    gasoline: float = None
    id: int = None
    iron: float = None
    lead: float = None
    munitions: float = None
    oil: float = None
    steel: float = None
    uranium: float = None


@attr.s(auto_attribs=True)
class TradePricePaginator(_BaseConverter):
    data: List["TradePrice"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class Trade(_BaseConverter):
    id: int = None
    type: "TradeType" = None
    date: datetime = None
    sender_id: int = None
    receiver_id: int = None
    sender: "Nation" = None
    receiver: "Nation" = None
    offer_resource: str = None
    offer_amount: int = None
    buy_or_sell: str = None
    price: int = None
    accepted: bool = None
    date_accepted: datetime = None
    original_trade_id: int = None


@attr.s(auto_attribs=True)
class TradePaginator(_BaseConverter):
    data: List["Trade"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class TreasureTrade(_BaseConverter):
    ...


@attr.s(auto_attribs=True)
class TreasureTradePaginator(_BaseConverter):
    data: List["TreasureTrade"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class Treasure(_BaseConverter):
    name: str = None
    color: str = None
    continent: str = None
    bonus: int = None
    spawn_date: str = None
    nation_id: int = None
    nation: "Nation" = None


@attr.s(auto_attribs=True)
class Treaty(_BaseConverter):
    id: int = None
    date: datetime = None
    treaty_type: str = None
    treaty_url: str = None
    turns_left: int = None
    alliance1_id: int = None
    alliance1: "Alliance" = None
    alliance2_id: int = None
    alliance2: "Alliance" = None
    approved: bool = None


@attr.s(auto_attribs=True)
class TreatyPaginator(_BaseConverter):
    data: List["Treaty"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class WarAttack(_BaseConverter):
    id: int = None
    date: datetime = None
    att_id: int = None
    attacker: "Nation" = None
    def_id: int = None
    defender: "Nation" = None
    type: "AttackType" = None
    war_id: int = None
    war: "War" = None
    victor: int = None
    success: int = None
    city_id: int = None
    infra_destroyed: float = None
    money_stolen: float = None
    resistance_lost: int = None
    city_infra_before: float = None
    infra_destroyed_value: float = None
    att_mun_used: float = None
    def_mun_used: float = None
    att_gas_used: float = None
    def_gas_used: float = None
    money_destroyed: float = None
    military_salvage_aluminum: float = None
    military_salvage_steel: float = None
    att_soldiers_used: int = None
    att_soldiers_lost: int = None
    def_soldiers_used: int = None
    def_soldiers_lost: int = None
    att_tanks_used: int = None
    att_tanks_lost: int = None
    def_tanks_used: int = None
    def_tanks_lost: int = None
    att_aircraft_used: int = None
    att_aircraft_lost: int = None
    def_aircraft_used: int = None
    def_aircraft_lost: int = None
    att_ships_used: int = None
    att_ships_lost: int = None
    def_ships_used: int = None
    def_ships_lost: int = None
    att_missiles_lost: int = None
    def_missiles_lost: int = None
    att_nukes_lost: int = None
    def_nukes_lost: int = None
    improvements_destroyed: str = None
    infra_destroyed_percentage: float = None
    cities_infra_before: "CityInfraDamage" = None
    money_looted: float = None
    coal_looted: float = None
    oil_looted: float = None
    uranium_looted: float = None
    iron_looted: float = None
    bauxite_looted: float = None
    lead_looted: float = None
    gasoline: float = None
    munitions_looted: float = None
    steel_looted: float = None
    aluminum_looted: float = None
    food_looted: float = None


@attr.s(auto_attribs=True)
class WarAttackPaginator(_BaseConverter):
    data: List["WarAttack"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class War(_BaseConverter):
    id: int = None
    date: datetime = None
    end_date: datetime = None
    reason: str = None
    war_type: "WarType" = None
    ground_control: int = None
    air_superiority: int = None
    naval_blockade: int = None
    winner_id: int = None
    attacks: List["WarAttack"] = None
    turns_left: int = None
    att_id: int = None
    att_alliance_id: int = None
    att_alliance_position: "AlliancePosition" = None
    attacker: "Nation" = None
    def_id: int = None
    def_alliance_id: int = None
    def_alliance_position: "AlliancePosition" = None
    defender: "Nation" = None
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
class  WarPaginator(_BaseConverter):
    data: List["War"] = None
    paginatorInfo: PaginatorInfo = None


@attr.s(auto_attribs=True)
class AttackType(_BaseEnum):
    AIRVINFRA = "AIRVINFRA"
    AIRVSOLDIERS = "AIRVSOLDIERS"
    AIRVTANKS = "AIRVTANKS"
    AIRVMONEY = "AIRVMONEY"
    AIRVSHIPS = "AIRVSHIPS"
    AIRVAIR = "AIRVAIR"
    GROUND = "GROUND"
    MISSILE = "MISSILE"
    MISSILEFAIL = "MISSILEFAIL"
    NUKE = "NUKE"
    NUKEFAIL = "NUKEFAIL"
    NAVAL = "NAVAL"
    FORTIFY = "FORTIFY"
    PEACE = "PEACE"
    VICTORY = "VICTORY"
    ALLIANCELOOT = "ALLIANCELOOT"


@attr.s(auto_attribs=True)
class WarType(_BaseEnum):
    ORDINARY = "ORDINARY"
    ATTRITION = "ATTRITION"
    RAID = "RAID"


@attr.s(auto_attribs=True)
class SocialPolicy(_BaseEnum):
    ANARCHIST = "ANARCHIST"
    LIBERTARIAN = "LIBERTARIAN"
    LIBERAL = "LIBERAL"
    MODERATE = "MODERATE"
    CONSERVATIVE = "CONSERVATIVE"
    AUTHORITARIAN = "AUTHORITARIAN"
    FASCIST = "FASCIST"


@attr.s(auto_attribs=True)
class WarPolicy(_BaseEnum):
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
class EconomicPolicy(_BaseEnum):
    EXTREME_LEFT = "EXTREME_LEFT"
    FAR_LEFT = "FAR_LEFT"
    LEFT = "LEFT"
    MODERATE = "MODERATE"
    RIGHT = "RIGHT"
    FAR_RIGHT = "FAR_RIGHT"
    EXTREME_RIGHT = "EXTREME_RIGHT"


@attr.s(auto_attribs=True)
class DomesticPolicy(_BaseEnum):
    MANIFEST_DESTINY = "MANIFEST_DESTINY"
    OPEN_MARKETS = "OPEN_MARKETS"
    TECHNOLOGICAL_ADVANCEMENT = "TECHNOLOGICAL_ADVANCEMENT"
    IMPERIALISM = "IMPERIALISM"
    URBANIZATION = "URBANIZATION"
    RAPID_EXPANSION = "RAPID_EXPANSION"


@attr.s(auto_attribs=True)
class TradeType(_BaseEnum):
    GLOBAL = "GLOBAL"
    PERSONAL = "PERSONAL"
    ALLIANCE = "ALLIANCE"


@attr.s(auto_attribs=True)
class BountyType(_BaseEnum):
    ORDINARY = "ORDINARY"
    ATTRITION = "ATTRITION"
    RAID = "RAID"
    NUCLEAR = "NUCLEAR"


@attr.s(auto_attribs=True)
class AlliancePosition(_BaseEnum):
    NOALLIANCE = "NOALLIANCE"
    APPLICANT = "APPLICANT"
    MEMBER = "MEMBER"
    OFFICER = "OFFICER"
    HEIR = "HEIR"
    LEADER = "LEADER"


@attr.s(auto_attribs=True)
class GovernmentType(_BaseEnum):
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
class Award(_BaseConverter):
    name: str = None
    image: str = None


@attr.s(auto_attribs=True)
class CityInfraDamage(_BaseConverter):
    """What the hell is this?"""
    id: int = None
    infrastructure: float = None


@attr.s(auto_attribs=True)
class TaxBracket(_BaseConverter):
    id: int = None
    alliance_id: int = None
    alliance: "Alliance" = None
    date: datetime = None
    date_modified: datetime = None
    last_modifier_id: int = None
    last_modifier: "Nation" = None
    tax_rate: int = None
    resource_tax_rate: int = None
    bracket_name: str = None


@attr.s(auto_attribs=True)
class AlliancePositionInfo(_BaseConverter):
    id: int = None
    date: datetime = None
    alliance_id: int = None
    name: str = None
    creator_id: int = None
    last_editor_id: int = None
    date_modified: datetime = None
    position_level: int = None
    leader: bool = None
    heir: bool = None
    officer: bool = None
    member: bool = None
    permissions: int = None
    view_bank: bool = None
    withdraw_bank: bool = None
    change_permissions: bool = None
    see_spies: bool = None
    see_reset_timers: bool = None
    tax_brackets: bool = None
    post_announcements: bool = None
    manage_announcements: bool = None
    accept_applicants: bool = None
    remove_members: bool = None
    edit_alliance_info: bool = None
    manage_treaties: bool = None
    manage_market_share: bool = None
    manage_embargoes: bool = None
    promote_self_to_leader: bool = None


@attr.s(auto_attribs=True)
class PostType(_BaseEnum):
    NATION: int = 1
    ALLIANCE: int = 2


@attr.s(auto_attribs=True)
class EmbargoType(_BaseEnum):
    NATION_TO_NATION = "NATION_TO_NATION"
    NATION_TO_ALLIANCE = "NATION_TO_ALLIANCE"
    ALLIANCE_TO_NATION = "ALLIANCE_TO_NATION"
    ALLIANCE_TO_ALLIANCE = "ALLIANCE_TO_ALLIANCE"
