# %%
import pandas as pd
import altair as alt
import sqlite3

# %%
sqlite_file = "lahmansbaseballdb.sqlite"
db = sqlite3.connect(sqlite_file)

#%%
# careful to list your path to the file.
sqlite_file = 'lahmansbaseballdb.sqlite'
con = sqlite3.connect(sqlite_file)

results = pd.read_sql_query( 
    'SELECT gameid FROM allstarfull',
    con)

results

# %%
table = pd.read_sql_query(
    "SELECT * FROM sqlite_master WHERE type='table'",
    db)
print(table.filter(['name']))
print('\n\n')
# 8 is collegeplaying
print(table.sql[8])
# collegeplayers
# %%
