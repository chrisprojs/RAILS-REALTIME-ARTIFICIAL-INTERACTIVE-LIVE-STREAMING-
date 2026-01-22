import obswebsocket
from obswebsocket import obsws, requests
import os
import pandas as pd
import time
from moviepy.editor import VideoFileClip
import random
import config_variable

script_dir = os.path.dirname(os.path.abspath(__file__))


asset_folder = f"{script_dir}/asset"

# Buat objek WebSocket


video_df = pd.read_csv(f"{script_dir}/action_data.csv")

def change_video(label, previous_video):
    total_file = video_df.loc[video_df['label'] == label, 'total_file'].iloc[0]

    video_number = random.randint(1, total_file)
    while(previous_video['label']==label and int(previous_video['video_number'])==video_number):
        video_number = random.randint(1, total_file)
        
    print(f"Label: {label} , Video_number: {video_number}")

    file_name= os.path.abspath(f"{asset_folder}/video_part/{label}/{video_number}.mp4")
    
    config_variable.ws.call(requests.SetInputSettings(
        inputName="Main Video",
        inputSettings={"local_file": file_name}
    ))

    # pick random image from {folder}mockup_image/
    pick_random_image(f"{asset_folder}/mockup_image/")
    
    response_duration = get_video_duration(file_name)
    # print(response_duration)
    time.sleep(response_duration)
    return video_number

def get_video_duration(file_name):
    try:
        clip = VideoFileClip(file_name)
        duration = clip.duration
        clip.close()
        return duration
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def pick_random_image(folder_path):
    global ws
    # List all files in the folder
    files = os.listdir(folder_path)
    # Filter for image files (assuming .jpg and .png extensions)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not image_files:
        raise Exception("No image files found in the folder.")
    # Pick a random image file
    random_image = random.choice(image_files)

    image_file_name = os.path.abspath(f"{asset_folder}/mockup_image/{random_image}")

    config_variable.ws.call(requests.SetInputSettings(
        inputName="Product",
        inputSettings={"file": image_file_name}
    ))

