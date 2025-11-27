import requests
import os
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")  # loads the .env file automatically

api_key = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"
max_result = 50

def get_playlist_id():

    try:

        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={api_key}'


        response = requests.get(url)

        response.raise_for_status()


        data = response.json()



        channel_item = data["items"][0]

        channel_playlist_id = channel_item["contentDetails"]["relatedPlaylists"]["uploads"]


        print(channel_playlist_id)

        return channel_playlist_id

    except requests.exceptions.RequestException as e:
        raise e
    
def get_video_ids(playlist_id):

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_result}&playlistId={playlist_id}&key={api_key}"


    video_id_list = []
    page_token = None 

    try:
        while True: 
             
            url = base_url

            if page_token:
                url += f"&pageToken={page_token}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items',[]):
                video_id = item['contentDetails']['videoId']
                video_id_list.append(video_id)
            

            page_token = data.get('nextPageToken')

            if not page_token:
                break

        return video_id_list
    
    except requests.exceptions.RequestException as e:
        raise e

    

if __name__ == "__main__":
    playlist_id = get_playlist_id()
    get_video_ids(playlist_id)
