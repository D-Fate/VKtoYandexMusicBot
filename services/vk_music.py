from streaming_service import StreamingService
from schemas.models import Track, Source, SourceType
from typing import List, Optional

from vk_api import VkApi


class VKMusic(StreamingService):
    def __init__(self, credentials: dict):
        if 'login' in credentials and 'password' in credentials:
            self.session = VkApi(
                login=credentials['login'],
                password=credentials['password']
            )
            self.session.auth()
        elif 'access_token' in credentials:
            self.session = VkApi(token=credentials['access_token'])
        else:
            raise ValueError('Invalid credentials for VK')

    def parse_source_from_url(self, url: str) -> Source:
        return Source(
            type=SourceType.POST,
            id=url[url.find('wall') + 4:]
        )

    def get_tracks(self, source: Source) -> Optional[List[Track]]:
        vk = self.session.get_api()
        if source.type == SourceType.POST:
            post = vk.wall.getById(posts=source.id)

            if not post or 'attachments' not in post[0]:
                return None

            tracks = []
            for attachment in post[0]['attachments']:
                if attachment['type'] == 'audio':
                    tracks.append(Track(
                        artist=attachment['audio']['artist'],
                        title=attachment['audio']['title']
                    ))
            return tracks if tracks else None
        return None

    def search_track(self, track: Track) -> str | None:
        return None

    def create_playlist(self, name: str, track_ids: List[str]) -> bool:
        return False
