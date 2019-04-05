from __future__ import print_function
from flask import Flask, json, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from UploadForm import UploadForm
import time, boto3, requests, json, urllib.request, os
# Does not work on EC2
# from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
import random
import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

s3 = boto3.client(
   "s3",
   #aws_access_key_id = S3_KEY,
   #aws_secret_access_key = S3_SECRET
)

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

app = Flask('__name__')

# Initialize MYSQL
mysql = MySQL(app)
app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Initialize the app for use with this MySQL class
# mysql.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def string_to_boolean(stringValue):
    if stringValue == 'True':
        return True
    else:
        return False


def upload_file_to_s3(file, filename, acl):

    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            filename, #this will be the route the file is stored in -> myS3Bucket/myBucketName/filename
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return "{}{}".format(S3_LOCATION, filename)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/aws', methods=['GET', 'POST'])
def aws():
    form = UploadForm(request.form)
    # check if the post request has the file part
    if request.method == "POST" and form.validate():
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        # the file is stored here
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # All submitted form data can be forged, and filenames can be dangerous.
            # Secure them before adding to filesystem
            fileName = secure_filename(file.filename)
            # gets the audio/mp3 or audio/wav description
            fileContentType = file.content_type

            #the actual filename from the uploaded file
            print("Filename: " + fileName)
            print("fileContentType: " + fileContentType)
            # User must add thier username to make a transcription
            userName = form.userName.data
            # User can add a note when uploading the file
            fileDescription = form.fileDescription.data
            # Will return true of false - if user wants 1 or many users transcribed
            multipleSpeakersBoolean = form.multipleSpeakersRadioButton.data
            numberOfSpeakersInteger = form.numberOfSpeakersField.data
            multipleChannelsBoolean = form.multipleChannelsRadioButton.data

            # Convert String value to Bool value
            multipleSpeakersBoolean = string_to_boolean(multipleSpeakersBoolean)
            multipleChannelsBoolean = string_to_boolean(multipleChannelsBoolean)

            print("userName: " + userName)
            #return redirect(url_for('uploadAudioFile', filename=filename))

            # Temporary - replace with a SQL query and do an s3id++ to increment id value by 1
            # Format to Create ID and store in MySQL: "S3_xxxxxx"
            fileURL = str(upload_file_to_s3(file, fileName, acl="private"))
            print(fileURL)

            transcript = uploadAudioFile(fileURL, fileName, fileContentType, multipleSpeakersBoolean, numberOfSpeakersInteger, multipleChannelsBoolean)

            transcriptData = {}
            transcriptData["transcript"] = transcript
            transcriptData["fileName"] = fileName
            transcriptData["fileURL"] = fileURL
            transcriptData["fileContentType"] = fileContentType
            transcriptData["fileDescription"] = fileDescription
            transcriptData["userName"] = userName
            transcriptData["multipleSpeakersBoolean"] = multipleSpeakersBoolean
            transcriptData["numberOfSpeakersInteger"] = numberOfSpeakersInteger
            transcriptData["multipleChannelsBoolean"] = multipleChannelsBoolean

            # MySQL cursor to execute commands
            # Compatable with the flaskext.mysql module
            cur = mysql.get_db().cursor()

            # Check to see if the user exists already
            result = cur.execute("SELECT * FROM users WHERE username = %s", [userName])

            # User Does not Exist - so add to DB
            if result == 0:
                # Execute MySQL
                cur.execute("INSERT INTO users(username) VALUES (%s)", [userName])
                # Commit
                mysql.get_db().commit()
                # Close connection cursor
                cur.close()

            return(render_template('transcript.html', transcriptData=transcriptData))
        return(render_template('aws.html', form=form))
    return(render_template('aws.html', form=form))


import JsonToSRT

def parseJSON(fileURL):
    transcript = requests.get(fileURL).json()
    conversationList = JsonToSRT.convertJsonToSRT(transcript)
    #print("Type: " + str(type(transcript)))
    #print("\nThe Transcript: \n  " + transcript['results']['transcripts'][0]['transcript'])
    return conversationList


def uploadAudioFile(objectFileURL, fileName, fileContentType, multipleSpeakersBoolean, numberOfSpeakers, multipleChannelsBoolean):
    #Create the transcribe client
    transcribe = boto3.client('transcribe')

    # ShowSpeakerLabels must be turned on along with a valid int in MaxSpeakerLabels if speaker recognition is on
    try:
        transcribe.start_transcription_job(
          TranscriptionJobName = fileName,
          Media={'MediaFileUri': objectFileURL},
          MediaFormat=fileContentType[-3:], #get the last 3 characters which is the media type: mp3, wav
          LanguageCode='en-US',
          Settings = {
                    "MaxSpeakerLabels": numberOfSpeakers,
                    "ShowSpeakerLabels": multipleSpeakersBoolean,
                    "ChannelIdentification": multipleChannelsBoolean
                    }
          )
        while True:
          status = transcribe.get_transcription_job(TranscriptionJobName=fileName)
          if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
              break
          print("Not ready yet...")
          time.sleep(5)
        print(status)

    except:
      # Job Name already exists, overwrite it
      # Job Names are based off of the filenames in S3
      response = transcribe.delete_transcription_job(TranscriptionJobName=fileName)
      return uploadAudioFile(objectFileURL, fileName, fileContentType, multipleSpeakersBoolean, numberOfSpeakers, multipleChannelsBoolean)

    TranscriptedFileURL = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(TranscriptedFileURL)
    transcript = parseJSON(TranscriptedFileURL)

    return transcript

if __name__ == '__main__':
    app.secret_key = 'itsNotASecretIfItsInVersionControl' # TODO: Figure out how to put this in the config file
    app.run(host="0.0.0.0", port=5000, debug = True)
