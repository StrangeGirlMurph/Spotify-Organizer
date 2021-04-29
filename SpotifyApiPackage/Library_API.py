import requests
import pandas as pd


def Get_Users_Saved_Tracks(self):
    users_saved_tracks = []

    print(">> getting the saved tracks of the user... ")

    query = "https://api.spotify.com/v1/me/tracks?offset=0&limit=50"

    while query != None:
        last_request = requests.get(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        ).json()

        query = last_request["next"]

        for item in last_request["items"]:
            song = item["track"]
            users_saved_tracks.append([
                song["name"],
                [artist["name"] for artist in song["artists"]],
                song["album"]["name"],
                song["popularity"],
                song["explicit"],
                song["uri"],
                song["id"]
            ])

    return pd.DataFrame(users_saved_tracks, columns=["songname", "artists", "albumname", "popularity", "explicit", "uri", "id"])
