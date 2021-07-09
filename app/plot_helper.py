import pandas as pd
import plotly
import plotly.express as px
import json
from app.models import Water, Temperature
from sqlalchemy.sql import column

def get_fig(app):
    water_query = Water.query.where(column('zone').isnot(None))
    water_df = pd.read_sql(water_query.statement, water_query.session.bind)
    
    temp_query = Temperature.query
    temp_df = pd.read_sql(temp_query.statement, temp_query.session.bind)
    
    fig = px.scatter(water_df, x="start_ts", y="gallons", color="alias")
    #fig.add_line(temp_df, x="ts", y="temp")
        
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
