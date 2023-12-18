class URL_Skeleton:
    #                                            #
    # --- Constructor and built-in overrides --- #
    #                                            #
    def __init__(self, api):
        self.api = api

        # Shortcuts
        self.reg = api.URL_REGION
        self.svr = api.URL_REGION_SERVER
        self.key = f"api_key={api.KEY}"


class ACCOUNT_V1(URL_Skeleton):
    def base(self):
        return f"{self.reg}/riot/account/v1"

    def by_puuid(self, puuid) -> str:
        return f"{self.base()}/accounts/by-puuid/{puuid}?{self.key}"

    def by_ingamename_and_tagline(self, in_game_name, tag_line) -> str:
        return f"{self.base()}/accounts/by-riot-id/{in_game_name}/{tag_line}?{self.key}"

    def by_game_and_puuid(self, game_abbreviating, puuid) -> str:
        return f"{self.base()}/accounts/by-game/{game_abbreviating}/by-puuid/{puuid}?{self.key}"


class RIOT:
    def __init__(self, api):
        self.ACCOUNT_V1 = ACCOUNT_V1(api)


class SUMMONER_V4(URL_Skeleton):
    def base(self):
        return f"{self.svr}/lol/summoner/v4"

    def by_summoner_name(self, name) -> str:
        return f"{self.base()}/summoners/by-name/{name}?{self.key}"

    def by_account_id(self, account_id) -> str:
        return f"{self.base()}/summoners/by-account/{account_id}?{self.key}"

    def by_puuid(self, puuid) -> str:
        return f"{self.base()}/summoners/by-puuid/{puuid}?{self.key}"

    def by_summoner_id(self, summoner_id) -> str:
        return f"{self.base()}/summoners/{summoner_id}?{self.key}"


class MATCH_V5(URL_Skeleton):
    def base(self):
        return f"{self.reg}/lol/match/v5"

    def match_ids(self, puuid, start_number, count, queue):
        return (f"{self.base()}/matches/by-puuid/{puuid}/ids?"
                f"start={start_number}"
                f"&count={count}"
                f"{f'&type={queue.value}' if queue is not None else ''}"
                f"&{self.key}")

    def match_infos(self, match_id):
        return f"{self.base()}/matches/{match_id}?{self.key}"

    def match_timeline(self, match_id):
        return f"{self.base()}/matches/{match_id}/timeline?{self.key}"


class CHAMPION_V3(URL_Skeleton):
    def base(self):
        return f"{self.svr}/lol/platform/v3"

    def champion_rotation(self):
        return f"{self.base()}/champion-rotations?{self.key}"


class LOL:
    def __init__(self, api):
        self.ACCOUNT_V1 = ACCOUNT_V1(api)
        self.SUMMONER_V4 = SUMMONER_V4(api)
        self.MATCH_V5 = MATCH_V5(api)
        self.CHAMPION_V3 = CHAMPION_V3(api)


class MATCH_V1(URL_Skeleton):
    def base(self):
        return f"{self.reg}/val/match/v1"

    def match_ids(self, puuid):
        return f"{self.base()}/matchlists/by-puuid/{puuid}?{self.key}"

    def match_infos(self, match_id):
        return f"{self.base()}/matches/{match_id}?{self.key}"


class VAL:
    def __init__(self, api):
        self.MATCH_V1 = MATCH_V1(api)


class URL_MANAGER:
    #                                            #
    # --- Constructor and built-in overrides --- #
    #                                            #
    def __init__(self, api):
        self.RIOT = RIOT(api)
        self.LOL = LOL(api)
        self.VAL = VAL(api)
