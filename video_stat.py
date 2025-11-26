import requests
import os
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")  # loads the .env file automatically

api_key = os.getenv("API_KEY")
CHANNEL_HANDLE = "MrBeast"

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
    


if __name__ == "__main__":
    get_playlist_id()
