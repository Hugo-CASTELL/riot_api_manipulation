import pytest
import responses

from riot_api_manipulation import Region, Server, URL_MANAGER, API_LEAGUE


@pytest.fixture()
def setup():
    key = "KEY"
    region = Region.EUROPE
    server = Server.EU_WEST
    requests_capacity = 100000
    requests_capacity_second = requests_capacity
    return {'key': key,
            'region': region,
            'server': server,
            'requests_capacity': requests_capacity,
            'requests_capacity_second': requests_capacity_second,
            }


@pytest.fixture()
def keys():
    return {'champion_ids': {
                "freeChampionIds": [7, 13, 23, 28, 30, 43, 44, 45, 62, 64, 83, 85, 90, 110, 141, 143, 222, 236, 268, 432],
                "freeChampionIdsForNewPlayers": [222, 254, 33, 82, 131, 350, 54, 17, 18, 37, 51, 145, 134, 89, 875, 80, 115, 91, 113, 112],
                "maxNewPlayerLevel": 10},
            }


@pytest.fixture()
def basic_api_league(setup):
    return API_LEAGUE(setup['key'], setup['region'], setup['server'])


@pytest.fixture()
def url_manager(basic_api_league):
    return URL_MANAGER(basic_api_league)


@responses.activate
def test_champion_rotation(basic_api_league, url_manager, keys):
    responses.add(
        responses.GET,
        url_manager.LOL.CHAMPION_V3.champion_rotation(),
        json=keys['champion_ids']
    )

    api = basic_api_league
    champion_rotation = api.get_champions_rotation(raw_json=True)
    api.close()
    assert champion_rotation == keys['champion_ids']
