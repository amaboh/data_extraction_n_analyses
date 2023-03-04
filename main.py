import os
from pytube import YouTube
from youtube2text import Youtube2Text
from pydub import AudioSegment
import wget
import speech_recognition as sr 
from pydub.silence import split_on_silence

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# YouTube URL
url = "https://d3ctxlq1ktw2nl.cloudfront.net/staging/2023-2-4/316058431-22050-1-203d7339a8984.m4a"



# Download audio
if "youtube.com" in url:
    yt = YouTube(url)
    if yt.streams.filter(only_audio=True):
        stream = yt.streams.filter(only_audio=True).first()
        audiofile = f"{yt.title}.mp4"
        stream.download(filename=audiofile)
else:
    if url.endswith(".m4a"):
        audiofile = wget.download(url)


# Convert audio to WAV
def convert_to_wav(input_file):
    # Get the input file extension
    file_extension = os.path.splitext(input_file)[1]

    # Create an AudioSegment object from the input file
    if file_extension in ['.mp4', '.m4a', '.mp3']:
        audio = AudioSegment.from_file(input_file, format=file_extension[1:])
    else:
        print("Unsupported file format!")


    # Set the output file extension to .wav and export the file
    output_file = os.path.splitext(input_file)[0] + '.wav'
    audio.export(output_file, format='wav')
    print(f'File converted to {output_file}')
    return output_file

audiofile_wav = convert_to_wav(audiofile)



# create a speech recognition object
r = sr.Recognizer()

def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text
# save the output to a csv file
output_file = os.path.splitext(input_file)[0] + '.csv'

get_large_audio_transcription(audiofile_wav)

        
