# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 11:59:20 2023

@author: pk
"""

import requests
import pandas as pd
from collections import namedtuple
import matplotlib.pyplot as plt

Location = namedtuple('Location', ['latitude', 'longitude'])

Roskilde = Location(57.05, 9.92)
Beijing = Location(40.08, 116.58)
cities = (Roskilde, Beijing)
city_names = {Roskilde: 'Roskilde', Beijing: 'Beijing'}
df_cities = []
base_url = "https://api.open-meteo.com/v1/forecast"

for city in cities:
    params = {
        "latitude": city.latitude,
        "longitude": city.longitude,
        "hourly": "temperature_2m",
        "forecast_days":3
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # converting into pandas dataset
    hourly_data = data['hourly']
    df = pd.DataFrame(hourly_data)

    # add the additional data to the DataFrame
    df['latitude'] = data['latitude']
    df['longitude'] = data['longitude']
    df['timezone'] = data['timezone']
    df['elevation'] = data['elevation']
    df['City'] = city_names[city]
    df_cities.append(df)
    
df_combined = pd.concat(df_cities, ignore_index=True)



fig, ax = plt.subplots()
for city in df_combined['City'].unique():
    city_data = df_combined[df_combined['City'] == city]
    ax.plot(city_data['time'], city_data['temperature_2m'], label=city)
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (°C)')
ax.legend()
plt.show()

