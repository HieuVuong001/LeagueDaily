"""
Testing module for the LeagueDaily CLI app.
"""
from typer.testing import CliRunner
import datetime as dt
from datetime import datetime
from pytz import timezone
from src.main import app
from src.daily_update import TIME_FORMAT
import time
import pytest

runner = CliRunner()

@pytest.fixture(autouse=True)
def slow_down_tests():
  """Sleep between tests.

  API requires users to have 1-2 second delay
  between each calls.
  """
  yield
  time.sleep(1.2)

class TestDate():
  """Various tests with date input for the CLI app.

  Test for a day that is today, in the future,
  1 day before today and 2 days before today.
  """
  def test_today(self):
    """Test today as input

    App should run normally.
    """
    today = datetime.now(timezone("UTC"))
    today_str = today.strftime(TIME_FORMAT)

    result = runner.invoke(app, today_str)
    assert result.exit_code == 0
    assert "query limit" in result.stdout

  def test_next_week(self):
    """Test a date in the future

    App should not run because there is no result.
    """
    next_week = datetime.now(timezone("UTC")) + dt.timedelta(days=7)
    next_week_str = next_week.strftime(TIME_FORMAT)

    result_nw = runner.invoke(app, next_week_str)
    assert result_nw.exit_code == 1

  def test_past_date(self):
    """Test a date in the past

    App should run, but warning should be shown. 
    """
    two_days_ago = datetime.now(timezone("UTC")) - dt.timedelta(days=2)
    two_days_ago_str = two_days_ago.strftime(TIME_FORMAT)

    result = runner.invoke(app, two_days_ago_str)
    assert result.exit_code == 0
    assert "query limit" in result.stdout

  def test_yesterday(self):
    """Test yesterday from today.

    Since this is the default date, app should run normally.
    """
    yesterday = datetime.now(timezone("UTC")) - dt.timedelta(days=1)
    yesterday_str = yesterday.strftime(TIME_FORMAT)

    result = runner.invoke(app, yesterday_str)
    assert result.exit_code == 0
    assert "query limit" in result.stdout

  def test_wrong_date_format(self):
    """Test string as date.

    """
    d = "Hello"
    result = runner.invoke(app, d)
    assert result.exit_code == 2
    assert "League Daily" not in result.stdout

class TestInput():
  def test_valid_league(self):
    result = runner.invoke(app, ["2023-03-01", "--league", "LCS"])
    assert "LCS" in result.stdout
    assert result.exit_code == 0
    assert "query limit" in result.stdout

  def test_invalid_league(self):
    result = runner.invoke(app, ["2023-03-01", "--league", "NCS"])
    assert "League Daily" not in result.stdout
    assert "No result found!" in result.stdout