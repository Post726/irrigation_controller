from sqlalchemy import Column, Integer, String, Boolean, Time, DateTime, Float
from app.database import Base
from datetime import datetime


class Zone(Base):
    __tablename__ = 'zone'
    
    number = Column(Integer, primary_key=True)
    alias = Column(String(length=128))
    disabled = Column(Boolean, default=True)
    interval_days = Column(Integer, default=1)
    scheduled_time = Column(Time)
    duration_minutes = Column(Integer, default=60)

    def __init__(self, number=None, alias=None, disabled=None, interval_days=None, scheduled_time=None, duration_minutes=None):
        self.number = number
        self.alias = alias
        self.disabled = disabled
        self.interval_days = interval_days
        self.scheduled_time = scheduled_time
        self.duration_minutes = duration_minutes
    
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    
    
def init_zones(app):
    for i in range(1,7):
        if not Zone.query.get(i):
            zone = Zone(i)
            app.session.add(zone) 
        
    app.session.commit()


class Water(Base):
    __tablename__ = 'water'
    
    zone = Column(Integer, primary_key=True)
    alias = Column(String(length=128))
    start_ts = Column(DateTime, primary_key=True)
    end_ts = Column(DateTime, default=datetime.utcnow)
    gallons = Column(Float)
    
    def __init__(self, zone=None, alias=None, start_ts=None, gallons=None, end_ts=None):
        self.zone = zone
        self.alias = alias
        self.start_ts = start_ts
        self.gallons = gallons
        self.end_ts = end_ts


class Temperature(Base):
    __tablename__ = 'temperature'
    
    ts = Column(DateTime, primary_key=True, default=datetime.utcnow)
    temp = Column(Float)
    
    def __init__(self, temp=None, ts=None):
        self.temp = temp
        self.ts = ts
    