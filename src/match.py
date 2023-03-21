"""
  Blueprint/Intermediate class to store data pulled from API.
"""
class Match():
  """Match class to store data from API.

  Attributes:
    team_1: First team's name.
    team_2: Second team's name.
    result: Result of the match - whether team 1 wins or team 2 wins.
    leauge: the league that this match belongs to.

  """
  def __init__(self, team_1: str,
              team_2: str,
              result: str,
              league: str) -> None:
    """Initializes the Match instance given 
    both team's names, result, and league.

    """
    self.team_1 = team_1
    self.team_2 = team_2
    self.result = result
    self.league = league

  def __str__(self) -> str:
    """A string representation of the result.

    """
    return f"""
    | {self.league} |
    {self.team_1} vs {self.team_2} | Result: {self.result}
    """
