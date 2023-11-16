import time
import requests
import threading
from enum import Enum


class QueueType(Enum):
    RANKED = 'ranked'
    NORMAL = 'normal'
    TOURNAMENT = 'tourney'
    TUTORIAL = 'tutorial'


class Summoner:
    def __init__(self, summoner_name, account_id, profileicon_id, revision_date, id, puuid, summoner_level):
        self.summoner_name = summoner_name
        self.account_id = account_id
        self.profileicon_id = profileicon_id
        self.revision_date = revision_date
        self.id = id
        self.puuid = puuid
        self.summonerLevel = summoner_level


class API:
    def __init__(self, key: str, region: str, region_server: str):
        self.KEY = key
        self.REGION = region
        self.REGION_SERVER = region_server
        self.RIOT_URL_REGION = f"https://{region}.api.riotgames.com"
        self.RIOT_URL_RSERVER = f"https://{region_server}.api.riotgames.com"
        self.LEFT_REQUESTS = 100
        self.RIOT_RECOVERING_DELAY_IN_SECONDS = 40

    def delay_requests(self, number_of_requests):
        self.LEFT_REQUESTS -= number_of_requests
        time.sleep(self.RIOT_RECOVERING_DELAY_IN_SECONDS)
        self.LEFT_REQUESTS += number_of_requests

    def are_there_enough_requests_slots(self, needed_slots):
        return self.LEFT_REQUESTS >= needed_slots

    def prepare_sending(self, number_of_requests: int):
        # Waiting for enough requests slots if needed
        if self.LEFT_REQUESTS < number_of_requests:
            enough_slots = self.are_there_enough_requests_slots(number_of_requests)
            while enough_slots is False:
                time.sleep(0.5)
                enough_slots = self.are_there_enough_requests_slots(number_of_requests)

        # Threading the used slots recovering
        delay_thread = threading.Thread(target=self.delay_requests, args=(number_of_requests,))
        delay_thread.start()

    def get_summoner(self, summoner_name: str) -> Summoner:
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = f"{self.RIOT_URL_RSERVER}/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={self.KEY}"
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return Summoner(summoner_name,
                        json['accountId'],
                        json['profileIconId'],
                        json['revisionDate'],
                        json['id'],
                        json['puuid'],
                        json['summonerLevel'])

    def list_match_ids(self, puuid: str, nb_matches: int, start_number: int = 0, queue: QueueType = None):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = (f"{self.RIOT_URL_REGION}/lol/match/v5/matches/by-puuid/{puuid}/ids"
               f"?start={start_number}&count={nb_matches}{f'&type={queue.value}' if queue is not None else ''}"
               f"?api_key={self.KEY}")
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return [match_id for match_id in json]

    def get_match_info(self, match_id: str):
        # Needing only one request
        self.prepare_sending(1)

        # Getting data
        url = f"{self.RIOT_URL_REGION}/lol/match/v5/matches/{match_id}?api_key={self.KEY}"
        response = requests.get(url)

        # Exploiting data
        json = response.json()
        return json
