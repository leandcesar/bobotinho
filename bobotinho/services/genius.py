# -*- coding: utf-8 -*-
import lyricsgenius

__all__ = ("Genius",)


class Genius:
    def __init__(self, *, key: str) -> None:
        self.api = lyricsgenius.Genius(key)

    async def close(self) -> None:
        pass

    def get_lyrics(self, *, title: str = None, artist: str = None) -> str:
        title = title.lower().replace("ao vivo", "")
        song = self.api.search_song(title=title, artist=artist, get_full_info=False)
        if song and song.id and song.artist != "Genius Brasil":
            return song.lyrics
