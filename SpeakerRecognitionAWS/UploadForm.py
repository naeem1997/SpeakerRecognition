from wtforms import Form, StringField, TextAreaField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class UploadForm(Form):
    userName = StringField('Username', validators=[DataRequired()])
    fileName = StringField('File Name', validators=[DataRequired()])
    fileDescription = TextAreaField('File Description', validators=[DataRequired()])
    # AWS Transcribe Limits numbers of speakers with minimum of 2 and max of 10
    numberOfSpeakersField = IntegerField('Number of Speakers')
    numberOfChannelsField = IntegerField('Number of Channels')
    # Do not need another IntegerField for channels, Transcribe limits the maximum # of channls to 2
    submit = SubmitField('Submit')
