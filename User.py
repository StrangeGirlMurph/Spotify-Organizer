import requests
import pandas as pd
import numpy as np


from SpotifyApiPackage.Library_API import Get_Users_Saved_Tracks
from SpotifyApiPackage.Personalization_API import Get_a_Users_Top_Artists, Get_a_Users_Top_Tracks
from SpotifyApiPackage.Playlists_API import *
from SpotifyApiPackage.Tracks_API import Get_Audio_Features_for_Users_Saved_Tracks


class SpotifyUser:
    def __init__(self, users_spotify_id, refresh_token, base_64):
        self.users_spotify_id = users_spotify_id
        self.refresh_token = refresh_token
        self.base_64 = base_64

        self.refresh_Spotify_token()

    def refresh_Spotify_token(self):
        query = "https://accounts.spotify.com/api/token"

        response = requests.post(
            query,
            data={"grant_type": "refresh_token",
                  "refresh_token": self.refresh_token},
            headers={"Authorization": "Basic " + self.base_64}
        )
        response_json = response.json()
        self.spotify_token = response_json["access_token"]

    def get_all_data(self):
        self.users_saved_tracks = Get_Users_Saved_Tracks(self)
        self.users_top_artists = Get_a_Users_Top_Artists(self)
        self.users_top_tracks = Get_a_Users_Top_Tracks(self)

        Get_Audio_Features_for_Users_Saved_Tracks(self)

        print(self.users_saved_tracks.head())
