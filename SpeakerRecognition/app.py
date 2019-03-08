from __future__ import print_function
import time
import boto3
import json
import requests
import testParse

# this function will parse the response from AWS Transcribe
def getTranscriptionObject():
    TranscriptedFileURL = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print("\n\nFile Located at:")
    print(TranscriptedFileURL)
    r = requests.get(TranscriptedFileURL, allow_redirects=True)
    open('../Transcripts/transcriptedFileData.json', 'wb').write(r.content)
    testParse.open_and_parse()


transcribe = boto3.client('transcribe')
job_name = "TwoSpeakersTest27"
# one speaker:
# job_uri = "https://s3.us-east-2.amazonaws.com/4485testasr/testAudioFile.mp3"
# two speakers:
job_uri = "https://s3.us-east-2.amazonaws.com/4485testasr/liveRecording.wav"
transcribe.start_transcription_job(
  TranscriptionJobName=job_name,
  Media={'MediaFileUri': job_uri},
  MediaFormat='wav',
  LanguageCode='en-US',
  Settings = {
            "ChannelIdentification": False,
            #"MaxSpeakerLabels": 0,
            #"ShowSpeakerLabels": False

            }
)
while True:
  status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
  if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
      break
  print("Not ready yet...")
  time.sleep(5)
print(status)
getTranscriptionObject()
