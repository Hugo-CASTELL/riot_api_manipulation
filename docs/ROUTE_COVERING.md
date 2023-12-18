# APIs' covering [Work in progress] 

## ACCOUNT-V1 ![](https://geps.dev/progress/75)

|   | route                                                     | function                                                  |
|---|-----------------------------------------------------------|-----------------------------------------------------------|
| ✅ | /riot/account/v1/accounts/by-puuid/{puuid}                | API_RIOT.get_riot_account_by_puuid()                      |
| ✅ | /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine} | API_RIOT.get_riot_account_by_ingamename_and_tagline()     |
| ✅ | /riot/account/v1/accounts/by-game/{game}/by-puuid/{puuid} | API_RIOT.get_riot_account_activeshard_by_game_and_puuid() |
| ❌ | /riot/account/v1/accounts/me                              |                                                           |

## CHAMPION-MASTERY-V4 ![](https://geps.dev/progress/0)

## CHAMPION-V3 ![](https://geps.dev/progress/100)

|   | route                               | function                            |
|---|-------------------------------------|-------------------------------------|
| ✅ | /lol/platform/v3/champion-rotations | API_LEAGUE.get_champions_rotation() |

## CLASH-V1 ![](https://geps.dev/progress/0)

## LEAGUE-EXP-V4 ![](https://geps.dev/progress/0)

|   | route                                                | function |
|---|------------------------------------------------------|----------|
| ❌ | /lol/league-exp/v4/entries/{queue}/{tier}/{division} |          |

## LEAGUE-V4 ![](https://geps.dev/progress/0)

## LOL-CHALLENGES-V1 ![](https://geps.dev/progress/0)

## LOL-STATUS-V3 ![](https://geps.dev/progress/0)

|   | route                     | function |
|---|---------------------------|----------|
| ❌ | /lol/status/v3/shard-data |          |
 
## LOL-STATUS-V4 ![](https://geps.dev/progress/0)

|   | route                        | function |
|---|------------------------------|----------|
| ❌ | /lol/status/v4/platform-data |          |

## LOR-DECK-V1 ![](https://geps.dev/progress/0)

|   | route                 | method | function |
|---|-----------------------|--------|----------|
| ❌ | /lor/deck/v1/decks/me | GET    |          |
| ❌ | /lor/deck/v1/decks/me | POST   |          |

## LOR-INVENTORY-V1 ![](https://geps.dev/progress/0)

|   | route                      | function |
|---|----------------------------|----------|
| ❌ | /lor/inventory/v1/cards/me |          |

## LOR-MATCH-V1 ![](https://geps.dev/progress/0)

|   | route                                      | function |
|---|--------------------------------------------|----------|
| ❌ | /lor/match/v1/matches/by-puuid/{puuid}/ids |          |
| ❌ | /lor/match/v1/matches/{matchId}            |          |

## LOR-RANKED-V1 ![](https://geps.dev/progress/0)

## LOR-STATUS-V1 ![](https://geps.dev/progress/0)

## MATCH-V5 ![](https://geps.dev/progress/0)

## SPECTATOR-V4 ![](https://geps.dev/progress/0)

## SUMMONER-V4 ![](https://geps.dev/progress/66)

|   | route                                                      | function                                 |
|---|------------------------------------------------------------|------------------------------------------|
| ❌ | /fulfillment/v1/summoners/by-puuid/{rsoPUUID}              |                                          |
| ✅ | /lol/summoner/v4/summoners/by-account/{encryptedAccountId} | API_LEAGUE.get_summoner_by_account_id()  |
| ✅ | /lol/summoner/v4/summoners/by-name/{summonerName}          | API_LEAGUE.get_summoner_by_name()        |
| ✅ | /lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}       | API_LEAGUE.get_summoner_by_puuid()       |
| ❌ | /lol/summoner/v4/summoners/me                              |                                          |
| ✅ | /lol/summoner/v4/summoners/{encryptedSummonerId}           | API_LEAGUE.get_summoner_by_summoner_id() |

## TFT-LEAGUE-V1 ![](https://geps.dev/progress/0)

## TFT-MATCH-V1 ![](https://geps.dev/progress/0)

## TFT-STATUS-V1 ![](https://geps.dev/progress/0)

## TFT-SUMMONER-V1 ![](https://geps.dev/progress/0)

## TOURNAMENT-STUB-V5 ![](https://geps.dev/progress/0)

## TOURNAMENT-V5 ![](https://geps.dev/progress/0)

## VAL-CONTENT-V1 ![](https://geps.dev/progress/0)

## VAL-MATCH-V1 ![](https://geps.dev/progress/0)

## VAL-RANKED-V1 ![](https://geps.dev/progress/0)

## VAL-STATUS-V1 ![](https://geps.dev/progress/0)

## EVERYTHING IS NOT IMPLEMENTED YET !
