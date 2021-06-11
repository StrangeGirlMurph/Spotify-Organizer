import requests
import pandas as pd
import numpy as np

from SpotifyApiPackage.Library_API import Get_Users_Saved_Tracks
from SpotifyApiPackage.Personalization_API import Get_a_Users_Top_Artists, Get_a_Users_Top_Tracks
from SpotifyApiPackage.Playlists_API import *
from SpotifyApiPackage.Tracks_API import Get_Audio_Features


class SpotifyUser:
    def __init__(self, users_spotify_id, refresh_token, base_64):
        self.users_spotify_id = users_spotify_id
        self.refresh_token = refresh_token
        self.base_64 = base_64

        self.users_playlists = {}
        # time_range:
        # long_term all time
        # medium_term approximately last 6 months
        # short_term approximately last 4 weeks
        self.time_ranges = ["short_term", "medium_term", "long_term"]

        self.columns_for_song_dataframe = [
            "song name", "artists", "album name", "popularity", "explicit", "uri", "id"]
        self.columns_for_artist_datafram = [
            "name", "genres", "popularity", "followers", "uri", "id"]

        self.descriptions_audio_features = {
            "energy": "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.",
            "danceability": "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.",
            "valence": "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
            "tempo": "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
            "speechiness":  "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.",
            "acouticness": "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
            "instrumentalness": "Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.",
            "loudness": "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.",
            "liveness": "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live."
        }

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
        self.collect_audio_features_for_users_saved_tracks()

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

    def generate_a_playlist_for_an_artist(self, artist):
        if self.users_saved_tracks[self.users_saved_tracks["artists"].apply(lambda i: artist in i)].empty:
            print(
                "You don't have any songs of that artist in your library, you misspelled the artist or forgot to collect the data.")
            return
        else:
            if not bool(self.users_playlists):  # if empty
                self.collect_users_playlists()
            if artist in self.users_playlists:
                print("The Playlist for the artist already exists.")
                Replace_a_Playlists_Items(
                    self, self.users_playlists[artist],
                    self.users_saved_tracks[self.users_saved_tracks["artists"].apply(lambda i: artist in i)])
            else:
                playlist = Create_a_Playlist(
                    self, artist, self.generate_description_for_artist_playlist(artist), public=False)
                Add_Items_to_a_Playlist(
                    self, playlist["id"], self.users_saved_tracks[self.users_saved_tracks["artists"].apply(lambda i: artist in i)])

    def generate_a_playlist_for_an_audio_feature(self, feature):
        if not bool(self.users_playlists):  # if empty
            self.collect_users_playlists()
        if feature in self.users_playlists:
            print("The Playlist for the audio feature already exists.")
            Replace_a_Playlists_Items(
                self, self.users_playlists[feature],
                self.users_saved_tracks.sort_values(feature))
        else:
            playlist = Create_a_Playlist(
                self, feature, self.generate_description_for_audio_feature_playlist(feature), public=False)
            Add_Items_to_a_Playlist(
                self, playlist["id"], self.users_saved_tracks.sort_values(feature, ascending=False))

    def collect_audio_features_for_users_saved_tracks(self):
        features = pd.DataFrame(Get_Audio_Features(
            self, self.users_saved_tracks))
        self.users_saved_tracks = pd.merge(self.users_saved_tracks, features)

    def collect_users_playlists(self):
        items = Get_a_List_of_Current_Users_Playlists(self)

        self.users_playlists = {}
        for playlist in items:
            self.users_playlists[playlist["name"]] = playlist["id"]

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

    def generate_description_for_artist_playlist(self, name):
        return f"All my favourite songs by or with {name} <3"

    def generate_description_for_audio_feature_playlist(self, feature):
        return self.descriptions_audio_features[feature]
