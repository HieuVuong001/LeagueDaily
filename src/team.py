"""
  Add games to team history and get record against opponent team.
"""

from src.result import Result

class Team():
  """Add games to team's history and get record against other teams.

  Attributes:
    team_name: Name of the organization.
    history: List of records against opposition teams.
    league: The league that this team belongs to.

  """
  def __init__(self, team_name: str,
              league: str,
              history: dict[str, Result]) -> None:
    """Initializes the Team object given 
    the league it belongs to,
    and its scores against other teams.
    
    """
    self.team_name = team_name
    self.history = history
    self.league = league

  def add_game(self, game: Result):
    """Add game to team's history.

    If the opponent we've already faced -> add to current 
    record against them.

    If the opponent we've not faced -> set new record against them.

    Args:
      game: the match to update the team's history with.
    
    """
    # Add the game and its score.
    # Destructure the result
    if game.opponent in self.history:
    # increase the score if we win
      self.history[game.opponent] += game.score
    else:
      self.history[game.opponent] = game.score

  def get_score_against(self, opponent: str) -> None:
    """Get the score against opponent team.

      Get the score against opponent by looking up the team's history.

      Args:
        opponent: the opposition team to look up.

      Returns:
        Result object that contains opponent's name
        and our result against them.
    """
    return self.history[opponent]


  def __str__(self) -> str:
    """A string representation of the result.

    """
    return f"{self.team_name} result is {self.games}"
