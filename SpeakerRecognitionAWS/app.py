from __future__ import print_function
from flask import Flask, json, request, render_template, flash, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from UploadForm import UploadForm
import time, boto3, requests, json, urllib.request, os, random, botocore, xlsxwriter, io, datetime
from flaskext.mysql import MySQL
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
import JsonToSRT, JsonToSRTMultiChannel, JsonToStats, PrintToExcel

s3 = boto3.client(
   "s3",
)

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

app = Flask('__name__')
CORS(app)

# Initialize MYSQL
mysql = MySQL(app)
app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Initialize the app for use with this MySQL class
# mysql.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def int_to_boolean(intValue):
    if intValue == 1:
        return False
    else:
        return True

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

def upload_live_audio_to_s3(filename):
    try:
        s3.upload_file(
            filename,
            S3_BUCKET,
            filename, #this will be the route the file is stored in -> myS3Bucket/myBucketName/filename
            ExtraArgs={
                "ACL": "private",
                "ContentType": "wav" # audio file will always be wav with live audio
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return "{}{}".format(S3_LOCATION, filename)

def copy_filelike_to_filelike(src, dst, bufsize=16384):
    while True:
        buf = src.read(bufsize)
        if not buf:
            break
        dst.write(buf)

namesToTranscribe = []
@app.route('/postNames', methods=['GET', 'POST'])
def postNames():
    if request.method == "POST":
        list = request.form['names']
        str = ""
        for val in list:
            if val is not ",":
                str = str + val
            else:
                namesToTranscribe.append(str)
                str = ""
        namesToTranscribe.append(str)

# Global Var...
# I'm so sorry...
# I tried and tried, I couldnt get it to work without it
# Please help
transcriptData = {}
@app.route('/liveaudio', methods=['GET', 'POST'])
def liveaudio():
    if request.method == "POST":
        try:
            print("I should go first")
            filename = str(request.form['fileName'])
            username = str(request.form['username'])
            fileDescription = str(request.form['fileDescription'])
            numberOfSpeakersInteger = int(request.form['numberOfSpeakersField'])
            multipleChannelsBoolean = False
            fileContentType = "wav"

            file = io.BytesIO(request.files.get('data').read())
            filename = filename + ".wav"
            f = open(filename, 'wb')
            copy_filelike_to_filelike(file, f)

            if numberOfSpeakersInteger < 2:
                multipleSpeakersBoolean = False;
            else:
                multipleSpeakersBoolean = True;

            fileURL = str(upload_live_audio_to_s3(filename))
            TranscriptedFileURL = transcribe_audio_file(fileURL, filename, fileContentType, multipleSpeakersBoolean, numberOfSpeakersInteger, multipleChannelsBoolean)

            # Pass the JSON response URL and the SpeakerBoolean
            # to get the SRT format returned
            transcriptList = json_to_srt(TranscriptedFileURL, multipleSpeakersBoolean, multipleChannelsBoolean, "")

            # Pass the JSON response URL and get the confidence statistics returned
            statsList = json_to_stats(TranscriptedFileURL)

            transcriptData["transcript"] = transcriptList
            transcriptData["statistics"] = statsList
            transcriptData["fileName"] = filename
            transcriptData["fileURL"] = fileURL
            transcriptData["fileContentType"] = "wav"
            transcriptData["fileDescription"] = fileDescription
            transcriptData["userName"] = username
            transcriptData["multipleSpeakersBoolean"] = False
            transcriptData["numberOfSpeakersInteger"] = numberOfSpeakersInteger
            transcriptData["multipleChannelsBoolean"] = False

            f.close()
            os.remove(filename)
        except Exception as e:
            print("Error in live audio method" + str(e))
    if request.method == "GET":
        print("I should go second")
        return(render_template('transcript.html', transcriptData=transcriptData))

@app.route("/record", methods=['GET', 'POST'])
def record():
    form = UploadForm(request.form)
    return(render_template('record.html', form=form))

@app.route("/download", methods=['GET', 'POST'])
def download():
    return send_file("transcript.xlsx", as_attachment=True)


@app.route('/aws', methods=['GET', 'POST'])
def aws():
    form = UploadForm(request.form)
    # check if the post request has the file part
    if request.method == "POST" and form.validate():
        if 'file' not in request.files:
            flash('Missing file!', 'danger')
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
            numberOfSpeakersInteger = form.numberOfSpeakersField.data

            # If the expects only 0 or 1 speaker in the file, turn off speaker recognition
            # else - turn on
            if numberOfSpeakersInteger < 2:
                multipleSpeakersBoolean = False;
            else:
                multipleSpeakersBoolean = True;

            # Determine if users wants to enable Channel Idenfitication
            # Convert String value from input field to bool value
            multipleChannelsBoolean = form.numberOfChannelsField.data
            multipleChannelsBoolean = int_to_boolean(multipleChannelsBoolean)
            currentTime = datetime.datetime.now()

            # Temporary - replace with a SQL query and do an s3id++ to increment id value by 1
            # Format to Create ID and store in MySQL: "S3_xxxxxx"
            # Upload the file to S3 and return the location it is stored in
            fileURL = str(upload_file_to_s3(file, fileName, acl="private"))

            TranscriptedFileURL = transcribe_audio_file(fileURL, fileName, fileContentType, multipleSpeakersBoolean, numberOfSpeakersInteger, multipleChannelsBoolean)
            # Pass the JSON response URL and the SpeakerBoolean
            # to get the SRT format returned
            transcriptList = json_to_srt(TranscriptedFileURL, multipleSpeakersBoolean, multipleChannelsBoolean, namesToTranscribe)
            # Pass the JSON response URL and get the confidence statistics returned
            statsList = json_to_stats(TranscriptedFileURL)

            transcriptData = {}
            transcriptData["transcript"] = transcriptList
            transcriptData["statistics"] = statsList
            transcriptData["fileName"] = fileName
            transcriptData["fileURL"] = fileURL
            transcriptData["fileContentType"] = fileContentType
            transcriptData["fileDescription"] = fileDescription
            transcriptData["userName"] = userName
            transcriptData["multipleSpeakersBoolean"] = multipleSpeakersBoolean
            transcriptData["numberOfSpeakersInteger"] = numberOfSpeakersInteger
            transcriptData["multipleChannelsBoolean"] = multipleChannelsBoolean

            PrintToExcel.print_to_excel(transcriptData)

            # MySQL cursor to execute commands
            # Compatable with the flaskext.mysql module
            cur = mysql.get_db().cursor()

            # Check to see if the user exists already
            result = cur.execute("SELECT * FROM users WHERE username = %s", [userName])
            print("Result: " + str(result))

            # User Does not Exist - so add to DB
            if result == 0:
                # Execute MySQL
                cur.execute("INSERT INTO users(username) VALUES (%s)", [userName])
                # Commit

                mysql.get_db().commit()
                # Close connection cursor
            # Get the UserID
            userId = cur.execute("SELECT id FROM users WHERE username = %s", [userName])
            userId = cur.fetchone()

            cur.execute("INSERT INTO Transcripts(userID) VALUES (%s)", [userId])
            lastRow = cur.execute("SELECT TranscriptID FROM Transcripts ORDER BY TranscriptID DESC LIMIT 1")
            lastRow = cur.fetchone()
            lastRow = lastRow[0]

            cur.execute("UPDATE Transcripts SET filename =  '" + str(fileName) + "' WHERE TranscriptID = '" + str(lastRow) + "'")
            cur.execute("UPDATE Transcripts SET fileDescription =  '" + str(fileDescription) + "' WHERE TranscriptID = '" + str(lastRow) + "'")
            cur.execute("UPDATE Transcripts SET transcriptLocation =  '" + str(TranscriptedFileURL) + "' WHERE TranscriptID = '" + str(lastRow) + "'")
            cur.execute("UPDATE Transcripts SET fileFormat =  '" + str(fileContentType) + "' WHERE TranscriptID = '" + str(lastRow) + "'")
            cur.execute("UPDATE Transcripts SET fileLocation =  '" + str(fileURL) + "' WHERE TranscriptID = '" + str(lastRow) + "'")
            cur.execute("UPDATE Transcripts SET numberOfSpeakers =  '" + str(numberOfSpeakersInteger) + "' WHERE TranscriptID = '" + str(lastRow) + "'")
            cur.execute("UPDATE Transcripts SET channelIdentification =  '" + str(multipleChannelsBoolean) + "' WHERE TranscriptID = '" + str(lastRow) + "'")
            cur.execute("UPDATE Transcripts SET transcriptionDate =  '" + str(currentTime) + "' WHERE TranscriptID = '" + str(lastRow) + "'")

            mysql.get_db().commit()
            cur.close()

            return(render_template('transcript.html', transcriptData=transcriptData))
        return(render_template('aws.html', form=form))
    return(render_template('aws.html', form=form))

@app.route('/azure')
def azure():
    return render_template('azureVerification.html')

@app.route('/demo.html')
def demo():
    return render_template('demo.html')

@app.route('/recorder.js')
def recorder():
    return render_template('recorder.js')

@app.route('/transcribe_azure.html', endpoint = "transcribe_azure.html")
def transcribe_azure():
    return render_template('transcribe_azure.html')


# Convert the hard to read json response to SRT Format
# This format will allow the user to see who spoke when
# For more info, reference JsonToSRT.py and JsonToSRTMultiChannel.py
# The MultiChannel and MultiSpeaker responses are different, so different methods
#   are needed to parse them
def json_to_srt(fileURL, multipleSpeakersBoolean, multipleChannelsBoolean, namesToTranscribe):
    jsonData = requests.get(fileURL).json()

    if multipleSpeakersBoolean:
        return JsonToSRT.convertJsonToSRT(jsonData, namesToTranscribe)
    elif multipleChannelsBoolean:
        return JsonToSRTMultiChannel.convertJsonToSRT(jsonData)
    else:
        return JsonToSRT.convertJsonToSRT_singleSpeaker(jsonData)

def json_to_stats(fileURL):
    jsonData = requests.get(fileURL).json()
    statsList = JsonToStats.get_stats_from_json(jsonData)
    return statsList

def create_settings_object(multipleSpeakersBoolean, numberOfSpeakers, multipleChannelsBoolean):
    # If there will be multiple Speakers
    # By AWS Requirments,
    #   - Max Speaker Label must be between 2 - 10
    #   - Channel Identifcation must be False
    #   - Shower Speaker labels must be true

    # If the multiple speakers settings is ON
    if multipleSpeakersBoolean:
        return   {
                  "MaxSpeakerLabels": numberOfSpeakers,
                  "ShowSpeakerLabels": True,
                  "ChannelIdentification": False
                  }

    # If there is just 1 speaker on 1 channel
    # Leave settings object empty
    if not multipleSpeakersBoolean and numberOfSpeakers < 2:
        return { }

    # If the multiple channels settings is ON
    if multipleChannelsBoolean:
        return { "ChannelIdentification": True }

def transcribe_audio_file(objectFileURL, fileName, fileContentType, multipleSpeakersBoolean, numberOfSpeakers, multipleChannelsBoolean):
    #Create the transcribe client
    transcribe = boto3.client('transcribe')
    customSettings = create_settings_object(multipleSpeakersBoolean, numberOfSpeakers, multipleChannelsBoolean)

    # ShowSpeakerLabels must be turned on along with a valid int in MaxSpeakerLabels if speaker recognition is on
    try:
        transcribe.start_transcription_job(
          TranscriptionJobName = fileName,
          Media={'MediaFileUri': objectFileURL},
          MediaFormat=fileContentType[-3:], #get the last 3 characters which is the media type: mp3, wav
          LanguageCode='en-US',
          Settings = customSettings
          )
        while True:
          status = transcribe.get_transcription_job(TranscriptionJobName=fileName)
          if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
              break
          print("Waiting on AWS Transcribe...")
          time.sleep(5)
        print(status)

    except Exception as e:
      # Job Name already exists, overwrite it
      # Job Names are based off of the filenames in S3
      if "The requested job name already exists" in str(e):
          print("Transcription Job name already exists...")
          print("Overwriting with this job...")

          response = transcribe.delete_transcription_job(TranscriptionJobName=fileName)
          if "HTTPStatusCode': 200" in str(response):
              print("Success! I deleted the old transcription job.")
              print("Rerunning transcription attempt...")
              return transcribe_audio_file(objectFileURL, fileName, fileContentType, multipleSpeakersBoolean, numberOfSpeakers, multipleChannelsBoolean)
      else:
          print("Error!" + str(e))

    TranscriptedFileURL = status['TranscriptionJob']['Transcript']['TranscriptFileUri']


    return TranscriptedFileURL

if __name__ == '__main__':
    app.secret_key = 'itsNotASecretIfItsInVersionControl' # TODO: Figure out how to put this in the config file
    app.run(host="0.0.0.0", port=5000, debug = True)
