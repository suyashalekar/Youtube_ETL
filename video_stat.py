import requests
import os
import json
from dotenv import load_dotenv
from datetime import date


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



def extract_video_data(video_ids_list):
    extract_data = []

    def batch_list(video_ids_list,batch_size):
        for video_id in range(0,len(video_ids_list),batch_size):
            yield video_ids_list[video_id: video_id + batch_size]
    
    try:
        for batch in batch_list(video_ids_list,max_result):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={api_key}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']

                video_data_dic = {
                    "video_id" : video_id,
                    'title' : snippet['title'],
                    'publishedAt' : snippet['publishedAt'],
                    'duration' : contentDetails['duration'],
                    'viewCount' : statistics.get('viewCount',None),
                    'likeCount' : statistics.get('likeCount',None),
                    'commentCount' : statistics.get('commentCount',None)
                }

                extract_data.append(video_data_dic)

        return extract_data

    except requests.exceptions.RequestException as e:
        raise e

def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path,"w", encoding="utf-8") as json_extracted_data_file:
        json.dump(extracted_data,json_extracted_data_file,indent=4,
                  ensure_ascii=False)
        


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids_list = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids_list)
    save_to_json(video_data)
        
