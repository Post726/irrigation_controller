from app import app

if __name__ == "__main__":
    #db.drop_all()
    #db.session.commit()
    #db.create_all()
    #init_zones()
    
    #for zone in Zone.query.all():
    #    if not zone.disabled:
    #        schedule.every(zone.interval_days).day.at(zone.scheduled_time.strftime("%H:%M")).do(run_water, zone.number, zone.alias, zone.duration_minutes)

    app.run(debug=True, host='0.0.0.0', port=8888)