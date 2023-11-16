# %%
import pandas as pd
import altair as alt
import sqlite3

# %%
sqlite_file = "lahmansbaseballdb.sqlite"
db = sqlite3.connect(sqlite_file)

# %%
college = """SELECT playerid,schoolid,yearid
             FROM collegeplaying
             """
collegeplayers = pd.read_sql_query(college, db)
print(collegeplayers)
# %%
