from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, DateField, IntegerField, TextAreaField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class ImportLogForm(FlaskForm):
    #import_csv = StringField('Importera fil (namn från validering)', validators=[DataRequired()], default='')
    uploaded = TextAreaField('Uploaded')
    submit = SubmitField('Importera')
