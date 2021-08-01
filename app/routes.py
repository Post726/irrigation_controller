from flask import Flask, render_template, request, jsonify, url_for
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
from sqlalchemy.sql import column
import json
import os
import time
from app import app, board
from app.config import Config
from app.plot_helper import get_fig
from app.models import Zone, Water, Schedule
from app.forms import ZoneForm, ZonesForm, RunNowForm
from app.tasks import run_water
from app.board import pins


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()


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
    zoneList = app.session.query(Zone).all()
    scheduleList = app.session.query(Schedule).all()
        
    data = {
        'zones': zoneList,
        'schedules': scheduleList
        }
    
    zonesForm = ZonesForm(data=data)
        
    if zonesForm.validate_on_submit():
        for zoneForm in zonesForm.zones.entries:
            zone = app.session.query(Zone).get(zoneForm.data['number'])
            
            zone.alias = zoneForm.data['alias']
            
        for scheduleForm in zonesForm.schedules.entries:
            sched = app.session.query(Schedule).get(scheduleForm.data['number'])
            
            sched.zone = scheduleForm.data['zone']
            sched.disabled = bool(scheduleForm.data.get('disabled', False))
            sched.interval_days = scheduleForm.data['interval_days']
            sched.scheduled_time = scheduleForm.data['scheduled_time']
            sched.duration_minutes = scheduleForm.data['duration_minutes']
        
        app.session.commit()
        
        os.system('sudo systemctl restart irrigation')
        
        # create a message to send to the template
        message = f"Zones Updated!"
        return render_template('zones.html', form=zonesForm, message=message)
    else:
        return render_template('zones.html', form=zonesForm)


@app.route('/run_now', methods=['GET', 'POST'])
def runNow():
    runNowForm = RunNowForm()
    runNowForm.zone.choices = [(zone.number, zone.alias or "Not Set") for zone in app.session.query(Zone).all()]
    
    if runNowForm.validate_on_submit():
        zone = app.session.query(Zone).get(runNowForm.data['zone'])
        duration = runNowForm.data['duration']
        
        run_water.delay(zone.number, zone.alias, duration)
        
        # create a message to send to the template
        message = f"Running!"
        return render_template('run_now.html', form=runNowForm, message=message)
    else:
        return render_template('run_now.html', form=runNowForm)
    

@app.route('/data', methods=['GET'])
def data():
    water = app.session.query(Water).order_by(Water.start_ts.desc()).all()
    
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
