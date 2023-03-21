from moviepy.editor import VideoFileClip, concatenate_videoclips
import os 


def concat_clips(myPath, concat_name, type): 
    try : 
        os.path.isdir(myPath)
    except: 
        print("No path found!")
        exit()

    fullfilename = lambda x: os.path.join(myPath, x)

    ##Find all clips in folder
    video_names = [f for f in os.listdir(myPath) if os.path.isfile(fullfilename(f)) and f.find(".mp4",-4)!=-1 and f.find(concat_name)==-1]
    if video_names == []: 
        print("Empty path - no .mp4 files found")
        exit()
    ###Load clip
    video_list = [VideoFileClip(fullfilename(_)) for _ in video_names]

    ### FINAL ASSEMBLY
    final = concatenate_videoclips([x for x in video_list], method='compose')
    final.write_videofile(fullfilename(concat_name+type), codec = "libx264", audio_codec='aac', 
                     temp_audiofile='temp-audio.m4a', 
                     remove_temp=True)



# myPath = "/Users/williamsorensen/Desktop/TikTok_compilations"
# concat_name = "TikTok_concat.mp4"
# concat_clips(myPath, concat_name)

