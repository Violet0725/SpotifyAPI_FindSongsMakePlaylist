from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth



load_dotenv()

id = os.getenv("CLIENT_ID")
sec = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=id, client_secret=sec,
                                               redirect_uri='https://api.spotify.com/v1/me',
                                               scope='playlist-modify-public'))
def get_token():
    auth_string = id + ":" + sec
    auth_bytes = auth_string.encode("utf-8")
    auth__base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth__base64,
        "Cotent-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists.")
        return None
    return json_result[0]

def get_songs(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def add_songs(lst, name):
    playlist_name = name + "'s top 10 songs"
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name)
    for song_name in lst:
        results = sp.search(q=song_name, type='track')
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            sp.playlist_add_items(playlist['id'], [track_uri])
    print(f"Playlist '{playlist_name}' has been created with your selected songs.")

token = get_token()
artist_name = "蔡依林"
result = search_for_artist(token, artist_name)
artist_id = result["id"]
songs = get_songs(token, artist_id)

song_list = []

for i, song in enumerate(songs):
    print(f"{i+1}. {song['name']}")
    song_list.append(song['name'])

res = input("Would you like to make a new playlist for these songs? (Y/N) ")

if res.upper() == "Y":
    add_songs(song_list, artist_name)
elif res.upper() == "N":
    pass

