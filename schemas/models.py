from enum import Enum
from pydantic import BaseModel, Field


class Track(BaseModel):
    """
        Модель для представления данных о музыкальном треке.
        Обеспечивает валидацию и ограничения полей.

        Attributes:
            artist (str): Исполнитель трека (макс. 255 символов).
            title (str): Название трека (макс. 255 символов).
    """
    artist: str = Field(..., max_length=255, description='Исполнитель')
    title: str = Field(..., max_length=255, description='Название трека')


class SourceType(str, Enum):
    """
        TODO: уточнить описание
        Типы источников, поддерживаемых системой.

        Возможные значения:
        - playlist: Плейлист (Spotify, YouTube, VK, Yandex.Music)
        - post: Пост со стены (VK)
    """
    PLAYLIST = 'playlist'
    POST = 'post'


class Source(BaseModel):
    """
        Модель для представления источника данных (плейлист, пост).

        Attributes:
            type (SourceType): Тип источника.
                Примеры: playlist, post.
            id (str): Уникальный идентификатор источника в сервисе.
    """
    type: SourceType = Field(
        ...,
        description='Тип источника: playlist/post'
    )
    id: str = Field(
        ...,
        max_length=34,
        examples=['12345_67890', 'PL55713C70BA91BD6E', '37i9dQZF1DXcBWIGoYBM5M'],
        description='ID источника. Зависит от сервиса: '
                    'VK: {owner_id}_{id} (до 21 символа), '
                    'Yandex.Music: число (до 10 символов), '
                    'YouTube: строка с префиксом PL (до 34 символов), '
                    'Spotify: base62-строка (22 символа)'
    )
