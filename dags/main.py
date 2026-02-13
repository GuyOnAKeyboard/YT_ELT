from airflow import DAG
import pendulum
from datetime import datetime, timedelta

from api.video_stats import get_channel_playlist_id, get_video_id,extract_video_data,save_to_json

locat_tz=pendulum.timezone("Asia/Kolkata")

default_args = {
    "owner": "data_engineering",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1,tzinfo=locat_tz),
    "email": ["data-team@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    # "retries": 2,
    "max_active_runs":1,
    # "retry_delay": timedelta(hours=1),
}

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='Json produced with raw data',
    schedule='0 14 * * *',
    catchup=False
) as dag:
    
    #define dag
    playlistId=get_channel_playlist_id()
    videoIds=get_video_id(playlistId)
    extractedData=extract_video_data(videoIds)
    saveJsonTask=save_to_json(extractedData)
    
    #define dependencies
    playlistId>>videoIds>>extractedData>>saveJsonTask
    