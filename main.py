from SpotifyApiPackage.User import SpotifyUser

# add your stuff here (to see how: https://www.youtube.com/watch?v=-FsFT6OwE1A):
User = SpotifyUser(
    users_spotify_id="",
    refresh_token="",
    base_64=""
)

User.get_all_data()
