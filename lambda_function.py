import googleapiclient.discovery
import pandas as pd
from datetime import datetime
import re
import os
import boto3
import io
import time
import pytz
import random

def lambda_handler(event, context):

    start_time = time.time()  # Start Timer

    #define api key
    api_keys = os.getenv("youtube_api_keys", "").split(",")
    api_keys = [key.strip('"') for key in api_keys]
    api_key = random.choice(api_keys)
    

    # all channels
    t_series_channels = {
    "T-Series Hindi": "UCq-Fj5jknLsUf-MWSy4_brA",
    "T-Series Telugu": "UCnJjcn5FrgrOEp5_N45ZLEQ",
    "T-Series Tamil": "UCAEv0ANkT221wXsTnxFnBsQ",
    "T-Series Kannada": "UCovxnbWKPCA5iJDxa9zbBew",
    "T-Series Malayalam": "UCUoj77TIUy9DhLNe5EVmF-A",
    "T-Series Bhakti Sagar": "UCaayLD9i5x4MmIoVZxXSv_g"
    }

    # Establishing YT API Connection
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    #utility functions
    ### Function1: Get the video playlist ID's
    def get_playlist_id(channel_yt_id):
        request = youtube.channels().list(part="snippet,contentDetails,statistics", id=channel_yt_id)
        response = request.execute()
        return response['items'][0]["contentDetails"]["relatedPlaylists"]['uploads']

    t_series_vido_playlist_ids = {}
    for channel_name, channel_id in t_series_channels.items():
        playlist_id =  get_playlist_id(channel_id)
        t_series_vido_playlist_ids[channel_name] = playlist_id


    ### Function2: Get all video Ids
    def get_video_ids(youtube, playlist_id):
        video_ids = []
        next_page_token = None

        while True:
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                maxResults=50,
                playlistId=playlist_id,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response['items']:
                published_at = item['snippet']['publishedAt']
                published_date = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                
                # Filter videos published from 2022 onwards
                if published_date >= datetime(2022, 1, 1):
                    video_ids.append(item['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return video_ids

    t_series_channels_video_ids = {}
    for channel_name, channel_playlist_id in t_series_vido_playlist_ids.items():
        print('*' * 50)
        print(f'Fetching Data for Channel: `{channel_name}` initiated')
        video_ids = get_video_ids(youtube, channel_playlist_id)
        t_series_channels_video_ids[channel_name] = video_ids
        print(f'Fetching Data for Channel: `{channel_name}` completed')
        print('*' * 50)

    ### Function3: Get all video details
    def get_video_details(youtube, channel_name, video_ids):
        all_video_info = []
        
        complete_status = 0
        for i in range(0, len(video_ids), 50):
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=','.join(video_ids[i:i+50])
            )
            response = request.execute() 

            for video in response['items']:
                stats_to_keep = {'snippet': ['title', 'description', 'tags', 'publishedAt', 'thumbnails', 'liveBroadcastContent'],
                                'statistics': ['viewCount', 'likeCount', 'commentCount'],
                                'contentDetails': ['duration']
                                }
                video_info = {'video_id': video['id']}

                for k, fields in stats_to_keep.items():
                    for field in fields:
                        if field == 'thumbnails':
                            if 'maxres' in video.get(k, {}).get(field, None).keys():
                                thum_url = video.get(k, {}).get(field, None)['maxres'].get('url')
                            elif 'standard' in video.get(k, {}).get(field, None).keys():
                                thum_url = video.get(k, {}).get(field, None)['standard'].get('url')
                            elif 'high' in video.get(k, {}).get(field, None).keys():
                                thum_url = video.get(k, {}).get(field, None)['high'].get('url')
                            else:
                                thum_url = None
                            video_info[field] = thum_url
                        else:
                            video_info[field] = video.get(k, {}).get(field, None)

                # Determine content_type
                try:
                    duration = video_info["duration"]  # e.g., "PT59S"
                    title = video_info["title"].lower()
                    description = video_info["description"].lower()
                    
                    match = re.search(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
                    hours = int(match.group(1)[:-1]) * 3600 if match.group(1) else 0
                    minutes = int(match.group(2)[:-1]) * 60 if match.group(2) else 0
                    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
                    total_seconds = hours + minutes + seconds
                    
                    if (total_seconds <= 60) or ("#shorts" in title) or ("#shorts" in description) or (description == ''):
                        video_info['content_type'] = "Shorts"
                    else:
                        video_info['content_type'] = "Video"
                    
                    # add channel name and channel id
                    video_info['channel_name'] = channel_name
                    
                    all_video_info.append(video_info)
                    complete_status += 1
                except:
                    continue

                if complete_status % 500 == 0:
                    print("500 Completed ---> ")
        
        return all_video_info

    t_series_channels_video_data = {}
    for channel_name, channel_video_ids in t_series_channels_video_ids.items():
        print('*' * 50)
        print(f'Fetching Data for Channel: `{channel_name}` initiated')
        video_data = get_video_details(youtube, channel_name, channel_video_ids)
        t_series_channels_video_data[channel_name] = video_data
        print(f'Fetching Data for Channel: `{channel_name}` completed')
        print('*' * 50)


    #Creating the dataframe
    video_df_hindi = pd.DataFrame(t_series_channels_video_data['T-Series Hindi'])
    video_df_telugu = pd.DataFrame(t_series_channels_video_data['T-Series Telugu'])
    video_df_tamil = pd.DataFrame(t_series_channels_video_data['T-Series Tamil'])
    video_df_kannada = pd.DataFrame(t_series_channels_video_data['T-Series Kannada'])
    video_df_malayalam = pd.DataFrame(t_series_channels_video_data['T-Series Malayalam'])
    video_df_bhakti_sagar = pd.DataFrame(t_series_channels_video_data['T-Series Bhakti Sagar'])

    # let's concat everything
    Video_df = pd.concat([video_df_hindi, video_df_telugu, video_df_tamil, video_df_kannada, video_df_malayalam, video_df_bhakti_sagar])
    Video_df['video_link'] = Video_df['video_id'].apply(lambda x: 'https://www.youtube.com/watch?v=' + x)

    #add a new column: `inserted_at`
    #Define IST Time Zone
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(pytz.utc).astimezone(ist).strftime('%Y-%m-%d %H:%M:%S').replace(':', '_')
    print("Time Now: ", current_time)
    Video_df['inserted_at'] = datetime.now(pytz.utc).astimezone(ist)
    Video_df['inserted_at'] = Video_df['inserted_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    Video_df['inserted_at'] = pd.to_datetime(Video_df['inserted_at'])

    # Convert to datetime
    Video_df['publishedAt'] = pd.to_datetime(Video_df['publishedAt'], format='%Y-%m-%dT%H:%M:%SZ', utc=True)
    Video_df['publishedAt'] = Video_df['publishedAt'].dt.tz_localize(None)


    # re-arrange cols and take required one
    cols = ['video_id', 'publishedAt', 'title',  'duration', 'content_type', 'tags', 'video_link', 'description', 'thumbnails', 'viewCount',
         'likeCount', 'commentCount', 'channel_name', 'inserted_at']
    Video_df = Video_df[cols]

    ### rename the cols
    # Dictionary mapping old column names to new names
    column_replacements = {
        "publishedAt": "published_at",
        "viewCount": "'view_count'",
        "commentCount": "comment_count",
        "likeCount": "like_count",
    }

    # Rename columns
    Video_df.rename(columns=column_replacements, inplace=True)

    print(Video_df.shape)
    print(Video_df.head(3))

    ### Store to S3
    # AWS S3 Configuration
    s3_bucket = "t-series-youtube-analytics" 
    s3_file_key = f"raw_data/t_series_youtube_data_{current_time}.csv"  

    # Convert DataFrame to CSV in memory
    csv_buffer = io.StringIO()
    Video_df.to_csv(csv_buffer, index=False)

    client = boto3.client('s3')
    client.put_object(
        Bucket = s3_bucket,
        Key = s3_file_key,
        Body=csv_buffer.getvalue()
    )
    print(f"CSV file uploaded to s3://{s3_bucket}/{s3_file_key}")

    end_time = time.time()  # End Timer
    execution_time = end_time - start_time  # Total time taken

    print(f"Execution Time: {execution_time:.4f} seconds")