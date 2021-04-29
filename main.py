# https://www.youtube.com/watch?v=-FsFT6OwE1A

from SpotifyApiPackage.User import SpotifyUser

User = SpotifyUser(
    users_spotify_id="",
    refresh_token="",
    base_64=""
)

User.get_all_data()
