# %%
import pandas as pd
import altair as alt
import sqlite3

# %%
sqlite_file = "lahmansbaseballdb.sqlite"
db = sqlite3.connect(sqlite_file)

# %%
# TASK 1
# Write an SQL query to create a new dataframe about baseball players who
# attended BYU-Idaho. The new table should contain five columns:
# playerID, schoolID, salary, and the yearID/teamID associated with
# each salary. Order the table by salary (highest to lowest) and
# print out the table in your report.

students = """SELECT sal.playerid, cp.schoolid, sal.salary, sal.yearid,  sal.teamid
                FROM salaries as sal
                LEFT JOIN collegeplaying as cp
                ON cp.playerid = sal.playerid
                WHERE schoolid = 'byu'
                ORDER BY salary DESC
            """
students_players = pd.read_sql_query(students, db)
print(students_players)

# %%
# result
# TASK 2
# This three-part question requires you to calculate batting average (number of hits
# divided by the number of at-bats)

# a)Write an SQL query that provides playerID, yearID, and batting average (h/ab)
# for players with at least 1 at bat (ab column) that year. Sort the table from
# highest batting average to lowest, and then by playerid alphabetically.
# Show the top 5 results in your report.
hits = """SELECT h, ab, playerid, yearid FROM batting WHERE ab >= 1"""
hits_total = pd.read_sql_query(hits, db)
hits_total["batting_avg"] = hits_total["H"] / hits_total["AB"]
ab1_filtered = hits_total[["playerID", "yearID", "batting_avg"]]
ab1_filtered = ab1_filtered.sort_values(
    by=["batting_avg", "playerID"], ascending=[False, True]
)
ab1_filtered.head(5)

# b)Use the same query as above, but only include players with at least 10
# at bats that year. Print the top 5 results.
hits = """SELECT h, ab, playerid, yearid FROM batting WHERE ab >= 10"""
hits_total = pd.read_sql_query(hits, db)
hits_total["batting_avg"] = hits_total["H"] / hits_total["AB"]
ab10_filtered = hits_total[["playerID", "yearID", "batting_avg"]]
ab10_filtered = ab10_filtered.sort_values(
    by=["batting_avg", "playerID"], ascending=[False, True]
)
ab10_filtered.head(5)

# c)Now calculate the batting average for players over their entire careers
# (all years combined). Only include players with at least 100 at bats,
# and print the top 5 results.
hits = """SELECT h, ab, playerid, yearid FROM batting WHERE ab >= 100"""
hits_total = pd.read_sql_query(hits, db)
hits_total["batting_avg"] = hits_total["H"] / hits_total["AB"]
ab100_filtered = hits_total[["playerID", "batting_avg"]]
ab100_filtered = ab100_filtered.groupby("playerID").mean()
ab100_filtered = ab100_filtered.sort_values(
    by=["batting_avg", "playerID"], ascending=[False, True]
)
ab100_filtered.head(5)


# %%
# TASK 3
# Pick any two baseball teams and compare them using a metric of your choice
# (average salary, home runs, number of wins, etc). Write an SQL query to get
# the data you need, then make a graph in Altair to visualize the comparison.
# What do you learn?

# Scale colors for each team
color_scale = alt.Scale(range=["red", "#f2e709"])

# select all teams
teams = """SELECT * FROM teams"""
teams_total = pd.read_sql_query(teams, db)

# select first team Cincinnati Reds
team1 = """SELECT * FROM teams WHERE name = 'Cincinnati Reds'"""
team_chosen_1 = pd.read_sql_query(team1, db)
team_chosen_1["Year"] = pd.to_datetime(team_chosen_1["yearID"], format="%Y")
chart1 = (
    alt.Chart(team_chosen_1)
    .mark_point()
    .encode(
        y=alt.Y("HR:Q", title="Home Runs"),
        x="Year:T",
        color=alt.Color("name", type="nominal", scale=color_scale),
    )
    .properties(title="CIN vs PIT home runs")
)

# select second team Pittsburgh Pirates
team2 = """SELECT * FROM teams WHERE name = 'Pittsburgh Pirates'"""
team_chosen_2 = pd.read_sql_query(team2, db)
team_chosen_2["Year"] = pd.to_datetime(team_chosen_1["yearID"], format="%Y")
chart2 = (
    alt.Chart(team_chosen_2)
    .mark_point()
    .encode(
        y=alt.Y("HR:Q", title="Home Runs"),
        x="Year:T",
        color=alt.Color("name", type="nominal", scale=color_scale),
    )
)

hr_compared = chart1 + chart2
hr_compared
