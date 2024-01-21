# riot_api_manipulation : access games' data with ease
![Logo Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) [![Version 0.0.8](https://img.shields.io/badge/0.0.8-%2316c60c.svg?style=for-the-badge&label=version)](https://test.pypi.org/project/riot-api-manipulation/)

[riot_api_manipulation](https://test.pypi.org/project/riot-api-manipulation/) is a python library designed to manipulate [Riot APIs](https://developer.riotgames.com/apis) with ease. Its key benefits include three fundamentals : simple usage, technical abstraction and reliability.

## 📦 Setup

###### Installation
```python
pip install --index-url https://test.pypi.org/simple/ riot-api-manipulation 
```

###### Upgrade
```python
pip install --upgrade --index-url https://test.pypi.org/simple/ --no-deps riot-api-manipulation 
```

## 💯 Covering

![](https://geps.dev/progress/40) League of Legends  <BR>
![](https://geps.dev/progress/40) Valorant           <BR>
![](https://geps.dev/progress/0) Teamfight Tactics   <BR>
![](https://geps.dev/progress/0) League of Runeterra <BR>

All routes listed here : [click me to discover what is implemented !](./docs/ROUTE_COVERING.md)

## 💻 Getting started

### 1. Important point : closing

riot_api_manipulation uses parallel threads to track left requests and the function API.close() terminates these threads.
Make sure to add it at the end of your script or at the closing of your application.
```python
api_lol = API_LOL("YOUR_API_KEY", Region.EUROPE, Server.EU_WEST)
# Exploiting api [...]
api_lol.close()
```

### 2. Usage examples

To see more usage examples with expected outputs, [take a look here](./docs/EXAMPLES.md).

###### Get summoner's last game infos
```python
# Opening the api manager with a key, a region and a server
api_lol = API_LOL("YOUR_API_KEY", Region.EUROPE, Server.EU_WEST)

# Getting summoner's details
summoner = api_lol.get_summoner_by_name("SUMMONER_NAME")

# Recovering his last game and searching his infos in it
last_match_infos = (summoner.get_last_game()
                    .get_infos_of_summoner())

# Closing the api manager (for threads, as said earlier !)
api_lol.close()

# Enjoy results
print(summoner)
print(last_match_infos)
```

###### Get summoner's last ranked games with infos and timeline
```python
# Opening the api manager with a key, a region and a server
api_lol = API_LOL("YOUR_API_KEY", Region.EUROPE, Server.EU_NORTH)

# Getting summoner's details
summoner = api_lol.get_summoner_by_name("SUMMONER_NAME")

# Recovering his 10 last ranked games infos and timelines
last_games_full = summoner.get_match_history(nb_matches=10, queue=QueueType.RANKED, load_infos=True, load_timelines=True)

# Closing the api manager (for threads, as said earlier !)
api_lol.close()

# Enjoy results
for game in last_games_full:
    print(game.json)
    print(game.json_timeline)
```

## 🔭 How to contribute

Do you have a suggestion or a new feature in mind ? <BR>
Take a look to the [issue tracker](https://github.com/Hugo-CASTELL/riot_api_manipulation/issues) !

Maybe do you want to contribute, solve an issue or develop new enhancements ? <BR>
Read the [contributing guidelines](./docs/CONTRIBUTING.md), create a new branch and let's start !

## 📚 Documentation

[Usage examples](./docs/EXAMPLES.md) <BR>
[Riot api routes covering](./docs/ROUTE_COVERING.md) <BR>
[Contributing guidelines](./docs/CONTRIBUTING.md) <BR>
