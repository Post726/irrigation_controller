from flask import Flask, render_template, request, jsonify, url_for
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
import json
import os
from config import Config
from models import db
from irrigation import sql_helper

from plot_helper import get_fig

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)
db.init_app(app)
bootstrap = Bootstrap(app)

from models import Zone, Water
from forms import ZoneForm, ZonesForm


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
        return render_template('zones.html', zonesForm=zonesForm, message=message)
    else:
        return render_template('zones.html', zonesForm=zonesForm)
    

@app.route('/data', methods=['GET'])
def data():
    water = Water.query.all()
    
    return render_template('data.html', water=water)


@app.route('/plot', methods=['GET'])
def plot():
    plot_json = get_fig(app)
    return render_template('plot.html', plot_json=plot_json)


if __name__ == "__main__":
    #db.drop_all()
    #db.session.commit()
    #db.create_all()
    #init_zones()

    app.run(debug=True, host='0.0.0.0', port=8888)