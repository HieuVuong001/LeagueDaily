"""
  Represent result for a Team.
"""
class Result():
  """Result class for a Team.

  Attributes:
    opponent: Opposition team name.
    score: our record against them.

  """
  def __init__(self, opponent, score):
    """Initializes the Result given 
    opponent's name and score against them.

    """
    self.opponent = opponent
    self.score = score

  def __str__(self):
    """A string representation of the result.

    """
    return f"wins against {self.opponent} with a score of {self.score}"

