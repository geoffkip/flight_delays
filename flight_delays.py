#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 22:13:32 2018

@author: geoffrey.kip
"""

from os import chdir, getcwd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set working directory
wd="/Users/geoffrey.kip/Projects/flight_delays"
chdir(wd)

# Read in all data
flights= pd.read_csv("./data/flights.csv")
airports= pd.read_csv("./data/airports.csv")
airlines= pd.read_csv("./data/airlines.csv")

# Rename columns
flights.describe()
flights.shape
flights= flights[:1000]
flights.rename(columns={'AIRLINE': 'IATA_CODE', 'ORIGIN_AIRPORT':'ORIGIN_AIRPORT_CODE',
                        'DESTINATION_AIRPORT':'DESTINATION_AIRPORT_CODE'}, inplace=True)

origin_airports = airports.rename(columns={'IATA_CODE':'ORIGIN_AIRPORT_CODE','AIRPORT': 'ORIGIN_AIRPORT',
                                           'CITY':'ORIGIN_CITY'})
destination_airports = airports.rename(columns={'IATA_CODE':'DESTINATION_AIRPORT_CODE','AIRPORT': 'DESTINATION_AIRPORT',
                                                'CITY':'DESTINATION_CITY'})
# Merge datasets together
flights2 = pd.merge(flights, airlines,  how='left', on="IATA_CODE")
flights3 = pd.merge(flights2, origin_airports[['ORIGIN_AIRPORT_CODE','ORIGIN_AIRPORT',
 'ORIGIN_CITY']], how= 'left', left_on='ORIGIN_AIRPORT_CODE', right_on='ORIGIN_AIRPORT_CODE')
flights_df = pd.merge(flights3, destination_airports[['DESTINATION_AIRPORT_CODE','DESTINATION_AIRPORT',
 'DESTINATION_CITY']], how= 'left', left_on='DESTINATION_AIRPORT_CODE', right_on='DESTINATION_AIRPORT_CODE')

# Recode some variables
#TO DO CODE MONTHS DAYS, SEASONS, LATE EARLY

# GRAPHS
#1) Aiports with the most origin flights
top_ten_origin_airports= flights_df['ORIGIN_AIRPORT'].value_counts()[:10]
labels = (np.array(top_ten_origin_airports.index))
fig1, ax1 = plt.subplots()
ax1.pie(top_ten_origin_airports, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.set_title('Percentage of Flights from Origin Airports')
plt.show()

#2 Cities with most flights from
top_ten_origin_cities= flights_df['ORIGIN_CITY'].value_counts()[:10]
labels = (np.array(top_ten_origin_cities.index))
y_pos=np.arange(len(labels))

plt.figure(figsize=(18,5))
plt.bar(labels,top_ten_origin_cities, align='center',alpha=0.5)
plt.xticks(y_pos, labels)
plt.ylabel('Flight Counts')
plt.title('Flight Counts by Cities')
plt.show()
