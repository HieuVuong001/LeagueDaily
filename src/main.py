"""
Typer wrapper.
"""

import typer
from daily_update import TODAY_UTC, DATE, DailyUpdate
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
  display = Display()
  daily_update = DailyUpdate(since)

  if since == DATE:
    # Pull data
    daily_update.get_data()

    # Feed data to display
    display.process_data(daily_update.get_info())

    # Display
    display.show_master_table()
  else:
    # Parse the date, if it's not valid then just terminate
    # Year - Month - Date
    date_comp = since.split("-")
    year = TODAY_UTC.strftime("%Y")

    if date_comp[0] != year:
      display.warn("Not supported due to API quota. Terminating")
      raise typer.Abort()
    else:
      # warn the user that 500 query is the limit
      # execute as normal
       # Pull data
      daily_update.get_data()

      # Feed data to display
      display.process_data(daily_update.get_info())

      display.show_master_table()
      display.show_limit_warning()

if __name__ == "__main__":
  typer.run(main)
