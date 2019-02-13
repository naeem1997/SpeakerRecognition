from __future__ import print_function
from flask import Flask
import time
import boto3

app = Flask(__name__)

# TODO:

@app.route('/')
def main():
    transcribe = boto3.client('transcribe')
    job_name = "TranscriptionJob12345111Test"
    job_uri = "https://s3.us-east-2.amazonaws.com/4485testasr/testAudioFile.mp3"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
    print(status)





if __name__ == '__main__':
    app.run(debug=True)
