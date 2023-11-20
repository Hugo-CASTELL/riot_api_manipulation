# riot_api_manipulation : access games' data with ease
![Logo Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

### Content

- [Description](#-description)
- [Release](#-release)
- [Getting started](#-getting-started)
- [Documentation](#-documentation)

## 📕 Description

The aim of the project is to assist developers and data analysts in manipulating [Riot APIs](https://developer.riotgames.com/apis) and making their life easier.

With optimized auto-tracking on left requests due to riot limitations and shortcuts to access data, do not worry more on how will your project access data from riot api.

Write cleaner code while being faster.

## ✅ Release
[![Version 0.0.5](https://img.shields.io/badge/0.0.5-%2316c60c.svg?style=for-the-badge&label=version)](https://test.pypi.org/project/riot-api-manipulation/)

View the package here : https://test.pypi.org/project/riot-api-manipulation/

## 💻 Getting started

### 1. Installation

###### Windows
```python
py -m pip --upgrade pip
py -m pip install --index-url https://test.pypi.org/simple/ --no-deps riot-api-manipulation 
```

###### Unix
```python
python3 -m pip --upgrade pip
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps riot-api-manipulation 
```

### 2. Important point : opening and closing

API uses threads to track left requests, API.close() terminates subprocesses.
Be aware that threads can exist during 2 to 30 minutes depending on your api-key type if api is not closed so make sure to add it at the end of a script or at the closing of your application.
```python
api_league = API_LEAGUE("YOUR_API_KEY", "europe", "euw1")
# Exploiting api [...]
api_league.close()
```

### 3. Usage examples

###### Get summoner informations
```python
api_league = API_LEAGUE("YOUR_API_KEY", "europe", "euw1")

summoner = api_league.get_summoner("SUMMONER_NAME")

api_league.close()

print(summoner)
```

###### Get summoner's last game infos
```python
api_league = API_LEAGUE("YOUR_API_KEY", "europe", "euw1")

last_match_infos = (
    api_league.get_summoner("SUMMONER_NAME")
              .get_last_game()
              .get_infos_of_summoner()
                   )

api_league.close()

print(last_match_infos)
```

###### Get summoner's last ranked games with infos and timeline
```python
api_league = API_LEAGUE("YOUR_API_KEY", "europe", "euw1")

summoner = api_league.get_summoner("SUMMONER_NAME")
last_games_full = summoner.get_match_history(nb_matches=10, queue=QueueType.RANKED, load_infos=True, load_timelines=True)

api_league.close()

for game in last_games_full:
    print(game.json)
    print(game.json_timeline)
```

## 📚 Documentation

- [Sources](./riot_api/)
