#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 09:47:39 2023

@author: jisaspatel
"""

import pandas as pd
import numpy as np
import prerprocessor

def medals_per_country(data):
    tmp = data.copy()
    tmp.dropna(subset=['Medal'],inplace=True)
    tmp.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal','region','Gold','Silver','Bronze'],inplace=True)
    tmp = tmp.groupby('region').count()['Name'].reset_index()
    return tmp    


def won_ath_country(data):
    tmp = data.copy()
    tmp.dropna(subset=['Medal'],inplace=True)
    tmp.drop_duplicates(subset=['Name'],inplace=True)
    tmp = tmp.groupby('region').count()['Name'].reset_index()
    return tmp

def ath_per_country(data):
    tmp = data.copy()
    tmp.drop_duplicates(subset=['Name'],inplace=True)
    tmp = tmp.groupby('region').count()['Name'].reset_index()
    return tmp


def top_athletes(data,region,year):
 #   x = data['Medal'].dropna()
    x = data.copy()
    x.dropna(subset=['Medal'],inplace=True)
    if((region=='OVERALL') &  (year == 'OVERALL')):
        ath = x.groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    if((region!='OVERALL') &  (year == 'OVERALL')):
        ath = x[x['region']==region].groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    if((region=='OVERALL') &  (year != 'OVERALL')):
        ath = x[x['Year']==year].groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    if((region!='OVERALL') &  (year != 'OVERALL')):
        ath = x[(x['region']==region) & (x['Year']==year)].groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    ath['Total'] = ath['Gold']+ath['Silver']+ath['Bronze']   
    return ath

def heat_data_for_region(data,selected_country):
    medal_dropedna = data.dropna(subset=['Medal'])
    medal_droped_duplicates = medal_dropedna.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal','region','Gold','Silver','Bronze'])
    new_medal_region = medal_droped_duplicates[medal_droped_duplicates['region']==selected_country]
    region_sport_pivot = new_medal_region.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count')
    region_sport_pivot = region_sport_pivot.fillna(0).astype('int')
    return region_sport_pivot

def ath10_of_region(data,region):
    
    if(region=='OVERALL'):
        ath=  data.groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    else:
        ath = data[data['region']==region].groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    ath['Total'] = ath['Gold']+ath['Silver']+ath['Bronze']
    ath = ath.sort_values('Total',ascending=False).reset_index().drop('index',axis=1)
    return ath.head(10)

def top20_athlete(data,sport,sex):
    if((sport=='OVERALL' )&(sex=='Overall') ): 
        ath = data.groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    elif((sport!='OVERALL' )&(sex=='Overall')):
        ath = data[data['Sport']==sport].groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    elif((sport=='OVERALL' )&(sex!='Overall')):
        ath = data[data['Sex']==sex].groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    else:
        ath = data[(data['Sport']==sport) & (data['Sex']==sex)].groupby('Name').sum()[['Gold','Silver','Bronze']].reset_index()
    
    ath['Total'] = ath['Gold']+ath['Silver']+ath['Bronze']    
    return ath

def get_pivot(data):
    tmp = data.drop_duplicates(['Year','Sport','Event'])
    tmp = tmp.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int')
    return tmp


def get_top10_gold(data):
    tmp = data.copy()
    tmp = tmp.sort_values('Gold',ascending=False).reset_index().drop('index',axis=1)
    return tmp.head(10)

def get_top10_silver(data):
    tmp = data.copy()
    tmp = tmp.sort_values('Silver',ascending=False).reset_index().drop('index',axis=1)
    return tmp.head(10)

def get_top10_bronze(data):
    tmp = data.copy()
    tmp = tmp.sort_values('Bronze',ascending=False).reset_index().drop('index',axis=1)
    return tmp.head(10)

def get_top10_total(data):
    tmp = data.copy()
    tmp = tmp.sort_values('Total',ascending=False).reset_index().drop('index',axis=1)
    return tmp.head(10)

def data_over_time(data,title):
    tmp = data.groupby('Year').nunique()[[title]].reset_index().sort_values('Year')
    return tmp

def get_medal_tally(data,year,country):
    
    medal_droped = data.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal','region','Gold','Silver','Bronze'])  
    flag=0
    if ((year=='OVERALL') and (country == 'OVERALL')):
        tmp = medal_droped
        
    if ((year!='OVERALL') and (country == 'OVERALL')):
        tmp = medal_droped[medal_droped['Year']==year].sort_values(by='region').reset_index()

    if ((year=='OVERALL') and (country != 'OVERALL')):
        flag=1
        tmp = medal_droped[medal_droped['region']==country].sort_values(by='Year').reset_index()
        
    if ((year!='OVERALL') and (country != 'OVERALL')):
        tmp = medal_droped[(medal_droped['Year']==year) & (medal_droped['region']==country)].reset_index()
        
    if(flag==0):
        x = tmp.groupby('region').sum()[['Gold','Silver','Bronze']].reset_index().sort_values('Gold',ascending=False).reset_index()
    else:
        x = tmp.groupby('Year').sum()[['Gold','Silver','Bronze']].reset_index().sort_values('Year').reset_index()
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze'] 
    return x
    

def country_year_sport(data):
    years = data['Year'].unique().tolist()
    years.sort()
    years.insert(0,'OVERALL')
    regions = data['region'].dropna().unique().tolist()
    regions.sort()
    regions.insert(0,'OVERALL')
    sport = data['Sport'].dropna().unique().tolist()
    sport.sort()
    sport.insert(0,'OVERALL')
    return years, regions, sport    
