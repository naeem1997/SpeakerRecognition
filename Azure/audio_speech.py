import azure.cognitiveservices.speech as speechsdk
import time
import wave
from pydub import AudioSegment

speech_key, service_region = "db21b5b0dae54b7b99d787b8676b1850", "westus"

# # convert mp3 file to wav                                                       
# sound = AudioSegment.from_mp3("transcript.mp3")
# sound.export("transcript.wav", format="wav")


# # transcribe audio file                                                         
# AUDIO_FILE = "transcript.wav"
# audiofilename = "dnc-2004-speech.mp3"
audiofilename = "OSR_us_000_0010_8k.wav"

"""performs continuous speech recognition with input from an audio file"""
# <SpeechContinuousRecognitionWithFile>
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = speechsdk.audio.AudioConfig(filename=audiofilename)

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

done = False

def stop_cb(evt):
    """callback that stops continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    speech_recognizer.stop_continuous_recognition()
    done = True

# Connect callbacks to the events fired by the speech recognizer
speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
# stop continuous recognition on either session stopped or canceled events
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

# Start continuous speech recognition
speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(.5)
# </SpeechContinuousRecognitionWithFile>