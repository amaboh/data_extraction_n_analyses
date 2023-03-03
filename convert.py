import ssl
ssl._create_default_https_context = ssl._create_unverified_context


import os
import csv
import whisper
from pytube import YouTube

# download the YouTube video
url = "https://www.youtube.com/watch?v=VyGpknh4rPM&ab_channel=Dr.VanitaRattan"
yt = YouTube(url)
stream = yt.streams.filter(only_audio=True).first()
audiofile = f"{yt.title}.mp3"
stream.download(filename=audiofile)

# load the Whisper model and audio file
model = whisper.load_model("base")
audio = whisper.load_audio(audiofile)
audio = whisper.pad_or_trim(audio)

# generate the log-Mel spectrogram and detect the spoken language
mel = whisper.log_mel_spectrogram(audio).to(model.device)
_, probs = model.detect_language(mel)
mel = mel.float()
language = max(probs, key=probs.get)

# decode the audio and extract the text
options = whisper.DecodingOptions(language=language)
result = whisper.decode(model, mel, options)
text = result.text

# save the text to a CSV file in the current directory
cwd = os.getcwd()
csvfile = f"{yt.title}.csv"
with open(csvfile, "w") as f:
    writer = csv.writer(f)
    writer.writerow([text])
print(f"Transcription saved to {csvfile}")
