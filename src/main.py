"""
Typer wrapper.
"""

import typer
from daily_update import DailyUpdate
from rich.table import Table
from rich.console import Console

def main(date: str = typer.Argument(None)):
  """
  Output table of results for the last 24 hours.

  If date is provided, provide results
  from given date to today.

  """
  # Initialize the data collecting process
  update = DailyUpdate()

  # Create new console object
  console = Console()
  # List of tables to render
  tables = {}

  # Master tables to hold all results
  tables["master"] = Table(
    title="[bold color(121)]League Daily[/bold color(121)]"
    )
  tables["master"].add_column("Team 1", justify="left", style="bold red")
  tables["master"].add_column("Score", style="bold")
  tables["master"].add_column("Team 2", justify="left", style="bold blue")
  tables["master"].add_column("League", justify="left", style="bold color(67)")

  leagues = update.get_output_list()

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
      tables["master"].add_row(team_1, f"{score_1} - {score_2}", team_2, league)

  if date is None:
    console.print(tables["master"])

if __name__ == "__main__":
  typer.run(main)
