from __future__ import print_function
import time
import boto3
import json
import requests

# this function will parse the response from AWS Transcribe
def getTranscriptionObject():
    TranscriptionJobObject = status['TranscriptionJob']
    TranscriptObject = TranscriptionJobObject['Transcript']
    TranscriptedFileURL = TranscriptObject['TranscriptFileUri']
    print("File Located at:")
    print(TranscriptedFileURL)
    r = requests.get(TranscriptedFileURL, allow_redirects=True)
    open('transcriptedFileData.txt', 'wb').write(r.content)


transcribe = boto3.client('transcribe')
job_name = "TwoSpeakersTest18"
# one speaker:
# job_uri = "https://s3.us-east-2.amazonaws.com/4485testasr/testAudioFile.mp3"
# two speakers:
job_uri = "https://s3.us-east-2.amazonaws.com/4485testasr/twoSpeakers.mp3"
transcribe.start_transcription_job(
  TranscriptionJobName=job_name,
  Media={'MediaFileUri': job_uri},
  MediaFormat='mp3',
  LanguageCode='en-US',
  Settings={'MaxSpeakerLabels': 2, "ShowSpeakerLabels": True}

)
while True:
  status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
  if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
      break
  print("Not ready yet...")
  time.sleep(5)
print(status)
getTranscriptionObject()
getTextFromTranscription()
