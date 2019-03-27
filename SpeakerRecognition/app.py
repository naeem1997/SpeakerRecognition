from __future__ import print_function
from flask import Flask, json, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from UploadForm import UploadForm
import time, boto3, requests, json, urllib.request, os
from flask_mysqldb import MySQL

ALLOWED_EXTENSIONS = set(['wav'])



app = Flask('__name__')

app.config.from_pyfile('../config.py')

# Initialize MYSQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/aws', methods=['GET', 'POST'])
def aws():
    form = UploadForm(request.form)
    if request.method == "POST" and form.validate():
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        #the actual filename from the uploaded file
            filename = secure_filename(file.filename)




        userName = form.userName.data

        # MySQL cursor to execute commands
        cur = mysql.connection.cursor()

        # Execute MySQL
        cur.execute("INSERT INTO users(username) VALUES (%s)", [userName])

        # Commit
        mysql.connection.commit()

        # Close connection cursor
        cur.close()

        # TODO:
        flash('This message will be lost!', 'success')
        return redirect(url_for('index'))
    return render_template('aws.html', form=form)


def getRequest(fileURL):

    transcript = requests.get(fileURL).json()
    print("Type: " + str(type(transcript)))
    print("\nThe Transcript: \n  " + transcript['results']['transcripts'][0]['transcript'])
    return transcript['results']['transcripts'][0]['transcript']


@app.route('/upload', methods=['POST'])
def uploadAudioFile():
    transcribe = boto3.client('transcribe')
    job_name = "TwoSpeakersTest35"
    # one speaker:
    # job_uri = "https://s3.us-east-2.amazonaws.com/4485testasr/testAudioFile.mp3"
    # two speakers:
    # job_uri = "https://s3.us-east-2.amazonaws.com/4485testasr/liveRecording.wav"
    # transcribe.start_transcription_job(
    #   TranscriptionJobName=job_name,
    #   Media={'MediaFileUri': job_uri},
    #   MediaFormat='wav',
    #   LanguageCode='en-US',
    #   Settings = {
    #             "ChannelIdentification": False,
    #             #"MaxSpeakerLabels": 0,
    #             #"ShowSpeakerLabels": False
    #
    #             }
    # )
    # while True:
    #   status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    #   if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
    #       break
    #   print("Not ready yet...")
    #   time.sleep(5)
    # print(status)
    #
    # TranscriptedFileURL = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    # print(TranscriptedFileURL)
    # transcript = getRequest(TranscriptedFileURL)
    #
    return render_template('upload.html')#), transcript = transcript)




if __name__ == '__main__':
    app.secret_key = 'itsNotASecretIfItsInVersionControl' # TODO: Figure out how to put this in the config file
    app.run(host="0.0.0.0", port=5000, debug = True)
