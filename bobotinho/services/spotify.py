# -*- coding: utf-8 -*-
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

__all__ = ("Spotify",)


class Spotify:
    def __init__(self, *, client: str, secret: str) -> None:
        self.api = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client, client_secret=secret))

    async def close(self) -> None:
        pass

    def get_songs_from_playlist(self, *, url: str) -> list[dict]:
        playlist = self.api.playlist(url)
        if playlist:
            return [
                {
                    "track_name": track["track"]["name"],
                    "artist_name": track["track"]["artists"][0]["name"],
                    "track_url": track["track"]["external_urls"]["spotify"],
                }
                for track in playlist["tracks"]["items"]
            ]
