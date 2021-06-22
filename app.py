from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField, BooleanField, TimeField, FieldList, FormField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange
import json
from irrigation import sql_helper

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

# Flask-Bootstrap requires this line
Bootstrap(app)

db_name = 'sockmarket.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://irrigation:cali@localhost/irrigation'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Zone(db.Model):
    __tablename__ = 'zone'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=128))
    disabled = db.Column(db.Boolean)
    interval_days = db.Column(db.Integer)
    scheduled_time = db.Column(db.Time)
    duration_minutes = db.Column(db.Integer)

    def __init__(self, id, name, disabled, interval_days, scheduled_time, duration_minutes):
        self.id = id
        self.name = name
        self.disabled = disabled
        self.interval_days = interval_days
        self.scheduled_time = scheduled_time
        self.duration_minutes = duration_minutes


class ZoneForm(FlaskForm):
    id = IntegerField('ID')
    name = StringField('Name')
    disabled = BooleanField('Disabled', default=True)
    interval_days = IntegerField('Interval (days)')
    scheduled_time = TimeField('Time')
    duration_minutes = IntegerField('Duration (minutes)', default=60)
    
    # submit = SubmitField('Add/Update Zone')

class ZoneListForm(FlaskForm):
    FieldList(FormField(ZoneForm))
    
    submit = SubmitField('Add/Update Zone')



@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form1 = ZoneForm(obj=Zone.query.get(1))
    if form1.validate_on_submit():
        record = Zone.query.get(request.form['id'])
        
        if record is None:
            record = Zone(request.form['id'], request.form['name'], bool(request.form.get('disabled', False)), request.form['interval_days'], request.form['scheduled_time'], request.form['duration_minutes'])
            db.session.add(record)
        else:
            record.id = request.form['id']
            record.name = request.form['name']
            record.disabled = bool(request.form.get('disabled', False))
            record.interval_days = request.form['interval_days']
            record.scheduled_time = request.form['scheduled_time']
            record.duration_minutes = request.form['duration_minutes']
        
        db.session.commit()
        # create a message to send to the template
        message = f"The data for sock name has been submitted."
        return render_template('add_zone.html', message=message)
    else:
        # show validaton errors
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_zone.html', form1=form1)

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/data", methods=["GET"])
def list_data():
    return jsonify({'water': sql_helper.Water().get_list()})


@app.route("/zones", methods=["GET", "POST"])
def zones():
    if request.method == 'GET':
        # send the form
        return render_template('zones.html')
    else: # request.method == 'POST':
        # todo
        return render_template("zones.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=8888)