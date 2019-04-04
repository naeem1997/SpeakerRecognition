from wtforms import Form, StringField, TextAreaField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class UploadForm(Form):
    userName = StringField('Username', validators=[DataRequired()])
    fileName = StringField('File Name', validators=[DataRequired()])
    fileDescription = StringField('File Description', validators=[DataRequired()])
    multipleSpeakersRadioButton = RadioField('Multiple Speakers', choices=[('False','1 Speaker'),('True','2+ Speakers')])
    # AWS Transcribe Limits numbers of speakers with minimum of 2 and max of 10
    numberOfSpeakersField = IntegerField('Number of Speakers', validators=[NumberRange(min=2, max=10)])
    multipleChannelsRadioButton = RadioField('Multiple Channels', choices=[('False','1 Channel'),('True','2 Channels')])
    # Do not need another IntegerField for channels, Transcribe limits the maximum # of channls to 2
    submit = SubmitField('Submit')
