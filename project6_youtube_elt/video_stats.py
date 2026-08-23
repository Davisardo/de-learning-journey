import requests
import json
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv("./.env")


api_key = os.getenv("YOUTUBE_API_KEY")
channel_handle = "MrBeast"
MAX_RESULTS = 50


def get_playlist_id():

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={api_key}"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        # print(json.dumps(data,indent=4))

        channel_items = data["items"][0]

        channel_playlistid = channel_items["contentDetails"]["relatedPlaylists"][
            "uploads"
        ]

        # print(channel_playlistid)

        return channel_playlistid

    except requests.exceptions.RequestException as e:
        raise e


def get_video_id(playlist_id):
    video_ids = []
    page_token = None

    try:
        while True:
            url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAX_RESULTS}&playlistId={playlist_id}&key={api_key}"

            if page_token:
                url += f"&pageToken={page_token}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            page_token = data.get("nextPageToken")

            if not page_token:
                break
        return video_ids

    except requests.exceptions.RequestException as e:
        raise e


def batch_list(video_id_list, batch_size=MAX_RESULTS):
    for i in range(0, len(video_id_list), batch_size):
        yield video_id_list[i : i + batch_size]


def extract_video_data(video_ids):
    extracted_data = []

    try:
        for batch in batch_list(video_ids, MAX_RESULTS):
            video_id_string = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id_string}&key={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get("items", []):
                snippet = item.get("snippet", {})
                content_details = item.get("contentDetails", {})
                statistics = item.get("statistics", {})
                video_data = {
                    "video_id": item.get("id"),
                    "title": snippet.get("title"),
                    "published_at": snippet.get("publishedAt"),
                    "duration": content_details.get("duration"),
                    "view_count": statistics.get("viewCount", None),
                    "like_count": statistics.get("likeCount", None),
                    "comment_count": statistics.get("commentCount", None),
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e


def save_to_json(extracted_data):
    file_path = f"./data/youtube_data_{date.today()}.json"

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    playlist_id = get_playlist_id()
    video_ids = get_video_id(playlist_id)
    extracted_data = extract_video_data(video_ids)
    save_to_json(extracted_data)
