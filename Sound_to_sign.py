#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 12:24:45 2021

@author: hugofrelin
"""

import speech_recognition as sr

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx, AudioFileClip

from pydub import AudioSegment


def get_transcript(filename):
    '''This is function uses Googles natural language processing to convert the audio to text. 
    Takes a filename and returns a string.
    '''
    
    # obtain path to the .wav file in the same folder as this script
    
    from os import path
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), filename)
    
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    
    return r.recognize_google(audio)



def pair_word_with_signvideo(word):
    '''Pairs up each word with a video from the database of signvideos'''
    
    filename = r'/Users/hugofrelin/Desktop/Year2/DAPP2/Dataset/'+ str(word) + ".mp4"
    
    sign_video = VideoFileClip(filename)
    
    return sign_video



def does_file_exist(word):
    '''Checks if the video is in the database or not'''
    
    filename = r'/Users/hugofrelin/Desktop/Year2/DAPP2/Dataset/'+ str(word) + ".mp4"
    
    try:
        open(filename)
        # Try to open the file
    except IOError: #If it does not work, the file is not in the directory and we can return False
        return False
    
    return True #else return True


def get_wav(filename):
    
    '''Takes an mp3 file and converts into a .wav file that can be transcribed.
    '''    
    audioclip = AudioFileClip(filename)
    
    audioclip.write_audiofile("Audio.mp3")
    
    # files                                                                         
    src = "Audio.mp3"
    dst = "Audio.wav"

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    

def main():
    
    file_to_analyse = "Dora.mp4" #Enter the name of the video to analyse
    
    file_to_analyse_concat = VideoFileClip(file_to_analyse) 
    #This creates an instance of class VideoClipFile based on the video. 
    #This is needed for patching the video together with the signs later on
    
    get_wav(file_to_analyse)
    #Gets a .wav file from the video
    
    translated_words = [] 
    not_translated = []
    #To keep track of end result
    
    
    video_array = []
    
    audio_file = "Audio.wav" 
    #Audio.wav was created from the audio from video previously.
    
    
    transcript = get_transcript(audio_file)
    #Call to get transcript of video. Returns a string that we split into a list of words 
    
    transcript = transcript.split(" ") 
    #Splitting the string into a list of strings
    
    for word in transcript:
    #Thius loop  goes through all the words in the transcript and if there is a 
    #translation for the word it adds the filename of the translation to the list video_array
    
        if does_file_exist(word) == True:
        
            translated_words.append(word)
            
            filename = r'/Users/hugofrelin/Desktop/Year2/DAPP2/Dataset/'+ str(word) + ".mp4"
            
            
            video_array.append(filename)
            
        else:
            
            not_translated.append(word)
    
    
    translated_video = VideoFileClip(video_array[0])        
    #Creates the signing video, and fills it with the first sign on the list
    
    for i in range(1, len(video_array)):
    #Iterates over the list of videos and adds them to the signing video
        
        addition = VideoFileClip(video_array[i])
        
        translated_video = concatenate_videoclips([translated_video, addition])

    
    translated_video = translated_video.fx(vfx.speedx, 1.5)
    #This is just to make the signs as long as the original video. 
    #This has to be solved differently.
    
    
    translated_video.write_videofile("Sign_for_video.mp4")
    #Writes the file for sign translation
    
    video = CompositeVideoClip([file_to_analyse_concat, translated_video.set_position((0.5,0.5), relative = True)])
    #Concatenates the translation video to original
    
    video.write_videofile("Dora_with_signs.mp4")
    #Writes the final product
    
    
    print("\n\n\nThese words were translated:")
    print(translated_words)
    print("\nThese words were not in the dictionary: ")
    print(not_translated)
    #These print statements are here to show what words were translated and which weren't
    
    
if __name__ == "__main__":
    main()



