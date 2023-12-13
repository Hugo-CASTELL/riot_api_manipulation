from riot_api_manipulation.enums import QueueType
from riot_api_manipulation.internal_helpers import json_format_str


class Riot_Account:
    #                                            #
    # --- Constructor and built-in overrides --- #
    #                                            #
    def __init__(self, puuid=None, game_name=None, tag_line=None,
                 json_builder=None,
                 api_riot=None):
        """
        Object class permitting to store a Riot Account (ACCOUNT V1) and perform shortcuts api calls

        :param puuid: consistent id across regions
        :param game_name: in-game player name
        :param tag_line: playerName#01234 without #
        :param json_builder: the RIOT's json if you have it : Note it has priority on other parameters for redefining them
        :param api_riot: manager to perform shortcuts calls
        """
        self.puuid = puuid
        self.game_name = game_name
        self.tag_line = tag_line

        if json_builder is not None:
            self.puuid = json_builder['puuid']
            self.game_name = json_builder['gameName']
            self.tag_line = json_builder['tagLine']

        self.api_riot = api_riot

    #                   #
    # --- Shortcuts --- #
    #                   #
    def get_active_shard_by_game(self, game_abbreviating: str):
        """
        Returns the active shard where is playing the Riot Account

        :param game_abbreviating: val for Valorant or lor for League Of Runeterra
        """
        if self.api_riot is None:
            raise Exception(f"Riot Account: {self.game_name}#{self.tag_line} has no internal api riot specified.")

        self.api_riot.get_riot_account_activeshard_by_game_and_puuid(game_abbreviating, self.puuid)


class Summoner:
    #                                            #
    # --- Constructor and built-in overrides --- #
    #                                            #
    def __init__(self, summoner_name=None, account_id=None, profile_icon_id=None, revision_date=None, id=None,
                 puuid=None, summoner_level=None,
                 json_builder=None,
                 api_league=None):
        """
        Object class permitting to store a Summoner (SUMMONER V4) and perform shortcuts api calls

        :param summoner_name: summoner in game name
        :param account_id: riot account id
        :param profile_icon_id: profile icon id
        :param revision_date:
        :param id: summoner id
        :param puuid: consistent id across regions
        :param summoner_level: actual summoner game level
        :param json_builder: the RIOT's json if you have it : Note it has priority on other parameters for redefining them
        :param api_league: manager to perform shortcuts calls
        """
        self.summoner_name = summoner_name
        self.account_id = account_id
        self.profile_icon_id = profile_icon_id
        self.revision_date = revision_date
        self.id = id
        self.puuid = puuid
        self.summonerLevel = summoner_level
        self.match_history = []

        if json_builder is not None:
            self.summoner_name = json_builder['name']
            self.account_id = json_builder['accountId']
            self.profile_icon_id = json_builder['profileIconId']
            self.revision_date = json_builder['revisionDate']
            self.id = json_builder['id']
            self.puuid = json_builder['puuid']
            self.summonerLevel = json_builder['summonerLevel']

        self.api_league = api_league

    def __str__(self):
        return str(vars(self))

    #                   #
    # --- Shortcuts --- #
    #                   #
    def get_match_history(self, nb_matches: int = 30, start_number: int = 0, queue: QueueType = None,
                          load_infos: bool = False, load_timelines: bool = False,
                          raw_json: bool = False):
        """
        Returns summoner's match history

        :param nb_matches: number of matches loaded
        :param start_number: start number in history
        :param queue: by default as None to ensure loading all matches, queue is a filter
        :param load_infos: by default as False, permits to load game infos for each match if set to True and raw_json is False
        :param load_timelines: by default as False, permits to load timeline for each match if set to True and raw_json is False
        :param raw_json: by default as False, permits to return raw json if set to True
        :return: list[League_Match] or string if raw_json
        """
        if self.api_league is None:
            raise Exception(f"Summoner: {self.summoner_name} has no internal api league specified.")

        # Getting data
        matches = self.api_league.list_match_only_ids(self.puuid, nb_matches, start_number, queue,
                                                      summoner_associated=self, raw_json=raw_json)

        if raw_json is False:
            # Fill match history with None when there is no space
            if len(self.match_history) < start_number+nb_matches:
                for i in range(len(self.match_history), start_number+nb_matches):
                    self.match_history.append(None)

            # Storing the match in the summoner history
            for i in range(start_number, start_number+nb_matches):
                if self.match_history[i] is None:
                    self.match_history[i] = matches[i-start_number]

            # Loading infos when necessary
            load_something: bool = load_infos is True or load_timelines is True

            if load_something is True:
                for match in self.match_history[start_number:start_number+nb_matches]:
                    if load_infos is True and load_timelines is True:
                        match.get_full_infos()
                    elif load_infos is True:
                        match.get_infos()
                    elif load_timelines is True:
                        match.get_timeline()

        return matches

    def get_last_game(self, queue: QueueType = None,
                      raw_json: bool = False):
        """
        Returns summoner's last game (id only or League_Match)

        :param queue: by default as None to ensure loading all matches, queue is a filter
        :param raw_json: by default as False, permits to return raw json if set to True
        :return: League_Match or string if raw_json
        """
        return self.get_match_history(nb_matches=1, start_number=0, queue=queue, raw_json=raw_json)[0]


class League_Match:
    #                                            #
    # --- Constructor and built-in overrides --- #
    #                                            #
    def __init__(self, match_id,
                 summoner: Summoner = None, json=None, json_timeline=None, api_league=None):
        """
        Object class permitting to store a League_Match (MATCH V5) and perform shortcuts api calls

        :param match_id: match id
        :param summoner: if there is one, the summoner where match was found in history
        :param json: raw json of game's infos (metadata and info)
        :param json_timeline: raw_json of game's timeline
        :param api_league: manager to perform shortcuts calls
        """
        self.match_id = match_id
        self.summoner = summoner
        self.api_league = api_league
        self.json = json
        self.json_timeline = json_timeline
        if json is not None:
            self.metadata = json['metadata']
            self.infos = json['info']

    def __str__(self):
        if self.infos is not None:
            return json_format_str(self.infos)
        else:
            return str(vars(self))

    def __getitem__(self, item):
        if self.json is None:
            raise Exception(f"League_Match: {self.match_id} infos (json) is not loaded.")

        return self.json['metadata'][item]

    #                   #
    # --- Shortcuts --- #
    #                   #
    def get_infos(self,
                  raw_json: bool = False):
        """
        Loads game's infos in League_Match and can return or self to perform shortcuts or raw json

        :param raw_json: by default as False, permits to return raw json if set to True
        """
        if self.json is None:
            if self.api_league is None:
                raise Exception(f"League_Match: {self.match_id} has no internal api league specified.")

            # Getting json
            json = self.api_league.get_match_infos(self.match_id, raw_json=True)

            # Processing for object
            self.json = json
            self.metadata = json['metadata']
            self.infos = json['info']

        # Return statement
        return self.json if raw_json else self

    def get_timeline(self,
                     raw_json: bool = False):
        """
        Loads game's timeline in League_Match and can return or self to perform shortcuts or raw json

        :param raw_json: by default as False, permits to return raw json if set to True
        """
        if self.json_timeline is None:
            if self.api_league is None:
                raise Exception(f"League_Match: {self.match_id} has no internal api league specified.")

            # Getting json
            json_timeline = self.api_league.get_match_timeline(self.match_id, raw_json=True)

            # Processing for object
            self.json_timeline = json_timeline

        # Return statement
        return self.json_timeline if raw_json else self

    def get_full_infos(self):
        """
        Loads game's infos and timeline in the League_Match
        """
        self.get_infos()
        self.get_timeline()
        return self

    def get_infos_of_summoner(self,
                              puuid: str = None):
        """
        Returns summoner (by default self.summoner or custom puuid) game's infos found in infos json in the League_Match
        """
        if self.summoner is None:
            raise Exception(f"League_Match: {self.match_id} has no internal summoner specified.")

        if self.json is None:
            self.get_infos()

        index = self.metadata['participants'].index(self.summoner.puuid if puuid is None else puuid)
        return self.infos['participants'][index]


class Champion_Rotation:
    #                                            #
    # --- Constructor and built-in overrides --- #
    #                                            #
    def __init__(self, max_new_player_level=None, free_champion_ids=None, free_champion_ids_for_new_players=None,
                 json_builder=None,
                 api_league=None):
        """
        Object class permitting to store a Champion_Rotation (CHAMPION V3)

        :param max_new_player_level:
        :param free_champion_ids: weekly free champions
        :param free_champion_ids_for_new_players: champions for player which level is under max_new_player_level
        :param json_builder: the RIOT's json if you have it : Note it has priority on other parameters for redefining them
        :param api_league: manager to perform shortcuts calls
        """
        self.max_new_player_level = max_new_player_level
        self.free_champion_ids = free_champion_ids
        self.free_champion_ids_for_new_players = free_champion_ids_for_new_players

        if json_builder is not None:
            self.max_new_player_level = json_builder['maxNewPlayerLevel'],
            self.free_champion_ids = json_builder['freeChampionIds'],
            self.free_champion_ids_for_new_players = json_builder['freeChampionIdsForNewPlayers']

        self.api_league = api_league

# endregion
