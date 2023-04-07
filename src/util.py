"""
Collection of util functions.

"""
from typing import List

def generate_league_query(date: str, leagues:List[str]):
  if len(leagues) == 1:
    # Only 1 leauge is provided
    return f"SG.DateTime_UTC >= '{date}' AND Tournament LIKE '%{leagues[0]}%'"
  else:
    # loop thru each league and add to the query
    league_info = ""
    for index, league in enumerate(leagues):
      league_info += f"Tournament LIKE '%{league}%'"
      if index != (len(leagues) - 1):
        # if not the last item
        # add the word or
        league_info += " OR "

    base_query = f"SG.DateTime_UTC >= '{date}' AND ({league_info})"

    return base_query

def generate_general_query(date: str):
  return f"SG.DateTime_UTC >= '{date}'"

def generate_team_query(date: str, teams: List[str]):
  if len(teams) == 1:
    # Only 1 leauge is provided
    return f"SG.DateTime_UTC >= '{date}' AND (Team1='{teams[0]}' OR Team2='{teams[0]}')"
  else:
    # loop thru each league and add to the query
    teams_info = ""
    for index, team in enumerate(teams):
      teams_info += f"Team1='{team}' OR Team2='{team}'"
      if index != (len(teams) - 1):
        # if not the last item
        # add the word or
        teams_info += " OR "

    base_query = f"SG.DateTime_UTC >= '{date}' AND ({teams_info})"

    return base_query