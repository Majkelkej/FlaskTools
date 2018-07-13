from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField

class ImportLogForm(FlaskForm):
    uploaded = TextAreaField('Uploaded')
    submit = SubmitField('Importera')
