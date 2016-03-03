import re
from urllib import urlencode


class Utils:
    def __init__(self):
        pass

    @staticmethod
    def parse_json(raw):
        data = re.sub(r'([\[,])(?=\s*[,\]])', r'\1null', raw)
        data = re.sub(r'"', r'\"', data)
        data = re.sub(r"'([\s\S]*?)(?<!\\)'", r'"\1"', data)
        data = re.sub(r"\\'", r"'", data)

        return data

    @staticmethod
    def extractModelLastMode(response):
        pass


class Url:
    base = 'https://www.whoscored.com'
    templates = {
        "livescores": "/matchesfeed/",
        "livescoreincidents": "/matchesfeed/{id}/IncidentsSummary/",
        "stagefixtures": "/tournamentsfeed/{stageId}/Fixtures/",
        "teamfixtures": "/teamsfeed/{teamId}/Fixtures/",
        "standings": "/stagesfeed/{stageId}/standings/",
        "forms": "/stagesfeed/{stageId}/forms/",
        "history": "/stagesfeed/{stageId}/history/",
        "streaks": "/stagesfeed/{stageId}/streaks/",
        "goals": "/tournamentsfeed/{stageId}/PlayerStatistics/",
        "cards": "/tournamentsfeed/{stageId}/PlayerStatistics/",
        "team-goals": "/teamsfeed/{teamId}/PlayerStatistics/",
        "team-cards": "/teamsfeed/{teamId}/PlayerStatistics/",
        "previousmeetings": "/teamsfeed/{homeTeamId}/PreviousMeetings/",
        "statistics": "/statisticsfeed/",
        "side-box-statistics": "/statisticsfeed/{statsType}/SideBoxStatistics/",
        "regionteams": "/teamsfeed/{id}/region",
        "ws-stage-stat": "/stagestatfeed/",
        "ws-teams-stage-stat": "/stagestatfeed/{stageId}/stageteams/",
        "ws-stage-filtered-team-stat": "/stagestatfeed/{stageId}/teamsstagefiltered/",
        "ws-teams-filtered-stage-stat": "/stagestatfeed/{stageId}/stageteamsfiltered/",
        "stage-top-player-stats": "/stagestatfeed/{stageId}/stagetopplayers",
        "live-team-stat": "/optamatchstatfeed/",
        "team-fixtures": "/teamsfeed/{teamId}/H2HFixtures/",
        "match-header": "/matchesfeed/{id}/MatchHeader",
        "match-live-update": "/matchesfeed/{id}/LiveMatch",
        "match-commentary": "/matchesfeed/{id}/MatchCommentary",
        "live-player-stats": "/matchesfeed/{id}/LivePlayerStats",
        "betting-stats": "/bettingstatfeed/",
        "overall-player-stat": "/stageplayerstatfeed/{playerId}/Overall",
        "stage-player-stat": "/stageplayerstatfeed/",
        "overall-team-stat": "/stageteamstatfeed/{teamId}/Overall",
        "stage-team-stat": "/stageteamstatfeed/",
        "stage-h2h-player-stat": "/stageplayerstatfeed/{stageId}/H2HTeamPlayers",
        "player-tournament-stat": "/stageplayerstatfeed/{playerId}/PlayerTournamentStats",
        "facts-filter": "/Facts/Data",
        "player-heatmap": "/Players/{id}/Heatmap",
        "match-centre": "/matchesfeed/{id}/MatchCentre",
        "match-centre2": "/matchesfeed/{id}/MatchCentre2",
        "player-tournament-history-stat": "/stageplayerstatfeed/{playerId}/PlayerHistoryTournamentStats",
        "custom-standings": "/tournamentsfeed/{stageId}/CustomStandings/",
        'player-stats': '/StatisticsFeed/1/GetPlayerStatistics',
        'player-stats2': '/StatisticsFeed/1/GetMatchCentrePlayerStatistics',
        'team-stats': '/StatisticsFeed/1/GetTeamStatistics',
        'tournament': '/Regions/{r}/Tournaments/{t}/',
        'season': '/Regions/{r}/Tournaments/{t}/Seasons/{s}',
        'stage': '/Regions/{r}/Tournaments/{t}/Seasons/{s}/Stages/{id}',
        'player': '/Players/{p}/'
    }

    def __init__(self):
        pass

    @staticmethod
    def get(key, parameters):
        url = Url.templates[key]
        try:
            url = re.sub(r'\{(\w*?)\}', lambda m: str(parameters.pop(m.group(1))), url)
        except KeyError:
            raise

        if len(parameters):
            url += '?' + urlencode(parameters)

        return Url.base + url
