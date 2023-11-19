import threading
import time
import requests
from enum import Enum


# region Enums

class QueueType(Enum):
    RANKED = 'ranked'
    NORMAL = 'normal'
    TOURNAMENT = 'tourney'
    TUTORIAL = 'tutorial'


# endregion Enums

# region APIs

class API_RIOT:
    def __init__(self, key: str, region: str, region_server: str, is_prod_key: bool = False,
                 custom_max_requests_capacity: int = None, custom_max_requests_capacity_per_second: int = None,
                 custom_delay_for_recovering_all_requests: int = None):
        #                        #
        # Helpers to connect api #
        #                        #
        self.KEY = key
        self.REGION = region
        self.REGION_SERVER = region_server
        self.RIOT_URL_REGION = f"https://{region}.api.riotgames.com"
        self.RIOT_URL_REGION_SERVER = f"https://{region_server}.api.riotgames.com"

        #                              #
        # ApiKey capacity manipulation #
        #                              #
        if custom_max_requests_capacity is None:
            self.MAX_REQUESTS = 30000 if is_prod_key is True else 100
        else:
            self.MAX_REQUESTS = custom_max_requests_capacity

        self.LEFT_REQUESTS = self.MAX_REQUESTS

        if custom_max_requests_capacity_per_second is None:
            self.MAX_REQUESTS_PER_SECOND = 500 if is_prod_key is True else 20
        else:
            self.MAX_REQUESTS_PER_SECOND = custom_max_requests_capacity_per_second

        self.LEFT_REQUESTS_PER_SECOND = self.MAX_REQUESTS_PER_SECOND

        if custom_delay_for_recovering_all_requests is None:
            self.RIOT_RECOVERING_DELAY_IN_SECONDS = 600 if is_prod_key is True else 120
        else:
            self.RIOT_RECOVERING_DELAY_IN_SECONDS = custom_delay_for_recovering_all_requests

        #                      #
        # Settings for threads #
        #                      #
        self.THREADS_LIST = []
        self.CLOSING = threading.Event()

    def __del__(self):
        # Closing on delete to avoid processes running with no father
        self.close()

    def close(self):
        # Activating the closing event to end all the threads sons
        self.CLOSING.set()

    def delay_requests(self, number_of_requests):
        # Updating left requests
        self.LEFT_REQUESTS -= number_of_requests
        self.LEFT_REQUESTS_PER_SECOND -= number_of_requests

        # Starting manual clock
        delay = self.RIOT_RECOVERING_DELAY_IN_SECONDS
        one_second_passed = self.RIOT_RECOVERING_DELAY_IN_SECONDS - 1
        while delay > 0:
            # Checking if the api manager is closing
            if self.CLOSING.is_set():
                break

            # Delay of one second
            time.sleep(1)
            delay -= 1

            # Updating left requests per second
            if delay == one_second_passed:
                self.LEFT_REQUESTS_PER_SECOND += number_of_requests

        # Updating left requests
        self.LEFT_REQUESTS += number_of_requests

    def are_there_enough_requests_slots(self, needed_slots):
        return self.LEFT_REQUESTS >= needed_slots

    def are_there_enough_requests_slots_in_second(self, needed_slots):
        return self.LEFT_REQUESTS_PER_SECOND >= needed_slots

    def prepare_sending(self, number_of_requests: int):
        # Critical point => number of requests by second
        if self.LEFT_REQUESTS_PER_SECOND < number_of_requests:
            # Waiting for slots
            enough_slots = self.are_there_enough_requests_slots_in_second(number_of_requests)
            iter_counter = 0
            while enough_slots is False:
                time.sleep(1)
                enough_slots = self.are_there_enough_requests_slots_in_second(number_of_requests)
                iter_counter += 1

                # Max iteration is two seconds => it means there are too much requests for apiKey capacity
                if iter_counter == 2 and enough_slots is False:
                    raise Exception("Impossible to run this amount of requests in a second with your apiKey capacity")

        # Waiting for enough requests slots if needed
        if self.LEFT_REQUESTS < number_of_requests:
            enough_slots = self.are_there_enough_requests_slots(number_of_requests)
            iter_counter = 0
            while enough_slots is False:
                time.sleep(1)
                enough_slots = self.are_there_enough_requests_slots(number_of_requests)
                iter_counter += 1

                # Max iteration is the max delay => it means there are too much requests for apiKey capacity
                if iter_counter > self.RIOT_RECOVERING_DELAY_IN_SECONDS and enough_slots is False:
                    raise Exception("Impossible to run this amount of requests with your apiKey capacity")

        # Threading the used slots recovering
        delay_thread = threading.Thread(target=self.delay_requests, args=(number_of_requests,))
        self.THREADS_LIST.append(delay_thread)
        delay_thread.start()

    def get_riot_account_by_puuid(self, puuid: str,
                                  raw_json: bool = False):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION}/riot/account/v1/accounts/by-puuid/{puuid}?"
               f"api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json if raw_json is True else Riot_Account(puuid,
                                                          json['gameName'],
                                                          json['tagLine'],
                                                          api_riot=self)

    def get_riot_account_by_ingamename_and_tagline(self, in_game_name: str, tag_line: str,
                                                   raw_json: bool = False):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION}/riot/account/v1/accounts/by-riot-id/{in_game_name}/{tag_line}?"
               f"api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json if raw_json is True else Riot_Account(json['puuid'],
                                                          in_game_name,
                                                          tag_line,
                                                          api_riot=self)

    def get_riot_account_activeshard_by_game_and_puuid(self, game_abbreviating: str, puuid: str,
                                                       raw_json: bool = False):
        # Verifications
        if game_abbreviating not in ['val', 'lor']:
            self.not_implemented_by_riot()

        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION}/riot/account/v1/accounts/by-game/{game_abbreviating}/by-puuid/{puuid}?"
               f"api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json if raw_json is True else json['activeShard']

    def not_implemented_by_riot(self):
        raise Exception("Not implemented by riot")


class API_LEAGUE(API_RIOT):
    def get_summoner(self, summoner_name: str,
                     raw_json: bool = False):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION_SERVER}/lol/summoner/v4/summoners/by-name/{summoner_name}?"
               f"api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json if raw_json is True else Summoner(summoner_name,
                                                      json['accountId'],
                                                      json['profileIconId'],
                                                      json['revisionDate'],
                                                      json['id'],
                                                      json['puuid'],
                                                      json['summonerLevel'],
                                                      api_league=self)

    def list_match_ids(self, puuid: str, nb_matches: int, start_number: int = 0, queue: QueueType = None,
                       raw_json: bool = False):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION}/lol/match/v5/matches/by-puuid/{puuid}/ids?"
               f"start={start_number}"
               f"&count={nb_matches}"
               f"{f'&type={queue.value}' if queue is not None else ''}"
               f"&api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json if raw_json is True else [match_id for match_id in json]

    def get_match_info(self, match_id: str):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION}/lol/match/v5/matches/{match_id}?"
               f"api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json


class API_VALORANT(API_RIOT):
    def list_match_ids(self, puuid: str,
                       raw_json: bool = False):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION}/val/match/v1/matchlists/by-puuid/{puuid}?"
               f"api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json if raw_json else [match_id for match_id in json]

    def get_match_info(self, match_id: str):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION}/val/match/v1/matches/{match_id}?"
               f"api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json

# endregion APIs


# region Object classes

class Riot_Account:
    def __init__(self, puuid, game_name, tag_line,
                 api_riot: API_RIOT = None):
        self.puuid = puuid
        self.game_name = game_name
        self.tag_line = tag_line
        self.api_riot = api_riot

    def get_active_shard_by_game(self, game_abbreviating: str):
        if self.api_riot is None:
            raise Exception(f"Riot Account: {self.game_name}#{self.tag_line} has no internal api riot specified.")

        self.api_riot.get_riot_account_activeshard_by_game_and_puuid(game_abbreviating, self.puuid)


class Summoner:
    def __init__(self, summoner_name, account_id, profile_icon_id, revision_date, id, puuid, summoner_level,
                 api_league: API_LEAGUE = None):
        self.summoner_name = summoner_name
        self.account_id = account_id
        self.profile_icon_id = profile_icon_id
        self.revision_date = revision_date
        self.id = id
        self.puuid = puuid
        self.summonerLevel = summoner_level
        self.api_league = api_league

    def get_match_history(self, nb_matches: int = 30, start_number: int = 0, queue: QueueType = None,
                          raw_json: bool = False):
        if self.api_league is None:
            raise Exception(f"Summoner: {self.summoner_name} has no internal api league specified.")

        return self.api_league.list_match_ids(self.puuid, nb_matches, start_number, queue, raw_json)

# endregion
