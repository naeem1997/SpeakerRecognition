import speech_recognition as sr
import os

# Each Recognizer instance has seven methods for recognizing speech from an audio source
r = sr.Recognizer()

current_working_dir: str = os.getcwd()
# Take the directory that we are getting the files from as an argument
# parameter: str = sys.argv[1]
parameter: str = 'naeem.wav'


# Use join instead of concatenating strings. Depending on the machine, it will either use / or \\
audio_file = os.path.join(current_working_dir, parameter)
wave_file = sr.AudioFile(audio_file)
with wave_file as source:
    audio = r.record(source)

transcript = r.recognize_google(audio)
print(transcript)
# file = open(parameter + "transcript.txt, 'r+')
# file.write("\"")
# file.write(transcript)
# file.write("\"")
# file.close()