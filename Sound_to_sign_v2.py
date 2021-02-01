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



def get_wav(filename, name):
    
    '''Takes an mp4 file and converts into a .wav file that can be transcribed. 
    The .wav file has the name enter
    '''    
    audioclip = AudioFileClip(filename)
    
    audioclip.write_audiofile("Audio.mp3")
    
    # files                                                                         
    src = "Audio.mp3"
    dst = name

    # convert wav to mp3                                                            
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")



def create_subclips(filename):
    '''Takes an audiofile and splits it into 10 seconds intervals, 
    and then returns a dictionary with the 10 second audiofiles. 
    1st 10 seconds has key subclip1, 2nd has key subclip2 and so on.
    Also saves the subclips as .wav files'''
    
    audio = AudioFileClip(filename)    
        
    length = audio.duration    
        
    turns = int(length / 10) + 1
        
    clips = {}
        
    i = 1
        
    while i <= turns:
            
        if i < turns:
            
            beginning = (i-1)*10
            end = i*10
            
            clips['subclip' + str(i)] = (audio.subclip(beginning, end))
            
        if i == turns:
                
            beginning = (i-1)*10
            end = length
                
            clips['subclip' + str(i)] = (audio.subclip(beginning, end))
                
                
        i = i + 1
    
    for subclips in clips:
        
        clips[subclips].write_audiofile(subclips + '.wav')
    
    return clips



def get_signs(transcript, videolength):
    ''' Takes a transcript and the length of the video that is the transcript of. 
    It returns a video of max that length of a signer doing those signs.
    '''
    
    video_array = []
    
    transcript = transcript.split(" ") 
    #Splitting the string into a list of strings
    
    for word in transcript:
    #This loop  goes through all the words in the transcript and if there is a 
    #translation for the word it adds the filename of the translation to the list video_array
    
        if does_file_exist(word) == True:
        
            
            filename = r'/Users/hugofrelin/Desktop/Year2/DAPP2/Dataset/'+ str(word) + ".mp4"
            
            
            video_array.append(filename)
    
    translated_video = VideoFileClip(video_array[0])  
    
    for i in range(1, len(video_array)):
    #Iterates over the list of videos and adds them to the signing video
        
        addition = VideoFileClip(video_array[i])
        
        translated_video = concatenate_videoclips([translated_video, addition])
    
    
    if translated_video.duration > videolength:
        
        factor = translated_video.duration / videolength
        
        translated_video = translated_video.fx(vfx.speedx, factor)
    
    # if translated_video.duration < videolength:
       
        #Add fade to the end so that it becomes of length videolength
        
    
    return translated_video



def main():
    
    videolength = 10
    
    file_to_analyse = "dora.mp4" #Enter the name of the video to analyse
    
    file_to_analyse_instance = VideoFileClip(file_to_analyse)
    
    get_wav(file_to_analyse, "dora_sound.wav")
    #Gets a .wav file from the video
        
    subclip_dictionary = create_subclips("dora_sound.wav")
    #Call the create_subclips function. This returns a dictionary with the audio divided into 10sec clips
    
    sign_translations = {}
    
    index = 1
    
    for key in subclip_dictionary:   
    #This for loop iterates over the 10sec audio clips and gets a translational sign video for each.
    #The videos are then put into the deictionary sign_translations and named in order.
    #video1 video2 etc
    
        transcript = get_transcript(key + ".wav")
        
        sign_translations['video' + str(index)] = get_signs(transcript, videolength)
        
        index = index + 1
        
    
    sign_videos_concat = sign_translations['video1']
    #Creates the final sign translation by adding video1. The reason for doing this is that we cannot 
    # add videos to an empty instances of VideoFileClip (at least I didn't find a way to do it)
    
    
    for key in sign_translations:
    #Adds all the sign translations in order, but skipping first one since its already added.
    
        if key != 'video1':
            
            sign_videos_concat = concatenate_videoclips([sign_videos_concat, sign_translations[key]])
    
    
    video = CompositeVideoClip([file_to_analyse_instance , sign_videos_concat.set_position((0.7,0.6), relative = True)])
    #Concatenates the translation video to original, and puts translation in the corner
    
    
    video.write_videofile("Dora_with_signs.mp4")
    
    
    
     
if __name__ == "__main__":
    main()
    
    
    
    # for i in range(1, len(subclips) + 1):
        
    #     short_transcript = get_transcript("subclip" + str(i) + ".wav")
        
    #     print(short_transcript)

    1+1
