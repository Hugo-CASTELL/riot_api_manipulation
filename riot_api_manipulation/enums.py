from enum import Enum


class Region(Enum):
    AMERICAS = 'americas'
    ASIA = 'asia'
    ESPORTS = 'esports'
    EUROPE = 'europe'


class Server(Enum):
    BRAZIL = 'br1'
    EU_WEST = 'euw1'
    EU_NORTH = 'eun1'
    JAPAN = 'jp1'
    KOREA = 'kr'
    LATIN_AMERICA_1 = 'kr'
    LATIN_AMERICA_2 = 'kr'
    NORTH_AMERICA = 'na1'
    OCEANIA = 'oc1'
    PHILIPPINES = 'ph2'
    RUSSIA = 'ru'
    SG2 = 'sg2'
    TH2 = 'th2'
    TR1 = 'tr1'
    TW2 = 'tw2'
    VN2 = 'vn2'


class QueueType(Enum):
    RANKED = 'ranked'
    NORMAL = 'normal'
    TOURNAMENT = 'tourney'
    TUTORIAL = 'tutorial'
