# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:46:36 2023

@author: visha
"""
from matplotlib import pyplot as plt
import matplotlib as mpl
import fastf1
import fastf1.plotting
import pandas as pd
from matplotlib.collections import LineCollection
import numpy as np
#%%
fastf1.Cache.enable_cache('C:/Users/visha/Desktop/Play/f1/cache')   #setup cache
fastf1.plotting.setup_mpl()                                         #setup matplotlib

session=fastf1.get_session(2023,"Bahrain",'Q')
session.load()
#%%

# PLOT LECLERC'S FASTEST LAP BY SPEED AND TIME

#%%
fast_leclerc = session.laps.pick_driver('LEC').pick_fastest()
lec_car_data = fast_leclerc.get_car_data()
t = lec_car_data['Time']
vCar = lec_car_data['Speed']
#%%
# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(t, vCar, label='Fast')
ax.set_xlabel('Time')
ax.set_ylabel('Speed [Km/h]')
ax.set_title('Leclerc is')
ax.legend()
plt.show()
#%%

# GETTING DIFFERENT INFO

#%%
event = session.event
print(event)

event = fastf1.get_event(2021, 'Monza')
print(event)
#%%
schedule = fastf1.get_event_schedule(2021)
print(schedule)
#%%
drivers = pd.unique(session.laps['Driver'])
print(drivers)
#%%
results = session.results
print(results[['Abbreviation','Q3']])
#%%
laps = session.laps
#%%

# GETTING TWO GRAPHS ON ONE PLOT

#%%
ver_lap = session.laps.pick_driver('VER').pick_fastest()
ham_lap = session.laps.pick_driver('HAM').pick_fastest()
alo_lap = session.laps.pick_driver('ALO').pick_fastest()
#%%
ver_tel = ver_lap.get_car_data().add_distance()
ham_tel = ham_lap.get_car_data().add_distance()
alo_tel = alo_lap.get_car_data().add_distance()
#%%
rbr_color = fastf1.plotting.team_color('RBR')
mer_color = fastf1.plotting.team_color('MER')
am_color = fastf1.plotting.team_color('AM')

fig, ax = plt.subplots()
ax.plot(ver_tel['Distance'], ver_tel['Speed'], color=rbr_color, label='VER')
ax.plot(ham_tel['Distance'], ham_tel['Speed'], color=mer_color, label='HAM')
ax.plot(alo_tel['Distance'], alo_tel['Speed'], color=am_color, label='ALO')

ax.set_xlabel('Distance in m')
ax.set_ylabel('Speed in km/h')

ax.legend()
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} Qualifying")

plt.show()
#%%

# AVG SPEEDS

#%%
print(round(ham_tel['Speed'].mean(),3))
print(round(ver_tel['Speed'].mean(),3))
print(round(alo_tel['Speed'].mean(),3))
print('-----')
print(round(ham_tel[ham_tel['Throttle']>=99]['Speed'].mean(),2))
print(round(ver_tel[ver_tel['Throttle']>=99]['Speed'].mean(),2))
print(round(alo_tel[alo_tel['Throttle']>=99]['Speed'].mean(),2))
print("-----")
print(round(ham_tel[ham_tel['Throttle']<99]['Speed'].mean(),2))
print(round(ver_tel[ver_tel['Throttle']<99]['Speed'].mean(),2))
print(round(alo_tel[alo_tel['Throttle']<99]['Speed'].mean(),2))
#%%
import fastf1 as ff1
year = 2021
wknd = 9
ses = 'R'
driver = 'RIC'
colormap = mpl.cm.plasma


session = ff1.get_session(year, wknd, ses)
weekend = session.event
session.load()
lap = session.laps.pick_driver("LEC").pick_fastest()
# Get telemetry data
x = lap.telemetry['X']              # values for x-axis
y = lap.telemetry['Y']              # values for y-axis
color = lap.telemetry['Speed']      # value to base color gradient on
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
# We create a plot with title and adjust some setting to make it look good.
fig, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig.suptitle(f'Speed', size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')


# After this, we plot the data itself.
# Create background track line
ax.plot(lap.telemetry['X'], lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)
#%%