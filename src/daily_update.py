"""
Get matches results from leaguepedia.com and bracket them.
"""
from datetime import datetime
import datetime as dt
import mwclient
from pytz import timezone
from match import Match
from result import Result
from team import Team
from typing import Dict, List, Tuple

TIME_FORMAT = "%Y-%m-%d"
TODAY_UTC = datetime.now(timezone("UTC"))
TODAY = TODAY_UTC.strftime(TIME_FORMAT)
DATE =  (TODAY_UTC - dt.timedelta(days=1)).strftime(TIME_FORMAT)

class DailyUpdate():
  """
  Pull data, create teams and assign matches accordingly.

  Attributes:
      data: League of Legends Esports results for the given date.
      teams: List of teams that played today. 
  """
  def __init__(self, date: str = DATE) -> None:
    """Initializes the instance by collecting result of matches for current day.
    
    """
    print(date)
    self.current_date = date
    self.data = self.get_data()
    self.teams = {}
    self.organize()


  def get_data(self) -> List[Match]:
    """Pull data from leaguepedia.

    Pulls esports result from leaguepedia and process into Match objects. 
    Matches contain team names, date and time of match, 
    the tournament it belongs, and match result.

    Returns:
      data: A list of Matches for the given date. (default = today) 

    """
    data = []

    # Pull data from the API
    site = mwclient.Site("lol.fandom.com", path="/")

    matches = site.api("cargoquery",
      limit = "max",
      tables = "ScoreboardGames=SG",
      fields = "SG.Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, \
          WinTeam, Tournament",
      where = f"SG.DateTime_UTC >= '{self.current_date} 00:00:00'"
    )["cargoquery"]

    for match in matches:
      match_detail = match["title"]
      team1 = match_detail["Team1"]
      team2 = match_detail["Team2"]
      league = match_detail["Tournament"]
      result = match_detail["WinTeam"]

      data.append(Match(team1, team2, result, league))

    return data

  def organize(self) -> None:
    """ Organize the data into usable dictionary.

    Organize the collected data into a dictionary team by team.
    Each team has their own match history and results.

    For example:
    {'100 Thieves': Result('Team Liquid, 1), Result('TSM', 1)}}

    Result has two attributes: opposition team, and our result against them. 

    """
    for match in self.data:
      team_1_name = match.team_1
      team_2_name = match.team_2
      res = match.result
      league = match.league

      # create a new team if the team isn't in seen
      if team_1_name not in self.teams:
        # Create a new Team with team 1
        self.teams[team_1_name] = Team(team_1_name, league, {})

      if team_2_name not in self.teams:
        self.teams[team_2_name] = Team(team_2_name, league, {})


      # Results are relative
      # team 1 wins against team 2, so team 1 gets +1, but team 2 gets 0
      # that's why we need two different Result objects for the same match
      team_1_result = Result(team_2_name, int(res == team_1_name))
      team_2_result = Result(team_1_name, int(res == team_2_name))

      # Add the relative result to each team history
      self.teams[team_1_name].add_game(team_1_result)
      self.teams[team_2_name].add_game(team_2_result)

  def get_all_output(self) -> str:
    """A string representation of matches happening today.

      For example:
        | Worlds 2022 | GAM 1 0 TES
        | Worlds 2022 | GAM 0 1 TES
    """
    # Mark off team that we have seen
    # Team A vs Team B --> when fetching result for team A
    # --> we also fetch result for team B
    seen = set()

    output = ""

    for team_name, team in self.teams.items():
      if team_name not in seen:
        # Mark as seen
        seen.add(team_name)

        # Loop thru game history and append result to output
        for opponent in team.history:
          if opponent not in seen:
            # Breaking into different parts for readability
            league_name = team.league
            home_score = team.get_score_against(opponent)
            opponent_score = self.teams[opponent]\
                            .get_score_against(team_name)

            output += (
            f"""
            | {league_name} |
            {team_name} {home_score} :{opponent_score} {opponent}\n
            """)

            # Mark as seen
            seen.add(opponent)

    return output

  def get_output_list(self) -> Dict[str, List[Tuple]]:
    """Returns a dict of league and match info.

    A dictionary with league name as key,
    and tuples of info as value.
    
    Sample tuple format:
      (team_name, home_score, opponent_score, opponent)

      Returns:
        List[Tuple] 
    """
    # Mark off team that we have seen
    # Team A vs Team B --> when fetching result for team A
    # --> we also fetch result for team B
    seen = set()

    leagues = {}

    for team_name, team in self.teams.items():
      if team_name not in seen:
        # Mark as seen
        seen.add(team_name)

        # Loop thru game history and append result to output
        for opponent in team.history:
          if opponent not in seen:
            # Breaking into different parts for readability
            league_name = team.league
            home_score = team.get_score_against(opponent)
            opponent_score = self.teams[opponent]\
                            .get_score_against(team_name)

            if league_name not in leagues:
              leagues[league_name] = [] # list of empty output

            output = (team_name, home_score, opponent_score, opponent)

            leagues[league_name].append(output)

            # Mark as seen
            seen.add(opponent)

    return leagues

  def __str__(self) -> str:
    """
    Output total matches happening today.

    Returns
      String output of total games happening today.
    """

    return f"Data collected. There are {len(self.teams)} teams playing today."
  