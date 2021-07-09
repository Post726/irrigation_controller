from flask import Flask, render_template, request, jsonify, url_for
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from sqlalchemy.sql import column
import json
import os
import time
from app import app, board
from app.config import Config
from app.models import db
from app.plot_helper import get_fig
from app.models import Zone, Water
from app.forms import ZoneForm, ZonesForm, RunNowForm
from app.tasks import run_water
from app.board import pins


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/zones', methods=['GET', 'POST'])
def zones():
    zoneList = []
    for i in range(1,7):
        zoneList.append(Zone.query.get(i))
        
    data = {
        'zones': zoneList
        }
    
    zonesForm = ZonesForm(data=data)
        
    if zonesForm.validate_on_submit():
        for zoneForm in zonesForm.zones.entries:
            zone = Zone.query.get(zoneForm.data['number'])
            
            zone.alias = zoneForm.data['alias']
            zone.disabled = bool(zoneForm.data.get('disabled', False))
            zone.interval_days = zoneForm.data['interval_days']
            zone.scheduled_time = zoneForm.data['scheduled_time']
            zone.duration_minutes = zoneForm.data['duration_minutes']
        
        db.session.commit()
        
        os.system('sudo systemctl restart irrigation')
        
        # create a message to send to the template
        message = f"Zones Updated!"
        return render_template('zones.html', form=zonesForm, message=message)
    else:
        return render_template('zones.html', form=zonesForm)


@app.route('/run_now', methods=['GET', 'POST'])
def runNow():
    runNowForm = RunNowForm()
    runNowForm.zone.choices = [(zone.number, zone.alias) for zone in Zone.query.where(~column('disabled')).all()]
    
    if runNowForm.validate_on_submit():
        zone = Zone.query.get(runNowForm.data['zone'])
        duration = runNowForm.data['duration']
        
        run_water.delay(zone.number, zone.alias, duration)
        
        # create a message to send to the template
        message = f"Running!"
        return render_template('run_now.html', form=runNowForm, message=message)
    else:
        return render_template('run_now.html', form=runNowForm)
    

@app.route('/data', methods=['GET'])
def data():
    water = Water.query.order_by(Water.start_ts.desc()).all()
    
    return render_template('data.html', water=water)


@app.route('/plot', methods=['GET'])
def plot():
    plot_json = get_fig(app)
    return render_template('plot.html', plot_json=plot_json)


@app.route('/status/<int:zone>', methods=['GET'])
def zone_status(zone):
    status = board.get_state(pins[zone])
    if status is None:
        status = 'None status'
    return str(status)
