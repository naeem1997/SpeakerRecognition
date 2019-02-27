import pyaudio
import wave
import sys, select, os # hack
import fileUploader


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 #sample rate
RECORD_SECONDS = 90

WAVE_OUTPUT_FILENAME = "liveRecording.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer

frames = []

def record_stream():
    # Record the Live Steam
    while True:
        # Clear interpreter console
        # cls command on windows, clear on Unix Systems
        os.system('cls' if os.name == 'nt' else 'clear')
        print("* Recording...")
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data) # 2 bytes per channel
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = input()
                break
        break
    print("* Finished.")
    close_stream()


def close_stream():
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


if __name__ == '__main__':
    record_stream()
    fileUploader.upload_file()
