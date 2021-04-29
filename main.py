# from datetime import date

# today = date.today()
# todayFormatted = today.strftime("%d/%m/%Y")

# import doesnt work: python version unten links auf 64 bit stellen

# https://www.youtube.com/watch?v=-FsFT6OwE1A

from SpotifyApiPackage.User import SpotifyUser

Murph = SpotifyUser(
    users_spotify_id="kaansünnenwold",
    refresh_token="AQBttNB1spg5rTSQrgqwkrkxGgNtdyZFPNO9qpqY19dszS_vaxGtlDp4QiG58CQ_wIBpuhMO6tBoDPJJQkTsrLYm-sKPg8o6P3Hy0owdXmvhEyEt1N1ES3cl_Es7dz5dzek",
    base_64="YWJjYzNkMGJmY2Y3NGQ2ZDk3NGIwNzFlNzFmY2NiZTM6MDZjY2M0NGM5NzJiNDljZGIyMDc1OTM1OGI0NmJjOGM="
)

Murph.get_all_data()


""" rf.refresh()
get_users_saved_tracks()
get_audio_features()
get_users_playlists()
# get_users_top_artists()
# get_users_top_tracks()
create_playlist("Cro")
create_playlist("danceability")

print(len(users_audio_features["song_uris"]["danceability"][0]))
# spotify:track:4tHqQMWSqmL6YjXwsqthDI, 37 """
