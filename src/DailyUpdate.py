import mwclient
from Match import Match
from datetime import datetime
from pytz import timezone

TIME_FORMAT = "%Y-%m-%d"

class DailyUpdate():
    def __init__(self):
        self.data = self.get_data()

    def get_data(self, date=datetime.now(timezone('UTC')).strftime(TIME_FORMAT)):
        data = []

        # Pull data from the API
        site = mwclient.Site('lol.fandom.com', path='/')

        matches = site.api('cargoquery',
            limit = 'max',
            tables = "ScoreboardGames=SG",
            fields = "SG.Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, WinTeam, Tournament",
            where = f"SG.DateTime_UTC >= '{date}'"
        )['cargoquery']


        for match in matches:
            match_detail = match['title']
            team1 = match_detail['Team1']
            team2 = match_detail['Team2']
            league = match_detail['Tournament']
            result = match_detail['WinTeam']

            data.append(Match(team1, team2, result, league))

        return data

update = DailyUpdate()

