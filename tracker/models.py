from sqlite3.dbapi2 import Date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

from datetime import datetime
today = datetime.today()

from .db import get_last_weight

class weight(FlaskForm):

    weight =  StringField('Enter your weight', validators=[DataRequired()])
    date =  DateField('Date', validators=[DataRequired()], default = today)
    summit = SubmitField('Submit')

    

