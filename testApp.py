from __future__ import print_function
import time
import boto3

transcribe = boto3.client('transcribe')
job_name = "TranscriptionJob1234567Test"
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
