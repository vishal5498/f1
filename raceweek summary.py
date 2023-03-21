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
print("This year's schedule:")
schedule = schedule[schedule['RoundNumber']>0]
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
which was held held on {} 
and the upcoming session is 
  {} 
which will be held on {}""".format(
      previous_session['EventName'].iloc[0],
      pd.to_datetime(previous_session['EventDate']).dt.date.iloc[0],
      upcoming_session['EventName'].iloc[0],
      pd.to_datetime(upcoming_session['EventDate']).dt.date.iloc[0]
      ))
#%%