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


from api import fetch_query


async def bank_info(key: str, alliance: int) -> dict:
    query = f"""
      alliances(id:{alliance}, first:1) {{
        data {{
          money
          coal
          uranium
          iron
          bauxite
          steel
          gasoline
          munitions
          oil
          food
          aluminum
        }}
      }}
    """

    response = await fetch_query(key, query)
    return response["alliances"]["data"]


async def bank_records(key: str, alliance: int) -> dict:
    query = f"""
         alliances(id:{alliance}, first:1){{
            data{{
              bankrecs{{
                id
                note
                pid
                sid
                rid
                stype
                rtype
                money
                coal
                uranium
                iron
                bauxite
                steel
                gasoline
                munitions
                oil
                food
                aluminum
              }}
            }}
          }}
        }}
    """

    response = await fetch_query(key, query)
    return response["alliances"]["data"]["bankrecs"]
