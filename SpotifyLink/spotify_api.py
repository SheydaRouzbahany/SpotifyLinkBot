import os
import base64
import json

from dotenv import load_dotenv
from requests import post, get

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = 'https://locahost:5000/callback'


AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'


def get_token():
    auth_string = CLIENT_ID + ":" + CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    headers = {  # associated with request
        "Authorization": "Basic " + auth_base64,  # authorization data
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    result = post(TOKEN_URL, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]


def search_for_track(token, track):
    ENDPOINT_URL = 'https://api.spotify.com/v1/search'

    headers = {
        "Authorization": "Bearer " + token
    }

    query = f"?q={track}&type=track&limit=1"

    query_url = ENDPOINT_URL + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def search_for_album(token, album, hipster):
    ENDPOINT_URL = 'https://api.spotify.com/v1/search'

    headers = {
        "Authorization": "Bearer " + token
    }

    # hipster tag broken
    # query = f"?q=tag:hipster&{album}&type=album&limit=1" if hipster else f"?q={album}&type=album&limit=1"
    query = f"?q={album}&type=album&limit=1"

    query_url = ENDPOINT_URL + query

    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


def get_album_link(album, hipster):
    token = get_token()
    result = search_for_album(token, album, hipster)

    if not result['albums']['items']:
        return "no matches found"

    useful = result['albums']['items'][0]
    link = useful['external_urls']['spotify']

    return link


def get_track_link(track):
    token = get_token()
    result = search_for_track(token, track)

    if not result['albums']['items']:
        return "no matches found"

    useful = result['tracks']['items'][0]
    link = useful['external_urls']['spotify']
    # popularity = useful['popularity'])
    return link