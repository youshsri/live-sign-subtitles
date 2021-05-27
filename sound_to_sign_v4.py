import speech_recognition as sr

from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, vfx, AudioFileClip

from pydub import AudioSegment

import pafy as pf

import download_youtube as dy

def download_YT_video(url, video_name):
    '''This function will return a YT video in mp4 format to your local directory.
    This function requires a url from the user and a filename for the saved file.'''

    try:
        # create pafy object 
        video = pf.new(url)

        # gets best video stream of mp4 format
        best = video.getbest(preftype='mp4')

        # create new video name by adding .mp4 extension
        video_name = video_name + '.mp4'

        # downloads video into local directory
        best.download(filepath=video_name, quiet=False)

        # return filename
        return video_name
    except:
        raise ValueError("URL is not valid")

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

def get_transcript(filename):
    '''This is function uses Googles natural language processing to convert the audio to text. 
    Takes a filename and returns a string.
    '''
    
    # obtain path to the .wav file in the same folder as this script
    from os import path
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), filename)
    
    # use the audio file as the audio source
    r = sr.Recognizer()
    
    # read the entire audio file
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  
    
    return r.recognize_google(audio)

def does_file_exist(word):
    '''Checks if the video is in the database or not.'''
    
    # create filename path to check
    filename = r'/Users/ayoushsrivastava/Documents/GitHub/live-sign-subtitles/Git_Dataset/' + str(word) + ".mp4"
    
    try:
        # check if file can be opened
        open(filename)
    except IOError: # if it doesn't work, the file is not in the directory and we can return False
        return False
    return True # else return True

def pair_word_with_signvideo(word):
    '''Pairs up each word with a video from the database of signvideos'''
    
    filename = r'/Users/ayoushsrivastava/Documents/GitHub/live-sign-subtitles/Git_Dataset/'+ str(word) + ".mp4"
    
    sign_video = VideoFileClip(filename)
    
    return sign_video

def get_signs(transcript, videolength):
    ''' Takes a transcript and the length of the video that is the transcript of. 
    It returns a video of max that length of a signer doing those signs.
    '''
    
    video_array = []

    print(transcript)
    
    transcript = transcript.split(" ") 
    #Splitting the string into a list of strings
    
    for word in transcript:
    #This loop  goes through all the words in the transcript and if there is a 
    #translation for the word it adds the filename of the translation to the list video_array
    
        print('\n'+word)

        if does_file_exist(word) == True:

            filename = r'/Users/ayoushsrivastava/Documents/GitHub/live-sign-subtitles/Git_Dataset/'+ str(word) + ".mp4"
            
            video_array.append(filename)
    
    
    if len(video_array) > 0:
        # If there are words in the sequence that we have in our dataset, initiate the concatenating
        translated_video = VideoFileClip(video_array[0])  
    
    else:
        return VideoFileClip(r'/Users/ayoushsrivastava/Documents/GitHub/live-sign-subtitles/Git_Dataset/blackscreen.mp4')
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
    
        blackscreen = VideoFileClip(r'/Users/ayoushsrivastava/Documents/GitHub/live-sign-subtitles/Git_Dataset/blackscreen.mp4')
        
        blackscreen_time = 10 - translated_video_dur
        
        multiplier = 10 / blackscreen_time
        
        blackscreen = blackscreen.fx(vfx.speedx, multiplier)
        
        translated_video = concatenate_videoclips([translated_video, blackscreen])
        
    return translated_video

def main(url):

    # pre-define length of clips that will be translated
    videolength = 10
    
    # name that the video will have when saved on your computer
    video_name = 'video_file'

    # download YT video and return file name
    video_name = download_YT_video(url, video_name)

    # define audio file name
    audio_file_name = "audio.wav"

    # create instance of VideoFileClip of video being downloaded
    file_to_analyse_instance = VideoFileClip(video_name)

    # retrieve wav file
    get_wav(video_name, audio_file_name)

    # create subclips
    subclip_dictionary = create_subclips(audio_file_name)

    #
    sign_translations = {}
    index = 1

    # pre-define transcript list
    transcript = ""
    streamlined_trans = []

    # iterate through each 10 second audio clip and get text transcript for each
    for key in subclip_dictionary:   
    
        # append streamlined transcript of each 10 second audio clip into list
        transcript = get_transcript(key + ".wav")

        # get streamlined transcript of each 10 second audio clip
        streamlined_trans.append(dy.streamline_transcript(transcript[-1]))

        # retrieve respective signs 
        sign_translations['video' + str(index)] = get_signs(transcript, videolength)

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
    
    print("Before")

    filename = 'with_signs.mp4'

    video.write_videofile(filename)
        
    print("Completed")

    return True

if __name__ == "__main__":
    main()