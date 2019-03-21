from __future__ import print_function
from flask import Flask, json, request, render_template
from werkzeug.utils import secure_filename
from UploadForm import UploadForm
import time, boto3, requests, json, urllib.request, os

app = Flask('__name__')

@app.route('/', methods=['GET','POST'])
def index():
    form = UploadForm(request.form)
    return render_template('home.html', form=form)

@app.route('/aws')
def aws():
    return render_template('aws.html')


def getRequest(fileURL):

    transcript = requests.get(fileURL).json()
    print("Type: " + str(type(transcript)))
    print("\nThe Transcript: \n  " + transcript['results']['transcripts'][0]['transcript'])
    return transcript['results']['transcripts'][0]['transcript']


@app.route('/upload', methods=['GET','POST'])
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
    app.run(host="0.0.0.0", port=5000, debug = True)
