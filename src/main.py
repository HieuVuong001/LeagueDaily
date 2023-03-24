"""
Typer wrapper.
"""

import typer
from daily_update import TODAY, TODAY_UTC, DATE
from display import Display

def main(
    since: str = typer.Argument(
      DATE, help="Get result since this given [Year-Month-Day].",
      ),
    ):
  """
  Output table of game results.

  If date is provided, provide results
  from given date to today.

  If date is not provided, show result for the last 24 hours.

  Arguments:
    since: A string in format Y-M-D

  """
  display = Display(since)

  if since == TODAY:
    display.get_data()
    display.show_master_table()
  else:
    # Parse the date, if it's not valid then just terminate
    # Year - Month - Date
    date_comp = since.split("-")
    year = TODAY_UTC.strftime("%Y")
    month = TODAY_UTC.strftime("%m")

    if date_comp[0] != year or int(date_comp[1]) != int(month):
      display.warn("Year is not supported due to API quota. Terminating")
      raise typer.Abort()
    else:
      # warn the user that 500 matches is the limit
      # execute as normal
      display.get_data()
      display.show_limit_warning()
      display.show_master_table()

if __name__ == "__main__":
  typer.run(main)
