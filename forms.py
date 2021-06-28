from flask_wtf import FlaskForm
from wtforms import validators, SubmitField, HiddenField, StringField, IntegerField, BooleanField, TimeField, FieldList, FormField
from wtforms.fields import html5 as h5fields


class ZoneForm(FlaskForm):
    number = HiddenField('ID')
    alias = StringField('Name', [validators.optional()])
    disabled = BooleanField('Disabled', [validators.optional()])
    interval_days = h5fields.IntegerField('Interval (days)', [validators.optional()])
    scheduled_time = h5fields.TimeField('Time', [validators.optional()])
    duration_minutes = h5fields.IntegerField('Duration (minutes)', [validators.optional()])
     
 
class ZonesForm(FlaskForm):
    zones = FieldList(FormField(ZoneForm), min_entries=6, max_entries=6)
    submit = SubmitField('Update')