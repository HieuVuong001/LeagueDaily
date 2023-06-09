# LeagueDaily

League of Legends Esports update straight from the terminal!

Now you can stay up-to-date with your favorite LoL teams/leagues despite your busy schedule.
# Install

requirement: `python3 >= 3.10`

`pip install leaguedaily`

Since this program is published as a PyPI package, you could start using it straight from the shell.

If for some reason it doesn't work, try adding Python to PATH. Useful [guide](https://realpython.com/add-python-to-path/).

# Usage

By default, running `leaguedaily` without any arguments will show League of Legends Esports result from the previous day.

![Screenshot from 2023-04-20 07-43-17](https://user-images.githubusercontent.com/60205090/233401825-ff74f03d-7e29-4fc0-ad0c-9f1fb5639e72.png)

You can also specify dates in the format of `YYYY-MM-DD` as an argument to the program.

![Screenshot from 2023-04-20 07-41-48](https://user-images.githubusercontent.com/60205090/233401471-2f539f98-7a97-4dcc-a5a1-5a292ff9d77d.png)


`--team` flag can be used to specify one or more teams in addition to the given date argument.

![Screenshot from 2023-04-20 07-45-08](https://user-images.githubusercontent.com/60205090/233402355-e9d1c5ce-2a57-47a3-bfcd-23bf0bb4cf02.png)


`--league` flag can be used to limit the results to only the given leagues.

![Screenshot from 2023-04-20 07-46-33](https://user-images.githubusercontent.com/60205090/233402764-f5ec7044-8899-4bc1-a7c6-2b442acddb5d.png)

# Developement

Before `main.py` can be run, run `export PYTHONPATH=$(pwd)` outside of the `src` folder. This helps python importing files from different folders in the project. 

# Known problems

1. Data is pulled from leaguepedia, so there is a limit as to how much data a normal user can pull. As a result, given a too far away date, program's result could be truncated, thus incorrect!

2. A BO3 series could be in the same day in local time, but in UTC (default time when pulled from API), 2 matches are on the same day and 1 match is on the next day (past midnight UTC time, but still the same day local time). In short, if this happens, the result could appear incorrectly. However, the chance of this happening is rather rare (< 1% during development and testing).

Since `leaguedaily` is created as a quick way to stay updated to *recent* LoL Esports News, these problems are not addressed. The program works consistently enough for what it is created for.

Cheers! 🎆 
