# -*- coding: utf-8 -*-
import json
import os
import googleapiclient.discovery

from art import tprint
from dotenv import load_dotenv
load_dotenv()

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv("API_KEY")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey = DEVELOPER_KEY)

def valid_id(id):
    if id[:2] == "PL":
        request = youtube.playlistItems().list(
            part="snippet",
            maxResults=0,
            playlistId=id
        )
        response = request.execute()
        if "error" not in response and response["pageInfo"]["totalResults"] != 0:
            return True
    else:
        request = youtube.channels().list(
            part="statistics",
            id=id,
            maxResults=1
        )
        response = request.execute()
        if response["pageInfo"]["totalResults"] == 1:
            return True
    return False

def get_query_or_id():
    while True:
        string = input("Enter search query or id: ")
        if valid_id(string) and len(string) < 100:
            return string, False
        if all(x.isalnum() or x.isspace() for x in string) and len(string) < 100:
            return string, True
        print("Id should be less than 100 characters long")
        print("Query should be less than 100 characters long and consist of\n",
            "numbers, letters(english lower- and uppercase) and spaces")

def get_playlists(id):
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=id,
        maxResults=15
    )
    return request.execute()

def search_for_channel(query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="channel"
    )
    response = request.execute()
    if len(response["items"]) == 0:
        print("No channels here..")
        return None
    for i, item in enumerate(response["items"]):
        print(f"{i+1}. \033[1m{item['snippet']['title']}\033[0m\n{item['snippet']['description']}")
    while True:
        num = input("Enter number of required channel: ")
        if num.isdigit() and 1 <= int(num) <= 5:
            return response["items"][int(num) - 1]["id"]["channelId"]
        print("Chose one of the options")

def chose_pl(playlists):
    if len(playlists["items"]) == 0:
        print("No playlists here")
        return None
    for i, item in enumerate(playlists["items"]):
        print(f"{i+1}. \033[1m{item['snippet']['title']}\033[0m\n{item['snippet']['description']}")
    while True:
        num = input("Enter number of required playlist: ")
        if num.isdigit() and 1 <= int(num) <= len(playlists["items"]):
            return playlists["items"][int(num) - 1]["id"]
        print("Chose one of the options")

def retrieve_pl_items(pl):
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=0,
        playlistId=pl
    )
    response = request.execute()
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=response["pageInfo"]["totalResults"],
        playlistId=pl
    )
    return request.execute()["items"]

def main():
    tprint("YT PL > to > M3U")
    s, is_query = get_query_or_id()
    if is_query:
        s = search_for_channel(s)
        if s is None:
            exit()
    
    if s[:2] == "PL":
        pl = s
    else:
        playlists = get_playlists(s)
        pl = chose_pl(playlists)
        if pl is None:
            exit()
    
    items = retrieve_pl_items(pl)
    with open("playlist.m3u", "w") as file:
        file.write("#EXTM3U\n")
        for item in items:
            file.write("#EXTINF:" + item["snippet"]["title"] + "\n")
            file.write("https://www.youtube.com/watch?v=" + item["snippet"]["resourceId"]["videoId"] + "\n")
    

if __name__ == "__main__":
    main()
