import requests


def Get_a_Users_Top_Tracks(self, time_range=""):
    # time_range:
    # long_term all time
    # medium_term approximately last 6 months
    # short_term approximately last 4 weeks

    if time_range == "long":
        time_range = "long_term"
    elif time_range == "mid":
        time_range = "medium_term"
    elif time_range == "short":
        time_range = "short_term"
    else:
        time_range = "long_term"

    users_top_tracks = [time_range, []]

    print(">> getting the users top tracks (time range: " + time_range + ")...")

    query = "https://api.spotify.com/v1/me/top/tracks?offset=0&limit=50&time_range={}".format(
        time_range)

    global response_users_top_tracks
    while query != None:
        response_users_top_tracks = requests.get(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        ).json()

        query = response_users_top_tracks["next"]

        for track in response_users_top_tracks["items"]:
            users_top_tracks[1].append(track["name"])

    return users_top_tracks


def Get_a_Users_Top_Artists(self, time_range=""):
    # time_range:
    # long_term all time
    # medium_term approximately last 6 months
    # short_term approximately last 4 weeks

    if time_range == "long":
        time_range = "long_term"
    elif time_range == "mid":
        time_range = "medium_term"
    elif time_range == "short":
        time_range = "short_term"
    else:
        time_range = "long_term"

    users_top_artists = [time_range, []]

    print(">> getting the users top artists(time range: " + time_range + ")...")

    query = "https://api.spotify.com/v1/me/top/artists?offset=0&limit=50&time_range={}".format(
        time_range)

    while query != None:
        response_users_top_artists = requests.get(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(self.spotify_token)}
        ).json()

        query = response_users_top_artists["next"]

        for artist in response_users_top_artists["items"]:
            users_top_artists[1].append(artist["name"])

    return users_top_artists
