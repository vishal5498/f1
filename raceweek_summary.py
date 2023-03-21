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
import shutil
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
#%%
event = fastf1.get_event(current_date.year, session_name)
print(event)
fastf1.Cache.enable_cache('cache')   #setup cache
session=fastf1.get_session(current_date.year, session_name,'Q')
session.load()
#%%