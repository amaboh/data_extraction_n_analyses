from pydub import AudioSegment
import os
from youtube2text import Youtube2Text


cwd = os.getcwd()

texxtile = f"{cwd}/textfile.csv"

def convert_audio_to_wav(input_file):
    audio = AudioSegment.from_file(input_file, format='mp4')
    
    output_file = os.path.splitext(input_file)[0]+ '.wav'
    audio.export(output_file, format='wav')
    
convert_audio_to_wav('Doctor V - Top 5 Vitamin C Mistakes   Skin Of Colour  Brown Or Black Skin.mp4')

converter = Youtube2Text()

converter.audio2text('Doctor V - Top 5 Vitamin C Mistakes   Skin Of Colour  Brown Or Black Skin.wav', textfile=texxtile)