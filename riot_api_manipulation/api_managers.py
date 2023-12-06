import time
import requests
import threading
from riot_api_manipulation.enums import *
from riot_api_manipulation.urls import URL_MANAGER
from riot_api_manipulation.object_classes import *


class API_MANAGER:
    #                                            #
    # --- Constructor and built-in overrides --- #
    #                                            #
    def __init__(self, key: str, region: Region, region_server: Server, is_prod_key: bool = False,
                 custom_max_requests_capacity: int = None, custom_max_requests_capacity_per_second: int = None,
                 custom_delay_for_recovering_all_requests: int = None,
                 logs_on: bool = False):
        """
        Api manager, left requests auto-tracking, handle rate limit exceptions and has functions to reach API easily

        :param key: valid api key
        :param region: region to perform calls
        :param region_server: server to perform calls
        :param is_prod_key: define if this is a prod key
        :param custom_max_requests_capacity: by default set in init, it is possible to custom max requests
        :param custom_max_requests_capacity_per_second: by default set in init, it is possible to custom max requests per second
        :param custom_delay_for_recovering_all_requests: by default set in init, it is possible to custom recovering delay (not recommended)
        """
        #                        #
        # Helpers to connect api #
        #                        #
        self.KEY = key
        self.REGION = region.value if type(region) is Region else region
        self.REGION_SERVER = region_server.value if type(region_server) is Server else region_server
        self.URL_REGION = f"https://{self.REGION}.api.riotgames.com"
        self.URL_REGION_SERVER = f"https://{self.REGION_SERVER}.api.riotgames.com"
        self.URLS = URL_MANAGER(self)

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

        #                   #
        # Custom attributes #
        #                   #
        self.TOTAL_SENT_REQUESTS = 0
        self.logs_on = logs_on

        self.__print_log(f"{type(self)} ready")

    def __del__(self):
        # Closing on delete to avoid processes running with no father
        self.close()

    #                                     #
    # --- Manager internal mechanisms --- #
    #                                     #
    def close(self):
        """
        Closes the api manager
        """
        self.__print_log("Closing")
        # Activating the closing event to end all the threads sons
        self.CLOSING.set()

    def raise_exception(self, error_text: str):
        """
        Internal raise exception to ensure closing properly

        :param error_text: exception text
        """
        self.close()
        raise Exception(f"riot_api_manipulation: {error_text}")

    def __print_log(self, log: str):
        """
        Print log if logs are set to on

        :param log: log text
        """
        if self.logs_on:
            print(f"riot_api_manipulation: {log}")

    def not_implemented_by_riot(self):
        self.raise_exception("Not implemented by RIOT")

    def delay_requests(self, number_of_requests):
        """
        Performed asynchronously, permits to reduce empty slots of the number of requests needed and wait to add them back

        :param number_of_requests: number of requests to delay
        """
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
        """
        Called before sending requests, permits to wait synchronously to have enough slots to perform requests and then delay it

        :param number_of_requests: number of requests to wait and delay
        """
        # Critical point => number of requests by second
        if self.LEFT_REQUESTS_PER_SECOND < number_of_requests:
            # Waiting for slots
            self.__print_log(f"Waiting for requests slots in a second")
            enough_slots = self.are_there_enough_requests_slots_in_second(number_of_requests)
            iter_counter = 0
            while enough_slots is False:
                time.sleep(1)
                enough_slots = self.are_there_enough_requests_slots_in_second(number_of_requests)
                iter_counter += 1

                # Max iteration is two seconds => it means there are too much requests for apiKey capacity
                if iter_counter == 2 and enough_slots is False:
                    self.raise_exception(
                        "Impossible to run this amount of requests in a second with your apiKey capacity")

        # Waiting for enough requests slots if needed
        if self.LEFT_REQUESTS < number_of_requests:
            self.__print_log(f"Waiting for requests slots : maximum waiting {self.RIOT_RECOVERING_DELAY_IN_SECONDS}s")
            enough_slots = self.are_there_enough_requests_slots(number_of_requests)
            iter_counter = 0
            while enough_slots is False:
                time.sleep(1)
                enough_slots = self.are_there_enough_requests_slots(number_of_requests)
                iter_counter += 1

                # Max iteration is the max delay => it means there are too much requests for apiKey capacity
                if iter_counter > self.RIOT_RECOVERING_DELAY_IN_SECONDS and enough_slots is False:
                    self.raise_exception("Impossible to run this amount of requests with your apiKey capacity")

        # Threading the used slots recovering
        delay_thread = threading.Thread(target=self.delay_requests, args=(number_of_requests,))
        self.THREADS_LIST.append(delay_thread)
        delay_thread.start()

    def get_json(self, url):
        """
        Reach RIOT's API, handle errors and returns response as json

        :param url:
        :return: riot's response json
        """
        # Notifying one request used
        self.prepare_sending(1)

        # Sending requests
        self.TOTAL_SENT_REQUESTS += 1
        response = requests.get(url)

        # Common errors
        code = response.status_code

        # Checking errors
        if code == 400:
            self.raise_exception("400 : Bad request -> Url parameters problem (type, not passing regex...)")
        elif code == 401:
            self.raise_exception("401 : Unauthorized -> Api key may be expired")
        elif code == 403:
            self.raise_exception("403 : Forbidden -> Check request formulation (spelling, cases...)")
        elif code == 404:
            self.raise_exception("404 : Data not found -> Data was not found but request was well written")
        elif code == 405:
            self.raise_exception("405 : Method not allowed -> Your api key doesn't give you access to this method")
        elif code == 415:
            self.raise_exception("415 : Unsupported media type -> Change your media type")
        elif code == 500:
            self.raise_exception("500 : Internal server error -> Riot server error, consider retry")
        elif code == 502:
            self.raise_exception("502 : Bad gateway -> Absent or not enough internet connection")
        elif code == 503:
            self.raise_exception("503 : Service unavailable -> Riot service is down, retry later")
        elif code == 504:
            self.raise_exception("504 : Gateway timeout -> Absent or not enough internet connection")
        elif code == 429:  # 429 : Rate limit exceeded => delay request
            self.__print_log(f"Rate limit was exceeded, retry in {self.RIOT_RECOVERING_DELAY_IN_SECONDS}s")
            time.sleep(self.RIOT_RECOVERING_DELAY_IN_SECONDS)
            self.get_json(url)
            return

        # If no errors then return json
        json = response.json()
        return json


class API_RIOT(API_MANAGER):
    #                         #
    # --- Private helpers --- #
    #                         #
    def __process_riot_account(self, url: str, raw_json: bool):
        # Getting data
        json = self.get_json(url)

        # Exploiting data
        return json if raw_json is True else Riot_Account(json_builder=json, api_riot=self)

    #                                 #
    # --- API routes as functions --- #
    #                                 #
    # ACCOUNT V1
    def get_riot_account_by_puuid(self, puuid: str,
                                  raw_json: bool = False):
        """
        Returns riot account find by puuid

        :param puuid: consistent id across regions
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        url = self.URLS.RIOT.ACCOUNT_V1.by_puuid(puuid)

        return self.__process_riot_account(url, raw_json)

    def get_riot_account_by_ingamename_and_tagline(self, in_game_name: str, tag_line: str,
                                                   raw_json: bool = False):
        """
        Returns riot account find by in-game name and tagline

        :param in_game_name: in-game player name
        :param tag_line: playerName#01234 without #
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        url = self.URLS.RIOT.ACCOUNT_V1.by_ingamename_and_tagline(in_game_name, tag_line)

        return self.__process_riot_account(url, raw_json)

    def get_riot_account_activeshard_by_game_and_puuid(self, game_abbreviating: str, puuid: str,
                                                       raw_json: bool = False):
        """
        Returns riot account find by game abbreviating and puuid

        :param game_abbreviating: val for Valorant or lor for League Of Runeterra
        :param puuid: consistent id across regions
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        # Verifications
        if game_abbreviating not in ['val', 'lor']:
            self.not_implemented_by_riot()

        # Getting data
        url = self.URLS.RIOT.ACCOUNT_V1.by_game_and_puuid(game_abbreviating, puuid)
        json = self.get_json(url)

        # Exploiting data
        return json if raw_json is True else json['activeShard']


class API_LEAGUE(API_RIOT):
    #                         #
    # --- Private helpers --- #
    #                         #
    def __process_summoner(self, url: str, raw_json: bool):
        # Getting data
        json = self.get_json(url)

        # Exploiting data
        return json if raw_json is True else Summoner(json_builder=json, api_league=self)

    #                                 #
    # --- API routes as functions --- #
    #                                 #
    # SUMMONER V4
    def get_summoner_by_name(self, summoner_name: str,
                             raw_json: bool = False):
        """
        Returns summoner find by name

        :param summoner_name: in-game summoner name
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        url = self.URLS.LOL.SUMMONER_V4.by_summoner_name(summoner_name)

        return self.__process_summoner(url, raw_json)

    def get_summoner_by_account_id(self, account_id: str,
                                   raw_json: bool = False):
        """
        Returns summoner find by account id

        :param account_id: riot account id
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        url = self.URLS.LOL.SUMMONER_V4.by_account_id(account_id)

        return self.__process_summoner(url, raw_json)

    def get_summoner_by_puuid(self, puuid: str,
                              raw_json: bool = False):
        """
        Returns summoner find by puuid

        :param puuid: consistent id across regions
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        url = self.URLS.LOL.SUMMONER_V4.by_puuid(puuid)

        return self.__process_summoner(url, raw_json)

    def get_summoner_by_summoner_id(self, summoner_id: str,
                                    raw_json: bool = False):
        """
        Returns summoner find by summoner id

        :param summoner_id: summoner id in region
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        url = self.URLS.LOL.SUMMONER_V4.by_summoner_id(summoner_id)

        return self.__process_summoner(url, raw_json)

    # MATCH V5
    def list_match_only_ids(self, puuid: str, nb_matches: int, start_number: int = 0, queue: QueueType = None,
                            summoner_associated=None, raw_json: bool = False):
        """
        Returns a list of League_Match where only id is loaded

        :param puuid: consistent id across regions of player calling
        :param nb_matches: total of matches loaded
        :param start_number: where to start in puuid history
        :param queue: by default as None to ensure loading all matches, queue is a filter
        :param summoner_associated: object class Summoner associated if there is one
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        # Static
        max_ids_per_request = 100

        # Processing for max count
        count_divided = [max_ids_per_request for _ in range(nb_matches // max_ids_per_request)]
        count_divided.append(nb_matches % max_ids_per_request)

        # Getting data
        jsons = []
        for count in count_divided:
            # Getting json and storing it
            url = self.URLS.LOL.MATCH_V5.match_ids(puuid, start_number, count, queue)
            json = self.get_json(url)
            jsons.append(json)

            # Increasing start number
            start_number += count

        # Exploiting data
        if raw_json:
            return jsons
        else:
            league_matches = []
            for json in jsons:
                for match_id in json:
                    league_matches.append(League_Match(match_id, summoner=summoner_associated, api_league=self))
            return league_matches

    def get_match_infos(self, match_id: str,
                        raw_json: bool = False):
        """
        Returns League_Match loaded with game's infos

        :param match_id: match id
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        # Getting data
        url = self.URLS.LOL.MATCH_V5.match_infos(match_id)
        json = self.get_json(url)

        # Exploiting data
        return json if raw_json is True else League_Match(match_id, json=json, api_league=self)

    def get_match_timeline(self, match_id: str,
                           raw_json: bool = False):
        """
        Returns League_Match loaded with game's timeline

        :param match_id: match id
        :param raw_json: by default as False, permits to return raw json if set to True
        """
        # Getting data
        url = self.URLS.LOL.MATCH_V5.match_timeline(match_id)
        json = self.get_json(url)

        # Exploiting data
        return json if raw_json is True else League_Match(match_id, json_timeline=json, api_league=self)

    # CHAMPION V3
    def get_champions_rotation(self,
                               raw_json: bool = False):
        """
        Returns Champion_Rotation

        :param raw_json: by default as False, permits to return raw json if set to True
        """
        # Getting data
        url = self.URLS.LOL.CHAMPION_V3.champion_rotation()
        json = self.get_json(url)

        # Exploiting data
        return json if raw_json is True else Champion_Rotation(json_builder=json)


class API_VALORANT(API_RIOT):
    #                                 #
    # --- API routes as functions --- #
    #                                 #
    # MATCH V1
    def list_match_ids(self, puuid: str,
                       raw_json: bool = False):
        # Getting data
        url = self.URLS.VAL.MATCH_V1.match_ids(puuid)
        json = self.get_json(url)

        # Exploiting data
        return json if raw_json else [match_id for match_id in json]

    def get_match_infos(self, match_id: str):
        # Getting data
        url = self.URLS.VAL.MATCH_V1.match_infos(match_id)
        json = self.get_json(url)

        # Exploiting data
        return json
