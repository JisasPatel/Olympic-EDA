#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 15:54:00 2023

@author: jisaspatel
"""

import pandas as pd
import prerprocessor as pre
import working as wr
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

data = pre.process()
years, regions, sports = wr.country_year_sport(data)

st.sidebar.image('4.png')

st.sidebar.title('OLYMPIC DATA ANALYSIS')
option = st.sidebar.radio('Select an option',
                 ('Home','Olympic Analysis','Medal tally','Country analysis','Athlete analysis')
)

if option == 'Home':
    st.sidebar.header('Home')
    st.header('DATA - set')
    st.dataframe(data)

if option == 'Olympic Analysis':
    st.sidebar.header('Olympic Analysis')
    
    max_year = data['Year'].max()
    min_year = data['Year'].min()
    
    c1, c2, c3 = st.columns(3)
   
    with c1:
        st.header('Countries')
        st.write(data['region'].nunique())
   
    with c2:
        st.header('Events')
        st.write(data['Event'].nunique())

    with c3:
        st.header('Sports')
        st.write(data['Sport'].nunique())
    
    c1, c2, c3 = st.columns(3)
   
    with c1:
        st.header('Athletes')
        st.write(data['Name'].nunique())
   
    with c2:
        st.header('Cities')
        st.write(data['City'].nunique())

    with c3:
        st.header('Years')
        total_years = max_year - min_year
        st.write(total_years)
    
    st.header('Number Of Countries Over The Years')
    country_over_years = wr.data_over_time(data, 'region')
    fig_c = px.line(country_over_years,x = 'Year', y='region',labels={'region':'Countries'})
    st.plotly_chart(fig_c)
    
    st.header('Number Of Events Over The Years')
    event_over_years = wr.data_over_time(data, 'Event')
    fig_e = px.line(event_over_years,x = 'Year', y='Event')
    st.plotly_chart(fig_e)
    
    st.header('Number Of Athletes Over The Years')
    athletes_over_years = wr.data_over_time(data, 'Name')
    fig_a = px.line(athletes_over_years,x = 'Year', y='Name',labels={'Name':'Athletes'})
    st.plotly_chart(fig_a)
    
    st.header('Number Of Events Over The Years For Each Sport')
    pivot = wr.get_pivot(data)
    fig_p = px.imshow(pivot,width=1000,height=1000,color_continuous_scale='sunset')
    st.plotly_chart(fig_p)
    

if option == 'Medal tally':
    st.sidebar.header('Medal Tally')
    selected_year = st.sidebar.selectbox("Year",years)
    selected_country = st.sidebar.selectbox("country",regions)
    temp = wr.get_medal_tally(data, selected_year, selected_country).drop(['index'],axis=1) 
    
    if ((selected_year=='OVERALL') and (selected_country == 'OVERALL')):
        max_g = temp['Gold'].max()
        max_s = temp['Silver'].max()
        max_b = temp['Bronze'].max()
        max_t = temp['Total'].max()
    
        c0, c1, c2, c3, c4 = st.columns(5)
       
        with c0:
            st.header('Max')
       
        with c1:
            st.header('Gold')
            st.write(max_g)
       
        with c2:
            st.header('Silver')
            st.write(max_s)
        
        with c3:
            st.header('Bronze')
            st.write(max_b)
        
        with c4:
            st.header('Total')
            st.write(max_t)
        st.header('Overall Medal Tally')
        st.dataframe(temp,use_container_width=True)
        
        st.title('Top 10 Countries Bar Chart')
        bar = st.selectbox("Select medal",["Gold","Silver","Bronze","Total"])
        if (bar == "Gold"):
            top10 = wr.get_top10_gold(temp)
            fig = px.bar(top10,x="region", y='Gold', title='Gold Medal bar chart',labels={'region':'Country','Gold':'Gold'} )
        
        if (bar == "Silver"):
            top10 = wr.get_top10_silver(temp)
            fig = px.bar(top10,x="region", y='Silver', title='Silver Medal bar chart',labels={'region':'Country','Silver':'Silver'})

        
        if (bar == "Bronze"):
            top10 = wr.get_top10_bronze(temp)
            fig = px.bar(top10,x="region", y='Bronze', title='Bronze Medal bar chart',labels={'region':'Country','Bronze':'Bronze'})

            
        if (bar == "Total"):
            top10 = wr.get_top10_total(temp)
            fig = px.bar(top10,x="region", y='Total', title='Total Medal bar chart',labels={'region':'Country','Total':'Total'})

        fig.update_xaxes(type='category')
        st.plotly_chart(fig)
        
        
        st.title('Overall Performance Of Athletes')
        med = st.selectbox("Select Medals",["Gold","Silver","Bronze","Total"])
        top20 = wr.top20_athlete(data,'OVERALL','Overall')
        if (med == "Gold"):
            top20 = top20.sort_values('Gold',ascending=False).reset_index().drop('index',axis=1)
        
        if (med == "Silver"):
            top20 = top20.sort_values('Silver',ascending=False).reset_index().drop('index',axis=1)
        
        if (med == "Bronze"):
            top20 = top20.sort_values('Bronze',ascending=False).reset_index().drop('index',axis=1)
            
        if (med == "Total"):
            top20 = top20.sort_values('Total',ascending=False).reset_index().drop('index',axis=1)
        st.table(top20.head(20))
        
        
        
        

   
    
    if ((selected_year!='OVERALL') and (selected_country == 'OVERALL')):
        
        max_g = temp['Gold'].max()
        max_s = temp['Silver'].max()
        max_b = temp['Bronze'].max()
        max_t = temp['Total'].max()
    
        st.header('Max Medal By A Country In Year '+ str(selected_year))
        c1, c2, c3, c4 = st.columns(4)
              
        with c1:
            st.header('Gold')
            st.write(max_g)
       
        with c2:
            st.header('Silver')
            st.write(max_s)
        
        with c3:
            st.header('Bronze')
            st.write(max_b)
        
        with c4:
            st.header('Total')
            st.write(max_t)
        
        st.header('Overall Medal Tally In ' + str(selected_year))
        st.dataframe(temp,use_container_width=True)
        
        st.title('Top 10 Countries Bar Chart')
        bar = st.selectbox("Select medal",["Gold","Silver","Bronze","Total"])
        if (bar == "Gold"):
            top10 = wr.get_top10_gold(temp)
            fig = px.bar(top10,x="region", y='Gold', title='Gold Medal bar chart',labels={'region':'Country','Gold':'Gold'} )
        
        if (bar == "Silver"):
            top10 = wr.get_top10_silver(temp)
            fig = px.bar(top10,x="region", y='Silver', title='Silver Medal bar chart',labels={'region':'Country','Silver':'Silver'})

        
        if (bar == "Bronze"):
            top10 = wr.get_top10_bronze(temp)
            fig = px.bar(top10,x="region", y='Bronze', title='Bronze Medal bar chart',labels={'region':'Country','Bronze':'Bronze'})

            
        if (bar == "Total"):
            top10 = wr.get_top10_total(temp)
            fig = px.bar(top10,x="region", y='Total', title='Total Medal bar chart',labels={'region':'Country','Total':'Total'})

        fig.update_xaxes(type='category')
        st.plotly_chart(fig)
        
        st.title('Top Athletes In '+str(selected_year))
        data_ath = wr.top_athletes(data, selected_country, selected_year)
        data_ath = data_ath.sort_values(['Gold','Total'],ascending=False).reset_index().drop('index',axis=1)
        st.dataframe(data_ath.head(10),use_container_width=True)



    if ((selected_year=='OVERALL') and (selected_country != 'OVERALL')):
        max_g = temp['Gold'].max()
        max_s = temp['Silver'].max()
        max_b = temp['Bronze'].max()
        max_t = temp['Total'].max()
    
        st.header('Max Medal Of '+ selected_country+' in a year')
        c1, c2, c3, c4 = st.columns(4)
       
        with c1:
            st.header('Gold')
            st.write(max_g)
       
        with c2:
            st.header('Silver')
            st.write(max_s)
        
        with c3:
            st.header('Bronze')
            st.write(max_b)
        
        with c4:
            st.header('Total')
            st.write(max_t)
        
        
        st.header('Overall Medal Tally Of ' +selected_country)
        st.dataframe(temp,use_container_width=True)
        
        st.title('Line chart of medals over the years')
        bar = st.selectbox("Select medal",["Gold","Silver","Bronze","Total"])
        if (bar == "Gold"):
            fig = px.line(temp,x='Year',y='Gold',title='line chart for gold')
        
        if (bar == "Silver"):
            fig = px.line(temp,x='Year',y='Silver',title='line chart for silver')
        
        if (bar == "Bronze"):
            fig = px.line(temp,x='Year',y='Bronze',title='line chart for bronze')
            
        if (bar == "Total"):
            fig = px.line(temp,x='Year',y='Total',title='line chart for total')
            
        st.plotly_chart(fig)
        
        st.title('Athletes of '+selected_country)
        data_ath = wr.top_athletes(data, selected_country, selected_year)
        data_ath = data_ath.sort_values(['Gold','Total'],ascending=False).reset_index().drop('index',axis=1)
        st.dataframe(data_ath.head(10),use_container_width=True)
        
        
    if ((selected_year!='OVERALL') and (selected_country != 'OVERALL')):
        st.header('Medal tally of ' +selected_country +" in " +str(selected_year))
        st.dataframe(temp,use_container_width=True)
        st.title('Top Athletes Of '+selected_country+' in '+str(selected_year))
        data_ath = wr.top_athletes(data, selected_country, selected_year)
        data_ath = data_ath.sort_values('Gold',ascending=False).reset_index().drop('index',axis=1)
        st.dataframe(data_ath.head(10),use_container_width=True)




    

if option == 'Country analysis':
    st.sidebar.header('country analysis')
    r_temp = regions.copy()
    r_temp.remove('OVERALL')
    r_temp.remove('India')
    r_temp.insert(0,'India')

    selected_country = st.sidebar.selectbox("Select a country",r_temp)        
    temp = wr.get_medal_tally(data, 'OVERALL', selected_country).drop(['index'],axis=1)
    tmp_bar_chart = wr.get_medal_tally(data, 'OVERALL', 'OVERALL').drop(['index'],axis=1)
    
    st.title('Total No. Of Medals Won')
    tmp_medals = wr.medals_per_country(data).rename(columns={'region':'Country','Name':'No. Of Medals Won'}).sort_values('No. Of Medals Won',ascending=False).reset_index().drop('index',axis=1)
    st.dataframe(tmp_medals,use_container_width=True)
    
    st.title('Top 10 Countries With Highest No Of Medals ')
    bar = st.selectbox("Select medal",["Gold","Silver","Bronze","Total"])
    if (bar == "Gold"):
        top10 = wr.get_top10_gold(tmp_bar_chart)
        fig = px.bar(top10,x="region", y='Gold', title='Gold Medal bar chart',labels={'region':'Country','Gold':'Gold'} )
    
    if (bar == "Silver"):
        top10 = wr.get_top10_silver(tmp_bar_chart)
        fig = px.bar(top10,x="region", y='Silver', title='Silver Medal bar chart',labels={'region':'Country','Silver':'Silver'})

    
    if (bar == "Bronze"):
        top10 = wr.get_top10_bronze(tmp_bar_chart)
        fig = px.bar(top10,x="region", y='Bronze', title='Bronze Medal bar chart',labels={'region':'Country','Bronze':'Bronze'})

        
    if (bar == "Total"):
        top10 = wr.get_top10_total(tmp_bar_chart)
        fig = px.bar(top10,x="region", y='Total', title='Total Medal bar chart',labels={'region':'Country','Total':'Total'})

    fig.update_xaxes(type='category')
    st.plotly_chart(fig)
    
    
    
    st.title(selected_country +"'s medals over the years")

    line = st.selectbox("Select medal for "+selected_country,["Gold","Silver","Bronze","Total"])
    if (line == "Gold"):
        fig = px.line(temp,x='Year',y='Gold',title='line chart for gold')
    
    if (line == "Silver"):
        fig = px.line(temp,x='Year',y='Silver',title='line chart for silver')
    
    if (line == "Bronze"):
        fig = px.line(temp,x='Year',y='Bronze',title='line chart for bronze')
    
    if (line == "Total"):
        fig = px.line(temp,x='Year',y='Total',title='line chart for total')
        
    st.plotly_chart(fig)

    st.title(selected_country+"'s performance in different sports over the years")
    heat_data = wr.heat_data_for_region(data,selected_country)
    fig_heat = px.imshow(heat_data,width=1000,height=1000,color_continuous_scale='sunset')
    st.plotly_chart(fig_heat)
    

    st.title('Top performing athletes from '+selected_country)
    tmp_ath = wr.ath10_of_region(data, selected_country)
    st.table(tmp_ath)
    

    

if option == 'Athlete analysis':
    st.sidebar.header('Athlete analysis')
    st.title('Top 20 Athletes')
    c1, c2, c3= st.columns(3)
    with c1 :
        sp = st.selectbox("Select sports",sports)
    with c2:
        med = st.selectbox("Select Medals",["Gold","Silver","Bronze","Total"]) 
        
    with c3:
        sx = st.selectbox("Select Sex",["Overall","M","F"])
        
    top20 = wr.top20_athlete(data,sp,sx)
    if (med == "Gold"):
        top20 = top20.sort_values('Gold',ascending=False).reset_index().drop('index',axis=1)
    
    if (med == "Silver"):
        top20 = top20.sort_values('Silver',ascending=False).reset_index().drop('index',axis=1)
    
    if (med == "Bronze"):
        top20 = top20.sort_values('Bronze',ascending=False).reset_index().drop('index',axis=1)
        
    if (med == "Total"):
        top20 = top20.sort_values('Total',ascending=False).reset_index().drop('index',axis=1)
    st.table(top20.head(20))
    
    st.header('Male - Female Athletes Over The Years')
    tmp_yr_sx = data.groupby(['Year','Sex']).nunique()[['Name']].reset_index().sort_values('Year')
    fig_sx = px.line(tmp_yr_sx,height=600,width=800,x='Year',y='Name',color='Sex')
    st.plotly_chart(fig_sx)
    
    st.title('No Of Athlets Of Each Country')
    data_ath_country = wr.ath_per_country(data).rename(columns={'region':'Country','Name':'No. Of Athlete'}).sort_values('No. Of Athlete',ascending=False).reset_index().drop('index',axis=1)
    st.dataframe(data_ath_country,use_container_width=True)

    
    st.title('Top 10 Countries with Highest No Of Athletes Participation')
    fig_bar_athletes = px.bar(data_ath_country.head(10),x='Country',y='No. Of Athlete')
    st.plotly_chart(fig_bar_athletes)
    
    st.title('No of Athletes won medals')
    winner_country = wr.won_ath_country(data).rename(columns={'region':'Country','Name':'No. Of Athlete Won'}).sort_values('No. Of Athlete Won',ascending=False).reset_index().drop('index',axis=1)
    st.dataframe(winner_country,use_container_width=True)

    st.title('Top 10 Countries with Highest No Of Athletes winning a medal')
    fig_bar_winner = px.bar(winner_country.head(10),x='Country',y='No. Of Athlete Won')
    st.plotly_chart(fig_bar_winner)











