from User import SpotifyUser

# add your stuff here (to see how: https://www.youtube.com/watch?v=-FsFT6OwE1A):
User = SpotifyUser(
    users_spotify_id="",
    refresh_token="",
    base_64=""
)

User.get_all_data()
User.generate_a_playlist_for_an_artist("Oliver Tree")
