import os
from pytube import YouTube
from youtube2text import Youtube2Text
from pydub import AudioSegment

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# YouTube URL
url = "https://www.youtube.com/watch?v=VyGpknh4rPM&ab_channel=Dr.VanitaRattan"

# Download audio
yt = YouTube(url)
stream = yt.streams.filter(only_audio=True).first()
audiofile = f"{yt.title}.mp3"
stream.download(filename=audiofile)

# Convert audio to WAV
def convert_to_wav(input_file):
    audio = AudioSegment.from_file(input_file, format='mp3')
    output_file = os.path.splitext(input_file)[0] + '.wav'
    audio.export(output_file, format='wav')
    print(f'File converted to {output_file}')

convert_to_wav(audiofile)
add
# Transcribe audio to text and store in CSV
cwd = os.getcwd()
converter = Youtube2Text()
textfile = f"{cwd}/text.csv"

converter.url2text(url)
converter.audio2text(audiofile=f"{yt.title}.wav", textfile=textfile)
