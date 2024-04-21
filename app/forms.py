from flask_wtf import FlaskForm
from wtforms import validators, SubmitField, HiddenField, StringField, IntegerField, BooleanField, TimeField, FieldList, FormField, SelectField
from wtforms.fields import html5 as h5fields


class ZoneForm(FlaskForm):
    number = HiddenField('ID')
    alias = StringField('Name', [validators.optional()])
     
 
class ZonesForm(FlaskForm):
    zones = FieldList(FormField(ZoneForm), min_entries=6, max_entries=6)
    submit = SubmitField('Update')


class ScheduleForm(FlaskForm):
    number = HiddenField('ID')
    zone = SelectField('Zone', choices=[])
    disabled = BooleanField('Disabled', [validators.optional()])
    interval_days = h5fields.IntegerField('Interval (days)', [validators.optional()])
    scheduled_time = h5fields.TimeField('Time', [validators.optional()])
    duration_minutes = h5fields.IntegerField('Duration (minutes)', [validators.optional()])
     
 
class SchedulesForm(FlaskForm):
    schedules = FieldList(FormField(ScheduleForm), min_entries=12, max_entries=12)
    submit = SubmitField('Update')
    

class RunNowForm(FlaskForm):
    zone = SelectField('Zone', choices=[])
    duration = h5fields.IntegerField('Duration (minutes)', default=1)
    submit = SubmitField('Run Now!')
    