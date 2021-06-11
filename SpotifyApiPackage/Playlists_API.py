import requests
import json
import numpy as np
import pandas as pd


def Add_Items_to_a_Playlist(self, playlist_id, songs):
    print(">> adding the items to the playlist...")

    # uris from dataframe to a numpy array
    uris = songs["uri"].to_numpy()
    # split list of uris in fitting pieces
    uris = [uris[i:i + 100] for i in range(0, len(uris), 100)]
    # make a comma separated string out of them
    for i, val in enumerate(uris):
        uris[i] = ','.join(val)

    for songs in uris:
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            playlist_id, songs)

        response = requests.post(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        ).json()

    if "error" in response:
        print(f"the following error accured: {response['error']}")


def Replace_a_Playlists_Items(self, playlist_id, songs):
    print(">> replacing the items in the playlist...")

    # uris from dataframe to a numpy array
    uris = songs["uri"].to_numpy()
    # split list of uris in fitting pieces
    uris = [uris[i:i + 100] for i in range(0, len(uris), 100)]
    # make a comma separated string out of them
    for i, val in enumerate(uris):
        uris[i] = ','.join(val)

    for songs in uris:
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            playlist_id, songs)

        response = requests.put(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        ).json()

    if "error" in response:
        print(f"the following error accured: {response['error']}")


def Get_a_List_of_Current_Users_Playlists(self):
    playlists = []

    print(">> getting user's current playlists...")

    query = "https://api.spotify.com/v1/me/playlists"

    while query != None:
        last_response = requests.get(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        ).json()

        query = last_response["next"]

        playlists.extend(last_response["items"])

    return playlists


def Create_a_Playlist(self, name, description, public=False):
    # name String
    # description String
    # public Bool

    print(">> creating the playlist...")

    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        self.users_spotify_id)

    request_body = json.dumps({
        "name": name,
        "description": description,
        "public": public
    })

    response = requests.post(
        query,
        data=request_body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer {}".format(self.spotify_token)}
    ).json()

    if "error" in response:
        print(f"the following error accured: {response['error']}")

    return response
