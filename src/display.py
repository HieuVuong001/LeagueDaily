"""
Display output to the terminal using data from DailyUpdate.
"""

from rich.console import Console
from rich.table import Table
from daily_update import DailyUpdate

class Display():
  """
    A wrapper class to display information from DailyUpdate
  """
  def __init__(self, date: str):
    self.data = None
    self.tables = None
    self.console = Console()
    self.date = date
    self.warning_message = (
    """
    [bold red]
    There is a 500 results per query limit from the API
    The result might be truncated.
    [/bold red])
    """
    )

  def get_data(self) -> None:
    """ Get data from Leaguepedia.

    Initiate the data collecting process.

    Data is store in the object.
    
    """
    self.data = DailyUpdate(self.date)
    self.tables = self.setup_tables()

  def setup_tables(self):
    # List of tables to render
    tables = {}

    # Master tables to hold all results
    tables["master"] = Table(
      title="[bold color(121)]League Daily[/bold color(121)]"
      )
    tables["master"].add_column("Team 1", justify="left", style="bold red")
    tables["master"].add_column("Score", style="bold")
    tables["master"].add_column("Team 2", justify="left", style="bold blue")
    tables["master"].add_column(
      "League", justify="left", style="bold color(67)"
      )

    leagues = self.data.get_output_list()

    for league, matches_info in leagues.items():
      # Store smaller tables for each league
      if league not in tables:
        tables[league] = Table(
          title=f"[bold color(121)]{league}[/bold color(121)]"
          )
        tables[league].add_column("Team 1", justify="left", style="bold red")
        tables[league].add_column("Score", style="bold")
        tables[league].add_column("Team 2", justify="left", style="bold blue")

      # Loop through list of tuples and unpack, add to table
      for match in matches_info:
        # unpack match, and add to table
        team_1, score_1, score_2, team_2 = match
        tables[league].add_row(team_1, f"{score_1} - {score_2}", team_2)
        tables["master"].add_row(
          team_1, f"{score_1} - {score_2}", team_2, league
          )

    return tables

  def warn(self, message: str) -> None:
    self.console.print(f"[bold red]{message}[/bold red]")

  def show_master_table(self):
    self.console.print(self.tables["master"])

  def show_limit_warning(self):
    self.console.print(self.warning_message)
