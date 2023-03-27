"""
Typer wrapper.
"""

import typer
from src.daily_update import DATE, DailyUpdate
from src.display import Display
from src.util import *
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
from zoneinfo import ZoneInfo
from typing import Optional, List


app = typer.Typer()


@app.command()
def main(
    since: str = typer.Argument(
      DATE, help="Get result since this given [Year-Month-Day].",
      ),
    league: Optional[List[str]] = typer.Option(None),
    ):
  """
  Output table of game results.

  If date is provided, provide results
  from given date to today.

  If date is not provided, show result for the last 24 hours.

  Arguments:
    since: A string in format Y-M-D

  """
  # Initiate objects to pull and display information
  display = Display()
  daily_update = DailyUpdate()

  general_query = generate_general_query(since)

  if since == DATE:
    # Pull data and process
    daily_update.get_data(general_query)
    display.process_data(daily_update.get_info())

    # Display table
    display.show_master_table()
  else:
    # Parse input date into datetime object
    local_tz = str(get_localzone())
    parsed_date = since.split("-")
    given = datetime(
      int(parsed_date[0]),
      int(parsed_date[1]),
      int(parsed_date[2]),
      tzinfo=ZoneInfo(local_tz)
    )

    # Convert timezone to UTC and get current time
    given_utc = given.astimezone(ZoneInfo("UTC"))
    current_utc = datetime.now(timezone("UTC"))

    # if given time > current time then abort
    # else execute, but show output limit warning
    if given_utc > current_utc:
      display.warn("Invalid date! Abort!")
      raise typer.Exit(1)
    else:
      # Pull and process data
      daily_update.get_data(general_query)
      display.process_data(daily_update.get_info())

      # Display table and warning
      display.show_master_table()
      display.warn(display.maximum_output_warning())


if __name__ == "__main__":
  app()
