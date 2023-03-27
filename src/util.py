"""Collection of util functions.

"""
def generate_league_query(date: str, league:str):
  return f"SG.DateTime_UTC >= '{date}' AND Tournament='{league}'"

def generate_general_query(date: str):
  return f"SG.DateTime_UTC >= '{date}'"
