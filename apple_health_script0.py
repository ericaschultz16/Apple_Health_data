#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:49:43 2021

@author: ericaschultz
"""
#Title: Apple Health Data
#sources used: https://towardsdatascience.com/data-analysis-of-your-applewatch-workouts-672fe0366e7c

#I'm using this article from Towards Data Science as guidance for cleaning the data.

#%%
import pandas as pd
import xmltodict

path = "/Users/ericaschultz/Desktop/My_Projects/DATA/apple_health_export/export.xml"
with open(path, 'r') as file:
    data = xmltodict.parse(file.read())

#Records list
records_list = data['HealthData']['Record']
df_records = pd.DataFrame(records_list)

#Workout list
workout_list = data['HealthData']['Workout']
df_workouts = pd.DataFrame(workout_list)

#%%

#Understanding the datasets

print(df_records.info())
print('\n')
print(df_records.describe())
print('\n')
print(df_workouts.info())
print('\n')
print(df_workouts.describe())

#%%
#Converting the data types

df_workouts[['@duration', '@totalDistance', '@totalEnergyBurned']] = df_workouts[['@duration', '@totalDistance', '@totalEnergyBurned']].apply(pd.to_numeric)
print(df_workouts.dtypes) 

date_format = '%Y-%m-%d %H:%M:%S %z'
df_workouts['@creationDate'] = pd.to_datetime(df_workouts['@creationDate'], format = date_format)
df_workouts['@startDate'] = pd.to_datetime(df_workouts['@startDate'], format = date_format)
df_workouts['@endDate'] = pd.to_datetime(df_workouts['@endDate'], format = date_format)
print(df_workouts.dtypes)

#%%
#What are the kinds of workouts in this dataset?

print(df_workouts['@workoutActivityType'].value_counts())
#A lot of these have low counts bc they're not really workouts but just random things I tried to record. I'm going to keep only the "workouts" that I know were part of my typical workouts.

type_list = ['Cycling', 'Yoga', 'HighIntensityIntervalTraining', 'Other', 'TraditionalStrengthTraining', 'CoreTraining', 'Walking', 'MixedCardio', 'Rowing']
string = "HKWorkoutActivityType"
workout_type_list = [string + i for i in type_list]
#print(workout_type_list)

df_workouts = df_workouts[df_workouts['@workoutActivityType'].isin(workout_type_list)]
print(df_workouts['@workoutActivityType'].value_counts())
#%%

#I want to change the workout types so they're easier to read.
for i in range(len(type_list)):
    df_workouts.loc[df_workouts['@workoutActivityType'] == workout_type_list[i], df_workouts['@workoutActivityType']] = type_list[i]
#This method gives me a "SettingWithCopyWarning" (even though this is a solution I found for this warning). It does appear that the change is made to the DF, but if I can find a better solution that doesn't give me the warning that would be better.
print(df_workouts['@workoutActivityType'].value_counts())

#%%





















