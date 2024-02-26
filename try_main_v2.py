# %%
import pandas as pd
import altair as alt
import sqlite3
import plotly.express as px
import plotly.graph_objects as go

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

# %%
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

# %%
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

# %%
# select all teams
teams = """SELECT * FROM teams"""
teams_total = pd.read_sql_query(teams, db)

teams_total

# %%
team1 = "Cincinnati Reds"
team2 = "Pittsburgh Pirates"
# select first team Cincinnati Reds
select_teams = """SELECT * FROM teams WHERE name = 'Cincinnati Reds' OR name = 'Pittsburgh Pirates'"""
chosen_teams = pd.read_sql_query(select_teams, db)
chosen_teams["Year"] = pd.to_datetime(chosen_teams["yearID"], format="%Y")

chosen_teams

chart_1 = px.scatter(
    chosen_teams,
    x="Year",
    y="HR",
    color="name",
    labels={"HR": "Home Runs", "name": "Team"},
    title="Home Runs through the years",
)
chart_1.show()

# %%
