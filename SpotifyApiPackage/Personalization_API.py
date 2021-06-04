import requests
import json


def Get_a_Users_Top_Tracks(self):
    top_tracks = {
        "long_term": [],
        "medium_term": [],
        "short_term": []
    }

    print(">> getting user's top tracks...")

    for time_range in self.time_ranges:
        query = "https://api.spotify.com/v1/me/top/tracks?offset=0&limit=50&time_range={}".format(
            time_range)

        while query != None:
            last_response = requests.get(
                query,
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer {}".format(self.spotify_token)}
            ).json()
            query = last_response["next"]

            top_tracks[time_range].extend(last_response["items"])

    return top_tracks


def Get_a_Users_Top_Artists(self):
    top_artists = {
        "long_term": [],
        "medium_term": [],
        "short_term": []
    }

    print(">> getting user's top artists...")

    for time_range in self.time_ranges:
        query = "https://api.spotify.com/v1/me/top/artists?offset=0&limit=50&time_range={}".format(
            time_range)

        while query != None:
            last_response = requests.get(
                query,
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer {}".format(self.spotify_token)}
            ).json()
            query = last_response["next"]

            top_artists[time_range].extend(last_response["items"])

    return top_artists
