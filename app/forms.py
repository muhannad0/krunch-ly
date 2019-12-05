from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from app.models import Links

class LinkForm(FlaskForm):
    longLink = StringField('Enter URL', validators=[DataRequired(), URL(require_tld=True, message='Invalid URL. Should be eg: http://xyz.com')])
    submit = SubmitField('Shorten')