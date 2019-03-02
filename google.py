#Google Transcribe
#Diarization == true, used to determine speakers.

from google.cloud import speech_v1p1beta1 as speech
client = speech.SpeechClient()

speech_file = 'file.wav'

with open(speech_file, 'rb') as audio_file:
    content = audio_file.read()

audio = speech.types.RecognitionAudio(content=content)

config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=8000,
    language_code='en-US',
    enable_speaker_diarization=True,
    diarization_speaker_count=2)

print('Waiting for operation to complete...')
response = client.recognize(config, audio)

#Prints transcripts
result = response.results[-1]

words_info = result.alternatives[0].words

# Output
for word_info in words_info:
    print("word: '{}', speaker_tag: {}".format(word_info.word,
                                               word_info.speaker_tag))