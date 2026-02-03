import requests as r
import json
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL=os.getenv("BASE_URL")
channel_handle = os.getenv("channel_handle")
maxResult=50

def get_channel_playlist_id():
    try:
        url=f'{BASE_URL}channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}'
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

def get_video_id(playlistId):
    video_ids=[]
    pageToken=None
    baseUrl=f'{BASE_URL}playlistItems?part=contentDetails&maxResults={maxResult}&playlistId={playlistId}&key={API_KEY}'
    try:
      while True:  
        url=baseUrl
        
        if pageToken:
            url += f'&pageToken={pageToken}'
            
        response = r.get(url)
        response.raise_for_status()
        data = response.json()
        for item in data.get('items',[]):
           video_id=item['contentDetails']['videoId']
           video_ids.append(video_id)
        pageToken=data.get('nextPageToken')

        if not pageToken:
           break
    
      return video_ids

    except r.RequestException as e:
        print(f"Error fetching video IDs: {e}")
        return None


def extract_video_data(videoIds):
    extractedData=[]
    
    def batchList(videoListIds,batchSize):
        for id in range(0,len(videoListIds),batchSize):
            yield videoListIds[id:id+batchSize]
    
    try:
        for batch in batchList(videoIds,maxResult):
            videoIdStr=",".join(batch)
                
            url=f'{BASE_URL}videos?part=contentDetails&part=snippet&part=statistics&id={videoIdStr}&key={API_KEY}'
            response = r.get(url)
            response.raise_for_status()
            data = response.json()
            

            for item in data.get('items',[]):
                video_id=item['id']
                snippetData=item['snippet']
                contentDetails=item['contentDetails']
                statistics=item['statistics']
                
                video_data={
                    "video_id":video_id,
                    "title":snippetData['title'],
                    "publishedAt":snippetData['publishedAt'],
                    "duration":contentDetails['duration'],
                    "viewCount":statistics.get('viewCount',None),
                    "likecount":statistics.get('likeCount',None),
                    "commentCount":statistics.get('commentCount',None),
                }
                extractedData.append(video_data)
                
        return extractedData
    except r.RequestException as e:
        print(f"Error fetching channel playlist ID: {e}")
        return None

def save_to_json(extractedData):
    file_path=f'./data/YT_data{date.today()}.json'
    
    with open(file_path,'w',encoding='utf-8') as json_outfile:
        json.dump(extractedData,json_outfile,indent=4,ensure_ascii=False)
    

if __name__ == "__main__":
   playlistId=get_channel_playlist_id()
   videoIds=get_video_id(playlistId)
   extractedData=extract_video_data(videoIds)
   save_to_json(extractedData)