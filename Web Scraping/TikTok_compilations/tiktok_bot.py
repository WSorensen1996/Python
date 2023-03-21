from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib 
import requests
import urllib.request
from time import sleep
import os 
from movie_concat import concat_clips 
import csv   
########################################################################################################
c = 3 # number of compilations to make
n = 3 # Number of clips in compilation
likes_lim = 10000
comment_lim = 5000

run_tiktok = True
########################################################################################################

if run_tiktok: 
    driver = webdriver.Chrome()
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    driver.get("http://tiktok.com")
    print("Close window and click on clip")
    sleep(10)

def delete(): 
    for i in range(n): 
        try: 
            os.remove(fullfilename(clip_name+str(i)+".mp4"))
        except: 
            print("Could not find clip to delete!")

def check_path(myPath): 
    try : 
        os.path.isdir(myPath)
    except: 
        print("No path found!")
        exit()

def clean(_): 
    if _.find("M")!=-1: 
        try: 
            return float(_[:-1])*1000000
        except: 
            return _ 
    if _.find("K")!=-1: 
        try: 
            return float(_[:-1])*1000
        except: 
            return _ 
    try:
        return float(_) 
    except: 
        print("Website not positioned right - task quit")
        exit()


def append_downloads(src): 
    with open(fullfilename(csv_file), "a") as f :
        writer_object = csv.writer(f)
        writer_object.writerow([src])


def exists_downloads(src): 
    with open(fullfilename(csv_file),"r") as f :
        reader = csv.reader(f, delimiter="\t")
        for row in reader: 
            if [src]==row: 
                print("SRC already in downloads")
                return False
        return True

def create_csv(csv_header): 
    with open(fullfilename(csv_file), "a") as f :
        writer_object = csv.writer(f)
        writer_object.writerow(csv_header)

fullfilename = lambda x: os.path.join(myPath, x)

def get_tiktok_clips(n, myPath): 
    clips_gathered = 0
    while clips_gathered<n: 

        likes_class_str = 'browse-like-count'
        comments_class_str = 'browse-comment-count' 
        src_string = driver.page_source
        #print(src_string)
        likes_index = src_string.find(likes_class_str)+len(likes_class_str)+46
        comments_index = src_string.find(comments_class_str)+len(comments_class_str)+46

        likes = src_string[likes_index:likes_index+20]
        comments = src_string[comments_index:comments_index+20]

        likes_end_index = likes.find("</strong>")
        comments_end_index = comments.find("</strong>")

        likes = clean(likes[:likes_end_index])
        comments = clean(comments[: comments_end_index])

        if likes > likes_lim and comments > comment_lim : 
            sub_index = src_string.find('<video')
            sub_string = src_string[sub_index: (sub_index+500)]
            substring_list = sub_string.split()
            src = substring_list[1][5:]
            src_id = "amp;rc="
            src_id = src.find(src_id)+len(src_id)
            src_id = src[src_id:]
            if exists_downloads(src_id): 
                print("\nDownloading starts...")
                print("Downloading - SRC_ID:    ", src_id)
                name = clip_name+str(clips_gathered)
                name=name+".mp4"
                fullfilename = os.path.join(myPath, name)
                urllib.request.urlretrieve(src, fullfilename)
                print("Download completed..!!\n")

                append_downloads(src_id)

                clips_gathered +=1 
                sleep(1)
        print("Likes: ",likes, "Comments: ", comments)
        try:
            elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[1]/button[3]')))
            elem.click()
        except:
            print("Error - iterating too fast")
            sleep(1)

    print(f"Succes! {n} videos was downloaded")
    return clips_gathered





if __name__== "__main__": 
    csv_header = ["Src"]
    myPath = "/Users/williamsorensen/Desktop/TikTok_compilations"
    csv_file = "Downloads_list.csv"
    clip_name = "tiktok_clip_"
    concat_name = "TikTok_compilation"


    if not(os.path.exists(fullfilename(csv_file))): 
        create_csv(csv_header)
    
    if run_tiktok: 
        for i in range(c): 
            if get_tiktok_clips(n, myPath) == n: 
                type = str(i)+".mp4"
                concat_clips(myPath, concat_name, type)#Path to clip-folder, name of concat-file and type: .mp4 #Only takes .mp4
                delete()
