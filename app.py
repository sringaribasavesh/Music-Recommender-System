import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os
load_dotenv()

# Access the variables
client_id = st.secrets("SPOTIPY_CLIENT_ID")
client_secret = st.secrets("SPOTIPY_CLIENT_SECRET")

# ✅ Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 🎨 Get album cover using Spotify API
def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # fallback image

# 🔁 Recommend similar songs
def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_music_names = []
    recommended_music_posters = []
    
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        title = music.iloc[i[0]].song
        recommended_music_posters.append(get_song_album_cover_url(title, artist))
        recommended_music_names.append(title)
        
    return recommended_music_names, recommended_music_posters

# 🧠 Load data
music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similar.pkl','rb'))

# 🎧 Song list with placeholder
music_list = music['song'].unique().tolist()
music_list.insert(0, "Select a song...")  # 👈 Placeholder

# 🖼️ Streamlit UI
st.header('Music Recommender System')

selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

# 👇 Only show recommendation if a valid song is selected
if st.button('Show Recommendation') and selected_song != "Select a song...":
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(recommended_music_posters[i], use_container_width=True)
            st.caption(recommended_music_names[i])
