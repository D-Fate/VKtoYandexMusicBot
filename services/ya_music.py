from streaming_service import StreamingService
from schemas.models import Track, Source
from typing import List, Optional

import yandex_music as yam

from yandex_music.utils.difference import Difference


class YaMusic(StreamingService):
    def __init__(self, credentials: dict):
        self.client = yam.Client(
            token=credentials['yandex_token']
            if 'yandex_token' in credentials
            else None
        ).init()

    def parse_source_from_url(self, url: str) -> Source:
        pass

    def get_tracks(self, source: Source) -> Optional[List[Track]]:
        pass

    def search_track(self, track: Track) -> Optional[str]:
        search_result = self.client.search(
            text=f'{track.artist} — {track.title}',
            type_='track'
        )
        if search_result['tracks'] is None:
            return None
        return search_result['tracks']['results'][0].track_id

    def create_playlist(self, name, track_ids: List[str]) -> bool:
        pair_ids = [
            {'id': pair[0], 'album_id': pair[1]}
            for pair in map(lambda track_id: track_id.split(':'), track_ids)
        ]
        new_playlist = self.client.users_playlists_create(
            title=name,
            visibility='private'
        )
        if not new_playlist:
            return False

        self.client.users_playlists_change(
            kind=new_playlist.kind,
            diff=Difference().add_insert(0, pair_ids).to_json()
        )
        return True
