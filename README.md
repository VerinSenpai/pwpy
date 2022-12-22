<div align="center">
    <h1>pwpy</h1>
    <a href="https://pypi.org/project/pwpy"><img height="20" alt="Supported python versions" src="https://img.shields.io/pypi/pyversions/pwpy"></a>
    <a href="https://pypi.org/project/pwpy"><img height="20" alt="PyPI version" src="https://img.shields.io/pypi/v/pwpy"></a>
</div>

A robust collection of tools, scrapers, and prebuilt api queries designed to make developing for Politics and War and the v3 API easy!

### Installation
You can install PWPY from PyPI using the following command.
```commandline
python -m pip install -U pwpy
```

### Using the API
PWPY includes wrapper functions that will handle sending and receiving queries for you.
```python
from pwpy import api

query: dict = {
    "field": "nations",
    "args": {"id": 6},
    "data": {"data": "nation_name"}
}

nation = await api.get_query(query, "your_api_key")

print(nation["nations"]["data"]["nation_name"])
```
Alternatively, PWPY also provides prebuilt queries.
```python
from pwpy import queries

nation = await queries.nation_identify(6, "your_api_key")

print(nation["nation_name"])
```
Running either of these code snippets will print "Mountania" to your console.

Note that the "get_query" function will take either a formatted query dictionary (see below) or a properly written gql query string.

Using the built-in query factory is simple. It requires your dict to have 3 keys.

* **Field:** the name of the field you are querying
* **Args:** the arguments that will be used to filter your search
* **Data:** the data you are trying to retrieve

Note that when writing queries you must still know and understand the schema you are trying to pull from.

You may also wish to send multiple queries at once. For this, we have the BulkQuery object.

```python
from pwpy import api

bulk_query = api.BulkQuery("your_api_key")

for page in range(10):
    query: dict = {
        "field": f"page_{page}: nations",
        "args": {"first": 50, "page": page},
        "data": {"data": ("id", "nation_name", "leader_name")}
    }
    bulk_query.insert(query)

nations = await bulk_query.get()
```
The v3 API supports sending multiple queries at one time in the same payload. In order to take advantage of this with the
same field type however, we must provide a different name for each "page". In the above code snippet, we do this
programmatically by appending "page_{page}: " before the actual field name. In the return response, the api will only
provide that page name, not the field that it came from. Keep this in mind if you intend to send multiple pages from
different fields. 

This is an example of what the query above would return:
```
{
    "page_1": [
        {"id": 34904, "nation_name": "Libaria", "leader_name": "Verin"},
        {"id": 6, "nation_name": "Mountania", "leader_name": "Alex"}
    ],
    "page_2": [
        ...
    ]
}
```

Also note that the BulkQuery object breaks queries up into chunks, so we don't run into issues when sending a large number
of queries. By default, the chunk size is 10 (10 queries per request) but you can change this by specifying a different
chunk_size argument when you initialize BulkQuery. In the above code, we only generate 10 queries, so only 1 request will
be made. 10 is just an arbitrary default. You should change the chunk_size to meet your needs, bearing in mind that the
rate limit is 60 requests per minute.

With that said, PWPY will handle rate limits gracefully, re-attempting any failed requests when the rate limit is up
automatically and proceeding with any queued up requests afterwards. This shouldn't raise any errors but may cause
requests to take longer to return.

### Calculators

PWPY also includes a number of calculators which while less exciting are no less useful.

Let's calculate the cost of going from 1500 infra to 3000.

```python
from pwpy import utils

cost = utils.infra_cost(1500, 3000)
```
Running this code should return a float of "50057534.0".

The same usage applies to the land_cost calculator.

The city_cost calculator takes the city you're trying to buy.

```python
from pwpy import utils

cost = utils.city_cost(11)
```
This will return a float of "38025000.0"

You can validate the results of all calculators using these links:
* https://politicsandwar.com/tools/city
* https://politicsandwar.com/tools/infra
* https://politicsandwar.com/tools/land