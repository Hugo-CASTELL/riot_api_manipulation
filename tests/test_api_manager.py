import time
import pytest

from riot_api_manipulation import API_RIOT, Region, Server


@pytest.fixture()
def setup():
    key = "KEY"
    region = Region.EUROPE
    server = Server.EU_WEST
    return {'key': key,
            'region': region,
            'expected-region-url': f"https://{region.value}.api.riotgames.com",
            'server': server,
            'expected-server-url': f"https://{server.value}.api.riotgames.com",
            }


@pytest.fixture()
def basic_api_riot(setup):
    return API_RIOT(setup['key'], setup['region'], setup['server'], debug=False)


@pytest.fixture()
def basic_api_riot_prod_key(setup):
    return API_RIOT(setup['key'], setup['region'], setup['server'], debug=False, is_prod_key=True)


@pytest.fixture()
def depleted_requests_api_riot(basic_api_riot):
    api = basic_api_riot
    api.LEFT_REQUESTS -= api.MAX_REQUESTS
    api.TOTAL_SENT_REQUESTS = api.MAX_REQUESTS
    return api


@pytest.fixture()
def depleted_requests_api_riot_prod_key(basic_api_riot_prod_key):
    api = basic_api_riot_prod_key
    api.LEFT_REQUESTS -= api.MAX_REQUESTS
    api.TOTAL_SENT_REQUESTS = api.MAX_REQUESTS
    return api


@pytest.fixture()
def closed_api_riot(depleted_requests_api_riot):
    api = depleted_requests_api_riot
    api.close()
    return api


@pytest.fixture()
def closed_api_riot_prod_key(depleted_requests_api_riot_prod_key):
    api = depleted_requests_api_riot_prod_key
    api.close()
    return api


def test_setup(setup, closed_api_riot):
    api = closed_api_riot
    assert api.URL_REGION == setup['expected-region-url']
    assert api.URL_REGION_SERVER == setup['expected-server-url']


def test_prod_key(closed_api_riot, closed_api_riot_prod_key):
    api = closed_api_riot
    api_prod_key = closed_api_riot_prod_key
    assert api.LEFT_REQUESTS == api_prod_key.LEFT_REQUESTS
    assert api.MAX_REQUESTS < api_prod_key.MAX_REQUESTS
    assert api.MAX_REQUESTS_PER_SECOND < api_prod_key.MAX_REQUESTS_PER_SECOND


def test_api_opening(basic_api_riot):
    api = basic_api_riot
    api.close()
    assert api is not None


def test_api_has_no_left_requests(depleted_requests_api_riot):
    api = depleted_requests_api_riot
    api.close()
    assert api.LEFT_REQUESTS == 0


def test_api_is_well_closed(closed_api_riot):
    api = closed_api_riot
    # Waiting for all the threads to end
    time.sleep(1.5)
    assert api.CLOSING.is_set()
    assert bool(True in [thread.is_alive() for thread in api.THREADS_LIST]) is False


def test_prepare_sending(basic_api_riot):
    api = basic_api_riot
    requests_number = round(api.MAX_REQUESTS_PER_SECOND/2)
    api.prepare_sending(requests_number)
    api.close()
    assert api.LEFT_REQUESTS == api.MAX_REQUESTS - requests_number
    assert len(api.THREADS_LIST) == 1
