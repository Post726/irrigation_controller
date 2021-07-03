from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Zone(db.Model):
    __tablename__ = 'zone'
    
    number = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(length=128))
    disabled = db.Column(db.Boolean, default=True)
    interval_days = db.Column(db.Integer, default=1)
    scheduled_time = db.Column(db.Time)
    duration_minutes = db.Column(db.Integer, default=60)

    def __init__(self, number=None, alias=None, disabled=None, interval_days=None, scheduled_time=None, duration_minutes=None):
        self.number = number
        self.alias = alias
        self.disabled = disabled
        self.interval_days = interval_days
        self.scheduled_time = scheduled_time
        self.duration_minutes = duration_minutes
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    
def init_zones():
    for i in range(1,7):
        if not Zone.query.get(i):
            zone = Zone(i)
            db.session.add(zone) 
        
    db.session.commit()


class Water(db.Model):
    __tablename__ = 'water'
    
    zone = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(length=128))
    start_ts = db.Column(db.DateTime, primary_key=True)
    end_ts = db.Column(db.DateTime, default=datetime.utcnow)
    gallons = db.Column(db.Float)
    
    def __init__(self, zone=None, alias=None, start_ts=None, gallons=None, end_ts=None):
        self.zone = zone
        self.alias = alias
        self.start_ts = start_ts
        self.gallons = gallons
        self.end_ts = end_ts


class Temperature(db.Model):
    __tablename__ = 'temperature'
    
    ts = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    temp = db.Column(db.Float)
    
    def __init__(self, temp=None, ts=None):
        self.temp = temp
        self.ts = ts
    