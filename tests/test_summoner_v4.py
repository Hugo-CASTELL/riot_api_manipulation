import pytest
import responses

from riot_api_manipulation import Region, Server, URL_MANAGER, API_LEAGUE, Summoner


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
    return {'id': "id_expected",
            'accountId': "accountId_expected",
            'puuid': "puuid_expected",
            'name': "name_expected",
            'profileIconId': "profileIconId_expected",
            'revisionDate': "revisionDate_expected",
            'summonerLevel': 300
            }


@pytest.fixture()
def basic_api_league(setup):
    return API_LEAGUE(setup['key'], setup['region'], setup['server'])


@pytest.fixture()
def url_manager(basic_api_league):
    return URL_MANAGER(basic_api_league)


@responses.activate
def test_summoner_by_puuid(basic_api_league, url_manager, keys):
    responses.add(
        responses.GET,
        url_manager.LOL.SUMMONER_V4.by_puuid(keys['puuid']),
        json={
            "id": keys['id'],
            "accountId": keys['accountId'],
            "puuid": keys['puuid'],
            "name": keys['name'],
            "profileIconId": keys['profileIconId'],
            "revisionDate": keys['revisionDate'],
            "summonerLevel": keys['summonerLevel']
        }
    )

    api = basic_api_league
    summoner: Summoner = api.get_summoner_by_puuid(keys['puuid'])
    api.close()
    assert summoner.api_league is api
    assert summoner.id == keys['id']
    assert summoner.puuid == keys['puuid']
    assert summoner.account_id == keys['accountId']
    assert summoner.summoner_name == keys['name']
    assert summoner.profile_icon_id == keys['profileIconId']
    assert summoner.revision_date == keys['revisionDate']
    assert summoner.summonerLevel == keys['summonerLevel']


@responses.activate
def test_summoner_by_summoner_id(basic_api_league, url_manager, keys):
    responses.add(
        responses.GET,
        url_manager.LOL.SUMMONER_V4.by_summoner_id(keys['id']),
        json={
            "id": keys['id'],
            "accountId": keys['accountId'],
            "puuid": keys['puuid'],
            "name": keys['name'],
            "profileIconId": keys['profileIconId'],
            "revisionDate": keys['revisionDate'],
            "summonerLevel": keys['summonerLevel']
        }
    )

    api = basic_api_league
    summoner: Summoner = api.get_summoner_by_summoner_id(keys['id'])
    api.close()
    assert summoner.api_league is api
    assert summoner.id == keys['id']
    assert summoner.puuid == keys['puuid']
    assert summoner.account_id == keys['accountId']
    assert summoner.summoner_name == keys['name']
    assert summoner.profile_icon_id == keys['profileIconId']
    assert summoner.revision_date == keys['revisionDate']
    assert summoner.summonerLevel == keys['summonerLevel']


@responses.activate
def test_summoner_by_summoner_name(basic_api_league, url_manager, keys):
    responses.add(
        responses.GET,
        url_manager.LOL.SUMMONER_V4.by_summoner_name(keys['name']),
        json={
            "id": keys['id'],
            "accountId": keys['accountId'],
            "puuid": keys['puuid'],
            "name": keys['name'],
            "profileIconId": keys['profileIconId'],
            "revisionDate": keys['revisionDate'],
            "summonerLevel": keys['summonerLevel']
        }
    )

    api = basic_api_league
    summoner: Summoner = api.get_summoner_by_name(keys['name'])
    api.close()
    assert summoner.api_league is api
    assert summoner.id == keys['id']
    assert summoner.puuid == keys['puuid']
    assert summoner.account_id == keys['accountId']
    assert summoner.summoner_name == keys['name']
    assert summoner.profile_icon_id == keys['profileIconId']
    assert summoner.revision_date == keys['revisionDate']
    assert summoner.summonerLevel == keys['summonerLevel']


@responses.activate
def test_summoner_by_summoner_account_id(basic_api_league, url_manager, keys):
    responses.add(
        responses.GET,
        url_manager.LOL.SUMMONER_V4.by_account_id(keys['accountId']),
        json={
            "id": keys['id'],
            "accountId": keys['accountId'],
            "puuid": keys['puuid'],
            "name": keys['name'],
            "profileIconId": keys['profileIconId'],
            "revisionDate": keys['revisionDate'],
            "summonerLevel": keys['summonerLevel']
        }
    )

    api = basic_api_league
    summoner: Summoner = api.get_summoner_by_account_id(keys['accountId'])
    api.close()
    assert summoner.api_league is api
    assert summoner.id == keys['id']
    assert summoner.puuid == keys['puuid']
    assert summoner.account_id == keys['accountId']
    assert summoner.summoner_name == keys['name']
    assert summoner.profile_icon_id == keys['profileIconId']
    assert summoner.revision_date == keys['revisionDate']
    assert summoner.summonerLevel == keys['summonerLevel']
