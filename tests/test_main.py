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

  Test for a day that is in the future,
  1 day before today and 2 days before today.

  Test invalid date as date input.
  """
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

  def test_wrong_date_format(self):
    """Test string as date.

    """
    d = "Hello"
    result = runner.invoke(app, d)
    assert result.exit_code == 2
    assert "League Daily" not in result.stdout

class TestInput():
  """Test various inputs.
  
    Test one league, two leagues, both valid and invalid.
  """
  def test_valid_league(self):
    """Valid league, program should run normally.

    """
    result = runner.invoke(app, ["2023-03-01", "--league", "LCS"])
    assert "LCS" in result.stdout
    assert result.exit_code == 0
    assert "query limit" in result.stdout

  def test_invalid_league(self):
    """Test invalid league, program should not run.

    """
    result = runner.invoke(app, ["2023-03-01", "--league", "NCS"])
    assert "League Daily" not in result.stdout
    assert "No result found!" in result.stdout

  def test_valid_and_invalid_league(self):
    """Test one valid league and invalid league.

    Program should run normally, but invalid league matches will not show.
    """
    result = runner.invoke(app,
                          ["2023-03-01", "--league", "LCS", "--league", "NCS"]
                          )
    assert "LCS" in result.stdout
    assert "No result found!" not in result.stdout
    assert result.exit_code == 0

  def test_two_leagues(self):
    """Test two valid leagues.

    Program should run normally, and both tables for two leagues
    should show.
    """
    result = runner.invoke(app,
                          ["2023-03-20", "--league", "LCS", "--league", "LPL"]
                          )
    assert result.exit_code == 0
    assert "LCS" in result.stdout
    assert "LPL" in result.stdout
    assert "query limit" in result.stdout
    assert "No result found!" not in result.stdout


  def test_single_team(self):
    """Test a single team as input

    Program should run and exit normally.
    Table should only show the results for that team
    title should be the league the team is playing in.
    """
    result = runner.invoke(app,
                           ["2023-03-20", "--teams", "100 Thieves"])
    assert result.exit_code == 0
    assert "LCS" in result.stdout
    assert "query limit" in result.stdout
    assert "No result found!" not in result.stdout


  def test_two_teams(self):
    """Test two teams as input

    Program should run and exit normally.
    Table should only show the results for the two teams
    title should be the league the teams are playing in.
    """
    result = runner.invoke(app,
                          ["2023-03-20", "--teams", "100 Thieves",
                          "--teams", "T1"])
    assert result.exit_code == 0
    assert "LCS" in result.stdout
    assert "LCK" in result.stdout
    assert "query limit" in result.stdout
    assert "No result found!" not in result.stdout


  def test_team_and_same_league(self):
    """Test a team and the same league

    This should run normally with only one table.
    """
    result = runner.invoke(app,
                         ["2023-03-20", "--teams", "100 Thieves",
                          "--league", "LCS"])
    assert result.exit_code == 0
    assert "LCS" in result.stdout
    assert "League Daily" not in result.stdout
    assert "No result found!" not in result.stdout
    assert "query limit" in result.stdout


  def test_team_and_diff_league(self):
    """Test a team and a different league

    This should run normally.
    One table should only be for the given team
    Other table will be for all team in given league.
    """
    result = runner.invoke(app,
                          ["2023-03-20", "--teams", "100 Thieves",
                          "--league", "LCK"])
    assert result.exit_code == 0
    assert "LCK" in result.stdout
    assert "LCS" in result.stdout
    assert "League Daily" not in result.stdout
    assert "No result found!" not in result.stdout
    assert "query limit" in result.stdout

  def test_invalid_team(self):
    """Test invalid team as input

    Program should exit with error exit code
    """
    result = runner.invoke(app, ["2023-03-20", "--teams", "100 Theft"])
    assert "League Daily" not in result.stdout
    assert "No result found!" in result.stdout
