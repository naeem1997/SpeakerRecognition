from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(Form):
    fileName = StringField('File Name', validators=[DataRequired()])
    fileDescription = StringField('File Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
