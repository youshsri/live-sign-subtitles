#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 28-02-2021
@author: hugofrelin & lito
"""

import speech_recognition as sr

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx, AudioFileClip

from pydub import AudioSegment

from pytube import YouTube


def correct_last(transcript, past):

    correction = []
    words = 0
    words2 = 0
    
    if len(past) == 1:
        return transcript
    reverse = past[::-1] #create an array that is inverse to the transcript
                                #makes it easier to handle dat
    
    #find the position of the 1st word of the transcript in the helpclip
    for index1 in transcript:   
        #print(index1)       
        words2 = words2 + 1
        if index1 == reverse[0]:
            words = 0
            break
    
    #if not, find the second word of the transcript
    if transcript[words2-1] != reverse[0]:
        words2 = 0
        for index1 in reverse:  
            #print(index1)       
            words2 = words2 + 1
            if index1 == reverse[1]:
                words = 1
                break
    
    #if the second word is not found, there is a problem with the helpclip 
    #(maybe there was silence for the last seconds of the helpclip)
    #trancsript won't be corrected
    if len(reverse) < words+words2+1:
        return transcript
    
    #if there is no problem, we will create a correction array with the words we need to change in the transcript
    else:
        for index4 in range(words2):
            transcript.pop(0)
            correction.append(reverse[words+index4])
        
    #the elements in the correction array are added to the transcript
    reverse1 = transcript[::-1]
    
    for index5 in range(len(correction)):
        reverse1.append(correction[index5])
        
    
    transcript = reverse1[::-1]    
    return transcript
    
def correct1(transcript, future):
    words = words2 = 0
    correction = []
    
    if len(future) == 1:
        return transcript
    
    reverse = transcript[::-1] #create an array that is inverse to the transcript
                            # makes it easier to handle dat
    
    #find the position of the word that corresponds to the first element in the 
    #future helpclip in the reverse array
    for index1 in reverse:   
    #print(index1)       
        words2 = words2 + 1
        if index1 == future[0]:
            i = -1
            break
    
    # if first word of the future helpclip is not found, try to find the second, third...
    if (reverse[words2-1] != future[0]) or (words2 >= len(reverse)/2):
        words2 = 0
        for i in range(len(future)-1):
            try:
                # if reverse[words2-i] != future[i]:
                for index1 in reverse:
                    # print(index1)
                    # print(future[i+1])
                    words2 = words2 + 1
                    if index1 == future[i+1]:
                        break
                if index1 == future[i+1]:
                    break
                else :
                    words2 = 0
            except IndexError:
                return transcript
                #if there's an index error here, the actual code would just return the uncorrected transcript
                #(no error would appear)
            
    
     #find the position of the word in the future helpclip
    # print(words2)
    #create a correction array and delete what every word that
    #is both in the future helpclip and the transcript + the incorrect word
    for index4 in range(words2):
        reverse.pop(0)
        try:
            if i != -1:
                correction.append(future[i+index4+1])
            else:
                correction.append(future[index4])
        except IndexError:
               return transcript
    
            
        transcript = reverse[::-1]  
            
        # add the correction to the transcript
        for index5 in range(len(correction)):
            transcript.append(correction[index5])
        
    return transcript

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
    
    filename = r'/Users/Lito/Desktop/Imperial/Year 2/Sign Language project/Dataset/'+ str(word) + ".mp4"
    
    sign_video = VideoFileClip(filename)
    
    return sign_video



def does_file_exist(word):
    '''Checks if the video is in the database or not'''
    
    filename = r'/Users/Lito/Desktop/Imperial/Year 2/Sign Language project/Dataset/'+ str(word) + ".mp4"
    
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

def create_helpclips(filename):
    audio = AudioFileClip(filename)    
        
    length = audio.duration    
        
    times = int(length / 10) + 1
    
    helpclips = {}
    
    m = 1
        
    while m < times:
                        
        beginning = (10*m)-2
        
        # if m==times-1:
        #     end = 10*m
        # else:
        end = (10*m)+2
            
        helpclips['helpclip' + str(m)] = (audio.subclip(beginning, end))
        
                
        m = m + 1
    
    for subclips1 in helpclips:
        
        helpclips[subclips1].write_audiofile(subclips1 + '.wav')

def get_signs(transcript, videolength, past, future):
    ''' Takes a transcript and the length of the video that is the transcript of. 
    It returns a video of max that length of a signer doing those signs.
    '''
    
    video_array = []
    
    transcript = transcript.split(" ") 
    #Splitting the string into a list of strings
    
    #past = past.split(" ")
    #future = future.split(" ")
    
    #if the first subclip being translated, the first words wonn't be corrected
    if (past == 0):
        future = future.split(" ")
        transcript = correct1(transcript, future)
        
    #if the last subclip is being translated, tha last words it contains don't need correcting
    elif future == 0:
        past = past.split(" ")
        transcript = correct_last(transcript, past)
    
    
    else :
        future = future.split(" ")
        transcript = correct1(transcript, future)
        past = past.split(" ")
        transcript = correct_last(transcript, past)
    
    
    for word in transcript:
    #This loop  goes through all the words in the transcript and if there is a 
    #translation for the word it adds the filename of the translation to the list video_array
    
        if does_file_exist(word) == True:
        
            
            filename = r'/Users/Lito/Desktop/Imperial/Year 2/Sign Language project/Dataset/'+ str(word) + ".mp4"
            
            
            video_array.append(filename)
        
        
    if len(video_array) > 0:
        # If there are words in the sequence that we have in our dataset, initiate the concatenating
        translated_video = VideoFileClip(video_array[0])  
    
    else:
        return VideoFileClip(r'/Users/Lito/Desktop/Imperial/Year 2/Sign Language project/Dataset/blackscreen.mp4')
        # Else, return a 10 second long black screen. 
        # The black screen is ugly, so we will have to think of something better later on.
    
    for i in range(1, len(video_array)):
    #Iterates over the list of videos and adds them to the signing video
        
        addition = VideoFileClip(video_array[i])
        
        translated_video = concatenate_videoclips([translated_video, addition])
    
    translated_video_dur = translated_video.duration 
    # Gets the length of the sign video. So we can adjust it to be exactly 10 seconds.
    
    if translated_video_dur > videolength:
    # If it is longer, we speed it up.
        factor = translated_video.duration / videolength
        
        translated_video = translated_video.fx(vfx.speedx, factor)
    
    if translated_video_dur < videolength:
    # If it is shorter, we fill out the end with a black sreen.
    
        blackscreen = VideoFileClip(r'/Users/Lito/Desktop/Imperial/Year 2/Sign Language project/Dataset/blackscreen.mp4')
        
        blackscreen_time = 10 - translated_video_dur
        
        multiplier = 10 / blackscreen_time
        
        blackscreen = blackscreen.fx(vfx.speedx, multiplier)
        
        translated_video = concatenate_videoclips([translated_video, blackscreen])
        
    
    return translated_video


def download_YT_video(url, video_name):
    try:
        video = YouTube(url)
        stream = video.streams.filter()
        stream[0].download(filename = video_name)
        filename = video_name + '.mp4'
        return filename
    except:
        if url == None:
            raise ValueError("Must have an existing url")



def main():
    
    videolength = 10
    #length of each segment that is being translated
    
    url = 'https://www.youtube.com/watch?v=MTbVu3aX9OE&ab_channel=BBCNews'
    # The youtube url to be translated
    
    video_name = 'video1'
    #What you want the video to be stored as one your computer
    
    download_YT_video(url, video_name)
    # Calling function to retrieve yt video
    
    
    file_to_analyse = video_name + '.mp4' 
    # This is the video we will translate
    
    file_to_analyse_instance = VideoFileClip(file_to_analyse)
    #file_to_analyse_instance = VideoFileClip('/Users/Lito/Desktop/Imperial/Year 2/Sign Language project/video1.mp4')
    # Creates an instance of class VideoFileClip based on the video
    
    get_wav(file_to_analyse, video_name + ".wav")
    #Gets a .wav file from the video
        
    subclip_dictionary = create_subclips(video_name + ".wav")
    #Call the create_subclips function. This returns a dictionary with the audio divided into 10sec clips
    
    create_helpclips(video_name + ".wav")
    
    sign_translations = {}
    
    index = 1
    
    for key in range(1,len(subclip_dictionary)+1):   
    #This for loop iterates over the 10sec audio clips and gets a translational sign video for each.
    #The videos are then put into the deictionary sign_translations and named in order.
    #video1 video2 etc
    
    
        transcript = get_transcript("subclip" + str(key) + ".wav")
        
        
        if key == len(subclip_dictionary):
            future_trans = 0
            past_trans = get_transcript("helpclip" + str(key-1) + ".wav")
         
        elif key == 1:
            future_trans = get_transcript("helpclip" + str(key) + ".wav")
            past_trans = 0

        else:
            past_trans = get_transcript("helpclip" + str(key-1) + ".wav")
            future_trans = get_transcript("helpclip" + str(key) + ".wav")
        
        sign_translations['video' + str(index)] = get_signs(transcript, videolength, past_trans, future_trans)
        
        index = index + 1
        
    
    sign_videos_concat = sign_translations['video1']
    #Creates the final sign translation by adding video1. The reason for doing this is that we cannot 
    # add videos to an empty instances of VideoFileClip (at least I didn't find a way to do it)
    
    
    for key in sign_translations:
    #Adds all the sign translations in order, but skipping first one since its already added.
    
        if key != 'video1':
            
            sign_videos_concat = concatenate_videoclips([sign_videos_concat, sign_translations[key]])
    
    
    video = CompositeVideoClip([file_to_analyse_instance , sign_videos_concat.set_position((0.6,0.5), relative = True)])
    #Concatenates the translation video to original, and puts translation in the corner
    
    
    video.write_videofile("video_with_signs.mp4")
    
    
    
     
if __name__ == "__main__":
    main()
    
  
