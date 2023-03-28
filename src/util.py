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
