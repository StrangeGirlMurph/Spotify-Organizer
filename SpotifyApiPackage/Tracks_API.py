import requests
import pandas as pd
import numpy as np


def Get_Audio_Features(self, songs):
    print(">> getting the audio features for the user saved tracks...")

    # ids from dataframe to a numpy array
    ids = songs["id"].to_numpy()
    # split list of ids in fitting pieces
    ids = [ids[i:i + 100] for i in range(0, len(ids), 100)]
    # make a comma separated string out of them
    for i, val in enumerate(ids):
        ids[i] = ','.join(val)

    listOfSongs = []

    for songs in ids:
        query = "https://api.spotify.com/v1/audio-features/?ids={}".format(
            songs)

        response = requests.get(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        ).json()

        listOfSongs.extend(response["audio_features"])

    # list with json objects
    return listOfSongs
