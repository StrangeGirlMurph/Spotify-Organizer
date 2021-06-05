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

        # time_range:
        # long_term all time
        # medium_term approximately last 6 months
        # short_term approximately last 4 weeks
        self.time_ranges = ["short_term", "medium_term", "long_term"]

        self.columns_for_song_dataframe = [
            "song name", "artists", "album name", "popularity", "explicit", "uri", "id"]
        self.columns_for_artist_datafram = [
            "name", "genres", "popularity", "followers", "uri", "id"]

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
        self.collect_users_saved_tracks()
        self.collect_users_top_tracks()
        self.collect_users_top_artists()

    def collect_users_saved_tracks(self):
        items = Get_Users_Saved_Tracks(self)
        users_saved_tracks = []

        for item in items:
            track = item["track"]
            users_saved_tracks.append(self.filtered_list_from_track(track))

        self.users_saved_tracks = pd.DataFrame(
            users_saved_tracks, columns=self.columns_for_song_dataframe)

    def collect_users_top_tracks(self):
        dict_with_items = Get_a_Users_Top_Tracks(self)
        users_top_tracks = {
            "long_term": [],
            "medium_term": [],
            "short_term": []
        }
        self.users_top_tracks = {}

        for range, items in dict_with_items.items():
            for track in items:
                users_top_tracks[range].append(
                    self.filtered_list_from_track(track))

            self.users_top_tracks[range] = pd.DataFrame(
                users_top_tracks[range], columns=self.columns_for_song_dataframe)

    def collect_users_top_artists(self):
        dict_with_items = Get_a_Users_Top_Artists(self)
        users_top_artists = {
            "long_term": [],
            "medium_term": [],
            "short_term": []
        }
        self.users_top_artists = {}

        for range, items in dict_with_items.items():
            for artist in items:
                users_top_artists[range].append(
                    self.filtered_list_from_artist(artist))

            self.users_top_artists[range] = pd.DataFrame(
                users_top_artists[range], columns=self.columns_for_artist_datafram)

    def filtered_list_from_track(self, track):
        # returns the most important parts of a track as a list
        return [
            track["name"],  # song name
            [artist["name"] for artist in track["artists"]],  # artists
            track["album"]["name"],  # album name
            track["popularity"],  # popularity
            track["explicit"],  # explicit
            track["uri"],  # uri
            track["id"]  # id
        ]

    def filtered_list_from_artist(self, artist):
        # returns the most important parts of an artist as a list
        return [
            artist["name"],  # name
            artist["genres"],  # genres
            artist["popularity"],  # popularity
            artist["followers"]["total"],  # followers
            artist["uri"],  # uri
            artist["id"]  # id
        ]
