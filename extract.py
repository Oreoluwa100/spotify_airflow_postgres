import base64
import requests
import json
import datetime
import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()
import os

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

#get access token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token" 

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    result = requests.post(url, headers = headers, data = data)
    
    # Check for a successful request
    if result.status_code == 200:
        json_result = json.loads(result.content)
        token = json_result["access_token"]
        return token
    else:
        raise Exception(f"Failed to retrieve token: {result.status_code}")

def get_auth_header(token): 
    return {"Authorization": f"Bearer {token}"} #access token format

token = get_token()
headers = get_auth_header(token)

#get artist id
def search_artist_id(artist_name):
    url = "https://api.spotify.com/v1/search"
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = requests.get(query_url, headers = headers)
    if result.status_code == 200:
        artist_id = json.loads(result.content)['artists']['items'][0]['id']
        if len(artist_id) == 0:
            print("No artist with this name exists")
        else:
            return artist_id
    else:
        raise Exception(f"Failed to retrieve artist id: {result.status_code}")    

#get artist details
def get_artist_details(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    result = requests.get(url, headers = headers)
    if result.status_code == 200:
        artist_details = json.loads(result.content)
        return artist_details
    else:
        raise Exception(f"Failed to retrieve artist details: {result.status_code}")    

#get album details
def get_album_details(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    result = requests.get(url, headers = headers)
    if result.status_code == 200:
        album_details = json.loads(result.content)['items']
        return album_details
    else:
        raise Exception(f"Failed to retrieve album details: {result.status_code}")

#get album tracks
def get_album_tracks(album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    result = requests.get(url, headers = headers)
    if result.status_code == 200:
        track_details = json.loads(result.content)
        return track_details

#get artist top tracks
def get_artist_top_tracks(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    result = requests.get(url, headers = headers)
    if result.status_code == 200:
        top_tracks = json.loads(result.content)['tracks']
        return top_tracks
    else:
        raise Exception(f"Failed to retrieve top tracks: {result.status_code}")
