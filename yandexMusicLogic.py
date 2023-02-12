import yandex_music as yam
from yandex_music.utils.difference import Difference
from datetime import datetime


def get_client(token: str | None = None) -> yam.Client:
    """ Возвращает объект клиента Яндекс.Музыки. Для авторизации
        используется токен.
    """
    return yam.Client(token=token).init()


def get_tracks_id(client: yam.Client, tracks: dict) -> list:
    """ По словарю tracks названий треков и имен исполнителей составляет
        список track_id Яндекс.Музыки.
    """
    tracks_id = [{'id': 0, 'album_id': 0}] * len(tracks)
    i = 0
    for title in tracks:
        search_result = client.search(text=f'{tracks[title]} — {title}',
                                      type_='track')
        if search_result['tracks'] is not None:
            parsed_id = search_result['tracks']['results'][0].track_id.split(':')
            tracks_id[i] = {'id': parsed_id[0], 'album_id': parsed_id[1]}
            i += 1
    return tracks_id[:i]


def create_buffer_playlist(client: yam.Client, tracks_id: list) -> bool:
    """ Создает буферный плейлист с треками, ассоциированными
        с данными tracks_id.
    """
    buffer_playlist = client.users_playlists_create(
        title=datetime.now().strftime('VKtoYaM %Y-%m-%dT%H:%M:%SZ'),
        visibility='private'
    )
    if not buffer_playlist:
        return False

    client.users_playlists_change(
        kind=buffer_playlist.kind,
        diff=Difference().add_insert(0, tracks_id).to_json()
    )
    return True
