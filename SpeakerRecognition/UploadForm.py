from wtforms import Form, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class UploadForm(Form):
    userName = StringField('Username', validators=[DataRequired()])
    fileName = StringField('File Name', validators=[DataRequired()])
    fileDescription = StringField('File Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
