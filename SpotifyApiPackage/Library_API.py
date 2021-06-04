import requests
import pandas as pd


def Get_Users_Saved_Tracks(self):
    songs = []

    print(">> getting user's saved tracks...")

    query = "https://api.spotify.com/v1/me/tracks?offset=0&limit=50"

    while query != None:
        last_response = requests.get(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        ).json()

        query = last_response["next"]

        songs.extend(last_response["items"])

    return songs
