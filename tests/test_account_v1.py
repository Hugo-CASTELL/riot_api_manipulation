import pytest
import responses

from riot_api_manipulation import API_RIOT, Region, Server, URL_MANAGER, Riot_Account


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
    return {'puuid': "puuid_expected",
            'gameName': "gameName_expected",
            'tagLine': "tagLine_expected",
            'game': "val",
            'activeShard': "eu",
            }


@pytest.fixture()
def basic_api_riot(setup):
    return API_RIOT(setup['key'], setup['region'], setup['server'], logs_on=False)


@pytest.fixture()
def url_manager(basic_api_riot):
    return URL_MANAGER(basic_api_riot)


@responses.activate
def test_account_by_puuid(basic_api_riot, url_manager, keys):
    responses.add(
        responses.GET,
        url_manager.RIOT.ACCOUNT_V1.by_puuid(keys['puuid']),
        json={
            "puuid": keys['puuid'],
            "gameName": keys['gameName'],
            "tagLine": keys['tagLine']
        }
    )

    api = basic_api_riot
    riot_account: Riot_Account = api.get_riot_account_by_puuid(keys['puuid'])
    api.close()
    assert riot_account.api_riot is api
    assert riot_account.puuid == keys['puuid']
    assert riot_account.game_name == keys['gameName']
    assert riot_account.tag_line == keys['tagLine']


@responses.activate
def test_account_by_ingamename_and_tagline(basic_api_riot, url_manager, keys):
    responses.add(
        responses.GET,
        url_manager.RIOT.ACCOUNT_V1.by_ingamename_and_tagline(keys['gameName'], keys['tagLine']),
        json={
            "puuid": keys['puuid'],
            "gameName": keys['gameName'],
            "tagLine": keys['tagLine']
        }
    )

    api = basic_api_riot
    riot_account: Riot_Account = api.get_riot_account_by_ingamename_and_tagline(keys['gameName'], keys['tagLine'])
    api.close()
    assert riot_account.api_riot is api
    assert riot_account.puuid == keys['puuid']
    assert riot_account.game_name == keys['gameName']
    assert riot_account.tag_line == keys['tagLine']


@responses.activate
def test_account_activeshard(basic_api_riot, url_manager, keys):
    responses.add(
        responses.GET,
        url_manager.RIOT.ACCOUNT_V1.by_game_and_puuid(keys['game'], keys['tagLine']),
        json={
            "puuid": keys['puuid'],
            "game": keys['game'],
            "activeShard": keys['activeShard']
        }
    )

    api = basic_api_riot
    active_shard: str = api.get_riot_account_activeshard_by_game_and_puuid(keys['game'], keys['tagLine'])
    api.close()
    assert active_shard == keys['activeShard']
