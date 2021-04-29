import requests


def Add_Items_to_a_Playlist(playlist_id, name, category):
    # add all songs to new playlist
    print(">> adding the items to the playlist...")

    global response_add_songs
    if category == "artist":
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            playlist_id, users_saved_tracks["artists"][name])
        response_add_songs = requests.post(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(rf.spotify_token)}
        ).json()
    elif category == "audio_feature":
        for songs in users_audio_features["song_uris"][name]:
            query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
                playlist_id, songs)

            response_add_songs = requests.post(
                query,
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer {}".format(rf.spotify_token)}
            ).json()

    if "error" in response_add_songs:
        print("the following error accured:")
        print(response_add_songs["error"])


def Replace_a_Playlists_Items(playlist_id, name, category):
    print(">> replacing the items in the playlist...")

    global response_replace_songs
    if category == "artist":
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            playlist_id, users_saved_tracks["artists"][name])
        response_replace_songs = requests.put(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(rf.spotify_token)}
        ).json()
    elif category == "audio_feature":
        for songs in users_audio_features["song_uris"][name]:
            query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
                playlist_id, songs)
            response_replace_songs = requests.put(
                query,
                headers={"Content-Type": "application/json",
                         "Authorization": "Bearer {}".format(rf.spotify_token)}
            ).json()

    if "error" in response_replace_songs:
        print("the following error accured:")
        print(response_replace_songs["error"])
    else:
        print(">> finished")


def Get_a_List_of_Current_Users_Playlists():
    global users_playlists
    users_playlists = {}

    print(">> getting the playlists of the user...")

    query = "https://api.spotify.com/v1/me/playlists"

    global response_users_playlists
    while query != None:
        response_users_playlists = requests.get(
            query,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer {}".format(rf.spotify_token)}
        ).json()

        query = response_users_playlists["next"]

        for playlist in response_users_playlists["items"]:
            users_playlists[playlist["name"]] = playlist["id"]


def Create_a_Playlist(name):
    print(">> creating the playlist... for", name)

    if name in descriptions_audio_features:
        description = descriptions_audio_features[name]
        category = "audio_feature"
    elif name in users_saved_tracks["artists"]:
        description = "All my favorite songs of " + name + " <3"
        category = "artist"
    else:
        print("You don't have any songs of that artist in your library or you misspelled the artist or audio feature.")
        return

    if name in users_playlists:
        print("The Playlist for the artist or audio feature already exists.")
        return replace_playlists_items(users_playlists[name], name, category)

    query = "https://api.spotify.com/v1/users/{}/playlists".format(
        users_spotify_id)

    request_body = json.dumps({
        "name": name,
        "description": description,
        "public": False
    })

    global response_create_playlist
    response_create_playlist = requests.post(
        query,
        data=request_body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer {}".format(rf.spotify_token)}
    ).json()

    if "error" in response_create_playlist:
        print("the following error accured:")
        print(response_create_playlist["error"])

    add_items_to_playlist(response_create_playlist["id"], name, category)
