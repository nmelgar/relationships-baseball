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
#     attended BYU-Idaho. The new table should contain five columns:
#     playerID, schoolID, salary, and the yearID/teamID associated with
#     each salary. Order the table by salary (highest to lowest) and
#     print out the table in your report.

salary = """SELECT playerid,salary,yearid,teamid 
             FROM salaries"""
salaries = pd.read_sql_query(salary, db)
# salaries

college = """SELECT playerid,schoolid,yearid 
             FROM collegeplaying
             WHERE schoolid = 'byu'
             """
collegeplayers = pd.read_sql_query(college, db)
# collegeplayers


# %%
# result
# TASK 2
# This three-part question requires you to calculate batting average (number of hits
# divided by the number of at-bats)
#     a)Write an SQL query that provides playerID, yearID, and batting average (h/ab)
#         for players with at least 1 at bat (ab column) that year. Sort the table from
#         highest batting average to lowest, and then by playerid alphabetically.
#         Show the top 5 results in your report.
# get the hits
hits = """SELECT h FROM batting"""
hits_total = pd.read_sql_query(hits, db)
# print(hits_total)

# get the at bats
at_bats = """SELECT ab FROM batting"""
at_bats_total = pd.read_sql_query(at_bats, db)
# print(at_bats_total)

batting = """SELECT playerid, yearid, ab
            FROM batting
            WHERE ab > 1
            ORDER BY ab, playerid
            """
bats = pd.read_sql_query(batting, db)
# print(bats)

#     b)Use the same query as above, but only include players with at least 10
#         at bats that year. Print the top 5 results.
#     c)Now calculate the batting average for players over their entire careers
#         (all years combined). Only include players with at least 100 at bats,
#         and print the top 5 results.

# %%
# TASK 3
# Pick any two baseball teams and compare them using a metric of your choice
#     (average salary, home runs, number of wins, etc). Write an SQL query to get
#     the data you need, then make a graph in Altair to visualize the comparison.
#     What do you learn?

# %%
