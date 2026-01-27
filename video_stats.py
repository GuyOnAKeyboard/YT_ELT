import requests as r
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")
channel_handle = 'MrBeast'

def get_channel_playlist_id():
    try:
        url=f'{BASE_URL}{channel_handle}&key={API_KEY}'
        response = r.get(url)
        response.raise_for_status()
        data = response.json()

        channle_items=data["items"][0]

        channel_playlistId=channle_items["contentDetails"]["relatedPlaylists"]["uploads"]
        # print(channel_playlistId)
        return channel_playlistId
    except r.RequestException as e:
        print(f"Error fetching channel playlist ID: {e}")
        return None

if __name__ == "__main__":
   get_channel_playlist_id()