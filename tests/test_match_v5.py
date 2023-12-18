import pytest
import responses

from riot_api_manipulation import Region, Server, URL_MANAGER, API_LOL, Summoner, Lol_Match


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
    return {'match_ids': ["EUR_1234567890", "EUR_0987654321", "EUR_1357913579", "EUR_2468135790"],
            'match_id_example': "EUR_1234567890",
            'timeline_example': {
                "timeline": {}
            },
            'json_example': {
                "metadata": {
                    "dataVersion": "2",
                    "matchId": "EUR_1234567890",
                    "participants": [
                        "test",
                        "test",
                        "test",
                        "test",
                        "test",
                        "test",
                        "test",
                        "test",
                        "test",
                        "test"
                    ]
                },
                "info": {
                    "gameCreation": 1700528898151,
                    "gameDuration": 2141,
                    "gameEndTimestamp": 1700531065066,
                    "gameId": 1,
                    "gameMode": "CLASSIC",
                    "gameName": "teambuilder-match-1",
                    "gameStartTimestamp": 1700528924184,
                    "gameType": "MATCHED_GAME",
                    "gameVersion": "13.22.541.9804",
                    "mapId": 11,
                    "participants": [
                        {"infos_of_first_player": "test"},
                        {"infos_of_second_player": "test"},
                        {"infos_of_third_player": "test"},
                        {"infos_of_fourth_player": "test"},
                        {"infos_of_fifth_player": "test"},
                        {"infos_of_sixth_player": "test"},
                        {"infos_of_seventh_player": "test"},
                        {"infos_of_eighth_player": "test"},
                        {"infos_of_ninth_player": "test"},
                        {"infos_of_tenth_player": "test"}
                    ],
                }
            }
            }


@pytest.fixture()
def summoner_keys():
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
    return API_LOL(setup['key'], setup['region'], setup['server'], logs_on=False)


@pytest.fixture()
def url_manager(basic_api_league):
    return URL_MANAGER(basic_api_league)


@pytest.fixture()
@responses.activate
def summoner(basic_api_league, url_manager, summoner_keys):
    responses.add(
        responses.GET,
        url_manager.LOL.SUMMONER_V4.by_summoner_name(summoner_keys['name']),
        json={
            "id": summoner_keys['id'],
            "accountId": summoner_keys['accountId'],
            "puuid": summoner_keys['puuid'],
            "name": summoner_keys['name'],
            "profileIconId": summoner_keys['profileIconId'],
            "revisionDate": summoner_keys['revisionDate'],
            "summonerLevel": summoner_keys['summonerLevel']
        }
    )
    api = basic_api_league
    summoner: Summoner = api.get_summoner_by_name(summoner_keys['name'])
    api.close()
    return summoner


@responses.activate
def test_match_ids(basic_api_league, summoner, url_manager, summoner_keys, keys):
    start: int = 0
    count: int = 2
    responses.add(
        responses.GET,
        url_manager.LOL.MATCH_V5.match_ids(summoner_keys['puuid'], start, count, None),
        json=keys['match_ids'][start:count],
        status=200,
        content_type='application/json',
    )

    api = basic_api_league
    found_summoner: Summoner = summoner
    match_ids: list[Lol_Match] = api.list_match_only_ids(summoner.puuid, count, start,
                                                         summoner_associated=found_summoner)
    api.close()
    assert [match.match_id for match in match_ids] == keys['match_ids'][start:count]
    assert len(summoner.match_history) == 0


@responses.activate
def test_match_infos(basic_api_league, summoner, url_manager, summoner_keys, keys):
    responses.add(
        responses.GET,
        url_manager.LOL.MATCH_V5.match_infos(keys['match_id_example']),
        json=keys['json_example'],
    )

    api = basic_api_league
    match: Lol_Match = api.get_match_infos(keys['match_id_example'])
    api.close()
    assert match.match_id == keys['match_id_example']
    assert match.json == keys['json_example']


@responses.activate
def test_match_infos(basic_api_league, summoner, url_manager, summoner_keys, keys):
    responses.add(
        responses.GET,
        url_manager.LOL.MATCH_V5.match_timeline(keys['match_id_example']),
        json=keys['timeline_example'],
    )

    api = basic_api_league
    match: Lol_Match = api.get_match_timeline(keys['match_id_example'])
    api.close()
    assert match.match_id == keys['match_id_example']
    assert match.json_timeline == keys['timeline_example']
