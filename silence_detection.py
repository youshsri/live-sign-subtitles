from pydub import silence, AudioSegment

from moviepy import editor

def detect_silence_in_file(filename, silence_threshold = -30):
    
    '''
    This function will intake a audio file, convert it into a .wav format,
    and detect the periods of silence within the audio file.
    '''

    # convert video file into AudioFileClip and write mp3 file out
    audioclip = editor.AudioFileClip(filename)
    
    audioclip.write_audiofile("Silence_detect.mp3")

    # file name                                                                        
    src = "Silence_detect.mp3"

    # retrieve mp3 file as AudioSegment                                                            
    sound = AudioSegment.from_mp3(src)
    
    # detect silence ranges using specific silence_threshold
    silence_ranges = silence.detect_silence(sound, silence_thresh=silence_threshold)
    
    return sound, silence_ranges

def segment_silence(audio_clip, filename, min_silence_range, silence_threshold=-30, keep_silence_val=10):
    
    '''
    Provided the silence ranges of the AudioSegment, the AudioSegment will be segmented
    of all silence to form a clean cut video w/o any silence. This will aid in
    speech recognition.
    '''

    # segment silence out of AudioSegment object into a list of AudioSegment objects
    audio_segment_list = silence.split_on_silence(audio_clip, min_silence_range, silence_threshold, keep_silence_val)

    # create empty AudioSegment object
    concat_audio = AudioSegment.empty()

    # concatenate AudioSegment objects into single object
    for audio_segment in audio_segment_list:
        concat_audio += audio_segment

    # export silence-segmented AudioSegment object as a wav file
    concat_audio.export(filename, format='wav')

def main():

    # define filenames
    filename = ""
    out_dest_filename = "silence_cut.wav"

    # find silence ranges
    sound, silence_ranges = detect_silence_in_file(filename, silence_threshold=-30)

    # segment sound 
    segment_silence(sound, out_dest_filename, 1000)

    # print silence ranges for reference
    print(silence_ranges)

if __name__ == "__main__":
    main()
