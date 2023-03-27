"""
Typer wrapper.
"""

import typer
from src.daily_update import DATE, DailyUpdate
from src.display import Display
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
from zoneinfo import ZoneInfo

app = typer.Typer()


@app.command()
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
    local_tz = str(get_localzone())
    parsed_date = since.split("-")

    given = datetime(
      int(parsed_date[0]),
      int(parsed_date[1]),
      int(parsed_date[2]),
      tzinfo=ZoneInfo(local_tz)
    )

    given_utc = given.astimezone(ZoneInfo("UTC"))
    current_utc = datetime.now(timezone("UTC"))

    if given_utc > current_utc:
      # given date is in the future
      display.warn("Invalid date! Abort!")
      raise typer.Exit(1)
    else:
      # warn the user that 500 query is the limit
      # execute as normal
       # Pull data
      daily_update.get_data()

      # Feed data to display
      display.process_data(daily_update.get_info())

      display.show_master_table()
      display.warn(display.maximum_output_warning())


if __name__ == "__main__":
  app()
