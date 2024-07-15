import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from lyricsgenius import Genius

load_dotenv()
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
Redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')

genius = Genius(genius_access_token)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=Redirect_uri,
                                                scope="user-library-read playlist-read-private user-read-playback-state"))

#getting all my playlists & saved ones too names
#results = sp.current_user_playlists(limit=50)
#for idx, song in enumerate(results['items']):
#    print(f"{idx + 1}. {song['name']}")
#by {song['track']['album']['artists'][0]['name']}

def get_50_liked_songs():
    results = sp.current_user_saved_tracks(limit=50)
    for idx, song in enumerate(results['items']):
        print(f"{idx + 1}. {song['track']['album']['name']} by {song['track']['album']['artists'][0]['name']}")
        
def get_current_played_song_lyrics():
    results = sp.current_playback()
    
    title = results['item']['name']
    var = results['item']['artists']
    artist_name = var[0]['name']
    
    if results is not None:
        print('Currently playing: ')
        print(f"Track: {results['item']['name']}")
        print("Artists: ")
        for artist in results['item']['artists']:
            print(f"- {artist['name']}")
        print(f"Album: {results['item']['album']['name']}")
        print(f"Progress: {results['progress_ms'] // 1000} seconds")
        print(f"Duration: {results['item']['duration_ms'] // 1000} seconds")
        print_lyrics(title, artist_name)
    else:
        print("No track is playig!")
        
def print_lyrics(title, artist_name):
    song = genius.search_song(title, artist_name)
    # Print the lyrics
    if song:
        lyrics = song.lyrics
        cleaned_lyrics = lyrics.replace("Embed", "").strip()
        print(cleaned_lyrics)
    else:
        print("Song not found")

if __name__ == "__main__":
    get_current_played_song_lyrics()


