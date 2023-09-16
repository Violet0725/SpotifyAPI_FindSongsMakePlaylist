import tkinter
import customtkinter
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

def show_list():
    result_label.configure(text="")
    artist_name = artist_entry.get()
    token = get_token()
    result = search_for_artist(token, artist_name)
    if result:
        artist_id = result["id"]
        songs = get_songs(token, artist_id)
        song_list = [song['name'] for song in songs]

        song_name.configure(text=f"1. {song_list[0]}", font=("Arial", 14, "bold"))
        song_name1.configure(text=f"2. {song_list[1]}", font=("Arial", 14, "bold"))
        song_name2.configure(text=f"3. {song_list[2]}", font=("Arial", 14, "bold"))
        song_name3.configure(text=f"4. {song_list[3]}", font=("Arial", 14, "bold"))
        song_name4.configure(text=f"5. {song_list[4]}", font=("Arial", 14, "bold"))
        song_name5.configure(text=f"6. {song_list[5]}", font=("Arial", 14, "bold"))
        song_name6.configure(text=f"7. {song_list[6]}", font=("Arial", 14, "bold"))
        song_name7.configure(text=f"8. {song_list[7]}", font=("Arial", 14, "bold"))
        song_name8.configure(text=f"9. {song_list[8]}", font=("Arial", 14, "bold"))
        song_name9.configure(text=f"10. {song_list[9]}", font=("Arial", 14, "bold"))

        show_button.configure(text="Create Playlist on Spotify", command=create_playlist)
    else:
        song_name.configure(text="No artists with this name exist.", font=("Arial", 25, "bold"))

def create_playlist():
    artist_name = artist_entry.get()
    token = get_token()
    result = search_for_artist(token, artist_name)
    if result:
        artist_id = result["id"]
        songs = get_songs(token, artist_id)
        song_list = [song['name'] for song in songs]

        playlist_name = artist_name + "'s top 10 songs"
        user_id = sp.me()['id']
        playlist = sp.user_playlist_create(user_id, playlist_name)

        for song_name in song_list:
            results = sp.search(q=song_name, type='track')
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                sp.playlist_add_items(playlist['id'], [track_uri])

        result_label.configure(text=f"Playlist '{playlist_name}' has been created with your selected songs.", font=("Arial", 14, "bold"), text_color="yellow")
        show_button.configure(text="Show Top 10 songs", command=show_list)

# Create the main application window
app = customtkinter.CTk()
app.geometry("480x480")
app.title("Spotify Playlist Creator")

# Create labels and entry fields
artist_label = customtkinter.CTkLabel(app, text="Enter Artist Name:", font=("Arial", 25, "bold"))
artist_label.pack(pady=10)

artist_entry = customtkinter.CTkEntry(app,height=40)
artist_entry.pack(pady=5)

# Create a button to create the playlist
show_button = customtkinter.CTkButton(app, text="Show Top 10 songs", command=show_list, font=("Arial",16 , "bold"), width=120, height=30)
show_button.pack(pady=5)

# Create a label to display the result
result_label = customtkinter.CTkLabel(app, text="", wraplength=300)
result_label.pack()

song_name = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name.pack()
song_name1 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name1.pack()
song_name2 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name2.pack()
song_name3 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name3.pack()
song_name4 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name4.pack()
song_name5 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name5.pack()
song_name6 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name6.pack()
song_name7 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name7.pack()
song_name8 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name8.pack()
song_name9 = customtkinter.CTkLabel(app, text="", wraplength=300)
song_name9.pack()


# Start the GUI main loop
app.mainloop()