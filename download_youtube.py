# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 18:31:32 2021

@author: Ayoush Srivastava
"""

from pytube import YouTube
import speech_recognition as sr
import moviepy.editor as mp


def download_YT_video(url):
    try:
        video = YouTube(url)
        stream = video.streams.filter()
        stream[0].download(filename = 'audio')
        filename = 'audio.mp4'
        return filename
    except:
        if url == None:
            raise ValueError("Must have an existing url")

def convert_video_into_audio(video_file_name):
    
    video = mp.VideoFileClip(filename = video_file_name)
    
    audio = video.audio
    
    audio_file_name = 'audio.wav'
    
    audio.write_audiofile(audio_file_name)
    
    return audio_file_name
    
def convert_audio_into_text(audio_file_name):
    rinst = sr.Recognizer()
    audio_data = sr.AudioFile(audio_file_name)
    
    with audio_data as source:
        audio = rinst.record(source)
    
    text = rinst.recognize_google(audio)
    return text
    
def main():
    
    url = 'https://www.youtube.com/watch?v=4iLVoEg9aLk'
    
    video_file_name = download_YT_video(url)
    audio_file_name = convert_video_into_audio(video_file_name)
    text_data = convert_audio_into_text(audio_file_name)
    print(text_data)

if __name__ == "__main__":
    main()

