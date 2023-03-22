"""
Typer wrapper.
"""

import typer
import rich
from daily_update import DailyUpdate

def main(date: str = typer.Argument(None)):
  """
  Print out the number of results based on quantity.

  """
  # Initialize the data collecting process
  update = DailyUpdate()

  if date is None:
    # Update today
    rich.print(update.get_all_output())


if __name__ == "__main__":
  typer.run(main)
