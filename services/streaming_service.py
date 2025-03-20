from abc import ABC, abstractmethod
from typing import List
from schemas.models import Track, Source


class StreamingService(ABC):
    @abstractmethod
    def __init__(self, credentials: dict):
        pass

    @abstractmethod
    def parse_source_from_url(self, url: str) -> Source:
        pass

    @abstractmethod
    def get_tracks(self, source: Source) -> List[Track]:
        pass

    @abstractmethod
    def search_track(self, track: Track) -> str | None:
        pass

    def get_track_ids(self, tracks: List[Track]) -> List[str]:
        return [
            track_id
            for track in tracks
            if (track_id := self.search_track(track)) is not None
        ]

    @abstractmethod
    def create_playlist(self, name: str, track_ids: List[str]) -> bool:
        pass
