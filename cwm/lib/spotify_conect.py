import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='405a27a656a94cefac70660a07c985f1',client_secret='0e64d621fbc144d5a9bc0658eabca7c4',))