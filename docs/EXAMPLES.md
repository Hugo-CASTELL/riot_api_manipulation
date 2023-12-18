# Usage examples

Feel free to ask more in the wiki section or to open an issue.

Enhance your json exploring experience with: 
* [JSON Hero](https://jsonhero.io/) 
* [JSON Formatter](https://jsonformatter.org/json-viewer)
* [JSON Viewer of Code Beautify](https://codebeautify.org/jsonviewer)

#### Get summoner's last game infos
*Note:* Seen in the [README](../README.md)

Code : 
```python
# Opening the api manager with a key, a region and a server
api_lol = API_LOL("YOUR_API_KEY", Region.EUROPE, Server.EU_WEST)

# Getting summoner's details
summoner = api_lol.get_summoner_by_name("SUMMONER_NAME")

# Recovering his last game and searching his infos in it
last_match_infos = (summoner.get_last_game()
                    .get_infos_of_summoner())

# Closing the api manager (for threads, as said earlier !)
api_lol.close()

# Enjoy results
print(summoner)
print(last_match_infos)
```

Output example :
```
print(summoner) :
{'summoner_name': 'Worst Picks Ever', 'account_id': 'OgdZzv6Xpf7E5fCUM2QOrtNYk5MNVu6y0ean-VUtwNCaIRhAClshkqtc', 'profile_icon_id': 4353, 'revision_date': 1700531095000, 'id': 'dk55vo6pnyXLk4Ofonkw9yhfjtzcA391Eb5f8PLuqLVsxB10', 'puuid': 'WAsQ1dcV4SHWIZE7DmkN1QaTeHsIA_Hihch4S71xA0MucHIYuNGwydTg-AaAVhvae7l0OZgTPh6Cdg', 'summonerLevel': 302, 'match_history': [<riot_api_manipulation.object_classes.Lol_Match object at 0x0000024F37865340>], 'api_league': <riot_api_manipulation.api_managers.API_LOL object at 0x0000024F35482FD0>}
print(last_match_infos):
{'allInPings': 0, 'assistMePings': 4, 'assists': 2, 'baitPings': 0, 'baronKills': 0, 'basicPings': 0, 'bountyLevel': 0, 'challenges': {'12AssistStreakCount': 0, 'abilityUses': 425, 'acesBefore15Minutes': 0, 'alliedJungleMonsterKills': 61, 'baronTakedowns': 0, 'blastConeOppositeOpponentCount': 0, 'bountyGold': 1100, 'buffsStolen': 1, 'completeSupportQuestInTime': 0, 'controlWardTimeCoverageInRiverOrEnemyHalf': 0.6199653758399828, 'controlWardsPlaced': 1, 'damagePerMinute': 1070.7049171346737, 'damageTakenOnTeamPercentage': 0.26649093531131024, 'dancedWithRiftHerald': 0, 'deathsByEnemyChamps': 8, 'dodgeSkillShotsSmallWindow': 30, 'doubleAces': 0, 'dragonTakedowns': 2, 'earliestDragonTakedown': 870.1184601, 'earlyLaningPhaseGoldExpAdvantage': 0, 'effectiveHealAndShielding': 0, 'elderDragonKillsWithOpposingSoul': 0, 'elderDragonMultikills': 0, 'enemyChampionImmobilizations': 26, 'enemyJungleMonsterKills': 18, 'epicMonsterKillsNearEnemyJungler': 0, 'epicMonsterKillsWithin30SecondsOfSpawn': 0, 'epicMonsterSteals': 0, 'epicMonsterStolenWithoutSmite': 0, 'firstTurretKilled': 1, 'firstTurretKilledTime': 849.472711, 'flawlessAces': 0, 'fullTeamTakedown': 0, 'gameLength': 2141.1166642999997, 'goldPerMinute': 452.5045347385372, 'hadOpenNexus': 0, 'highestChampionDamage': 1, 'immobilizeAndKillWithAlly': 7, 'initialBuffCount': 2, 'initialCrabCount': 1, 'jungleCsBefore10Minutes': 76.00000011920929, 'junglerKillsEarlyJungle': 0, 'junglerTakedownsNearDamagedEpicMonster': 1, 'kTurretsDestroyedBeforePlatesFall': 0, 'kda': 2, 'killAfterHiddenWithAlly': 1, 'killParticipation': 0.47058823529411764, 'killedChampTookFullTeamDamageSurvived': 0, 'killingSprees': 1, 'killsNearEnemyTurret': 0, 'killsOnLanersEarlyJungleAsJungler': 0, 'killsOnRecentlyHealedByAramPack': 0, 'killsUnderOwnTurret': 1, 'killsWithHelpFromEpicMonster': 0, 'knockEnemyIntoTeamAndKill': 0, 'landSkillShotsEarlyGame': 0, 'laneMinionsFirst10Minutes': 0, 'laningPhaseGoldExpAdvantage': 1, 'legendaryCount': 0, 'lostAnInhibitor': 0, 'maxCsAdvantageOnLaneOpponent': 40.5, 'maxKillDeficit': 0, 'maxLevelLeadLaneOpponent': 2, 'mejaisFullStackInTime': 0, 'moreEnemyJungleThanOpponent': -40.00000002980232, 'multiKillOneSpell': 1, 'multiTurretRiftHeraldCount': 0, 'multikills': 0, 'multikillsAfterAggressiveFlash': 0, 'mythicItemUsed': 6665, 'outerTurretExecutesBefore10Minutes': 0, 'outnumberedKills': 4, 'outnumberedNexusKill': 0, 'perfectDragonSoulsTaken': 0, 'perfectGame': 0, 'pickKillWithAlly': 6, 'playedChampSelectPosition': 1, 'poroExplosions': 0, 'quickCleanse': 0, 'quickFirstTurret': 0, 'quickSoloKills': 0, 'riftHeraldTakedowns': 2, 'saveAllyFromDeath': 0, 'scuttleCrabKills': 4, 'skillshotsDodged': 172, 'skillshotsHit': 0, 'snowballsHit': 0, 'soloBaronKills': 0, 'soloKills': 8, 'stealthWardsPlaced': 14, 'survivedSingleDigitHpCount': 1, 'survivedThreeImmobilizesInFight': 11, 'takedownOnFirstTurret': 0, 'takedowns': 16, 'takedownsAfterGainingLevelAdvantage': 0, 'takedownsBeforeJungleMinionSpawn': 0, 'takedownsFirstXMinutes': 4, 'takedownsInAlcove': 0, 'takedownsInEnemyFountain': 0, 'teamBaronKills': 0, 'teamDamagePercentage': 0.29840268010354914, 'teamElderDragonKills': 0, 'teamRiftHeraldKills': 2, 'tookLargeDamageSurvived': 1, 'turretPlatesTaken': 3, 'turretTakedowns': 1, 'turretsTakenWithRiftHerald': 5, 'twentyMinionsIn3SecondsCount': 0, 'twoWardsOneSweeperCount': 0, 'unseenRecalls': 0, 'visionScoreAdvantageLaneOpponent': 0.8592017889022827, 'visionScorePerMinute': 0.9635695294005977, 'wardTakedowns': 2, 'wardTakedownsBefore20M': 1, 'wardsGuarded': 0}, 'champExperience': 18203, 'champLevel': 17, 'championId': 200, 'championName': 'Belveth', 'championTransform': 0, 'commandPings': 1, 'consumablesPurchased': 3, 'damageDealtToBuildings': 467, 'damageDealtToObjectives': 41750, 'damageDealtToTurrets': 467, 'damageSelfMitigated': 70135, 'dangerPings': 0, 'deaths': 8, 'detectorWardsPlaced': 1, 'doubleKills': 0, 'dragonKills': 1, 'eligibleForProgression': True, 'enemyMissingPings': 0, 'enemyVisionPings': 0, 'firstBloodAssist': False, 'firstBloodKill': False, 'firstTowerAssist': False, 'firstTowerKill': False, 'gameEndedInEarlySurrender': False, 'gameEndedInSurrender': False, 'getBackPings': 0, 'goldEarned': 16147, 'goldSpent': 15475, 'holdPings': 0, 'individualPosition': 'JUNGLE', 'inhibitorKills': 0, 'inhibitorTakedowns': 0, 'inhibitorsLost': 2, 'item0': 3153, 'item1': 6672, 'item2': 3111, 'item3': 6665, 'item4': 3091, 'item5': 1053, 'item6': 3340, 'itemsPurchased': 25, 'killingSprees': 3, 'kills': 14, 'lane': 'JUNGLE', 'largestCriticalStrike': 822, 'largestKillingSpree': 5, 'largestMultiKill': 1, 'longestTimeSpentLiving': 907, 'magicDamageDealt': 19607, 'magicDamageDealtToChampions': 4761, 'magicDamageTaken': 25794, 'missions': {'playerScore0': 0, 'playerScore1': 0, 'playerScore10': 0, 'playerScore11': 0, 'playerScore2': 0, 'playerScore3': 0, 'playerScore4': 0, 'playerScore5': 0, 'playerScore6': 0, 'playerScore7': 0, 'playerScore8': 0, 'playerScore9': 0}, 'needVisionPings': 0, 'neutralMinionsKilled': 157, 'nexusKills': 0, 'nexusLost': 1, 'nexusTakedowns': 0, 'objectivesStolen': 0, 'objectivesStolenAssists': 0, 'onMyWayPings': 22, 'participantId': 7, 'pentaKills': 0, 'perks': {'statPerks': {'defense': 5002, 'flex': 5008, 'offense': 5005}, 'styles': [{'description': 'primaryStyle', 'selections': [{'perk': 8010, 'var1': 2378, 'var2': 0, 'var3': 0}, {'perk': 9111, 'var1': 1544, 'var2': 320, 'var3': 0}, {'perk': 9104, 'var1': 13, 'var2': 40, 'var3': 0}, {'perk': 8299, 'var1': 1498, 'var2': 0, 'var3': 0}], 'style': 8000}, {'description': 'subStyle', 'selections': [{'perk': 8304, 'var1': 10, 'var2': 3, 'var3': 0}, {'perk': 8347, 'var1': 0, 'var2': 0, 'var3': 0}], 'style': 8300}]}, 'physicalDamageDealt': 199158, 'physicalDamageDealtToChampions': 24449, 'physicalDamageTaken': 19690, 'placement': 0, 'playerAugment1': 0, 'playerAugment2': 0, 'playerAugment3': 0, 'playerAugment4': 0, 'playerScore0': 0, 'playerScore1': 0, 'playerScore10': 0, 'playerScore11': 0, 'playerScore2': 0, 'playerScore3': 0, 'playerScore4': 0, 'playerScore5': 0, 'playerScore6': 0, 'playerScore7': 0, 'playerScore8': 0, 'playerScore9': 0, 'playerSubteamId': 0, 'profileIcon': 4353, 'pushPings': 2, 'puuid': 'WAsQ1dcV4SHWIZE7DmkN1QaTeHsIA_Hihch4S71xA0MucHIYuNGwydTg-AaAVhvae7l0OZgTPh6Cdg', 'quadraKills': 0, 'riotIdName': '', 'riotIdTagline': '', 'role': 'NONE', 'sightWardsBoughtInGame': 0, 'spell1Casts': 323, 'spell2Casts': 48, 'spell3Casts': 35, 'spell4Casts': 19, 'subteamPlacement': 0, 'summoner1Casts': 22, 'summoner1Id': 11, 'summoner2Casts': 4, 'summoner2Id': 4, 'summonerId': 'dk55vo6pnyXLk4Ofonkw9yhfjtzcA391Eb5f8PLuqLVsxB10', 'summonerLevel': 301, 'summonerName': 'Worst Picks Ever', 'teamEarlySurrendered': False, 'teamId': 200, 'teamPosition': 'JUNGLE', 'timeCCingOthers': 37, 'timePlayed': 2141, 'totalAllyJungleMinionsKilled': 93, 'totalDamageDealt': 279181, 'totalDamageDealtToChampions': 38208, 'totalDamageShieldedOnTeammates': 0, 'totalDamageTaken': 47316, 'totalEnemyJungleMinionsKilled': 28, 'totalHeal': 21841, 'totalHealsOnTeammates': 0, 'totalMinionsKilled': 46, 'totalTimeCCDealt': 417, 'totalTimeSpentDead': 365, 'totalUnitsHealed': 1, 'tripleKills': 0, 'trueDamageDealt': 60415, 'trueDamageDealtToChampions': 8997, 'trueDamageTaken': 1831, 'turretKills': 1, 'turretTakedowns': 1, 'turretsLost': 10, 'unrealKills': 0, 'visionClearedPings': 0, 'visionScore': 34, 'visionWardsBoughtInGame': 1, 'wardsKilled': 2, 'wardsPlaced': 15, 'win': False}
```

###### Get summoner's last ranked games with infos and timeline
*Note:* Seen in the [README](../README.md)

Code :
```python
# Opening the api manager with a key, a region and a server
api_lol = API_LOL("YOUR_API_KEY", Region.EUROPE, Server.EU_NORTH)

# Getting summoner's details
summoner = api_lol.get_summoner_by_name("SUMMONER_NAME")

# Recovering his 10 last ranked games infos and timelines
last_games_full = summoner.get_match_history(nb_matches=2, queue=QueueType.RANKED, load_infos=True, load_timelines=True)

# Closing the api manager (for threads, as said earlier !)
api_lol.close()

# Enjoy results
for game in last_games_full:
    print(game.json)
    print(game.json_timeline)
```

Output example : [here](./outputs/output_matches.txt)
