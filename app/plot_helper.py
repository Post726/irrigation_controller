import pandas as pd
import plotly
import plotly.express as px
import json
from datetime import datetime, date
from sqlalchemy.sql import column
from app.models import *


def plot_water(app):
    water_query = app.session.query(Water).where(column('zone').isnot(None))
    water_df = pd.read_sql(water_query.statement, water_query.session.bind)
    
    temp_query = app.session.query(Temperature)
    temp_df = pd.read_sql(temp_query.statement, temp_query.session.bind)
    
    fig = px.scatter(water_df, x="start_ts", y="gallons", color="alias")
    #fig.add_line(temp_df, x="ts", y="temp")
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def plot_timeline(app):
    zone_query = app.session.query(Zone)
    zones_df = pd.read_sql(zone_query.statement, zone_query.session.bind)
    
    schedule_query = app.session.query(Schedule).where(~column('disabled'))
    schedules_df = pd.merge(
        pd.read_sql(schedule_query.statement, schedule_query.session.bind)
        , zones_df
        , left_on='zone', right_on='number')
    
    today = str(date.today())
    
    schedules_df['start_time'] = pd.to_datetime(today + " " + schedules_df['scheduled_time'].astype(str))
    schedules_df['finished_time'] = pd.to_datetime(schedules_df['start_time']) + pd.to_timedelta(schedules_df['duration_minutes'], 'm')
    
    schedules_df['finished_in_past'] = schedules_df['start_time'] < datetime.now()
    
    schedules_df.loc[schedules_df['finished_in_past'], 'start_time'] = schedules_df['start_time'] + pd.Timedelta(days=1)
    schedules_df.loc[schedules_df['finished_in_past'], 'finished_time'] = schedules_df['finished_time'] + pd.Timedelta(days=1)
    
    
    fig = px.timeline(schedules_df, x_start="start_time", x_end="finished_time", y="alias", color="alias")
    
    fig.update_layout(xaxis=dict(
                      title='Timestamp', 
                      tickformat = '%H:%M:%S',
                  ))
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
