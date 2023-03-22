# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 11:13:04 2023

@author: visha
"""
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
import pandas as pd
from datetime import datetime
from pandasql import sqldf
import os
import numpy as np
import json
import shutil
track_figsizef = open('track_figsize.json')
track_figsize = json.load(track_figsizef)
#%%
folderPath = 'cache';
mysql = lambda q: sqldf(q, globals())       #setup sql
# Check Folder is exists or Not
if os.path.exists(folderPath):
      
    # Delete Folder code
    shutil.rmtree(folderPath)
    os.makedirs(folderPath)
    fastf1.Cache.enable_cache(folderPath)   #setup cache
    print("Cache refreshed")
else:
    os.makedirs(folderPath)
    fastf1.Cache.enable_cache(folderPath)   #setup cache
    print("Cache created")
fastf1.plotting.setup_mpl()
#%%
#get today's date
current_date = datetime.today()                                 
print("Today's date is: {}".format(current_date.date()))
#%%
#get's this year's schedule
schedule = fastf1.get_event_schedule(current_date.year)         
print("This year's schedule (previous 5):")
schedule = schedule[schedule['RoundNumber']>0]
print(schedule[['RoundNumber','EventName','EventDate']][schedule['EventDate']<current_date].tail(5))
print("\nThis year's schedule (upcoming 5):")
print(schedule[['RoundNumber','EventName','EventDate']][schedule['EventDate']>=current_date].head(5))
#%%
#get previous and upcoming session
previous_session = mysql("""SELECT * 
                             FROM schedule 
                             WHERE EventDate <= date('{}')
                             ORDER BY EventDate desc
                             LIMIT 1""".format(current_date.date()))
upcoming_session = mysql("""SELECT * 
                             FROM schedule 
                             WHERE EventDate >= date('{}')
                             ORDER BY EventDate asc
                             LIMIT 1""".format(current_date.date()))
print("""The previous session was 
  {} 
  which was held in 
  {} on {}
and the upcoming session is 
  {} 
  which will be held in 
  {} on {}""".format(
      previous_session['EventName'].iloc[0],
      previous_session['Location'].iloc[0],
      pd.to_datetime(previous_session['EventDate']).dt.date.iloc[0],
      upcoming_session['EventName'].iloc[0],
      upcoming_session['Location'].iloc[0],
      pd.to_datetime(upcoming_session['EventDate']).dt.date.iloc[0],
      ))
session_name = previous_session['EventName'].iloc[0]
location = previous_session['Location'].iloc[0]
#%%
fastf1.Cache.enable_cache('cache')   #setup cache
#%%
#get qualifying session details of previous race
session=fastf1.get_session(current_date.year, session_name,'Q')
session.load()
lap = session.laps.pick_fastest()
#%%
y = lap.telemetry['X']              # values for x-axis
x = lap.telemetry['Y']              # values for y-axis
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=tuple(map(float,track_figsize[location].split(', ')))
)
fig.set_facecolor('white')
fig.suptitle(f'{session_name}', size=24, y=0.97, color='black')
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')

ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=10, zorder=0)
#%%
track_figsizef.close()
#%%